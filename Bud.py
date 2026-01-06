import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Union Budget of India – Live Viewer",
    layout="wide"
)

st.title("🇮🇳 Union Budget of India – Live Budget Explorer")
st.markdown(
    "Interactive viewer for India’s Union Budget with year-wise and theme-wise analysis."
)

st.divider()

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_excel("Budget_DaTaset2.xlsx")

df = load_data()

# ---------------- ADD THEME LOGIC ----------------
def assign_theme(sub_theme):
    if sub_theme in [
        "Agri & Farmers Welfare", "Agricultural Research",
        "Crop Insurance", "Irrigation"
    ]:
        return "Agriculture"

    elif sub_theme in [
        "Defence Revenue", "Defence Capital",
        "Defence Pension", "Border Roads"
    ]:
        return "Defence"

    elif sub_theme in [
        "School Education", "Higher Education",
        "Mid Day Meal", "Skill Development"
    ]:
        return "Education"

    elif sub_theme in [
        "Health & Family Welfare", "Health Research",
        "Ayush", "Medical Education"
    ]:
        return "Health"

    elif sub_theme in [
        "Road Transport", "Railways",
        "Urban Development", "Housing", "Water Resources"
    ]:
        return "Infrastructure"

    else:
        return "Others"

df["Theme"] = df["Sub-Theme"].apply(assign_theme)

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filters")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["Year"].dropna().unique())
)

theme = st.sidebar.selectbox(
    "Select Theme",
    ["Agriculture", "Defence", "Education", "Health", "Infrastructure"]
)

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df["Year"] == year) &
    (df["Theme"] == theme)
]

# ---------------- SUMMARY ----------------
total_budget = filtered_df["Sub Allocation"].sum()

st.subheader(f"📊 {theme} Budget – {year}")
st.metric(
    label="Total Allocation (₹ Crore)",
    value=f"{total_budget:,.0f}"
)

# ---------------- TABLE ----------------
st.subheader("📄 Sub-Theme Allocation Details")
st.dataframe(
    filtered_df[["Sub-Theme", "Sub Allocation"]],
    use_container_width=True
)

# ---------------- BAR CHART ----------------
st.subheader("📈 Allocation by Sub-Theme")

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
    "🔗 This live budget explorer is connected via Tableau dashboard navigation."
)
