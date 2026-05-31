# PostgreSQL 16 Candidate Mapping Review

This review uses identifiers only. Candidate links are not confirmed validation coverage.

## Candidate Summary

- 94 PostgreSQL 16 controls have one legacy candidate by normalized `stig_id` suffix.
- 17 of those candidates have a severity mismatch and need higher-priority review.
- 17 PostgreSQL 16 controls have no legacy candidate by normalized `stig_id` suffix.
- 61 same-severity candidates with executable legacy validation have been promoted to partial reusable mappings.
- 16 same-severity candidates without executable legacy validation have been classified as `manual_only`.
- 34 previously unresolved PostgreSQL 16 controls have been reviewed.
- 0 PostgreSQL 16 controls remain `unmapped`.
- 20 controls are covered by repository-owned overlay checks.
- 22 controls are classified as `deployment_owned`.
- 2 controls remain `manual_only`.

## Remaining Unmapped Categories

- 0 severity mismatch candidates.
- 0 controls with no legacy candidate.

## Reviewed Severity Mismatch Candidates

| PG16 control | PG16 STIG ID | Legacy candidate | SRG ID |
| --- | --- | --- | --- |
| V-261858 | CD16-00-000200 | V-233512 | SRG-APP-000099-DB-000043 |
| V-261859 | CD16-00-000300 | V-233513 | SRG-APP-000456-DB-000390 |
| V-261861 | CD16-00-000500 | V-233515 | SRG-APP-000023-DB-000001 |
| V-261864 | CD16-00-000800 | V-233519 | SRG-APP-000172-DB-000075 |
| V-261865 | CD16-00-000900 | V-233520 | SRG-APP-000033-DB-000084 |
| V-261882 | CD16-00-002700 | V-233535 | SRG-APP-000360-DB-000320 |
| V-261883 | CD16-00-002800 | V-233536 | SRG-APP-000109-DB-000321 |
| V-261886 | CD16-00-003200 | V-233540 | SRG-APP-000133-DB-000198 |
| V-261894 | CD16-00-004100 | V-233547 | SRG-APP-000381-DB-000361 |
| V-261896 | CD16-00-004400 | V-233551 | SRG-APP-000494-DB-000344 |
| V-261901 | CD16-00-005200 | V-233559 | SRG-APP-000501-DB-000336 |
| V-261926 | CD16-00-008000 | V-233583 | SRG-APP-000514-DB-000382 |
| V-261927 | CD16-00-008100 | V-233584 | SRG-APP-000416-DB-000380 |
| V-261939 | CD16-00-009500 | V-233596 | SRG-APP-000171-DB-000074 |
| V-261946 | CD16-00-010200 | V-233602 | SRG-APP-000176-DB-000068 |
| V-261961 | CD16-00-011700 | V-233614 | SRG-APP-000340-DB-000304 |
| V-261966 | CD16-00-012300 | V-233619 | SRG-APP-000179-DB-000114 |

## Reviewed No Legacy Candidate Controls

| PG16 control | PG16 STIG ID | CCI refs |
| --- | --- | --- |
| V-261866 | CD16-00-001000 | CCI-000130 |
| V-261871 | CD16-00-001500 | CCI-001487 |
| V-261872 | CD16-00-001600 | CCI-000135 |
| V-261888 | CD16-00-003400 | CCI-000381 |
| V-261891 | CD16-00-003800 | CCI-000196 |
| V-261892 | CD16-00-003900 | CCI-000197 |
| V-261919 | CD16-00-007300 | CCI-001855 |
| V-261921 | CD16-00-007500 | CCI-001890 |
| V-261922 | CD16-00-007600 | CCI-001889 |
| V-261925 | CD16-00-007900 | CCI-001814 |
| V-261934 | CD16-00-009000 | CCI-002754 |
| V-261942 | CD16-00-009800 | CCI-000172 |
| V-261952 | CD16-00-010800 | CCI-000172 |
| V-261953 | CD16-00-010900 | CCI-000172 |
| V-261954 | CD16-00-011000 | CCI-000172 |
| V-261967 | CD16-00-012400 | CCI-001851 |
| V-283674 | CD16-00-009300 | CCI-003376 |

## Remaining Manual-Only Controls

| PG16 control | PG16 STIG ID | Rationale |
| --- | --- | --- |
| V-261934 | CD16-00-009000 | Requires system-specific behavioral evidence beyond a generic image assertion. |
| V-261954 | CD16-00-011000 | Requires application- and data-model-specific evidence beyond a generic image assertion. |
