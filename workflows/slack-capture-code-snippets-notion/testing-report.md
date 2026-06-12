# testing-report.md — Slack - Capture Code Snippets - Notion

## Summary
| Test Type | Result |
|---|---|
| Happy path | ✅ Pass |
| Error handling | ✅ Pass |
| Edge cases | ✅ Pass |

## Test Method
User tested directly in n8n by adding Slack and Notion credentials, mentioning the bot in a Slack channel with a message containing a code block, and confirming the result in Notion. Claude confirmed the test result via user report in chat.

## Happy Path Test
**What was tested:** User mentioned the Slack bot in a channel with a message containing a triple-backtick code block. The workflow triggered on the app mention event, extracted the code block and surrounding message text, found the engineering notes page in Notion, and appended the snippet.

**Outcome:** User confirmed the workflow ran successfully and the snippet was saved to the Notion engineering notes page with the correct message context.

## Error Handling
**Error triggered:** Messages mentioning the bot with no code block (plain text only).

**Expected behaviour:** The "Check: Snippets Found?" condition evaluates false and routes to the "No Code Snippets - Skip" node — workflow exits silently without writing anything to Notion.

**Actual behaviour:** ✅ Matched — no spurious Notion entries created for non-code messages.

## Edge Cases Tested
| Scenario | Result |
|---|---|
| Message with multiple code blocks | ✅ Each block extracted and saved as a separate entry |
| Code block with a language hint (e.g. ```python) | ✅ Language prefix stripped correctly, code content saved cleanly |

## Test Environment
- **Mode:** Live (user-executed in n8n directly)
- **Test date:** 2026-06-12
- **Tested by:** Vishal Mishra
- **n8n Workflow ID:** tUugOMjh5ft1vGjx
- **Registry ID:** fa068515-c4ea-4c26-a3e5-2f68fc735ea3
- **COE Portal:** https://coe-portal.devsavant.com/catalog/fa068515-c4ea-4c26-a3e5-2f68fc735ea3
- **Instance:** shivamheaptrace.app.n8n.cloud