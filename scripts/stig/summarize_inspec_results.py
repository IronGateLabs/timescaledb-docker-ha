#!/usr/bin/env python3
"""Summarize CINC Auditor/InSpec JSON results by control ID."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def control_status(control: dict) -> str:
    results = control.get("results") or []
    statuses = {result.get("status", "unknown") for result in results}
    if not results:
        return "not_run"
    if "failed" in statuses:
        return "failed"
    if "skipped" in statuses:
        return "skipped"
    if statuses == {"passed"}:
        return "passed"
    return "unknown"


def iter_controls(report: dict):
    for profile in report.get("profiles", []):
        profile_name = profile.get("name", "unknown-profile")
        for control in profile.get("controls", []):
            yield profile_name, control


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--json", action="store_true", help="emit machine-readable summary")
    parser.add_argument(
        "--traceability",
        type=Path,
        help="include PostgreSQL 16 STIG traceability status counts",
    )
    args = parser.parse_args()

    if not args.report.exists():
        print(f"report not found: {args.report}", file=sys.stderr)
        return 2

    with args.report.open(encoding="utf-8") as report_file:
        report = json.load(report_file)

    # Collapse controls that appear in more than one profile (an include_controls
    # wrapper lists each control as not_run while the dependency profile carries the
    # real result); prefer the evaluated status so counts are not double-reported.
    by_id: dict = {}
    for profile_name, control in iter_controls(report):
        cid = control.get("id", "unknown-control")
        status = control_status(control)
        prev = by_id.get(cid)
        if prev is None or (prev["status"] == "not_run" and status != "not_run"):
            by_id[cid] = {
                "profile": profile_name,
                "control_id": cid,
                "status": status,
            }
    controls = list(by_id.values())
    counts: Counter[str] = Counter(control["status"] for control in controls)

    summary = {
        "total_controls": len(controls),
        "status_counts": dict(sorted(counts.items())),
        "controls": controls,
    }
    if args.traceability:
        with args.traceability.open(encoding="utf-8") as traceability_file:
            traceability = json.load(traceability_file)
        traceability_counts: Counter[str] = Counter(
            control.get("status", "unknown") for control in traceability.get("controls", [])
        )
        summary["traceability_total_controls"] = len(traceability.get("controls", []))
        summary["traceability_status_counts"] = dict(sorted(traceability_counts.items()))
        validation_state_counts: Counter[str] = Counter(
            control.get("validation_state")
            for control in traceability.get("controls", [])
            if control.get("status") == "validation_only" and control.get("validation_state")
        )
        summary["traceability_validation_only_states"] = dict(sorted(validation_state_counts.items()))

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"total_controls={summary['total_controls']}")
        for status, count in summary["status_counts"].items():
            print(f"{status}={count}")
        if args.traceability:
            print(f"traceability_total_controls={summary['traceability_total_controls']}")
            for status, count in summary["traceability_status_counts"].items():
                print(f"traceability_{status}={count}")
            for state, count in summary.get("traceability_validation_only_states", {}).items():
                print(f"traceability_validation_only_{state}={count}")
        for control in controls:
            print(f"{control['profile']} {control['control_id']} {control['status']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
