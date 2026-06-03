# testing-report.md — Payments - Create Jira Ticket - On Stripe Failure

## Summary
| Test Type | Result |
|---|---|
| Happy path (success scenario) | ✅ Pass |
| Edge case — charge.failed with GBP + fallback failure_message | ✅ Pass |
| Notification path verification | N/A — no notification node in this workflow |

---

## Happy Path Test

**Input used:**
```json
{
  "type": "payment_intent.payment_failed",
  "id": "evt_test_3NkQr2LkdIwHu7ix29K6X8Yp",
  "data": {
    "object": {
      "id": "pi_3NkQr2LkdIwHu7ix29K6X8Yp",
      "amount": 4999,
      "currency": "usd",
      "customer": "cus_TestABC123",
      "last_payment_error": { "message": "Your card was declined." }
    }
  }
}
```

**Node-by-node results:**
| Node | Status | Output Summary |
|---|---|---|
| Stripe Payment Failure | ✅ | Pinned — simulated `payment_intent.payment_failed` event |
| Format Issue Data | ✅ | summary: `"Payment Failure: payment_intent.payment_failed — pi_3NkQr2..."`, amount: `49.99 USD`, failure reason: `"Your card was declined."` |
| Create Jira Issue | ✅ | Pinned — returned `PAYMENTS-42` |

**Overall outcome:** Stripe event received → issue summary and description correctly formatted → Jira ticket created successfully.

---

## Edge Case Test — charge.failed with GBP and fallback failure_message field

**Scenario:** Some Stripe charge events use `failure_message` instead of `last_payment_error.message`. Currency is GBP. Amount must be correctly divided by 100.

**Input used:**
```json
{
  "type": "charge.failed",
  "id": "evt_test_charge_failed_edge",
  "data": {
    "object": {
      "id": "ch_3NkQr2EdgeCase",
      "amount": 1200,
      "currency": "gbp",
      "customer": "cus_EdgeCase999",
      "failure_message": "Insufficient funds"
    }
  }
}
```

**Node-by-node results:**
| Node | Status | Output Summary |
|---|---|---|
| Format Issue Data | ✅ | summary: `"Payment Failure: charge.failed — ch_3NkQr2EdgeCase"`, amount: `12 GBP`, failure reason: `"Insufficient funds"` (fallback field used correctly) |
| Create Jira Issue | ✅ | Pinned — passed correct formatted fields |

**Overall outcome:** Fallback `failure_message` field logic works correctly. Currency conversion and uppercasing correct for GBP.

---

## Notification Path Verification

**Notification triggered:** N/A
**Notes:** This workflow creates a Jira ticket as the notification mechanism. No separate notification node.

---

## Test Environment
- **Mode:** Safe (pin data) — Stripe trigger and Jira create node were pinned; Format Issue Data executed live
- **Execution ID:** 12
- **Tested by:** Claude (automated)
- **Test date:** 2026-06-03
- **n8n Workflow ID:** cVpYw0iPd2fb9cjH
- **Registry ID:** 905a3326-eb03-4327-919c-972bc31ec22e
- **COE Portal:** http://localhost:3000/catalog/905a3326-eb03-4327-919c-972bc31ec22e
- **Instance:** shivamheaptrace.app.n8n.cloud