import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ── Page config ──────────────────────────────────────
st.set_page_config(
    page_title="Silent Hypoxia Risk Screener",
    page_icon="🫁",
    layout="centered"
)

st.title("🫁 Silent Hypoxia Early Detection System")
st.markdown("""
> **Silent hypoxia** is a condition where blood oxygen drops 
> dangerously low *without* causing breathlessness. 
> Patients feel fine while their organs are starved of oxygen.
""")
st.divider()

# ── Input Section ─────────────────────────────────────
st.header("📋 Enter Patient Vitals")

col1, col2, col3 = st.columns(3)

with col1:
    oxygen = st.number_input(
        "Oxygen Level (SpO2 %)",
        min_value=70.0, max_value=100.0,
        value=95.0, step=0.5)

with col2:
    pulse = st.number_input(
        "Pulse Rate (bpm)",
        min_value=40, max_value=200,
        value=80, step=1)

with col3:
    temperature = st.number_input(
        "Temperature (°F)",
        min_value=95.0, max_value=108.0,
        value=98.6, step=0.1)

st.divider()
st.header("🏥 Medical History")

col4, col5 = st.columns(2)

with col4:
    diabetes = st.checkbox("Diabetes")
    hypertension = st.checkbox("Hypertension")
    heart_disease = st.checkbox("Heart Disease")

with col5:
    asthma = st.checkbox("Asthma")
    obesity = st.checkbox("Obesity / Overweight")
    covid_contact = st.checkbox("Recent COVID-19 Exposure")

st.divider()
st.header("🤒 Current Symptoms")

col6, col7 = st.columns(2)

with col6:
    fatigue = st.checkbox("Unusual Fatigue")
    confusion = st.checkbox("Confusion / Brain Fog")

with col7:
    lips_blue = st.checkbox("Bluish Lips or Fingertips")

st.divider()

# ── Risk Calculation ──────────────────────────────────
def calculate_risk(oxygen, pulse, temperature,
                   diabetes, hypertension, heart_disease,
                   asthma, obesity, covid_contact,
                   fatigue, confusion, lips_blue):
    
    risk_score = 0
    reasons = []

    if oxygen < 90:
        risk_score += 45
        reasons.append("🔴 Critically low oxygen — Emergency")
    elif oxygen < 94:
        risk_score += 35
        reasons.append(f"🟠 Low oxygen — silent hypoxia zone ({oxygen}%)")
    elif oxygen < 96:
        risk_score += 15
        reasons.append(f"🟡 Borderline oxygen ({oxygen}%)")

    if pulse > 110:
        risk_score += 20
        reasons.append(f"🟠 Significantly elevated pulse ({pulse} bpm)")
    elif pulse > 100:
        risk_score += 12
        reasons.append(f"🟡 Mildly elevated pulse ({pulse} bpm)")

    if temperature > 101:
        risk_score += 15
        reasons.append(f"🟠 High fever ({temperature}°F)")
    elif temperature > 100.4:
        risk_score += 8
        reasons.append(f"🟡 Mild fever ({temperature}°F)")

    if diabetes:
        risk_score += 10
        reasons.append("Diabetes — increases hypoxia risk")
    if hypertension:
        risk_score += 8
        reasons.append("Hypertension — cardiovascular strain")
    if heart_disease:
        risk_score += 15
        reasons.append("Heart disease — high compounding risk")
    if asthma:
        risk_score += 8
        reasons.append("Asthma — respiratory vulnerability")
    if obesity:
        risk_score += 7
        reasons.append("Obesity — reduces lung capacity")
    if covid_contact:
        risk_score += 10
        reasons.append("Recent COVID exposure — elevated baseline risk")
    if lips_blue:
        risk_score += 30
        reasons.append("🔴 Bluish lips — sign of severe hypoxia")
    if confusion:
        risk_score += 20
        reasons.append("🟠 Confusion — brain oxygen deprivation sign")
    if fatigue:
        risk_score += 10
        reasons.append("Unusual fatigue — early warning sign")

    return risk_score, reasons

# ── Check Risk Button ─────────────────────────────────
if st.button("🔍 Check My Risk", type="primary", use_container_width=True):

    risk_score, reasons = calculate_risk(
        oxygen, pulse, temperature,
        diabetes, hypertension, heart_disease,
        asthma, obesity, covid_contact,
        fatigue, confusion, lips_blue
    )

    st.divider()
    st.header("📊 Your Result")

    # Risk gauge
    col_score, col_action = st.columns(2)

    with col_score:
        st.metric("Risk Score", f"{risk_score}/100")
        st.progress(min(risk_score/100, 1.0))

    with col_action:
        if risk_score >= 50:
            st.error("🚨 CRITICAL RISK")
            st.markdown("**Go to emergency room IMMEDIATELY**")
            action_color = "red"
        elif risk_score >= 35:
            st.warning("⚠️ HIGH RISK — Possible Silent Hypoxia")
            st.markdown("**Visit a doctor TODAY**")
            action_color = "orange"
        elif risk_score >= 20:
            st.warning("🟡 MODERATE RISK")
            st.markdown("**Monitor vitals every 2 hours**")
            action_color = "yellow"
        else:
            st.success("✅ LOW RISK — Currently Stable")
            st.markdown("**Daily monitoring sufficient**")
            action_color = "green"

    # Flags
    if reasons:
        st.divider()
        st.subheader("🚩 Risk Factors Identified")
        for r in reasons:
            st.markdown(f"- {r}")

    # How often to check
    st.divider()
    st.subheader("⏰ How Often Should You Check?")

    if risk_score >= 50:
        st.error("Go to hospital — do not self monitor")
    elif risk_score >= 35:
        st.warning("Every 30 minutes until you reach a doctor")
    elif risk_score >= 20:
        st.warning("Every 2 hours")
    else:
        st.success("Once daily is sufficient")

    # What to watch for between readings
    st.divider()
    st.subheader("👁️ Check Immediately If You Feel:")
    st.markdown("""
    - Suddenly very tired for no reason
    - Slightly confused or foggy
    - Lips or fingertips look bluish
    - Headache that came from nowhere
    
    *These are early physical signals that precede a crash.*
    """)

    # Oxygen gauge visual
    st.divider()
    st.subheader("📈 Your Oxygen Level vs Safe Range")

    fig, ax = plt.subplots(figsize=(8, 2))
    ax.barh(['SpO2'], [100], color='#f0f0f0', height=0.5)
    ax.barh(['SpO2'], [94], color='#ff4444', alpha=0.3, height=0.5)
    ax.barh(['SpO2'], [oxygen], color='steelblue', height=0.5)
    ax.axvline(x=94, color='red', linestyle='--',
               linewidth=2, label='Hypoxia threshold (94%)')
    ax.axvline(x=oxygen, color='steelblue',
               linewidth=3, label=f'Your reading ({oxygen}%)')
    ax.set_xlim(85, 100)
    ax.set_xlabel('Oxygen Saturation (%)')
    ax.legend(loc='lower right')
    ax.set_title('SpO2 Reading vs Clinical Threshold')
    st.pyplot(fig)
    plt.close()

st.divider()
st.caption("""
Built by Yoshitha | Silent Hypoxia Early Detection System
Dataset: 10,002 COVID-19 patient records | 
Key finding: 13.4% of at-risk patients missed by O2 alone
""")