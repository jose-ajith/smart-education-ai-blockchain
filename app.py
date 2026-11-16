import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import json
import time
from sklearn.ensemble import RandomForestClassifier

st.title("Smart Education: AI & Blockchain System")
st.caption("Sahrdaya College of Advanced Studies | Simple Prototype")

@st.cache_resource
def get_ai_model():
    np.random.seed(42)
    n = 300
    df = pd.DataFrame({
        "attendance": np.random.uniform(50, 100, n),
        "study_hours": np.random.uniform(2, 15, n),
        "score": np.random.uniform(40, 100, n)
    })
    df["target"] = ((df["attendance"] * 0.4 + df["score"] * 0.6) < 65).astype(int)
    model = RandomForestClassifier(random_state=42)
    model.fit(df[["attendance", "study_hours", "score"]], df["target"])
    return model

ai_model = get_ai_model()

if "chain" not in st.session_state:
    genesis = {
        "index": 0,
        "timestamp": time.time(),
        "data": "Genesis Block",
        "previous_hash": "0"
    }
    genesis["hash"] = hashlib.sha256(json.dumps(genesis, sort_keys=True).encode()).hexdigest()
    st.session_state.chain = [genesis]

def add_to_blockchain(record_data):
    prev_block = st.session_state.chain[-1]
    new_block = {
        "index": len(st.session_state.chain),
        "timestamp": time.time(),
        "data": record_data,
        "previous_hash": prev_block["hash"]
    }
    block_string = json.dumps(new_block, sort_keys=True)
    new_block["hash"] = hashlib.sha256(block_string.encode()).hexdigest()
    st.session_state.chain.append(new_block)

st.subheader("Enter Student Details")
student_id = st.text_input("Student Register ID", "EKAZBCA041")
attendance = st.slider("Attendance (%)", 30.0, 100.0, 70.0)
study_hours = st.slider("Weekly Study Hours", 1.0, 20.0, 5.0)
score = st.slider("Assignment/Quiz Score", 20.0, 100.0, 55.0)

if st.button("Run AI Prediction & Save to Blockchain", type="primary"):
    input_df = pd.DataFrame([[attendance, study_hours, score]], columns=["attendance", "study_hours", "score"])
    prediction = ai_model.predict(input_df)[0]

    status = "Needs Additional Support" if prediction == 1 else "On Track"
    resource = "Remedial Tutorials & Practice Sheets" if prediction == 1 else "Advanced Learning Modules"

    student_record = {
        "student_id": student_id,
        "metrics": {"attendance": attendance, "study_hours": study_hours, "score": score},
        "ai_prediction": status,
        "recommendation": resource
    }
    add_to_blockchain(student_record)

    if prediction == 1:
        st.warning(f"AI Status: **{status}**")
    else:
        st.success(f"AI Status: **{status}**")

    st.write(f"**Recommended Resource:** {resource}")
    st.info("Record securely hashed and appended to the Blockchain ledger!")

st.subheader("Immutable Blockchain Ledger")
for block in st.session_state.chain:
    with st.expander(f"Block #{block['index']} — Hash: {block['hash'][:16]}..."):
        st.json(block)
