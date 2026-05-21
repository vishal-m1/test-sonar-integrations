# context.md — Demo - Form Submissions - Query Who Filled

## Purpose
Demonstrates how an n8n-hosted form can capture team registrations and expose a queryable endpoint that answers "who has filled the form" — with no external credentials required.

## What It Does
1. **Form - Register** (Form Trigger): Presents a public n8n form with three fields — Full Name, Email Address, and Department (dropdown: Engineering / Sales / Marketing / HR). On submit, immediately confirms to the user.
2. **Mock - Store Submission** (Code node): Extracts the submitted fields and simulates writing to a data store. Logs the payload to the n8n console. In production, swap this for a Google Sheets, Notion, or Airtable node.
3. **Query - Who Filled the Form?** (Manual Trigger): Acts as the query entry point. Triggered manually (or wired to a chat/webhook trigger in production).
4. **Mock - Fetch All Submissions** (Code node): Returns a hardcoded list of 4 mock submissions representing past form fills. In production, swap for a real data-source read.
5. **Format - Query Response** (Set node): Packages the result into a clean structured object with `query`, `totalSubmissions`, `submissions[]`, and a human-readable `summary` string.

## Tools & Connectors Used
| Tool / Service | How It's Used |
|---|---|
| n8n Form Trigger | Hosts the public registration form |
| n8n Code Node (×2) | Mocks submission storage and retrieval logic |
| n8n Set Node | Formats the query response payload |

## Credentials Required
None — this is a fully mocked demo. No credentials are needed to run or test this workflow.

## KPI Baseline
| Metric | Value |
|---|---|
| Manual time per run (before) | ~5 minutes (checking spreadsheet manually) |
| Estimated runs per month | 30 |
| Projected hours saved/month | ~2.5 hours |

## Risk Self-Assessment
| Risk Type | Present? | Notes |
|---|---|---|
| Handles PII / personal data | Yes | Collects name, email — swap mock store with a secure destination in production |
| Makes external API calls | No | All nodes are mocked |
| Involves financial data | No | |
| Requires human decision point | No | Fully automated |

## Submitter
**Name:** Vishal Mishra  
**Date:** 2026-05-21  
**n8n Workflow ID:** re0S04xprxf68XyV  
**Instance:** vishalmishra.app.n8n.cloud
