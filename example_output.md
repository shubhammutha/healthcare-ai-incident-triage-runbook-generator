# Example Generated Output

## Input

Customer: Cedar Valley Hospital
Agent: Post-Discharge Follow-up Agent
Issue: Patient mentioned chest pain during a post-discharge call, but the AI agent did not escalate the conversation to a human nurse.
Patients Affected: 12
Production Impact: Yes
Human Escalation Failed: Yes

## Output

Incident Type: Patient Safety / Escalation Failure
Severity: P1 - Critical
Primary Team: Clinical Safety Team
Secondary Team: AI Engineering
Support Team: Customer Operations

## Runbook

1. Confirm affected customer: Cedar Valley Hospital.
2. Confirm affected AI agent/workflow: Post-Discharge Follow-up Agent.
3. Confirm incident time window: 9 AM - 10 AM.
4. Pull call transcripts and conversation IDs.
5. Search transcripts for high-risk symptoms.
6. Confirm whether human escalation was triggered.
7. Review validation layer logs and escalation decision logs.
8. Engage Clinical Safety for review.
9. Pause or restrict the affected workflow if missed escalation is confirmed.
10. Monitor new calls for similar missed escalation patterns.

## Customer Update

Hi Cedar Valley Hospital Team,

We are actively investigating an issue involving the Post-Discharge Follow-up Agent during 9 AM - 10 AM.

Current classification: Patient Safety / Escalation Failure
Current priority: P1 - Critical
Current status: Under Investigation

Our team is reviewing the affected workflow, related system logs, and customer impact. If patient safety, escalation, or integration impact is confirmed, we will route this to the appropriate specialized team and continue monitoring recovery.

Best,
Operations Team
