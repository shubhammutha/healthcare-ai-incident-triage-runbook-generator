# Sample Test Cases

## Test Case 1: Patient Safety Escalation Failure

Description:
Patient mentioned chest pain during a post-discharge call, but the AI agent did not escalate the conversation to a human nurse.

Expected Output:
- Incident Type: Patient Safety / Escalation Failure
- Severity: P1 - Critical
- Primary Team: Clinical Safety Team
- Secondary Team: AI Engineering

## Test Case 2: FHIR Integration Failure

Description:
Appointment scheduling agent completed calls successfully, but appointment confirmations failed to write back to the EHR through the FHIR API. Retry queue is growing.

Expected Output:
- Incident Type: FHIR / EHR Integration Failure
- Severity: P2 - High
- Primary Team: Integration Engineering
- Secondary Team: SRE / Infrastructure

## Test Case 3: Latency Degradation

Description:
Care navigation agent is responding slowly. Patients are experiencing long pauses and several requests are timing out.

Expected Output:
- Incident Type: Latency / Performance Degradation
- Severity: P2 - High if production impacted
- Primary Team: SRE / Infrastructure

## Test Case 4: Transcript Ingestion Issue

Description:
Call transcripts are missing from the operations review queue. Conversation logs are delayed after completed calls.

Expected Output:
- Incident Type: Transcript / Data Ingestion Issue
- Severity: P2 or P3 based on impact
- Primary Team: Data Platform Team

## Test Case 5: AI Response Quality Issue

Description:
The medication adherence agent gave an incorrect response and confused the patient about medication timing.

Expected Output:
- Incident Type: Agent Response Quality Issue
- Primary Team: AI Quality / Evaluation Team
- Secondary Team: Clinical Safety Team
