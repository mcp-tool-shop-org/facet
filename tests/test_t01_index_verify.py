"""T1 / T1b - the four-leg index verify and E16-1's encoding matrix.

Source: the E15 ritual (build + verify, seeded set 19); E16-1's anchor
(Ruling 31f - verify crashed under cp1252 at the completeness branch, and a
verifier whose FAILURE report cannot print is a check that cannot fail).

The PASSED line is read FROM ITS POSITION - the last non-empty line of the
verify output - never matched anywhere in prose, because verify quotes the
record and the record contains the word PASSED.

Both tests build/verify a per-run scratch --db, so the derived tracked DB is
never touched and leg 1's det temps get per-run paths. What the `fold` marker
still covers: the CORPUS itself is read live, and in a shared working copy a
concurrent fold writing docs/ between leg 1's two builds is a real race.
"""
import pytest

from conftest import run_py, last_nonempty

PASSED_LINE = "VERIFY PASSED - all four legs"


def _assert_verify_passed(rc, out, err, label):
    assert rc == 0, "%s: verify exited %d\nstdout:\n%s\nstderr:\n%s" % (label, rc, out, err)
    last = last_nonempty(out)
    assert last == PASSED_LINE, (
        "%s: the last non-empty line is not the PASSED line.\n"
        "expected: %r\ngot:      %r" % (label, PASSED_LINE, last))
    # the seeded set is 19 (the E15 ritual). A larger seeded set is a
    # deliberate change and updates this line in the same commit, per the law.
    assert any(ln.strip() == "19 / 19" for ln in out.splitlines()), (
        "%s: seeded-set summary '19 / 19' not found in verify output" % label)


@pytest.mark.fold
def test_t01_build_and_verify(built_db):
    rc, out, err = run_py("facet_index.py", ["verify", "--db", built_db])
    _assert_verify_passed(rc, out, err, "T1")
    # the discovery rule must be auditable in the transcript (E16-9): verify
    # prints what each glob found, so a document that stops matching is
    # visible rather than inferred from a count that looks plausible
    assert "[corpus] ruling documents discovered by the sorted glob" in out
    assert "[corpus] kickoff documents discovered by the sorted glob" in out
    # T15 (E17 amendment) and T15b (E17 Ruling 3e): the E16 and E17 arcs' count
    # legs are present and passing. The COUNT itself is not pinned here -
    # verify's own grep==db comparison is the invariant; this asserts the legs
    # exist and hold, so a leg silently dropped from COUNT_CHECKS is caught.
    import re
    for leg in ("E16 numbered rulings", "E16 lettered sub-rulings",
                "E17 numbered rulings", "E17 lettered sub-rulings"):
        assert re.search(re.escape(leg) + r"\s+grep\s+\d+\s+db\s+\d+\s+ok", out), (
            "count leg %r missing or not ok in verify output" % leg)
    assert re.search(r"E16 sequence\s+ruling 1-7 gaps: none", out), (
        "E16 sequence check missing or gapped")
    assert re.search(r"E17 sequence\s+ruling 1-4 gaps: none", out), (
        "E17 sequence check missing or gapped")
    # reported, not asserted: which determinism leg held (the .dump fallback is
    # pre-registered and legal; byte-identity is what this rig has measured)
    det = [ln for ln in out.splitlines() if ln.startswith("determinism leg that held:")]
    print("T1 %s" % (det[0] if det else "determinism-leg line not found"))


@pytest.mark.fold
@pytest.mark.parametrize("enc", ["utf-8", "cp1252"])
def test_t01b_encoding_matrix(built_db, enc):
    # cp1252 is FORCED rather than inherited so the leg reproduces Ruling
    # 31f's crash condition on any platform - on ubuntu CI the platform
    # default is utf-8 and a "default encoding" leg would silently test
    # nothing. Before E16-1 the cp1252 leg dies at facet_index.py:1768.
    rc, out, err = run_py(
        "facet_index.py", ["verify", "--db", built_db],
        env_extra={"PYTHONIOENCODING": enc}, encoding=enc)
    _assert_verify_passed(rc, out, err, "T1b[%s]" % enc)
