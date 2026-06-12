# testing-report.md — Files: Create Jira Task from Google Drive

## Summary
| Test Type | Result |
|---|---|
| Happy path | ✅ Pass |
| Error handling | ⚠️ Not tested — flagged for post-approval monitoring |
| Edge cases | ⚠️ Not tested — flagged for post-approval monitoring |

## Test Method
User tested directly in the automation editor by connecting credentials and uploading a file to the monitored Google Drive folder. User confirmed the result in chat.

## Happy Path Test
**What was tested:** User uploaded a file to the designated Google Drive folder and triggered the automation manually to confirm the full flow.
**Outcome:** User confirmed the automation ran successfully — a corresponding Jira Task was created in the ENG project with the correct file details.

## Error Handling
**Error triggered:** Not tested in this session.
**Expected behaviour:** If the Google Drive polling returns no new files, the automation exits silently with no Jira tasks created. If the Jira API call fails (e.g. invalid project key or auth error), the automation would error at the Create Jira Task node.
**Known gap:** Error path not explicitly tested — flagged for post-approval monitoring. Recommend adding an error notification (e.g. Slack alert) in a future iteration.

## Edge Cases Tested
| Scenario | Result |
|---|---|
| No new files in folder on polling interval | Not tested — flagged for post-approval monitoring |
| File uploaded with special characters in name | Not tested — flagged for post-approval monitoring |

## Test Environment
- **Mode:** Live (user-executed in automation editor directly)
- **Test date:** 2026-06-12
- **Tested by:** Vishal Mishra
- **n8n Workflow ID:** k8Y8SXrNH7VyNgGU
- **Registry ID:** 81f2e565-6b7a-4c49-9165-ef4a93345bfd
- **COE Portal:** https://coe-portal.devsavant.com/catalog/81f2e565-6b7a-4c49-9165-ef4a93345bfd
- **Instance:** shivamheaptrace.app.n8n.cloud