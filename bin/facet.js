#!/usr/bin/env node
"use strict";

// Pure JSON config - npm-launcher derives the asset names from convention:
//   binary:    facet-0.2.0-linux-x64  /  facet-0.2.0-win-x64.exe
//   checksums: checksums-0.2.0.txt
// It downloads from the GitHub Release for `tag`, verifies SHA256, caches, and
// execs with argv passthrough.
//
// This is the org's standard wrapper and it is standard ON PURPOSE. An earlier
// draft of this file hand-rolled a pip bootstrap instead, on the reasoning that
// facet-mcp is small enough to install from PyPI in a couple of seconds. That
// traded away the thing npm-launcher exists to provide - `npx` that works with
// NO Python on the machine - plus SHA256 verification of what actually gets
// executed, for the sake of avoiding one build matrix. Measured before
// reverting: the PyInstaller binary is 21 MB and runs. The reason backpropagate
// abandoned binaries (torch past GitHub's 2GB asset cap) does not apply to a
// package whose dependencies are stdlib, sqlite3 and mcp.
process.env.MCPTOOLSHOP_LAUNCH_CONFIG = JSON.stringify({
  toolName: "facet",
  owner: "mcp-tool-shop-org",
  repo: "facet",
  version: "0.6.0",
  tag: "v0.6.0",
});

require("@mcptoolshop/npm-launcher/bin/mcptoolshop-launch.js");
