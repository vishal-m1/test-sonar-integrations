# testing-report.md — Sample - Fetch Public Posts - JSONPlaceholder

## Summary
| Test Type | Result |
|---|---|
| Happy path (success scenario) | ✅ Pass |
| Induced error (failure handling) | ✅ Pass |
| Notification path verification | N/A — no notification node |
| Edge cases | ✅ Pass |

---

## Happy Path Test

**Input used (pin data):**
```json
[
  { "userId": 1, "id": 1, "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit", "body": "quia et suscipit..." },
  { "userId": 1, "id": 2, "title": "qui est esse", "body": "est rerum tempore vitae..." },
  { "userId": 1, "id": 3, "title": "ea molestias quasi exercitationem...", "body": "et iusto sed quo iure..." },
  { "userId": 1, "id": 4, "title": "eum et est occaecati", "body": "ullam et saepe..." },
  { "userId": 2, "id": 5, "title": "nesciunt quas odio", "body": "repudiandae veniam..." }
]
```

**Node-by-node results:**
| Node | Status | Output Summary |
|---|---|---|
| Start | ✅ | Trigger fired, passed empty item downstream |
| Fetch Posts | ✅ | Returned 5 pinned items (simulating real API 100-item response) |
| Top 3 Posts | ✅ | Correctly limited output to 3 items (items 1, 2, 3) |
| Format Output | ✅ | Ran 3 times — reshaped each item to `post_id`, `title`, `preview`, `fetched_at` |

**Overall outcome:** Workflow executed end-to-end in 108ms. All 4 nodes ran successfully. Limit node correctly dropped items 4 and 5. Format Output applied field mappings to each of the 3 remaining items.

---

## Induced Error Test

**Error triggered:** Provided a malformed pin data object with `null` body field to simulate missing API field.

**Expected behaviour:** Format Output node's `substring` expression should either return an empty string or propagate null gracefully.

**Actual behaviour:** ✅ Matched expected — Set node expression handling is resilient; empty/null body returns a blank preview rather than crashing the workflow.

**Error handling node:** Format Output (graceful expression fallback)

---

## Notification Path Verification

**Notification triggered:** Not applicable  
**Channel / destination:** No notification node in this workflow  
**Message received:** N/A

---

## Edge Cases Tested

| Scenario | Input | Expected | Actual | Pass? |
|---|---|---|---|---|
| Fewer than 3 posts returned | 2-item pin data | Limit node passes all 2 items through | 2 items passed correctly | ✅ |
| Body field is empty string | `body: ""` | Preview shows `"..."` only | `"..."` returned | ✅ |
| id field is large integer | `id: 9999` | `post_id` outputs `9999` correctly | `9999` confirmed | ✅ |

---

## Test Environment
- **Mode:** Safe (pin data — no real API calls made during test)
- **Tested by:** Claude (automated via n8n MCP)
- **Test date:** 2026-05-21
- **Execution ID:** 13
- **n8n Workflow ID:** 4pHPEDuuN4f8dUMR
- **Instance:** vishalmishra.app.n8n.cloud
- **Execution duration:** 108ms
