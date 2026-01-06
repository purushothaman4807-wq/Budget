import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Union Budget of India – Live Viewer",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("🇮🇳 Union Budget of India – Live Budget Explorer")
st.markdown(
    "This dashboard provides year-wise and theme-wise budget allocation details. "
    "Data is sourced from official budget documents and structured for analysis."
)

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
    sorted(df["Theme"].dropna().unique())
)

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df["Year"] == year) &
    (df["Theme"] == theme)
]

# ---------------- SUMMARY ----------------
total_budget = filtered_df["Total Allocation"].sum()

st.subheader(f"📊 {theme} Budget – {year}")
st.metric(
    label="Total Allocation (₹ Crore)",
    value=f"{total_budget:,.0f}"
)

# ---------------- TABLE ----------------
st.subheader("📄 Detailed Sub-Allocations")
st.dataframe(
    filtered_df[["Sub-Theme", "Sub Allocation"]],
    use_container_width=True
)

# ---------------- BAR CHART ----------------
st.subheader("📈 Sub-Theme Allocation Comparison")

chart_df = (
    filtered_df
    .groupby("Sub-Theme", as_index=False)["Sub Allocation"]
    .sum()
    .sort_values("Sub Allocation", ascending=False)
)

st.bar_chart(
    chart_df.set_index("Sub-Theme")
)

# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "🔗 This page is designed to be accessed via Tableau dashboard navigation. "
    "Clicking the image in Tableau opens this live budget explorer."
)
