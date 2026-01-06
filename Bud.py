import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Union Budget of India – Live Viewer",
    layout="wide"
)

st.title("🇮🇳 Union Budget of India – Live Budget Explorer")
st.markdown("Theme-wise and year-wise analysis of India’s Union Budget")

st.divider()

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_excel("Budget_DaTaset2.xlsx")

df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filters")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["Year"].dropna().unique())
)

theme = st.sidebar.selectbox(
    "Select Theme",
    ["All", "Agriculture", "Defence", "Health", "Education", "Infrastructure"]
)

# ---------------- THEME CONFIG ----------------
theme_config = {
    "Agriculture": {
        "ta": "AgricultureTA",
        "subs": ["Agri & Farmers Welfare", "Agri Research (ICAR)"]
    },
    "Defence": {
        "ta": "Defence TA",
        "subs": ["Revenue", "Capital Outlay", "Pensions", "Civil"]
    },
    "Health": {
        "ta": "Health TA",
        "subs": ["Health & FW", "Health Research"]
    },
    "Education": {
        "ta": "Education TA",
        "subs": ["School Education", "Higher Education"]
    },
    "Infrastructure": {
        "ta": "Infrastructure TA",
        "subs": ["Roads", "Railways", "Urban", "Power", "Water", "Ports", "Telecom"]
    }
}

year_df = df[df["Year"] == year]

# ================= ALL THEMES =================
if theme == "All":
    st.subheader(f"📊 Overall Budget Summary – {year}")

    total_budget = 0
    summary_rows = []

    for t, cfg in theme_config.items():
        ta_value = year_df[cfg["ta"]].values[0]
        total_budget += ta_value
        summary_rows.append([t, ta_value])

    summary_df = pd.DataFrame(
        summary_rows,
        columns=["Theme", "Total Allocation"]
    )

    st.metric(
        "Total Union Budget (₹ Crore)",
        f"{total_budget:,.0f}"
    )

    st.subheader("📈 Theme-wise Allocation")
    st.bar_chart(summary_df.set_index("Theme"))

    st.subheader("📄 Theme-wise Allocation Table")
    st.dataframe(summary_df, use_container_width=True)

# ================= SINGLE THEME =================
else:
    cfg = theme_config[theme]
    ta_col = cfg["ta"]
    sub_cols = cfg["subs"]

    total_allocation = year_df[ta_col].values[0]

    st.subheader(f"📊 {theme} Budget – {year}")
    st.metric(
        "Total Allocation (₹ Crore)",
        f"{total_allocation:,.0f}"
    )

    sub_df = year_df[sub_cols].T.reset_index()
    sub_df.columns = ["Sub-Theme", "Allocation"]

    st.subheader("📄 Sub-Theme Allocation Details")
    st.dataframe(sub_df, use_container_width=True)

    st.subheader("📈 Sub-Theme Allocation Comparison")
    st.bar_chart(sub_df.set_index("Sub-Theme"))

# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "Python-powered live budget explorer | Connected via Tableau dashboard navigation"
)
