"""Streamlit dashboard for AI Mercado Libre Optimizer.

This module provides an interactive web interface for product performance analysis
and optimization recommendations using Streamlit.
"""

import streamlit as st
import pandas as pd
import logging
from analyzer.product_ranking import rank_products, group_by_action
from analyzer.diagnosis import diagnose
from analyzer.recommendations import generate_recommendations
from logger_config import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)

st.set_page_config(page_title="ML Optimizer", layout="wide")

st.title("🚀 Mercado Libre AI Optimizer")
st.markdown("Product performance analysis with actionable insights")

# =========================
# DATA UPLOAD
# =========================

st.sidebar.header("📂 Upload Data")

uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])


def load_data(file):
    """Load and parse CSV data.
    
    Args:
        file: Uploaded file object from Streamlit.
        
    Returns:
        list: List of product dictionaries.
        
    Raises:
        ValueError: If file parsing fails.
    """
    try:
        df = pd.read_csv(file)
        logger.info(f"Successfully loaded CSV with {len(df)} products")
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error loading CSV file: {e}")
        st.error(f"Error loading file: {e}")
        raise


# =========================
# TRAFFIC LIGHT
# =========================

def color_category(category):
    """Map category to emoji indicator.
    
    Args:
        category (str): Product category ("scale", "optimize", "pause").
        
    Returns:
        str: Emoji-labeled category string.
    """
    color_map = {
        "scale": "🟢 Scale",
        "optimize": "🟡 Optimize",
        "pause": "🔴 Pause"
    }
    return color_map.get(category, "⚫ Unknown")


# =========================
# MAIN
# =========================

if uploaded_file:
    try:
        products = load_data(uploaded_file)
        logger.info(f"Starting analysis of {len(products)} uploaded products")

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
        # DETAILED ANALYSIS
        # =========================

        st.subheader("📋 Detailed Analysis")

        # Create tabs for each action category
        tab1, tab2, tab3 = st.tabs(["🟢 Scale", "🟡 Optimize", "🔴 Pause"])

        with tab1:
            if grouped["scale"]:
                for product in grouped["scale"]:
                    with st.expander(f"Product: {product['product_id']} (Score: {product['score']})"):
                        st.write(f"**Metrics:** {product['metrics']}")
                        problems = diagnose(product["metrics"])
                        actions = generate_recommendations(problems)
                        st.write("**Status:** ✅ Good Performance")
                        st.write("**Recommended Actions:**")
                        for action in actions:
                            st.write(f"- {action}")
            else:
                st.info("No products in scale category")

        with tab2:
            if grouped["optimize"]:
                for product in grouped["optimize"]:
                    with st.expander(f"Product: {product['product_id']} (Score: {product['score']})"):
                        st.write(f"**Metrics:** {product['metrics']}")
                        problems = diagnose(product["metrics"])
                        actions = generate_recommendations(problems)
                        st.write("**Issues Found:**")
                        for problem in problems:
                            st.warning(problem["message"])
                        st.write("**Recommended Actions:**")
                        for action in actions:
                            st.write(f"- {action}")
            else:
                st.info("No products in optimize category")

        with tab3:
            if grouped["pause"]:
                for product in grouped["pause"]:
                    with st.expander(f"Product: {product['product_id']} (Score: {product['score']})"):
                        st.write(f"**Metrics:** {product['metrics']}")
                        problems = diagnose(product["metrics"])
                        actions = generate_recommendations(problems)
                        st.write("**Critical Issues:**")
                        for problem in problems:
                            st.error(problem["message"])
                        st.write("**Recommended Actions:**")
                        for action in actions:
                            st.write(f"- {action}")
            else:
                st.info("No products in pause category")
        
        logger.info("Dashboard analysis completed successfully")

    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        st.error(f"Analysis failed: {e}")

else:
    st.info("📤 Please upload a CSV file to begin analysis")
    logger.info("Dashboard ready, waiting for file upload")
