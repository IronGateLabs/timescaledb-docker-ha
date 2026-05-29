#!/usr/bin/env python3
"""Generate a first-pass PostgreSQL 16 STIG control mapping.

The mapping starts every PostgreSQL 16 control as unmapped. If a local legacy
profile controls directory is provided, the generator records only portable
summary counts and any direct identifier overlap.
"""

import argparse
import json
import os
import re
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[2]


def _safe_path(path):
    """Resolve a CLI-supplied path and reject anything outside the repo root.

    Sanitizes an operator-supplied argparse path before filesystem I/O so a
    traversal value cannot escape the repository tree.
    """
    resolved = Path(path).resolve()
    if os.path.commonpath([str(_REPO_ROOT), str(resolved)]) != str(_REPO_ROOT):
        raise SystemExit(f"refusing path outside repository root: {path}")
    return resolved


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("traceability", type=Path, help="Traceability JSON file")
    parser.add_argument("output", type=Path, help="Output mapping JSON file")
    parser.add_argument(
        "--legacy-controls-dir",
        type=Path,
        help="Optional local controls directory from a legacy validation profile",
    )
    return parser.parse_args()


def legacy_control_ids(path):
    if not path:
        return {}

    controls = {}
    for item in path.glob("V-*.rb"):
        if not item.is_file():
            continue
        text = item.read_text(errors="replace")
        tags = dict(re.findall(r"tag\s+([a-zA-Z0-9_]+):\s*['\"]([^'\"]+)['\"]", text))
        controls[item.stem] = {
            "control_id": item.stem,
            "stig_id": tags.get("stig_id", ""),
            "severity": tags.get("severity", ""),
            "srg_id": tags.get("gtitle", ""),
        }
    return controls


def stig_suffix(stig_id):
    return stig_id.split("-", 1)[1] if "-" in stig_id else stig_id


def main():
    args = parse_args()
    traceability_path = _safe_path(args.traceability)
    traceability = json.loads(traceability_path.read_text())
    controls = traceability["controls"]
    pg16_ids = {control["control_id"] for control in controls}
    legacy_controls = legacy_control_ids(args.legacy_controls_dir)
    legacy_ids = set(legacy_controls)
    direct_overlap = sorted(pg16_ids & legacy_ids)
    legacy_by_suffix = {}
    for control in legacy_controls.values():
        if control["stig_id"]:
            legacy_by_suffix.setdefault(stig_suffix(control["stig_id"]), []).append(control)

    mappings = []
    for control in controls:
        control_id = control["control_id"]
        suffix_candidates = legacy_by_suffix.get(stig_suffix(control["stig_id"]), [])
        candidate_ids = sorted(candidate["control_id"] for candidate in suffix_candidates)
        candidate_srg_ids = sorted(
            {candidate["srg_id"] for candidate in suffix_candidates if candidate["srg_id"]}
        )
        candidate_basis = []
        if candidate_ids:
            candidate_basis.append("stig_id_suffix")
        severity_mismatch = sorted(
            candidate["control_id"]
            for candidate in suffix_candidates
            if candidate["severity"] and candidate["severity"] != control["severity"]
        )

        mappings.append(
            {
                "control_id": control_id,
                "stig_id": control["stig_id"],
                "severity": control["severity"],
                "cci_refs": control["cci_refs"],
                "mapping_status": "direct_match" if control_id in direct_overlap else "unmapped",
                "legacy_control_ids": [control_id] if control_id in direct_overlap else [],
                "candidate_legacy_control_ids": candidate_ids,
                "candidate_srg_ids": candidate_srg_ids,
                "candidate_basis": candidate_basis,
                "candidate_warnings": {
                    "severity_mismatch": severity_mismatch,
                },
                "overlay_checks": [],
                "automation_status": "not_yet_assessed",
                "container_validation": "not_yet_assessed",
                "implementation_owner": "unassigned",
                "validation_owner": "unassigned",
                "deployment_responsibility": "undetermined",
                "notes": "",
            }
        )

    output = {
        "schema_version": 1,
        "source_traceability": str(args.traceability),
        "content_policy": "Control identifiers and project-authored metadata only; do not copy benchmark prose.",
        "legacy_profile_summary": {
            "controls_count": len(legacy_ids),
            "direct_overlap_count": len(direct_overlap),
            "stig_id_suffix_candidate_count": sum(
                1 for control in controls if legacy_by_suffix.get(stig_suffix(control["stig_id"]))
            ),
        },
        "mappings": mappings,
    }
    output_path = _safe_path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n")
    print(f"Wrote {len(mappings)} mappings to {args.output}")


if __name__ == "__main__":
    main()
