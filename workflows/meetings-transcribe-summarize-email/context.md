# context.md — Meetings - Transcribe, Summarize & Email Action Items

## Purpose
Automates the end-to-end post-meeting workflow: transcribing a recording, extracting a structured summary and action items using Claude AI, and distributing results to attendees — eliminating ~15 minutes of manual note-taking and follow-up per meeting.

## What It Does
1. Receives a `POST` webhook call with the recording URL, meeting title, date, and attendee email list
2. Downloads the audio file from the provided URL as binary data
3. Sends the audio to OpenAI Whisper (`audio/transcribe`) to produce a full text transcript
4. Passes the transcript to Claude (`claude-opus-4-5`) with a structured prompt requesting JSON output: summary bullets, action items (with assignees + due dates), and key decisions
5. Parses the Claude JSON response and builds a formatted HTML email body
6. Sends the email to all attendees via Gmail with the meeting title and date in the subject line

## Tools & Connectors Used
| Tool / Service | How It's Used |
|---|---|
| n8n Webhook (POST) | Entry point — receives recording URL + attendee metadata |
| HTTP Request node | Downloads the audio file as binary from the recording URL |
| OpenAI (Whisper) | Transcribes the audio file to plain text |
| Anthropic Claude (`claude-opus-4-5`) | Analyzes transcript, returns structured JSON summary + action items |
| n8n Code node | Parses AI response, builds HTML email body |
| Gmail | Sends formatted HTML summary email to all attendees |

## Credentials Required
| Credential Name | Service | Notes |
|---|---|---|
| OpenAI | OpenAI API | Requires access to Whisper (`audio/transcribe`) |
| Anthropic | Anthropic API | Requires access to Claude (`claude-opus-4-5`) |
| Gmail OAuth2 | Gmail | Personal OAuth2 — scoped to sender's account |

> ⚠️ Never include credential values — names only.

## KPI Baseline
| Metric | Value |
|---|---|
| Manual time per run (before) | 15 minutes |
| Estimated runs per month | ~40 (10/week) |
| Projected hours saved/month | ~10 hours |

## Risk Self-Assessment
| Risk Type | Present? | Notes |
|---|---|---|
| Handles PII / personal data | Yes | Meeting transcripts may contain personal conversations |
| Makes external API calls | Yes | OpenAI (Whisper), Anthropic (Claude), Gmail |
| Involves financial data | No | — |
| Requires human decision point | No | Fully automated; attendees receive email automatically |

## Submitter
**Name:** Shivam  
**Date:** 2026-06-09  
**n8n Workflow ID:** 9uK3uoOKuswHL3e1  
**Instance:** shivamheaptrace.app.n8n.cloud
