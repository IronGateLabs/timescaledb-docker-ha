#!/usr/bin/env python3
"""Summarize CINC Auditor/InSpec JSON results by control ID."""

from __future__ import annotations

import argparse
import json
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
    args = parser.parse_args()

    with args.report.open(encoding="utf-8") as report_file:
        report = json.load(report_file)

    controls = []
    counts: Counter[str] = Counter()
    for profile_name, control in iter_controls(report):
        status = control_status(control)
        counts[status] += 1
        controls.append(
            {
                "profile": profile_name,
                "control_id": control.get("id", "unknown-control"),
                "status": status,
            }
        )

    summary = {
        "total_controls": len(controls),
        "status_counts": dict(sorted(counts.items())),
        "controls": controls,
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"total_controls={summary['total_controls']}")
        for status, count in summary["status_counts"].items():
            print(f"{status}={count}")
        for control in controls:
            print(f"{control['profile']} {control['control_id']} {control['status']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
