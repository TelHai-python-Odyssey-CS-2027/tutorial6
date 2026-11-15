"""Student-facing self-checks for Tutorial 6."""
from __future__ import annotations

import copy
from pathlib import Path


def _same(got, expected, tol=None):
    if tol is None:
        return got == expected
    try:
        return abs(got - expected) <= tol
    except TypeError:
        return False


def _run_groups(func, func_name, groups):
    earned = total = 0
    for title, points, cases in groups:
        problems = []
        for args, expected, tol, hint in cases:
            call = f"{func_name}({', '.join(repr(a) for a in args)})"
            try:
                got = func(*copy.deepcopy(args))
            except Exception as e:
                problems.append(
                    f"    Case failed: {call}\n    Raised {type(e).__name__}: {e}"
                )
                continue
            if not _same(got, expected, tol):
                msg = (
                    f"    Case failed: {call}\n"
                    f"    Expected: {expected!r}\n"
                    f"    Got:      {got!r}"
                )
                if hint:
                    msg += f"\n    Hint:     {hint}"
                problems.append(msg)
        total += points
        if problems:
            print(f"[FAIL] {title}  (0/{points} pt)")
            print("\n".join(problems))
        else:
            earned += points
            print(f"[PASS] {title}  ({points}/{points} pt)")
    print(f"\nSelf-check score: {earned}/{total}")
    return earned == total


LOAD_PATIENT_HR_GROUPS = [
    (
        "load_patient_hr: sample file",
        1,
        [
            (
                ("data/patients.tsv",),
                {"101": 72, "102": 88, "103": 65, "104": 95, "105": 70},
                None,
                "skip the header; id is a string, hr is an int",
            ),
        ],
    ),
]


def run_load_patient_hr_checks(func):
    return _run_groups(func, "load_patient_hr", LOAD_PATIENT_HR_GROUPS)


def run_write_high_hr_checks(func):
    patients = {"101": 72, "102": 88, "103": 65, "104": 95, "105": 70}
    out = Path("_tmp_high_hr.tsv")
    try:
        n = func(patients, 80, str(out))
    except Exception as e:
        print(f"[FAIL] write_high_hr raised {type(e).__name__}: {e}")
        return False
    ok = True
    if n != 2:
        print(f"[FAIL] write_high_hr should return 2, got {n!r}")
        ok = False
    if not out.is_file():
        print("[FAIL] output file was not created")
        return False
    lines = out.read_text(encoding="utf-8").splitlines()
    expected = {"102\t88", "104\t95"}
    got = set(lines)
    if got != expected:
        print(f"[FAIL] file content\n    Expected lines: {sorted(expected)}\n    Got: {lines}")
        ok = False
    else:
        print("[PASS] write_high_hr: count + file content")
    try:
        out.unlink()
    except OSError:
        pass
    print(f"\nSelf-check score: {1 if ok else 0}/1")
    return ok
