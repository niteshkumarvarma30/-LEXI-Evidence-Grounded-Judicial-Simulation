import streamlit as st
import requests

# ======================================================
# CONFIG
# ======================================================
BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="LEXI — Evidence-Grounded Judicial Simulation",
    layout="wide"
)

st.title("⚖️ LEXI — Evidence-Grounded Judicial Simulation")
st.caption("Incident-based • Adversarial • Human-in-the-loop verdicts")
st.markdown("---")

# ======================================================
# SESSION STATE
# ======================================================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "case_id" not in st.session_state:
    st.session_state.case_id = None

if "screening_result" not in st.session_state:
    st.session_state.screening_result = None

# ======================================================
# HOME
# ======================================================
if st.session_state.page == "home":

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🆕 Create New Case", use_container_width=True):
            st.session_state.page = "create"
            st.rerun()

    with col2:
        case_id_input = st.number_input(
            "📂 Existing Case ID", min_value=1, step=1
        )
        if st.button("Load Existing Case", use_container_width=True):
            with st.spinner("Loading case..."):
                res = requests.get(
                    f"{BACKEND_URL}/case/{int(case_id_input)}/history"
                )

            if res.status_code == 200:
                st.session_state.case_id = int(case_id_input)
                st.session_state.page = "active"
                st.success("Case loaded successfully")
                st.rerun()
            else:
                st.error("Failed to load case")

# ======================================================
# CREATE CASE
# ======================================================
elif st.session_state.page == "create":

    st.subheader("🆕 Create New Case")

    title = st.text_input("Incident Title")
    incident = st.text_area(
        "Incident Description (facts only)", height=160
    )

    # ---------------- Screening ----------------
    if st.button("Check Legal Validity"):
        if not incident.strip():
            st.warning("Please describe the incident.")
        else:
            with st.spinner("Performing legal screening..."):
                res = requests.post(
                    f"{BACKEND_URL}/screen-incident",
                    params={"incident": incident}
                )

            if res.status_code == 200:
                st.session_state.screening_result = res.json()
                st.success("Screening completed")
            else:
                st.error(res.text)

    # ---------------- Screening Result ----------------
    if st.session_state.screening_result:
        result = st.session_state.screening_result
        constitutional = result["constitutional"]
        maintainability = result["maintainability"]

        st.markdown("## ⚖️ Screening Result")

        # ---- Constitutional assessment ----
        st.markdown("### 🏛 Constitutional Assessment")
        st.write(constitutional["analysis"])

        if constitutional["constitutional_context"]:
            st.markdown("**Relevant Constitutional Context:**")
            for art in constitutional["constitutional_context"]:
                st.markdown(f"- {art}")
        else:
            st.info("No constitutional context required")

        # ---- Maintainability ----
        st.markdown("### ⚖️ Legal Maintainability")
        st.write(maintainability)

        if maintainability == "NOT MAINTAINABLE":
            st.error(
                "❌ This incident does not describe a legally "
                "maintainable criminal or civil dispute."
            )

        else:
            st.info(
                "ℹ️ This incident may proceed under ordinary "
                "criminal or civil law."
            )

            if st.button("📂 Register Case"):
                with st.spinner("Registering case..."):
                    res = requests.post(
                        f"{BACKEND_URL}/incident",
                        json={
                            "title": title,
                            "description": incident
                        }
                    )

                if res.status_code == 200:
                    data = res.json()
                    st.session_state.case_id = data["id"]
                    st.session_state.page = "active"
                    st.success(
                        f"Case registered successfully (ID: {data['id']})"
                    )
                    st.rerun()
                else:
                    st.error(res.text)

