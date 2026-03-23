# dashboard.py

import streamlit as st
import pandas as pd

from analyzer.product_ranking import rank_products, group_by_action


st.set_page_config(page_title="ML Optimizer", layout="wide")

st.title("🚀 Mercado Libre AI Optimizer")
st.markdown("Product performance analysis with traffic light system")

# =========================
# DATA UPLOAD
# =========================

st.sidebar.header("📂 Upload Data")

uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])


def load_data(file):
    df = pd.read_csv(file)
    return df.to_dict(orient="records")


# =========================
# TRAFFIC LIGHT COLORS
# =========================

def color_category(category):
    if category == "scale":
        return "🟢 Scale"
    elif category == "optimize":
        return "🟡 Optimize"
    else:
        return "🔴 Pause"


# =========================
# DASHBOARD
# =========================

if uploaded_file:
    products = load_data(uploaded_file)

    ranked = rank_products(products)
    grouped = group_by_action(ranked)

    # Convert to DataFrame
    df = pd.DataFrame(ranked)

    df["action"] = df["category"].apply(color_category)
    df["score"] = df["score"]

    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("🟢 Scale", len(grouped["scale"]))
    col2.metric("🟡 Optimize", len(grouped["optimize"]))
    col3.metric("🔴 Pause", len(grouped["pause"]))

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

    st.subheader("🔍 Filter by action")

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

    st.write("### Metrics")
    st.json(selected_product["metrics"])

    st.write("### Score")
    st.write(selected_product["score"])

    st.write("### Recommended Action")
    st.write(color_category(selected_product["category"]))

else:
    st.info("👈 Upload a CSV file to get started")
