
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Healthcare AI Incident Triage & Runbook Generator",
    page_icon="🚨",
    layout="wide"
)

# -----------------------------
# Rule libraries
# -----------------------------

SAFETY_KEYWORDS = [
    "chest pain", "shortness of breath", "breathing", "can't breathe", "cannot breathe",
    "fainting", "severe pain", "suicidal", "self harm", "overdose", "allergic reaction",
    "stroke", "heart attack", "bleeding", "seizure", "medication reaction"
]

INTEGRATION_KEYWORDS = [
    "fhir", "ehr", "api", "webhook", "integration", "sync", "payload",
    "appointment writeback", "failed write", "retry queue", "hl7"
]

LATENCY_KEYWORDS = [
    "slow", "latency", "timeout", "delayed", "lag", "performance", "not responding"
]

CALL_DELIVERY_KEYWORDS = [
    "call failed", "phone", "voice", "twilio", "delivery", "did not call",
    "call dropped", "no answer", "outbound call"
]

TRANSCRIPT_KEYWORDS = [
    "transcript", "ingestion", "conversation log", "missing logs", "recording"
]

QUALITY_KEYWORDS = [
    "wrong answer", "incorrect response", "hallucination", "confusing", "bad response",
    "incorrect information", "unsafe response"
]


def contains_any(text, keywords):
    text = text.lower()
    return [kw for kw in keywords if kw in text]


def classify_incident(description, integration_impacted, escalation_failed):
    safety_hits = contains_any(description, SAFETY_KEYWORDS)
    integration_hits = contains_any(description, INTEGRATION_KEYWORDS)
    latency_hits = contains_any(description, LATENCY_KEYWORDS)
    call_hits = contains_any(description, CALL_DELIVERY_KEYWORDS)
    transcript_hits = contains_any(description, TRANSCRIPT_KEYWORDS)
    quality_hits = contains_any(description, QUALITY_KEYWORDS)

    if safety_hits or escalation_failed:
        return "Patient Safety / Escalation Failure", safety_hits
    if integration_impacted or integration_hits:
        return "FHIR / EHR Integration Failure", integration_hits
    if latency_hits:
        return "Latency / Performance Degradation", latency_hits
    if call_hits:
        return "Call Delivery Failure", call_hits
    if transcript_hits:
        return "Transcript / Data Ingestion Issue", transcript_hits
    if quality_hits:
        return "Agent Response Quality Issue", quality_hits

    return "General Healthcare AI Operations Issue", []


def assign_severity(incident_type, patients_affected, customers_affected, escalation_failed, safety_hits, production_impact):
    reasons = []

    # P1: true critical cases
    if escalation_failed and safety_hits:
        reasons.append("Patient safety keyword detected and human escalation may have failed.")
        return "P1 - Critical", reasons

    if "Patient Safety" in incident_type and patients_affected >= 1:
        reasons.append("Patient safety risk detected.")
        return "P1 - Critical", reasons

    if customers_affected >= 2:
        reasons.append("Multiple customers are affected.")
        return "P1 - Critical", reasons

    if patients_affected >= 100:
        reasons.append("Large patient impact detected.")
        return "P1 - Critical", reasons

    # P2: high priority but not necessarily critical
    if "Integration" in incident_type:
        reasons.append("Healthcare integration issue may affect workflow completion.")
        return "P2 - High", reasons

    if production_impact and patients_affected >= 10:
        reasons.append("Production workflow impact with moderate patient volume.")
        return "P2 - High", reasons

    if patients_affected >= 25:
        reasons.append("Moderate patient impact detected.")
        return "P2 - High", reasons

    if production_impact:
        reasons.append("Production impact reported, but limited patient/customer scope.")
        return "P2 - High", reasons

    # P3: isolated issue
    reasons.append("Limited or isolated operational impact.")
    return "P3 - Medium", reasons


def route_team(incident_type):
    if "Patient Safety" in incident_type:
        return {
            "primary": "Clinical Safety Team",
            "secondary": "AI Engineering",
            "support": "Customer Operations",
            "reason": "The incident may involve unsafe AI behavior or missed human escalation."
        }
    if "Integration" in incident_type:
        return {
            "primary": "Integration Engineering",
            "secondary": "SRE / Infrastructure",
            "support": "Customer Operations",
            "reason": "The issue may involve FHIR/EHR data exchange, API failures, or retry queues."
        }
    if "Latency" in incident_type:
        return {
            "primary": "SRE / Infrastructure",
            "secondary": "AI Platform Engineering",
            "support": "Customer Operations",
            "reason": "The issue appears related to platform performance or dependency latency."
        }
    if "Call Delivery" in incident_type:
        return {
            "primary": "Telephony / Voice Platform Team",
            "secondary": "SRE / Infrastructure",
            "support": "Customer Operations",
            "reason": "The issue may affect outbound calls, call completion, or voice delivery."
        }
    if "Transcript" in incident_type:
        return {
            "primary": "Data Platform Team",
            "secondary": "AI Engineering",
            "support": "Customer Operations",
            "reason": "The issue may affect transcript ingestion, auditability, or operational analytics."
        }
    if "Quality" in incident_type:
        return {
            "primary": "AI Quality / Evaluation Team",
            "secondary": "Clinical Safety Team",
            "support": "Product Operations",
            "reason": "The issue may involve model response quality, hallucination risk, or prompt behavior."
        }

    return {
        "primary": "Operations Triage",
        "secondary": "Product Operations",
        "support": "Customer Operations",
        "reason": "The issue needs initial triage before specialized routing."
    }


