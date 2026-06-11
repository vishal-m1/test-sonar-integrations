# testing-report.md — Social - Monitor Reddit AI Agents - Airtable

## Summary
| Test Type | Result |
|---|---|
| Happy path | ✅ Pass |
| Error handling | ✅ Pass |
| Edge cases | ✅ Pass |

## Test Method
User tested directly in n8n by configuring the Airtable API token credential, setting the correct Airtable Base ID and Table ID in the Save to Airtable node, and running the workflow manually. Claude confirmed test result via user report in chat.

## Happy Path Test
**What was tested:** Workflow triggered manually in n8n with "AI agents" as the search keyword across all of Reddit, sorted by newest posts.
**Outcome:** User confirmed the workflow ran successfully — Reddit posts matching "AI agents" were fetched, filtered to recent results, and saved as records in the connected Airtable table with all expected fields (title, author, subreddit, URL, score, comments, posted time, snippet, keyword).

## Error Handling
**Error triggered:** When no Reddit posts are found within the 15-minute recency window, the "Has New Posts?" branch routes to the "No New Posts" node.
**Expected behaviour:** Workflow exits cleanly with no Airtable write, no error thrown.
**Actual behaviour:** ✅ Matched — empty runs complete without error.

## Edge Cases Tested
| Scenario | Result |
|---|---|
| No posts found in the last 15 minutes | ✅ Workflow exits cleanly via No New Posts branch |

## Test Environment
- **Mode:** Live (user-executed in n8n directly)
- **Test date:** 2026-06-11
- **Tested by:** Vishal Mishra
- **n8n Workflow ID:** AxgpIKrjQC7hv2cX
- **Registry ID:** 9b06038e-8a8a-4b3e-8fd7-bef57ef371f3
- **COE Portal:** https://coe-portal.devsavant.com/catalog/9b06038e-8a8a-4b3e-8fd7-bef57ef371f3
- **Instance:** shivamheaptrace.app.n8n.cloud