# testing-report.md — Messaging - Schedule Sync - Google Calendar

## Summary
| Test Type | Result |
|---|---|
| Happy path (success scenario) | ⏭️ Skipped — credentials not yet configured |
| Induced error (failure handling) | ⏭️ Skipped — credentials not yet configured |
| Notification path verification | ⏭️ Skipped — credentials not yet configured |
| Edge cases | ⏭️ Skipped — credentials not yet configured |

> ⚠️ **Testing skipped at author's request.** Credentials (Telegram API, Gmail OAuth2, OpenAI, Google Calendar OAuth2) have not yet been configured in the n8n instance. The workflow logic was validated via `validate_workflow` (9 nodes, no errors) and the workflow JSON was exported directly from `get_workflow_details` at submission time. Functional testing should be completed before admin approval.

---

## Happy Path Test

**Input used:** Not run — credentials not configured  
**Node-by-node results:**
| Node | Status | Output Summary |
|---|---|---|
| Telegram: New Message | ⏭️ Skipped | Requires Telegram API credential |
| Normalize: Telegram | ⏭️ Skipped | Depends on trigger |
| Gmail: New Email | ⏭️ Skipped | Requires Gmail OAuth2 credential |
| Normalize: Gmail | ⏭️ Skipped | Depends on trigger |
| AI: Extract Schedule | ⏭️ Skipped | Requires OpenAI credential |
| IF: Has Schedule? | ⏭️ Skipped | Depends on AI output |
| Google Calendar: Create Event | ⏭️ Skipped | Requires Google Calendar OAuth2 credential |
| No Schedule Found | ⏭️ Skipped | Depends on IF branch |

**Overall outcome:** Not tested

---

## Induced Error Test

**Error triggered:** Not run  
**Expected behaviour:** If AI extraction fails or credentials are misconfigured, n8n's built-in error handling surfaces the failure with a node-level error message  
**Actual behaviour:** Not verified  
**Error handling node:** n8n default node error handling

---

## Notification Path Verification

**Notification triggered:** N/A  
**Channel / destination:** Google Calendar primary calendar  
**Message received:** Not verified

---

## Edge Cases Tested

| Scenario | Input | Expected | Actual | Pass? |
|---|---|---|---|---|
| Message with no schedule (e.g. "Hey, how are you?") | Plain greeting text | `hasEvent = false` → No Calendar event created | Not tested | ⏭️ |
| Relative date ("tomorrow at 3pm") | Telegram message | AI resolves to correct IST datetime | Not tested | ⏭️ |
| Missing end time | "Meeting at 10am" | AI defaults end to 1 hour after start | Not tested | ⏭️ |
| Gmail with no schedule | Promotional email | `hasEvent = false` → silent pass-through | Not tested | ⏭️ |

---

## Test Environment
- **Mode:** Not run
- **Tested by:** Not tested (skipped at author request — credentials not configured)
- **Test date:** 2026-05-28
- **n8n Workflow ID:** 165zy4HYEoaJpUdC
- **Registry ID:** ffaab575-938b-4366-914d-6bdc3a0a6097
- **Instance:** vishalmishra.app.n8n.cloud
- **Validation:** `validate_workflow` passed — 9 nodes, 0 errors
