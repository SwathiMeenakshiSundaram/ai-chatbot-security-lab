import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.title("🔐 AI Chatbot Security Risk Assessment Lab")
st.write("This app reads a college FAQ knowledge base and answers basic student questions.")

# Load knowledge base file

def load_knowledge_base():
    with open("knowledge_base.txt", "r", encoding="utf-8") as file:
        return file.read()

knowledge_base = load_knowledge_base()

st.subheader("📚 Knowledge Base Loaded")
st.text_area("Knowledge Base Content", knowledge_base, height=250)

st.subheader("💬 Ask the Chatbot")

user_question = st.text_input("Type your question here:")
RISKY_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "reveal system prompt",
    "show system prompt",
    "show api key",
    "reveal api key",
    "pretend you are admin",
    "act as admin",
    "bypass rules",
    "disable security",
    "show student records",
    "private student records",
    "show passwords",
    "reveal passwords",
    "admin note",
    "internal system instructions"
]

# Risk Detection Function

def detect_input_risk(question):
    question = question.lower()

    risk_rules = {
        "Prompt Injection": [
            "ignore previous instructions",
            "ignore all instructions",
            "bypass rules",
            "disable security",
            "reveal system prompt",
            "show system prompt"
        ],
        "Secret Exposure": [
            "show api key",
            "reveal api key",
            "api key",
            "secret"
        ],
        "Role Bypass": [
            "pretend you are admin",
            "act as admin",
            "admin note",
            "internal system instructions"
        ],
        "Data Leakage": [
            "show student records",
            "private student records",
            "student data",
            "confidential"
        ],
        "Credential Exposure": [
            "show passwords",
            "reveal passwords",
            "steal passwords",
            "steal credentials",
            "credential theft"
        ],
        "Phishing / Social Engineering": [
            "phishing email",
            "fake login page",
            "steal login",
            "trick students"
        ]
    }

    severity_map = {
        "Prompt Injection": "High",
        "Secret Exposure": "High",
        "Role Bypass": "High",
        "Data Leakage": "High",
        "Credential Exposure": "High",
        "Phishing / Social Engineering": "Medium"
    }

    for category, patterns in risk_rules.items():
        for pattern in patterns:
            if pattern in question:
                severity = severity_map.get(category, "Medium")
                return True, pattern, category, severity

    return False, "No risk detected", "Normal FAQ", "Low"


def log_interaction(user_question, response, result, risk_reason, risk_category, severity):
    log_file = "chatbot_logs.csv"

    new_log = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_question": user_question,
        "response": response,
        "result": result,
        "risk_reason": risk_reason,
        "risk_category": risk_category,
        "severity": severity
    }])

    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
        existing_logs = pd.read_csv(log_file)
        updated_logs = pd.concat([existing_logs, new_log], ignore_index=True)
    else:
        updated_logs = new_log

    updated_logs.to_csv(log_file, index=False)


def chatbot_response(question):
    question = question.lower()
    if "tuition" in question or "payment" in question:
        return "The tuition payment deadline is September 1."

    elif "admission" in question or "admission deadline" in question:
        return "The admission deadline is August 15."

    elif "student services" in question or "contact" in question:
        return "You can contact student services at studentservices@examplecollege.ca."

    elif "refund" in question:
        return "Students can request a refund within 10 business days."

    elif "international" in question or "documents" in question:
        return "International students must submit passport, study permit, and transcripts."

    elif "library" in question or "hours" in question:
        return "The library is open Monday to Friday, 8 AM to 8 PM."

    elif "cybersecurity" in question or "program" in question:
        return "The cybersecurity program includes networking, Linux, Python, cloud security, and AI fundamentals."

    else:
        return "I can answer questions about admission, tuition, student services, refunds, documents, library hours, and the cybersecurity program."