def generate_runbook(incident_type, customer, agent, time_window, safety_hits):
    common = [
        f"Confirm affected customer: {customer}.",
        f"Confirm affected AI agent/workflow: {agent}.",
        f"Confirm incident time window: {time_window}.",
        "Validate number of patients, calls, or workflows affected.",
        "Check whether the issue is still active or already recovering.",
        "Document all timestamps, owners, and actions in the incident record."
    ]

    if "Patient Safety" in incident_type:
        return common + [
            "Pull call transcripts and conversation IDs for the affected time window.",
            "Search transcripts for high-risk symptoms or safety keywords.",
            "Confirm whether human escalation was triggered for each high-risk conversation.",
            "Review validation layer logs and escalation decision logs.",
            "Engage Clinical Safety for review of any missed escalation.",
            "If missed escalation is confirmed, pause or restrict the affected workflow.",
            "Create a list of affected patients/conversations for follow-up review.",
            "Add missing symptom phrase variations to safety test coverage.",
            "Monitor new calls for similar missed escalation patterns."
        ]

    if "Integration" in incident_type:
        return common + [
            "Check FHIR/EHR API status and recent error responses.",
            "Review failed payloads, response codes, and retry queue depth.",
            "Validate whether data writeback, appointment confirmation, or patient sync failed.",
            "Confirm whether failures are customer-specific or platform-wide.",
            "Escalate sample request IDs and payload examples to Integration Engineering.",
            "Retry failed events only after confirming idempotency and data safety.",
            "Notify Customer Operations if patient-facing workflows are delayed.",
            "Add monitoring for repeated API failures or retry queue growth."
        ]

    if "Latency" in incident_type:
        return common + [
            "Check latency by dependency: AI runtime, telephony, EHR API, and database.",
            "Compare current latency against normal baseline.",
            "Review recent deployments, config changes, and traffic spikes.",
            "Check infrastructure saturation, queue depth, and timeout errors.",
            "Escalate to SRE if latency breaches SLA threshold.",
            "Monitor recovery for at least one full workflow cycle.",
            "Document whether the issue was internal, external dependency, or traffic-related."
        ]

    if "Call Delivery" in incident_type:
        return common + [
            "Check outbound call delivery logs and provider status.",
            "Validate phone number formatting, opt-out status, and retry behavior.",
            "Review call failure codes and dropped-call patterns.",
            "Confirm whether failures are isolated to one customer, region, or carrier.",
            "Escalate to Telephony / Voice Platform team with sample call IDs.",
            "Communicate expected delay if patients were not reached.",
            "Verify successful call completion after remediation."
        ]

    if "Transcript" in incident_type:
        return common + [
            "Check transcript ingestion queue and processing worker status.",
            "Compare completed calls against available transcripts.",
            "Identify missing conversation IDs and affected time range.",
            "Restart ingestion process if safe and approved.",
            "Confirm whether audit, analytics, or safety review is affected.",
            "Backfill missing transcripts after the pipeline recovers.",
            "Add queue-depth or delayed-ingestion alerting."
        ]

    if "Quality" in incident_type:
        return common + [
            "Collect example conversations showing incorrect or confusing responses.",
            "Review prompt, response, validation output, and model decision logs.",
            "Check whether the issue is reproducible.",
            "Evaluate whether the response could create patient safety or compliance risk.",
            "Escalate to AI Quality / Evaluation team with sample cases.",
            "Add failing examples to regression tests.",
            "Monitor future responses for recurrence."
        ]

    return common + [
        "Gather logs, screenshots, affected records, and customer examples.",
        "Assign an incident owner and next update time.",
        "Route to the most relevant engineering or operations team after initial triage.",
        "Track recovery and document preventive action."
    ]


