# testing-report.md — Notifications - Telegram Message - Email & Google Sheets

## Summary
| Test Type | Result |
|---|---|
| Happy path (success scenario) | ✅ Pass (pin data — logic verified) |
| Induced error (failure handling) | ⚠️ Not executed (n8n trial expired) |
| Notification path verification | ✅ Pass (email node wiring confirmed) |
| Edge cases | ⚠️ Deferred to post-credential setup |

---

## Happy Path Test

**Input used:**
```json
{
  "message": {
    "message_id": 12345,
    "from": { "id": 987654321, "first_name": "Vishal", "last_name": "Mishra", "username": "vishalm" },
    "chat": { "id": 987654321, "type": "private" },
    "date": 1716800000,
    "text": "Hey, can we push the client demo to Thursday?"
  },
  "update_id": 99999001
}
```

**Node-by-node results:**
| Node | Status | Output Summary |
|---|---|---|
| Telegram - New Message | ✅ | Pin data accepted correctly |
| Format Message Data | ✅ | All 7 fields extracted |
| Gmail - Send Email | ⚠️ | Pinned — wiring verified |
| Google Sheets - Log Message | ⚠️ | Pinned — column mapping verified |

---

## Test Environment
- **Mode:** Safe (pin data)
- **Tested by:** Claude (automated)
- **Test date:** 2026-05-27
- **n8n Workflow ID:** mT2nuqc40wefhAMQ
- **Registry ID:** 44dd4daa-f887-4afc-93fb-833c0cfd1700
- **Instance:** vishalmishra.app.n8n.cloud
