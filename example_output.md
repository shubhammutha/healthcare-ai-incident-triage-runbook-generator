# Example Inputs and Outputs

This file includes sample test cases for the **Healthcare AI Incident Triage & Runbook Generator**.

The goal is to demonstrate how the tool helps an operations team classify healthcare AI incidents, assign severity, route issues to the right team, generate a runbook, draft customer communication, and create RCA notes.

---

## Example 1: Patient Safety / Escalation Failure

### Sample Input

**Customer / Health System:** Cedar Valley Hospital
**AI Agent / Workflow:** Post-Discharge Follow-up Agent
**Incident Time Window:** 9 AM - 10 AM
**Current Status:** Under Investigation
**Estimated Patients Affected:** 12
**Estimated Customers Affected:** 1

**Checkboxes Selected:**

* Production workflow impacted
* Human escalation may have failed

**Issue Description:**

```text
Patient mentioned chest pain during a post-discharge call, but the AI agent did not escalate the conversation to a human nurse. Multiple similar calls were reported between 9 AM and 10 AM.
```

### Expected Output

**Incident Type:** Patient Safety / Escalation Failure
**Severity:** P1 - Critical
**Primary Team:** Clinical Safety Team
**Secondary Team:** AI Engineering
**Support Team:** Customer Operations

### Why This Is P1

This is critical because the incident involves a possible patient safety risk. A symptom like chest pain should trigger human escalation.

### Generated Runbook

1. Confirm affected customer, agent, and time window.
2. Pull call transcripts and conversation IDs.
3. Search transcripts for safety keywords such as chest pain, breathing issue, severe pain, or medication reaction.
4. Confirm whether human escalation was triggered.
5. Review validation layer logs and escalation decision logs.
6. Engage Clinical Safety and AI Engineering.
7. Pause or restrict the affected workflow if missed escalation is confirmed.
8. Monitor new calls for similar missed escalation patterns.

---

## Example 2: FHIR / EHR Integration Failure

### Sample Input

**Customer / Health System:** Northstar Health
**AI Agent / Workflow:** Appointment Scheduling Agent
**Incident Time Window:** 2 PM - 3 PM
**Current Status:** Active
**Estimated Patients Affected:** 35
**Estimated Customers Affected:** 1

**Checkboxes Selected:**

* Production workflow impacted
* FHIR/EHR or external integration impacted

**Issue Description:**

```text
The appointment scheduling agent completed patient calls successfully, but appointment confirmations failed to write back to the EHR through the FHIR API. The retry queue is growing and several appointments are missing confirmation records.
```

### Expected Output

**Incident Type:** FHIR / EHR Integration Failure
**Severity:** P2 - High
**Primary Team:** Integration Engineering
**Secondary Team:** SRE / Infrastructure
**Support Team:** Customer Operations

### Why This Is P2

This is high priority because patient calls completed successfully, but appointment confirmations did not sync back to the healthcare system.

### Generated Runbook

1. Confirm affected customer, agent, and time window.
2. Check FHIR/EHR API status and error responses.
3. Review failed payloads, response codes, and retry queue depth.
4. Validate whether appointment writeback failed.
5. Confirm whether the issue is customer-specific or platform-wide.
6. Escalate sample request IDs to Integration Engineering.
7. Retry failed events only after confirming data safety.
8. Notify Customer Operations if workflows are delayed.

---

## Example 3: Latency / Performance Degradation

### Sample Input

**Customer / Health System:** MetroCare Network
**AI Agent / Workflow:** Care Navigation Agent
**Incident Time Window:** 11 AM - 12 PM
**Current Status:** Monitoring
**Estimated Patients Affected:** 28
**Estimated Customers Affected:** 1

**Checkboxes Selected:**

* Production workflow impacted

**Issue Description:**

```text
The care navigation agent is responding slowly. Patients are experiencing long pauses during calls, and several requests are timing out before the agent completes the workflow.
```

### Expected Output

**Incident Type:** Latency / Performance Degradation
**Severity:** P2 - High
**Primary Team:** SRE / Infrastructure
**Secondary Team:** AI Platform Engineering
**Support Team:** Customer Operations