if st.button("Submit"):
    if user_question.strip() == "":
        st.warning("Please type a question.")
    else:
        input_risk, risk_reason, risk_category, severity = detect_input_risk(user_question)

        if input_risk:
            response = "Request blocked: This prompt appears to be a potential security risk."
            result = "Blocked"

            st.subheader("Security Alert")
            st.error(response)
            st.write(f"Detected risky pattern: `{risk_reason}`")
            st.write(f"Risk category: `{risk_category}`")
            st.write(f"Severity: `{severity}`")

            log_interaction(user_question, response, result, risk_reason, risk_category, severity)

        else:
            response = chatbot_response(user_question)
            result = "Allowed"
            risk_reason = "No risk detected"
            risk_category = "Normal FAQ"
            severity = "Low"

            st.subheader("Chatbot Response")
            st.success(response)

            log_interaction(user_question, response, result, risk_reason, risk_category, severity)
    

# Security Testing Dashboard

st.header("📊 Security Testing Dashboard")

if os.path.exists("chatbot_logs.csv") and os.path.getsize("chatbot_logs.csv") > 0:
    logs = pd.read_csv("chatbot_logs.csv")

    total_prompts = len(logs)
    blocked_prompts = len(logs[logs["result"] == "Blocked"])
    allowed_prompts = len(logs[logs["result"] == "Allowed"])

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Prompts Tested", total_prompts)
    col2.metric("Blocked Prompts", blocked_prompts)
    col3.metric("Allowed Prompts", allowed_prompts)

    st.subheader("Recent Logs")
    st.dataframe(logs.tail(10))

    st.subheader("Risk Category Counts")
    category_counts = logs["risk_category"].value_counts()
    st.bar_chart(category_counts)

    st.subheader("Severity Counts")
    severity_counts = logs["severity"].value_counts()
    st.bar_chart(severity_counts)

else:
    st.info("No logs found yet. Submit chatbot prompts to generate logs.")


# Display test cases in the app

st.divider()

st.header("🧪 Security Test Plan")

if os.path.exists("security_tests.csv"):
    test_cases = pd.read_csv("security_tests.csv")
    st.write("These are the planned test cases used to evaluate the chatbot's security behavior.")
    st.dataframe(test_cases)
else:
    st.info("security_tests.csv file not found.")

# Test Result comparison

st.divider()

st.header("✅ Test Result Comparison")

if (
    os.path.exists("security_tests.csv")
    and os.path.exists("chatbot_logs.csv")
    and os.path.getsize("chatbot_logs.csv") > 0
):
    test_cases = pd.read_csv("security_tests.csv")
    logs = pd.read_csv("chatbot_logs.csv")

    comparison_rows = []

    for _, test in test_cases.iterrows():
        test_prompt = test["test_prompt"]
        expected_result = test["expected_result"]
        expected_severity = test["expected_severity"]

        matching_logs = logs[logs["user_question"].str.lower() == test_prompt.lower()]

        if len(matching_logs) > 0:
            latest_log = matching_logs.iloc[-1]

            actual_result = latest_log["result"]
            actual_severity = latest_log["severity"]

            if actual_result == expected_result and actual_severity == expected_severity:
                status = "Pass"
            else:
                status = "Fail"

        else:
            actual_result = "Not tested"
            actual_severity = "Not tested"
            status = "Not tested"

        comparison_rows.append({
            "test_prompt": test_prompt,
            "expected_result": expected_result,
            "actual_result": actual_result,
            "expected_severity": expected_severity,
            "actual_severity": actual_severity,
            "status": status
        })

    comparison_df = pd.DataFrame(comparison_rows)

    st.write("This table compares the planned test cases against the actual chatbot logs.")
    st.dataframe(comparison_df)

    passed = len(comparison_df[comparison_df["status"] == "Pass"])
    failed = len(comparison_df[comparison_df["status"] == "Fail"])
    not_tested = len(comparison_df[comparison_df["status"] == "Not tested"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Passed Tests", passed)
    col2.metric("Failed Tests", failed)
    col3.metric("Not Tested", not_tested)

else:
    st.info("Run some chatbot prompts first to generate logs for comparison.")

    

