# dashboard.py

import streamlit as st
import pandas as pd

from analyzer.product_ranking import rank_products, group_by_action
from analyzer.diagnosis import diagnose
from analyzer.recommendations import generate_recommendations


st.set_page_config(page_title="ML Optimizer", layout="wide")

st.title("🚀 Mercado Libre AI Optimizer")
st.markdown("Product performance analysis with actionable insights")

# =========================
# DATA UPLOAD
# =========================

st.sidebar.header("📂 Upload Data")

uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])


def load_data(file):
    df = pd.read_csv(file)
    return df.to_dict(orient="records")


# =========================
# TRAFFIC LIGHT
# =========================

def color_category(category):
    if category == "scale":
        return "🟢 Scale"
    elif category == "optimize":
        return "🟡 Optimize"
    else:
        return "🔴 Pause"


# =========================
# MAIN
# =========================

if uploaded_file:
    products = load_data(uploaded_file)

    ranked = rank_products(products)
    grouped = group_by_action(ranked)

    df = pd.DataFrame(ranked)

    df["action"] = df["category"].apply(color_category)

    # =========================
    # OVERVIEW
    # =========================

    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("🟢 Scale", len(grouped["scale"]))
    col2.metric("🟡 Optimize", len(grouped["optimize"]))
    col3.metric("🔴 Pause", len(grouped["pause"]))

    st.divider()

    # =========================
    # TOP PRODUCTS
    # =========================

    st.subheader("🏆 Top Performers")

    top_products = df.sort_values(by="score", ascending=False).head(3)

    for _, row in top_products.iterrows():
        st.success(f"{row['product_id']} | Score: {row['score']} | {row['action']}")

    st.divider()

    # =========================
    # MAIN TABLE
    # =========================

    st.subheader("📋 Product Ranking")

    st.dataframe(
        df[["product_id", "score", "action"]],
        use_container_width=True
    )

    st.divider()

    # =========================
    # FILTER
    # =========================

    st.subheader("🔍 Filter")

    option = st.selectbox(
        "Select category",
        ["All", "Scale", "Optimize", "Pause"]
    )

    if option != "All":
        filter_map = {
            "Scale": "scale",
            "Optimize": "optimize",
            "Pause": "pause"
        }
        df = df[df["category"] == filter_map[option]]

    st.dataframe(
        df[["product_id", "score", "action"]],
        use_container_width=True
    )

    st.divider()

    # =========================
    # PRODUCT DETAIL
    # =========================

    st.subheader("🔎 Product Detail")

    product_ids = df["product_id"].tolist()

    selected = st.selectbox("Select a product", product_ids)

    selected_product = next(p for p in ranked if p["product_id"] == selected)

    metrics = selected_product["metrics"]

    # =========================
    # KPIs
    # =========================

    st.write("### 📊 Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("CTR", f"{metrics['ctr']:.2%}")
    col2.metric("Conversion Rate", f"{metrics['conversion_rate']:.2%}")
    col3.metric("ACOS", f"{metrics['acos']:.2%}")

    # =========================
    # MONEY METRICS
    # =========================

    st.write("### 💰 Financials")

    original = next(p for p in products if p["id"] == selected)

    col1, col2 = st.columns(2)

    col1.metric("Revenue", f"${original['revenue']}")
    col2.metric("Ad Spend", f"${original['ad_spend']}")

    # =========================
    # ACTION
    # =========================

    st.write("### 🚦 Recommended Action")
    st.write(color_category(selected_product["category"]))

    # =========================
    # DIAGNOSIS
    # =========================

    st.write("### ⚠️ Detected Problems")

    problems = diagnose(metrics)

    for p in problems:
        st.warning(p["message"])

    # =========================
    # RECOMMENDATIONS
    # =========================

    st.write("### ✅ Recommended Actions")

    actions = generate_recommendations(problems)

    for a in actions:
        st.write(f"- {a}")

else:
    st.info("👈 Upload a CSV file to start analysis")