### Why This Is P2

This is high priority because a live production workflow is affected and patients are experiencing delays, but there is no confirmed patient safety escalation failure.

### Generated Runbook

1. Confirm affected customer, agent, and time window.
2. Check latency by dependency: AI runtime, telephony, EHR API, and database.
3. Compare current latency against normal baseline.
4. Review recent deployments, config changes, and traffic spikes.
5. Check infrastructure saturation, queue depth, and timeout errors.
6. Escalate to SRE if latency breaches SLA threshold.
7. Monitor recovery for one full workflow cycle.

---

## Example 4: Transcript / Data Ingestion Issue

### Sample Input

**Customer / Health System:** Riverbend Medical
**AI Agent / Workflow:** Medication Adherence Agent
**Incident Time Window:** 8 AM - 9 AM
**Current Status:** Under Investigation
**Estimated Patients Affected:** 5
**Estimated Customers Affected:** 1

**Checkboxes Selected:**

* None

**Issue Description:**

```text
Completed call transcripts are missing from the operations review queue. Conversation logs are delayed after completed calls, making it difficult for the operations team to review patient interactions.
```

### Expected Output

**Incident Type:** Transcript / Data Ingestion Issue
**Severity:** P3 - Medium
**Primary Team:** Data Platform Team
**Secondary Team:** AI Engineering
**Support Team:** Customer Operations

### Why This Is P3

This is medium priority because the issue appears limited and does not directly block patient calls or indicate patient safety impact.

### Generated Runbook

1. Confirm affected customer, agent, and time window.
2. Check transcript ingestion queue and worker status.
3. Compare completed calls against available transcripts.
4. Identify missing conversation IDs and affected time range.
5. Restart ingestion process if safe and approved.
6. Backfill missing transcripts after recovery.
7. Add queue-depth or delayed-ingestion alerting.

---

## Example 5: Agent Response Quality Issue

### Sample Input

**Customer / Health System:** Summit Health Group
**AI Agent / Workflow:** Medication Adherence Agent
**Incident Time Window:** 4 PM - 5 PM
**Current Status:** Under Investigation
**Estimated Patients Affected:** 6
**Estimated Customers Affected:** 1

**Checkboxes Selected:**

* Production workflow impacted

**Issue Description:**

```text
The medication adherence agent gave an incorrect response and confused the patient about medication timing. The patient asked whether they should skip a dose, and the response was unclear.
```

### Expected Output

**Incident Type:** Agent Response Quality Issue
**Severity:** P2 - High
**Primary Team:** AI Quality / Evaluation Team
**Secondary Team:** Clinical Safety Team
**Support Team:** Product Operations

### Why This Is P2

This is high priority because the issue happened in production and involved medication-related confusion. Even if it is not immediately classified as a missed escalation, it should be reviewed carefully.

### Generated Runbook

1. Confirm affected customer, agent, and time window.
2. Collect example conversations showing incorrect or confusing responses.
3. Review prompt, response, validation output, and model decision logs.
4. Check whether the issue is reproducible.
5. Evaluate whether the response could create patient safety or compliance risk.
6. Escalate to AI Quality / Evaluation team with sample cases.
7. Add failing examples to regression tests.
8. Monitor future responses for recurrence.

---

## Summary Table

| Example                                          | Incident Type                       | Severity      | Primary Team                 |
| ------------------------------------------------ | ----------------------------------- | ------------- | ---------------------------- |
| Patient mentions chest pain and escalation fails | Patient Safety / Escalation Failure | P1 - Critical | Clinical Safety Team         |
| Appointment confirmation fails in FHIR/EHR       | FHIR / EHR Integration Failure      | P2 - High     | Integration Engineering      |
| Agent response is slow or timing out             | Latency / Performance Degradation   | P2 - High     | SRE / Infrastructure         |
| Transcripts are missing or delayed               | Transcript / Data Ingestion Issue   | P3 - Medium   | Data Platform Team           |
| Agent gives confusing medication response        | Agent Response Quality Issue        | P2 - High     | AI Quality / Evaluation Team |

**The purpose of this project is to make incident response more structured, consistent, and safe for healthcare AI operations.**
