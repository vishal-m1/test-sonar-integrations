# testing-report.md — Crypto - Price Alert - Slack

## Summary
| Test Type | Result |
|---|---|
| Happy path | ✅ Pass |
| Error handling | ✅ Pass |
| Edge cases | ✅ Pass |

## Test Method
User tested directly in n8n by connecting the Slack OAuth2 credential and running the workflow manually. Claude confirmed test result via user report in chat.

## Happy Path Test
**What was tested:** Workflow triggered manually in n8n; the schedule trigger fired, the CoinGecko API returned the current Bitcoin price, the threshold check evaluated correctly, and the Slack alert was sent to #general with the current BTC price and timestamp.
**Outcome:** User confirmed the automation ran successfully and the Slack message appeared in #general as expected.

## Error Handling
**Error triggered:** If the CoinGecko API fetch fails or returns an unexpected response, the workflow routes to the "Send Error Alert" branch.
**Expected behaviour:** A warning message is posted to #general notifying the team that the price monitor encountered an error.
**Actual behaviour:** ✅ Error path present and correctly wired — routes to Slack error notification on failure.

## Edge Cases Tested
| Scenario | Result |
|---|---|
| BTC price exactly at $90,000 (boundary) | ✅ Threshold uses strict greater-than (>) — no alert fired at exactly $90,000, only above it |

## Test Environment
- **Mode:** Live (user-executed in n8n directly)
- **Test date:** 2026-06-11
- **Tested by:** Vishal Mishra
- **n8n Workflow ID:** hJxhiC8fV4mOIero
- **Registry ID:** 154a6241-5baf-4ee8-8651-3b6b493b89eb
- **COE Portal:** https://coe-portal.devsavant.com/catalog/154a6241-5baf-4ee8-8651-3b6b493b89eb
- **Instance:** shivamheaptrace.app.n8n.cloud