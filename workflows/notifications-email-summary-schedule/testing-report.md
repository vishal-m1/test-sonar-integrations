# testing-report.md — Notifications - Email Summary - Schedule

## Summary
| Test Type | Result |
|---|---|
| Happy path (success scenario) | ⚠️ Blocked — see note |
| Induced error (failure handling) | ⚠️ Blocked — see note |
| Notification path verification | ⚠️ Blocked — see note |
| Edge cases | ⚠️ Blocked — see note |

> **Note:** All test executions on the n8n instance `vishalmishra.app.n8n.cloud` are currently blocked because the n8n Cloud trial has expired. The workflow code passed `validate_workflow` with 0 errors (3 nodes, valid connections). Logic was reviewed manually. Live testing must be completed after the plan is upgraded before this workflow goes active.

---

## Workflow Validation

**Validation result:** ✅ PASSED  
**Node count:** 3  
**Errors:** None  
**Method:** `validate_workflow` via n8n MCP

---

## Happy Path Test

**Intended input:** Schedule trigger fires (no external input required)  
**Expected node-by-node flow:**
| Node | Expected Status | Expected Output Summary |
|---|---|---|
| Daily Schedule | ✅ | Triggers at 08:00 daily, passes empty item downstream |
| Build Email Summary | ✅ | Produces `emailSubject` and `emailBody` fields with today's date |
| Send Email Summary | ✅ | Sends HTML email to vishalm@devsavant.com via Gmail OAuth2 |

**Blocked reason:** n8n Cloud trial expired — execution returned plan upgrade error (execution ID: 24).

---

## Induced Error Test

**Error to test:** Missing Gmail credential  
**Expected behaviour:** Gmail node fails with credential error; upstream nodes succeed  
**Status:** ⚠️ Could not run — instance blocked  

---

## Notification Path Verification

**Notification triggered:** Intended — the workflow IS the notification  
**Channel / destination:** Gmail → vishalm@devsavant.com  
**Message received:** Not verified — blocked by trial expiry  

---

## Edge Cases Tested

| Scenario | Input | Expected | Actual | Pass? |
|---|---|---|---|---|
| Schedule fires at exactly 08:00 | n/a | Email sent | Not tested | ⚠️ |
| Date expression renders correctly | $now | MMMM d, yyyy format | Not verified live | ⚠️ |

---

## Test Environment
- **Mode:** Safe test attempted (pin data) — blocked by plan expiry
- **Tested by:** Claude (automated)
- **Test date:** 2026-05-28
- **n8n Workflow ID:** qw0FJYszLkQmDZPz
- **Registry ID:** a91594db-fb1c-4fa9-9a24-5eac079d3441
- **Instance:** vishalmishra.app.n8n.cloud
- **Validation:** ✅ Passed via validate_workflow (0 errors)
