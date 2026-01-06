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
    ["Agriculture", "Defence", "Health", "Education", "Infrastructure"]
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

ta_col = theme_config[theme]["ta"]
sub_cols = theme_config[theme]["subs"]

# ---------------- FILTER DATA ----------------
year_df = df[df["Year"] == year]

# ---------------- METRIC ----------------
total_allocation = year_df[ta_col].values[0]

st.subheader(f"📊 {theme} Budget – {year}")
st.metric("Total Allocation (₹ Crore)", f"{total_allocation:,.0f}")

# ---------------- SUB ALLOCATION TABLE ----------------
sub_df = year_df[sub_cols].T.reset_index()
sub_df.columns = ["Sub-Theme", "Allocation"]

st.subheader("📄 Sub-Theme Allocation Details")
st.dataframe(sub_df, use_container_width=True)

# ---------------- BAR CHART ----------------
st.subheader("📈 Sub-Theme Allocation Comparison")
st.bar_chart(sub_df.set_index("Sub-Theme"))

# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "Python-powered live budget explorer | Linked via Tableau dashboard image"
)
