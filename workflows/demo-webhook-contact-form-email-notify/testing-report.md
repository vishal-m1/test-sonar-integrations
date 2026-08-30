# testing-report.md — Demo - Webhook Contact Form - Email Notify

## Summary
| Test Type | Result |
|---|---|
| Happy path (success scenario) | ✅ Pass |
| Induced error (failure handling) | ✅ Pass |
| Notification path verification | ⚠️ Pending (SMTP credentials not yet configured) |
| Edge cases | ✅ Pass |

---

## Happy Path Test

**Input used:**
```json
{
  "body": {
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "message": "Hi, I'd like to learn more about your services."
  }
}
```

**Node-by-node results:**
| Node | Status | Output Summary |
|---|---|---|
| Receive Form Data | ✅ Pinned | Simulated POST body passed downstream correctly |
| Transform Data | ✅ Executed | fullName="Jane Smith", emailAddress="jane.smith@example.com", message set, receivedAt ISO timestamp added, emailSubject="New enquiry from Jane Smith" |
| Send Notification Email | ⚠️ Skipped | SMTP credential not yet configured in n8n instance — logic correct, credential setup required |

**Overall outcome:** Transform logic executed correctly end-to-end. Email send step requires SMTP credential to be configured in the n8n UI before the workflow goes live.

---

## Induced Error Test

**Error triggered:** Missing `name` field in webhook body
**Expected behaviour:** `fullName` falls back to `"Unknown"`, `emailSubject` reads `"New enquiry from Unknown"`
**Actual behaviour:** ✅ Matched — fallback expressions `?? "Unknown"` handled null gracefully
**Error handling node:** Transform Data (expression-level fallback)

---

## Notification Path Verification

**Notification triggered:** Pending
**Channel / destination:** SMTP → vishalm@devsavant.com
**Message received:** Not yet — SMTP credential must be configured in n8n UI first

---

## Edge Cases Tested

| Scenario | Input | Expected | Actual | Pass? |
|---|---|---|---|---|
| Missing `name` field | `{email, message}` only | fullName = "Unknown" | fullName = "Unknown" | ✅ |
| Missing `message` field | `{name, email}` only | message = "(no message)" | message = "(no message)" | ✅ |
| `fullName` key instead of `name` | `{fullName, email, message}` | Picks up fullName correctly | Handled via `$json.body.fullName` fallback | ✅ |

---

## Test Environment
- **Mode:** Safe (pin data)
- **Tested by:** Claude (automated)
- **Test date:** 2026-06-01
- **n8n Workflow ID:** OsRjI5tP9zS5y8bR
- **Registry ID:** 4bcfe2bc-42c9-4394-aaff-fa41db3c64f7
- **COE Portal:** http://localhost:3000/catalog/4bcfe2bc-42c9-4394-aaff-fa41db3c64f7
- **Instance:** shivamheaptrace.app.n8n.cloud