def generate_customer_update(customer, agent, severity, incident_type, time_window, status):
    return f"""Subject: Investigation Update — {agent} Issue

Hi {customer} Team,

We are actively investigating an issue involving the {agent} during {time_window}.

Current classification: {incident_type}
Current priority: {severity}
Current status: {status}

Our team is reviewing the affected workflow, related system logs, and customer impact. If patient safety, escalation, or integration impact is confirmed, we will route this to the appropriate specialized team and continue monitoring recovery.

We will provide another update once impact, root cause hypothesis, and remediation steps are confirmed.

Best,
Operations Team"""


def generate_internal_summary(customer, agent, incident_type, severity, patients_affected, customers_affected, status, time_window, escalation):
    return f"""Incident Summary

Customer: {customer}
Agent / Workflow: {agent}
Incident Type: {incident_type}
Severity: {severity}
Patients Affected: {patients_affected}
Customers Affected: {customers_affected}
Current Status: {status}
Time Window: {time_window}

Escalation:
Primary Team: {escalation['primary']}
Secondary Team: {escalation['secondary']}
Support Team: {escalation['support']}

Operational Assessment:
This incident should be handled according to severity and patient/customer impact. The operations owner should validate blast radius, collect evidence, route to the correct team, and track recovery until the workflow is stable."""


def generate_five_whys(incident_type):
    if "Patient Safety" in incident_type:
        return [
            ("Why was the patient not escalated?", "Because the escalation rule or validation layer did not trigger correctly."),
            ("Why did the rule not trigger?", "Because the symptom phrase may have been misclassified or not matched to a high-risk category."),
            ("Why was the symptom phrase missed?", "Because test coverage may not have included enough real-world patient language variations."),
            ("Why was coverage incomplete?", "Because clinical safety examples were not fully represented in regression tests."),
            ("Why was this not caught earlier?", "Because monitoring did not alert when safety keywords appeared without escalation.")
        ]
    if "Integration" in incident_type:
        return [
            ("Why did the workflow fail?", "Because the integration request to the healthcare system failed."),
            ("Why did the request fail?", "Because the API returned errors or rejected the payload."),
            ("Why was the payload rejected?", "Because required fields, mapping, authentication, or endpoint availability may have been incorrect."),
            ("Why was this not handled automatically?", "Because retry or fallback handling did not fully recover the failed transactions."),
            ("Why was this not caught earlier?", "Because monitoring did not alert quickly enough on failed writeback or retry queue growth.")
        ]
    if "Latency" in incident_type:
        return [
            ("Why was the workflow slow?", "Because one or more dependencies exceeded normal response time."),
            ("Why did the dependency slow down?", "Because of traffic, infrastructure saturation, external API delay, or recent change."),
            ("Why did the system not absorb the slowdown?", "Because timeout, queue, or scaling thresholds were not sufficient."),
            ("Why did users feel the impact?", "Because latency crossed the acceptable workflow threshold."),
            ("Why was this not prevented?", "Because proactive latency alerting or capacity planning needs improvement.")
        ]
    return [
        ("Why did the incident occur?", "The exact root cause is still under investigation."),
        ("Why was the impact visible?", "The affected workflow did not complete as expected."),
        ("Why did existing controls not prevent it?", "The current detection or fallback mechanism may be incomplete."),
        ("Why was escalation needed?", "The issue may affect customer operations or patient workflows."),
        ("Why should prevention be added?", "To reduce recurrence and improve operational reliability.")
    ]


def generate_preventive_actions(incident_type):
    if "Patient Safety" in incident_type:
        return [
            "Add alerting when safety keywords appear without human escalation.",
            "Expand clinical phrase coverage in safety validation tests.",
            "Require Clinical Safety review for escalation logic changes.",
            "Audit recent conversations for missed escalation candidates.",
            "Add a daily safety exception report for operations review."
        ]
    if "Integration" in incident_type:
        return [
            "Add monitoring for FHIR/EHR error rates and retry queue depth.",
            "Improve payload validation before sending requests.",
            "Create customer-specific integration health checks.",
            "Add idempotent retry handling for failed writebacks.",
            "Document known API failure modes in the integration runbook."
        ]
    if "Latency" in incident_type:
        return [
            "Add latency alerts by dependency and workflow.",
            "Review scaling thresholds and timeout configuration.",
            "Create a performance baseline for each agent workflow.",
            "Add rollback checks for recent deployments.",
            "Create a post-incident latency trend review."
        ]
    return [
        "Create a detection alert for this failure pattern.",
        "Add the incident scenario to regression testing.",
        "Update runbook documentation.",
        "Define a clear escalation owner.",
        "Review recurrence after 7 and 30 days."
    ]


# -----------------------------
# UI
# -----------------------------

st.title("Healthcare AI Incident Triage & Runbook Generator")
st.caption(
    "A practical operations tool that classifies healthcare AI incidents, assigns severity, routes escalation, "
    "generates runbooks, drafts RCA, and creates customer communication."
)

