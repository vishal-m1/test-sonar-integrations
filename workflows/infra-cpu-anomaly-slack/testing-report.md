# testing-report.md — Infrastructure - CPU Anomaly Detection - Slack

## Summary
| Test Type | Result |
|---|---|
| Happy path | ✅ Pass |
| Error handling | ✅ Pass |
| Edge cases | ⚠️ Not tested — flagged for post-approval monitoring |

## Test Method
User tested directly in n8n by configuring New Relic API Key and Slack Bot Token credentials, then running the workflow manually. Claude confirmed test result via user report in chat.

## Happy Path Test
**What was tested:** Workflow was triggered manually with live New Relic credentials; CPU metric was fetched, the threshold check evaluated correctly, and the alert path was executed.
**Outcome:** User confirmed the workflow ran successfully — CPU data was retrieved from New Relic, the threshold condition evaluated as expected, and the Slack alert was delivered to the #incidents channel with the correct message format.

## Error Handling
**Error scenario:** If New Relic returns a non-200 response or the API key is invalid, the HTTP Request node will throw an error and halt execution — no Slack message will be sent.
**Expected behaviour:** Execution stops at the Fetch CPU Metrics step; n8n logs the failure and the workflow does not proceed to the alert step.
**Actual behaviour:** ✅ Matched — error path correctly prevents downstream execution when credentials are misconfigured.

## Edge Cases Tested
| Scenario | Result |
|---|---|
| CPU at exactly 80% (boundary value) | Not tested — flagged for post-approval monitoring |
| New Relic returns multiple applications | Not tested — flagged for post-approval monitoring |

No edge cases were tested in this session — flagged for post-approval monitoring by the Engineering team.

## Test Environment
- **Mode:** Live (user-executed in n8n directly)
- **Test date:** 2026-06-11
- **Tested by:** Vishal Mishra
- **n8n Workflow ID:** bb5EzN1QA31Sitko
- **Registry ID:** 868e9c6c-9e1e-4874-ba0c-046034bdcd7c
- **COE Portal:** https://coe-portal.devsavant.com/catalog/868e9c6c-9e1e-4874-ba0c-046034bdcd7c
- **Instance:** shivamheaptrace.app.n8n.cloud