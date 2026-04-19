"""
Behavioral Anomaly & Funnel Analysis Dashboard
================================================
Author: Anoushka Rathore | github.com/sushi1507
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Behavioral Funnel Analysis",
    page_icon="🔍",
    layout="wide"
)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────

@st.cache_data
def load_data():
    df = pd.read_csv("data/user_events.csv")

    funnel = df.groupby("user_id")["event"].apply(list).reset_index()
    funnel.columns = ["user_id", "events"]

    funnel["visited"]   = funnel["events"].apply(lambda x: int("visit" in x))
    funnel["signed_up"] = funnel["events"].apply(lambda x: int("signup" in x))
    funnel["activated"] = funnel["events"].apply(lambda x: int("activation" in x))
    funnel["retained"]  = funnel["events"].apply(lambda x: int("retention_day7" in x))

    # Risk scoring
    def calculate_risk(row):
        score = 0
        if not row["signed_up"]:                          score += 1
        if row["signed_up"] and not row["activated"]:     score += 2
        if row["activated"] and not row["retained"]:      score += 3
        return score

    funnel["risk_score"] = funnel.apply(calculate_risk, axis=1)
    funnel["risk_level"] = funnel["risk_score"].apply(
        lambda x: "HIGH" if x >= 3 else ("MEDIUM" if x == 2 else "LOW")
    )

    # Anomaly flag
    funnel["anomaly_flag"] = funnel.apply(lambda r:
        "Activated — Not Retained"   if r["activated"] and not r["retained"]
        else ("Signed Up — Not Activated" if r["signed_up"] and not r["activated"]
        else ("Visit Only"               if not r["signed_up"]
        else "Healthy Journey")), axis=1
    )

    # Device + source (merge back)
    device_map  = df.groupby("user_id")["device"].first().reset_index()
    source_map  = df.groupby("user_id")["source"].first().reset_index()
    funnel = funnel.merge(device_map, on="user_id").merge(source_map, on="user_id")

    return funnel, df

funnel, raw_df = load_data()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.title("🔍 Behavioral Anomaly & Funnel Analysis Dashboard")
st.caption("Product funnel analytics with anomaly detection | Anoushka Rathore | github.com/sushi1507")
st.divider()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

st.sidebar.header("🔧 Filters")
risk_filter   = st.sidebar.multiselect("Risk Level",
    options=["HIGH", "MEDIUM", "LOW"], default=["HIGH", "MEDIUM", "LOW"])
device_filter = st.sidebar.multiselect("Device",
    options=funnel["device"].unique(), default=list(funnel["device"].unique()))
source_filter = st.sidebar.multiselect("Acquisition Source",
    options=funnel["source"].unique(), default=list(funnel["source"].unique()))

df_f = funnel[
    funnel["risk_level"].isin(risk_filter) &
    funnel["device"].isin(device_filter) &
    funnel["source"].isin(source_filter)
]

# ─────────────────────────────────────────────
# ROW 1: FUNNEL KPIs
# ─────────────────────────────────────────────

st.subheader("📊 Funnel Metrics")

total      = len(df_f)
signups    = df_f["signed_up"].sum()
activations= df_f["activated"].sum()
retained   = df_f["retained"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users",    total)
col2.metric("Signed Up",      f"{signups} ({signups/total*100:.0f}%)" if total else "0")
col3.metric("Activated",      f"{activations} ({activations/total*100:.0f}%)" if total else "0")
col4.metric("Retained Day 7", f"{retained} ({retained/total*100:.0f}%)" if total else "0")

st.divider()

# ─────────────────────────────────────────────
# ROW 2: DROP-OFF METRICS
# ─────────────────────────────────────────────

st.subheader("📉 Drop-off Analysis")
col_a, col_b, col_c = st.columns(3)

dropped_signup     = total - signups
dropped_activation = signups - activations
dropped_retention  = activations - retained

col_a.metric("Dropped at Signup",     dropped_signup,
             delta=f"-{dropped_signup/total*100:.0f}%" if total else "", delta_color="inverse")
col_b.metric("Dropped at Activation", dropped_activation,
             delta=f"-{dropped_activation/signups*100:.0f}%" if signups else "", delta_color="inverse")
col_c.metric("Dropped at Retention",  dropped_retention,
             delta=f"-{dropped_retention/activations*100:.0f}%" if activations else "", delta_color="inverse")

st.divider()

# ─────────────────────────────────────────────
# ROW 3: CHARTS
# ─────────────────────────────────────────────

col_x, col_y, col_z = st.columns(3)

with col_x:
    st.markdown("#### Risk Level Distribution")
    rl = df_f["risk_level"].value_counts().reset_index()
    rl.columns = ["Risk Level", "Users"]
    st.bar_chart(rl.set_index("Risk Level"))

with col_y:
    st.markdown("#### Anomaly Flag Breakdown")
    af = df_f["anomaly_flag"].value_counts().reset_index()
    af.columns = ["Anomaly", "Users"]
    st.bar_chart(af.set_index("Anomaly"))

with col_z:
    st.markdown("#### Drop-off by Device")
    device_drop = df_f[df_f["anomaly_flag"] != "Healthy Journey"].groupby(
        "device").size().reset_index(name="Drop-offs")
    st.bar_chart(device_drop.set_index("device"))

st.divider()

# ─────────────────────────────────────────────
# ROW 4: FUNNEL VISUALIZATION
# ─────────────────────────────────────────────

st.subheader("🔽 Funnel Drop-off View")

funnel_data = pd.DataFrame({
    "Stage":  ["Visit", "Sign Up", "Activation", "Day-7 Retention"],
    "Users":  [total, int(signups), int(activations), int(retained)]
})

st.bar_chart(funnel_data.set_index("Stage"))

st.divider()

# ─────────────────────────────────────────────
# ROW 5: USER RISK TABLE
# ─────────────────────────────────────────────

st.subheader("🚨 User Risk Table")

def color_risk(val):
    if val == "HIGH":   return "background-color: #ff4b4b; color: white"
    elif val == "MEDIUM": return "background-color: #ffa500; color: white"
    else:               return "background-color: #21c354; color: white"

def color_anomaly(val):
    if "Not Retained"   in str(val): return "background-color: #ff4b4b; color: white"
    if "Not Activated"  in str(val): return "background-color: #ffa500; color: white"
    if "Visit Only"     in str(val): return "color: #aaaaaa"
    return ""

display = df_f[["user_id", "risk_score", "risk_level", "anomaly_flag",
                "device", "source", "signed_up", "activated", "retained"]]

styled = (display.style
    .map(color_risk,    subset=["risk_level"])
    .map(color_anomaly, subset=["anomaly_flag"])
)

st.dataframe(styled, use_container_width=True, hide_index=True)

st.divider()

# ─────────────────────────────────────────────
# ROW 6: HIGH RISK ALERT QUEUE
# ─────────────────────────────────────────────

st.subheader("⚠️ High Risk User Queue")

high_risk = df_f[df_f["risk_level"] == "HIGH"]

if len(high_risk) > 0:
    st.error(f"🚨 {len(high_risk)} users flagged as HIGH risk — immediate investigation recommended")
    st.dataframe(
        high_risk[["user_id", "risk_score", "anomaly_flag", "device", "source"]],
        use_container_width=True, hide_index=True
    )
else:
    st.success("✅ No HIGH risk users in current filtered view")

st.caption("Anoushka Rathore | github.com/sushi1507 | linkedin.com/in/anoushka-rathore-452b22259")