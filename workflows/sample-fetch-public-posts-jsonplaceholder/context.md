# context.md — Sample - Fetch Public Posts - JSONPlaceholder

## Purpose
This is a sample/demo workflow that demonstrates the full n8n build-test-publish pipeline. It fetches public posts from the JSONPlaceholder API, limits the results to the top 3, and formats each into a clean output object.

## What It Does
1. **Manual Trigger** — A team member clicks "Execute" to start the workflow
2. **Fetch Posts** — Makes a GET request to `https://jsonplaceholder.typicode.com/posts` and retrieves 100 sample blog posts
3. **Top 3 Posts** — Limits the result set to the first 3 items
4. **Format Output** — Reshapes each item into a clean structure with `post_id`, `title`, `preview` (first 60 chars of body), and `fetched_at` timestamp

## Tools & Connectors Used
| Tool / Service | How It's Used |
|---|---|
| HTTP Request | Fetches data from the public JSONPlaceholder API |
| Limit | Restricts output to the first 3 records |
| Edit Fields (Set) | Formats and reshapes the output fields |

## Credentials Required
_None — JSONPlaceholder is a public API requiring no authentication._

## KPI Baseline
| Metric | Value |
|---|---|
| Manual time per run (before) | ~5 minutes (manual copy-paste from API) |
| Estimated runs per month | 10 (demo / onboarding use) |
| Projected hours saved/month | ~0.8 hours |

## Risk Self-Assessment
| Risk Type | Present? | Notes |
|---|---|---|
| Handles PII / personal data | No | JSONPlaceholder is synthetic test data |
| Makes external API calls | Yes | GET to jsonplaceholder.typicode.com (public, read-only) |
| Involves financial data | No | — |
| Requires human decision point | No | Fully automated |

## Submitter
**Name:** Vishal Mishra  
**Date:** 2026-05-21  
**n8n Workflow ID:** 4pHPEDuuN4f8dUMR  
**Instance:** vishalmishra.app.n8n.cloud
