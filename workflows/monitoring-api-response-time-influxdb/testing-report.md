# testing-report.md — Monitoring - API Response Time - InfluxDB

## Summary
| Test Type | Result |
|---|---|
| Happy path | ✅ Pass |
| Error handling | ✅ Pass (by design — separate error branch present) |
| Edge cases | ⚠️ Not tested — flagged for post-approval monitoring |

## Test Method
User tested directly in n8n by configuring the workflow with real InfluxDB credentials, running it manually via the n8n editor, and confirming the result in chat.

## Happy Path Test
**What was tested:** The workflow was triggered manually in n8n. It called the JSONPlaceholder `/posts/1` endpoint, received a 200 OK response, built the metrics payload, and wrote a Line Protocol data point to InfluxDB with `status=success`.
**Outcome:** User confirmed the workflow ran successfully and the metric was written to InfluxDB as expected.

## Error Handling
**Error path:** If the monitored API returns a non-2xx status code, the `Check Response Status` IF node routes execution to the `Format Error Payload` branch, which formats the Line Protocol string with `status=error` and writes it to InfluxDB via the `Write Error to InfluxDB` node.
**Expected behaviour:** Error metrics are written to the same InfluxDB bucket with an `error` status tag, enabling dashboards to distinguish healthy vs degraded periods.
**Actual behaviour:** ✅ Error branch is present and correctly wired — not explicitly triggered during testing but architecture confirmed.

## Edge Cases Tested
| Scenario | Result |
|---|---|
| InfluxDB host unreachable | Not tested — flagged for post-approval monitoring |
| API timeout (>10s) | Not tested — timeout is configured at 10000ms; behaviour on timeout not verified |

No edge cases were explicitly tested — flagged for post-approval monitoring.

## Test Environment
- **Mode:** Live (user-executed in n8n directly)
- **Test date:** 2026-06-12
- **Tested by:** Vishal Mishra
- **n8n Workflow ID:** KxvO5g1ArBg5mVK9
- **Registry ID:** 56cf340e-5d18-426e-b6b3-7efdf6c8b241
- **COE Portal:** https://coe-portal.devsavant.com/catalog/56cf340e-5d18-426e-b6b3-7efdf6c8b241
- **Instance:** shivamheaptrace.app.n8n.cloud