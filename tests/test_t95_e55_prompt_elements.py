"""T95 — the E55 Gate B element counter.

Fixtures are SYNTHETIC. The instrument reads prompt JSONs and E55's own manifest is a
prompt JSON, so pointing these legs at the real corpus would put the instrument inside its
own population — the E28 law. Nothing here touches `facet_E08` or the arc's manifest.

Each leg is written to fail if the rule is wrong in the specific way that leg exists to
catch, rather than to pass under any plausible implementation.
"""
import importlib.util
import json
import pathlib

import pytest

MOD = (pathlib.Path(__file__).resolve().parents[1]
       / "tools" / "diagnostics" / "e55_prompt_elements.py")


def _load():
    spec = importlib.util.spec_from_file_location("e55_prompt_elements", MOD)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


e55 = _load()


def test_comma_split_is_the_surface_count():
    r = e55.count_prompt("a red hat, a blue coat, green boots")
    assert r["prompt_surfaces"] == 3
    assert r["unique_elements"] == 3


def test_with_split_separates_two_occupants_in_one_comma_phrase():
    """CAN-FAIL leg for rule step 3.

    'X with Y' packs two occupants onto two different surfaces. A rule that only splits on
    commas returns 2 here. The assertion below is 3, so it FAILS under the comma-only
    implementation this step replaces — which is the property this leg exists to prove.
    """
    p = "a purple cloak with a silver clasp, green boots"
    r = e55.count_prompt(p)
    assert r["prompt_surfaces"] == 2, "comma split must still see 2 comma phrases"
    assert r["unique_elements"] == 3, (
        "' with ' split not applied: %s" % r["unique"])
    assert "a purple cloak" in r["unique"]
    assert "a silver clasp" in r["unique"]


def test_style_stoplist_drops_only_declared_phrases():
    r = e55.count_prompt(
        "a silver clasp, plain grey background, visible brushstrokes, "
        "painterly worked surface, seen from the front")
    assert r["unique"] == ["a silver clasp"]
    assert len(r["style_dropped"]) == 4
    # a phrase that merely CONTAINS a stop word is not dropped
    r2 = e55.count_prompt("a background-grey tabard")
    assert r2["unique_elements"] == 1


def test_dedupe_is_case_insensitive_and_first_seen():
    r = e55.count_prompt("green boots, GREEN BOOTS, a red hat, green boots")
    assert r["unique_elements"] == 2
    assert r["unique"] == ["green boots", "a red hat"]


def test_gate_a_raises_on_missing_artifact(tmp_path):
    with pytest.raises(FileNotFoundError):
        e55.load_prompt(str(tmp_path / "absent.json"), "prompt")


def test_gate_a_raises_on_missing_key(tmp_path):
    p = tmp_path / "a.json"
    p.write_bytes(json.dumps({"other": "x"}).encode("utf-8"))
    with pytest.raises(KeyError):
        e55.load_prompt(str(p), "prompt")


def test_gate_a_raises_on_empty_prompt(tmp_path):
    p = tmp_path / "a.json"
    p.write_bytes(json.dumps({"prompt": "   "}).encode("utf-8"))
    with pytest.raises(ValueError):
        e55.load_prompt(str(p), "prompt")


def test_gate_a_reaches_a_nested_workflow_node():
    """A saved ComfyUI workflow keeps its prompt at 7.inputs.text. Reaching it by dotted
    path is what keeps it a PRIMARY artifact instead of a hand-retyped manifest string."""
    import tempfile
    import os
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    try:
        with open(path, "wb") as fh:
            fh.write(json.dumps(
                {"7": {"inputs": {"text": "a red hat, green boots"}}}).encode("utf-8"))
        assert e55.load_prompt(path, "7.inputs.text") == "a red hat, green boots"
        with pytest.raises(KeyError):
            e55.load_prompt(path, "7.inputs.nope")
    finally:
        os.unlink(path)


def test_tier_is_constrained_not_free_text(tmp_path):
    art = tmp_path / "g.json"
    art.write_bytes(json.dumps({"prompt": "a red hat"}).encode("utf-8"))
    man = tmp_path / "m.json"
    man.write_bytes(json.dumps({"arms": [
        {"name": "X", "file": str(art), "key": "prompt", "tier": "guessed"}]}).encode("utf-8"))
    with pytest.raises(ValueError):
        e55.run(str(man))


def test_manifest_roundtrip_reports_counts(tmp_path):
    art = tmp_path / "g.json"
    art.write_bytes(json.dumps(
        {"prompt": "a burly warrior with a long red beard, gold knee plates, "
                   "plain grey background"}).encode("utf-8"))
    man = tmp_path / "m.json"
    man.write_bytes(json.dumps({"arms": [
        {"name": "X", "file": str(art), "key": "prompt",
         "tier": "as-generated"}]}).encode("utf-8"))
    res = e55.run(str(man))
    assert len(res["arms"]) == 1
    row = res["arms"][0]
    assert row["prompt_surfaces"] == 3
    assert row["unique_elements"] == 3   # warrior + beard + knee plates; background dropped
    assert row["tier"] == "as-generated"
    assert res["rule"] and res["stop_list"]


def test_selftest_legs_run():
    e55.selftest()
