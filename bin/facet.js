#!/usr/bin/env node
"use strict";

// ---------------------------------------------------------------------------
// npx @mcptoolshop/facet  ->  the facet-mcp record-index server.
//
// WHY THIS IS NOT @mcptoolshop/npm-launcher. The launcher downloads a
// PyInstaller binary from a GitHub Release and verifies its SHA256. That is the
// right shape for a tool whose runtime is heavy or whose users have no Python.
// facet-mcp is neither: it is two pure-Python modules plus `mcp`, it installs
// from PyPI in about two seconds, and building per-OS binaries for it would add
// a release-binaries workflow and three build matrices to ship something pip
// already ships. So this wrapper bootstraps a managed venv instead. It carries
// no npm dependencies at all.
//
// The version below is written by the release, and release.yml refuses to
// publish if it disagrees with package.json or the tag. That check is the only
// reason it is safe to pin an exact version here.
// ---------------------------------------------------------------------------

const { spawnSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const PKG = "facet-mcp";
const VERSION = "0.1.0";
const ENTRY = "facet-mcp";
const MIN_PY = [3, 11];

const isWindows = process.platform === "win32";
const venvBin = (root) => path.join(root, isWindows ? "Scripts" : "bin");
const exe = (name) => (isWindows ? `${name}.exe` : name);

function die(lines) {
  process.stderr.write(lines.join("\n") + "\n");
  process.exit(2);
}

// Every error names the next step, and the commands are copy-paste-runnable on
// the host that produced the error (no sudo on Windows, no shell quoting that
// dies on cmd.exe).
function noPythonError() {
  die([
    `facet needs Python ${MIN_PY.join(".")}+ on PATH and could not find it.`,
    "",
    "Next step - install Python, then re-run this command:",
    isWindows
      ? "  winget install Python.Python.3.12       (or https://python.org/downloads)"
      : "  brew install python@3.12                (macOS)\n  sudo apt install python3.12 python3.12-venv   (Debian/Ubuntu)",
    "",
    "Already have Python? Install the package directly instead:",
    `  pipx install ${PKG}==${VERSION}`,
    `  uv tool install ${PKG}==${VERSION}`,
  ]);
}

// Probe interpreters in preference order and take the first that is new enough.
// `py -3` is last because on Windows it can shadow a newer python3 on PATH.
function findPython() {
  const candidates = isWindows
    ? [["python", []], ["python3", []], ["py", ["-3"]]]
    : [["python3", []], ["python", []]];
  for (const [cmd, pre] of candidates) {
    const r = spawnSync(cmd, [...pre, "-c", "import sys;print('%d.%d' % sys.version_info[:2])"], {
      encoding: "utf8",
    });
    if (r.status !== 0 || !r.stdout) continue;
    const [maj, min] = r.stdout.trim().split(".").map(Number);
    if (maj > MIN_PY[0] || (maj === MIN_PY[0] && min >= MIN_PY[1])) {
      return { cmd, pre };
    }
  }
  return null;
}

// One venv per (package, version), so upgrading facet never mutates an
// environment an older pinned invocation is still using.
function ensureVenv(py) {
  const root = path.join(os.homedir(), ".mcptoolshop", "facet", VERSION);
  const entry = path.join(venvBin(root), exe(ENTRY));
  if (fs.existsSync(entry)) return entry;

  process.stderr.write(`facet: preparing ${PKG}==${VERSION} (first run only)\n`);
  fs.mkdirSync(path.dirname(root), { recursive: true });

  let r = spawnSync(py.cmd, [...py.pre, "-m", "venv", root], { stdio: "inherit" });
  if (r.status !== 0) {
    die([
      "facet: could not create a virtual environment.",
      "",
      "Next step - on Debian/Ubuntu the venv module ships separately:",
      "  sudo apt install python3-venv",
      "",
      "Or install the package directly:",
      `  pipx install ${PKG}==${VERSION}`,
    ]);
  }

  const pip = path.join(venvBin(root), exe("pip"));
  r = spawnSync(pip, ["install", "--quiet", "--disable-pip-version-check", `${PKG}==${VERSION}`], {
    stdio: "inherit",
  });
  if (r.status !== 0 || !fs.existsSync(entry)) {
    // Leave nothing half-built: a partial venv would be found by the
    // fs.existsSync check above on the next run and silently used.
    try {
      fs.rmSync(root, { recursive: true, force: true });
    } catch {}
    die([
      `facet: could not install ${PKG}==${VERSION} from PyPI.`,
      "",
      "Next step - check network access to pypi.org, then re-run.",
      "If you are offline or behind a proxy, install it directly:",
      `  pipx install ${PKG}==${VERSION}`,
    ]);
  }
  return entry;
}

const py = findPython();
if (!py) noPythonError();

const entry = ensureVenv(py);
const r = spawnSync(entry, process.argv.slice(2), { stdio: "inherit" });
process.exit(r.status === null ? 1 : r.status);