# ======================================================
# ACTIVE CASE
# ======================================================
elif st.session_state.page == "active":

    case_id = st.session_state.case_id
    st.subheader(f"📂 Active Case — ID {case_id}")

    with st.spinner("Loading case history..."):
        res = requests.get(f"{BACKEND_URL}/case/{case_id}/history")

    if res.status_code != 200:
        st.error("Failed to load case history")
        st.stop()

    history = res.json()

    # ---------------- Incident ----------------
    st.markdown("### 🗂 Incident")
    if history["incident"]:
        inc = history["incident"][0]
        st.markdown(f"**Title:** {inc.get('title','')}")
        st.markdown(f"**Description:** {inc.get('description','')}")
    else:
        st.warning("Incident not found")

    # ---------------- Claims ----------------
    st.markdown("### 📝 Claims")
    if history["claims"]:
        for c in history["claims"]:
            st.markdown(f"**Side {c['side']}**: {c['text']}")
    else:
        st.info("No claims yet")

    # ---------------- Evidence ----------------
    st.markdown("### 📎 Evidence")
    if history["evidence"]:
        for e in history["evidence"]:
            st.markdown(
                f"**Side {e['side']}** | {e.get('file_name','file')}"
            )
    else:
        st.info("No evidence submitted")

    st.markdown("---")

    # ======================================================
    # PARTY SUBMISSIONS
    # ======================================================
    st.markdown("## ⚖️ Party Submissions")

    colA, colB = st.columns(2)

    # Party A
    with colA:
        st.subheader("🧑‍⚖️ Party A (Petitioner)")
        claim_a = st.text_area("Claim / Argument", key="claim_a")

        if st.button("Submit A Claim"):
            with st.spinner("Submitting claim..."):
                res = requests.post(
                    f"{BACKEND_URL}/claim",
                    json={
                        "case_id": case_id,
                        "side": "A",
                        "text": claim_a
                    }
                )
            if res.status_code == 200:
                st.success("Claim submitted successfully")
                st.rerun()
            else:
                st.error("Failed to submit claim")

        file_a = st.file_uploader("Upload Evidence", key="file_a")
        if st.button("Upload A Evidence") and file_a:
            with st.spinner("Uploading evidence..."):
                res = requests.post(
                    f"{BACKEND_URL}/evidence/upload",
                    data={
                        "case_id": str(case_id),
                        "side": "A"
                    },
                    files={
                        "file": (
                            file_a.name,
                            file_a,
                            file_a.type
                        )
                    }
                )
            if res.status_code == 200:
                st.success("Evidence uploaded successfully")
                st.rerun()
            else:
                st.error("Evidence upload failed")

    # Party B
    with colB:
        st.subheader("🧑‍⚖️ Party B (Respondent)")
        claim_b = st.text_area(
            "Counter-Claim / Defense", key="claim_b"
        )

        if st.button("Submit B Claim"):
            with st.spinner("Submitting claim..."):
                res = requests.post(
                    f"{BACKEND_URL}/claim",
                    json={
                        "case_id": case_id,
                        "side": "B",
                        "text": claim_b
                    }
                )
            if res.status_code == 200:
                st.success("Claim submitted successfully")
                st.rerun()
            else:
                st.error("Failed to submit claim")

        file_b = st.file_uploader("Upload Evidence", key="file_b")
        if st.button("Upload B Evidence") and file_b:
            with st.spinner("Uploading evidence..."):
                res = requests.post(
                    f"{BACKEND_URL}/evidence/upload",
                    data={
                        "case_id": str(case_id),
                        "side": "B"
                    },
                    files={
                        "file": (
                            file_b.name,
                            file_b,
                            file_b.type
                        )
                    }
                )
            if res.status_code == 200:
                st.success("Evidence uploaded successfully")
                st.rerun()
            else:
                st.error("Evidence upload failed")

    st.markdown("---")

    # ======================================================
    # VERDICT
    # ======================================================
    st.markdown("## 🧾 Verdict Evaluation")

    case_type = st.selectbox("Case Type", ["criminal", "civil"])
    degree = st.slider(
        "Degree of Proof Against Respondent", 0.0, 1.0, 0.5
    )

    if st.button("Evaluate Verdict"):
        with st.spinner("Evaluating verdict..."):
            res = requests.get(
                f"{BACKEND_URL}/verdict-with-reason",
                params={
                    "case_id": case_id,
                    "score": degree,
                    "case_type": case_type
                }
            )

        if res.status_code == 200:
            verdict = res.json()

            if verdict["verdict"] == "GUILTY":
                st.error("🟥 VERDICT: GUILTY")
            else:
                st.success("🟩 VERDICT: NOT GUILTY")

            st.markdown("### 🧠 Judicial Reasoning")
            st.write(verdict["explanation"])
        else:
            st.error("Verdict evaluation failed")

    st.markdown("---")
    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.session_state.case_id = None
        st.session_state.screening_result = None
        st.rerun()

# ======================================================
# FOOTER
# ======================================================
st.caption(
    "LEXI is an educational judicial simulation system. "
    "It does not provide legal advice or real judgments."
)
