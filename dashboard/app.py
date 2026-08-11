import os

import requests
import streamlit as st


API = st.sidebar.text_input("API URL", os.getenv("API_URL", "http://localhost:8000"))
st.title("Security Analyst Feedback Dashboard")
st.caption("Review AI triage decisions and capture labels for the next training cycle.")

description = st.text_area("Alert", "Repeated failed SSH logins followed by a successful root login")
if st.button("Run triage"):
    response = requests.post(f"{API}/v1/triage", json={"alert_id": "dashboard-1", "title": "SIEM alert",
                                                              "description": description, "source": "dashboard"}, timeout=10)
    response.raise_for_status()
    st.session_state["prediction"] = response.json()

prediction = st.session_state.get("prediction")
if prediction:
    st.json(prediction)
    decision = st.radio("Analyst decision", ["approve", "reject", "correct"], horizontal=True)
    corrected = st.selectbox("Corrected severity", ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                             disabled=decision != "correct")
    note = st.text_area("Analyst note")
    if st.button("Submit feedback"):
        payload = {"alert_id": prediction["alert_id"], "model_version": prediction["model_version"],
                   "predicted_severity": prediction["severity"], "analyst_decision": decision,
                   "corrected_severity": corrected if decision == "correct" else None, "analyst_note": note}
        response = requests.post(f"{API}/v1/feedback", json=payload, timeout=10)
        response.raise_for_status()
        st.success("Feedback recorded")

if st.button("Refresh feedback metrics"):
    st.metric("Analyst agreement", requests.get(f"{API}/v1/feedback/metrics", timeout=10).json().get("analyst_agreement"))
