# Healthcare AI Incident Triage & Runbook Generator

This is a Streamlit operations tool created for a Hippocratic AI Operations team.

## What It Does

The tool takes an incident description and generates:

- Incident classification
- Severity level
- Escalation path
- Step-by-step operations runbook
- Customer communication draft
- Internal incident summary
- 5 Whys RCA draft
- Preventive actions

## Why This Project Is Different

This is not a monitoring dashboard. It is an operations workflow tool.

It shows how an Operations Analyst can think through:

1. What happened?
2. How severe is it?
3. Who should be involved?
4. What should we check first?
5. What should we tell the customer?
6. How do we prevent recurrence?

## Example Use Case

Input:

A patient mentioned chest pain during a post-discharge AI call, but the AI agent did not escalate the conversation to a human nurse.

Output:

- Incident Type: Patient Safety / Escalation Failure
- Severity: P1 - Critical
- Primary Team: Clinical Safety Team
- Secondary Team: AI Engineering
- Runbook: Pull transcripts, review escalation logs, validate safety rules, engage Clinical Safety, monitor new calls
- RCA: Escalation rule did not trigger because phrase coverage was incomplete
- Preventive Action: Add safety keyword monitoring and improve clinical phrase regression tests

## Tech Stack

- Python
- Streamlit
- Rule-based classification logic

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```


Incident Input
     ↓
Classification Engine
     ↓
Severity Assignment
     ↓
Escalation Routing
     ↓
Runbook + Customer Update + RCA

This tool simulates that workflow. It takes an incident description, detects whether the issue is related to patient safety, integration failure, latency, call delivery, transcript ingestion, or AI response quality. Then it generates a severity level, escalation team, operational runbook, customer update, 5 Whys RCA, and preventive actions.

The main value is that it helps reduce confusion during incidents and gives operations teams a structured process to move from detection to resolution.
