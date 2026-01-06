import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Union Budget of India – Live Viewer",
    layout="wide"
)

st.title("🇮🇳 Union Budget of India – Live Budget Explorer")
st.markdown("Year-wise and theme-wise budget allocation viewer")

st.divider()

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_excel("Budget_DaTaset2.xlsx")
    
    # CLEAN COLUMN NAMES (VERY IMPORTANT)
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df

df = load_data()

# ---------------- DEBUG: SHOW COLUMNS ----------------
st.sidebar.subheader("📌 Dataset Columns")
st.sidebar.write(list(df.columns))

# ---------------- IDENTIFY SUB THEME COLUMN ----------------
# Adjusted to match most common cases
if "Sub_Theme" in df.columns:
    sub_theme_col = "Sub_Theme"
elif "Sub_Sector" in df.columns:
    sub_theme_col = "Sub_Sector"
else:
    st.error("❌ Sub-theme column not found. Please check Excel file.")
    st.stop()

# ---------------- ADD THEME LOGIC ----------------
def assign_theme(sub_theme):
    sub_theme = str(sub_theme).lower()

    if any(word in sub_theme for word in ["agri", "farm", "crop", "irrigation"]):
        return "Agriculture"

    elif any(word in sub_theme for word in ["defence", "defense", "pension", "border"]):
        return "Defence"

    elif any(word in sub_theme for word in ["school", "education", "higher", "skill"]):
        return "Education"

    elif any(word in sub_theme for word in ["health", "medical", "ayush"]):
        return "Health"

    elif any(word in sub_theme for word in ["road", "rail", "urban", "housing", "water"]):
        return "Infrastructure"

    else:
        return "Others"

df["Theme"] = df[sub_theme_col].apply(assign_theme)

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filters")

year_col = "Year" if "Year" in df.columns else df.columns[0]

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df[year_col].dropna().unique())
)

theme = st.sidebar.selectbox(
    "Select Theme",
    ["Agriculture", "Defence", "Education", "Health", "Infrastructure"]
)

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df[year_col] == year) &
    (df["Theme"] == theme)
]

# ---------------- METRIC ----------------
total_budget = filtered_df["Sub_Allocation"].sum() if "Sub_Allocation" in df.columns else 0

st.subheader(f"📊 {theme} Budget – {year}")
st.metric(
    "Total Allocation (₹ Crore)",
    f"{total_budget:,.0f}"
)

# ---------------- TABLE ----------------
st.subheader("📄 Sub-Theme Allocation Details")

display_cols = [sub_theme_col]
if "Sub_Allocation" in df.columns:
    display_cols.append("Sub_Allocation")

st.dataframe(
    filtered_df[display_cols],
    use_container_width=True
)

# ---------------- BAR CHART ----------------
st.subheader("📈 Allocation by Sub-Theme")

if "Sub_Allocation" in df.columns:
    chart_df = (
        filtered_df
        .groupby(sub_theme_col, as_index=False)["Sub_Allocation"]
        .sum()
        .sort_values("Sub_Allocation", ascending=False)
    )

    st.bar_chart(chart_df.set_index(sub_theme_col))
else:
    st.warning("Sub Allocation column not found for chart.")

# ---------------- FOOTER ----------------
st.divider()
st.caption("Connected via Tableau dashboard navigation | Python-powered live viewer")
