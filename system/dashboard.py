# dashboard.py
import streamlit as st
import time

st.title("Autonomous Payment Ops Agent")

while True:
    st.metric("HDFC Failure Multiplier", SYSTEM_STATE["HDFC_failure_multiplier"])
    st.metric("Current Reward", last_reward)
    time.sleep(2)