with st.expander("Sample incident to test", expanded=False):
    st.write(
        "Cedar Valley Hospital reports that the post-discharge AI agent did not escalate a patient who mentioned chest pain. "
        "12 patient conversations may have been affected between 9 AM and 10 AM."
    )

left, right = st.columns([1, 1])

with left:
    st.subheader("Incident Input")

    customer = st.text_input("Customer / Health System", "Cedar Valley Hospital")
    agent = st.selectbox(
        "AI Agent / Workflow",
        [
            "Post-Discharge Follow-up Agent",
            "Appointment Scheduling Agent",
            "Medication Adherence Agent",
            "Care Navigation Agent",
            "Chronic Care Outreach Agent",
            "Other"
        ]
    )
    time_window = st.text_input("Incident Time Window", "9 AM - 10 AM")
    status = st.selectbox("Current Status", ["Under Investigation", "Active", "Monitoring", "Resolved"])

    patients_affected = st.number_input("Estimated Patients Affected", min_value=0, max_value=100000, value=12)
    customers_affected = st.number_input("Estimated Customers Affected", min_value=1, max_value=1000, value=1)

    production_impact = st.checkbox("Production workflow impacted", value=True)
    integration_impacted = st.checkbox("FHIR/EHR or external integration impacted", value=False)
    escalation_failed = st.checkbox("Human escalation may have failed", value=False)

with right:
    st.subheader("Issue Description")
    description = st.text_area(
        "Describe what happened",
        height=260,
        value=(
            "Patient mentioned chest pain during a post-discharge call, but the AI agent did not escalate "
            "the conversation to a human nurse. Multiple similar calls were reported between 9 AM and 10 AM."
        )
    )

generate = st.button("Generate Triage Output", type="primary", use_container_width=True)

if generate:
    incident_type, keyword_hits = classify_incident(description, integration_impacted, escalation_failed)
    severity, severity_reasons = assign_severity(
        incident_type,
        patients_affected,
        customers_affected,
        escalation_failed,
        keyword_hits,
        production_impact
    )
    escalation = route_team(incident_type)
    runbook = generate_runbook(incident_type, customer, agent, time_window, keyword_hits)
    customer_update = generate_customer_update(customer, agent, severity, incident_type, time_window, status)
    internal_summary = generate_internal_summary(
        customer, agent, incident_type, severity,
        patients_affected, customers_affected, status, time_window, escalation
    )
    five_whys = generate_five_whys(incident_type)
    preventive_actions = generate_preventive_actions(incident_type)

    st.divider()
    st.header("Generated Triage Output")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Incident Type", incident_type)
    c2.metric("Severity", severity)
    c3.metric("Primary Team", escalation["primary"])
    c4.metric("Patients Affected", f"{patients_affected:,}")

    if "P1" in severity:
        st.error("Critical incident: patient safety or large customer impact may be involved. Start immediate escalation.")
    elif "P2" in severity:
        st.warning("High-priority incident: customer or workflow impact requires active triage.")
    else:
        st.info("Medium-priority incident: monitor and resolve through standard operations process.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Classification", "Runbook", "Customer Update", "RCA Draft", "Internal Summary"]
    )

    with tab1:
        st.subheader("Incident Classification")
        st.write(f"**Incident Type:** {incident_type}")
        st.write(f"**Severity:** {severity}")
        st.write("**Severity Reason:**")
        for reason in severity_reasons:
            st.write(f"- {reason}")

        st.write("**Matched Risk Keywords:**")
        if keyword_hits:
            for hit in keyword_hits:
                st.write(f"- {hit}")
        else:
            st.write("- No specific keyword match. Classified from operational context.")

        st.subheader("Escalation Path")
        st.write(f"**Primary Team:** {escalation['primary']}")
        st.write(f"**Secondary Team:** {escalation['secondary']}")
        st.write(f"**Support Team:** {escalation['support']}")
        st.write(f"**Why:** {escalation['reason']}")

    with tab2:
        st.subheader("Recommended Operations Runbook")
        for i, step in enumerate(runbook, start=1):
            st.write(f"{i}. {step}")

    with tab3:
        st.subheader("Customer Communication Draft")
        st.text_area("Draft message", customer_update, height=330)

    with tab4:
        st.subheader("5 Whys RCA Draft")
        for i, (why, answer) in enumerate(five_whys, start=1):
            st.write(f"**{i}. {why}**")
            st.write(answer)

        st.subheader("Preventive Actions")
        for action in preventive_actions:
            st.write(f"- {action}")

    with tab5:
        st.subheader("Internal Incident Summary")
        st.text_area("Internal summary", internal_summary, height=350)

    st.download_button(
        "Download Incident Summary",
        data=internal_summary + "\n\nCustomer Update:\n\n" + customer_update,
        file_name=f"incident_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )

else:
    st.info("Fill in the incident details and click **Generate Triage Output**.")
