# 🚀 AI Mercado Libre Optimizer

An intelligent system designed to **analyze product performance, optimize advertising campaigns, and maximize sales on Mercado Libre** using data-driven decision making.

---

## 🎯 The Problem

Most Mercado Libre sellers operate without a clear optimization strategy:

* They invest in ads without measuring profitability
* They don’t know why products are not selling
* They fail to identify which products to scale or pause
* They lose money due to inefficient ACOS

---

## 💡 The Solution

This tool transforms raw performance data into **clear, actionable decisions**.

It allows you to:

* Detect underperforming products
* Identify high-potential products to scale
* Optimize advertising investment
* Reduce wasted spend and improve profitability

---

## 📊 Core Metrics

The system is built around key Mercado Ads performance indicators:

* **Impressions** → Visibility
* **Clicks** → User interest
* **CTR (Click Through Rate)** → Attraction power
* **Conversion Rate** → Sales efficiency
* **ACOS (Advertising Cost of Sales)** → Profitability

---

## ⚙️ How It Works

### 1. Data Input

Upload product performance data:

```json
{
  "impressions": 12000,
  "clicks": 150,
  "sales": 3,
  "ad_spend": 900,
  "revenue": 3000
}
```

---

### 2. Analysis Engine

The system automatically:

* Calculates key metrics
* Detects performance issues
* Evaluates profitability
* Applies ranking logic

---

### 3. Decision System

Each product is classified into:

* 🟢 **Scale** → High performance, increase investment
* 🟡 **Optimize** → Needs improvement
* 🔴 **Pause** → Low performance, stop spending

---

## 🧠 Architecture

### 📦 analyzer/

Performance intelligence layer:

* `metrics.py` → KPI calculations
* `diagnosis.py` → issue detection
* `recommendations.py` → action generation
* `product_ranking.py` → scoring & classification

---

### 💰 ads/

Advertising optimization layer:

* `acos_optimizer.py` → profitability control
* `bidding_logic.py` → bidding strategy & CPC estimation

---

### 🚀 Execution Layer

* `app.py` → single product analysis
* `app_batch.py` → bulk product analysis
* `dashboard.py` → visual interface (Streamlit)

---

## 📊 Dashboard (Streamlit)

Interactive interface with:

* Product ranking
* Traffic light system (Scale / Optimize / Pause)
* Performance overview
* Product-level insights

---

## ▶️ How to Use

### 1. Install dependencies

```bash
pip install streamlit pandas
```

---

### 2. Run the dashboard

```bash
streamlit run dashboard.py
```

---

### 3. Upload your data

CSV format:

```csv
id,impressions,clicks,sales,ad_spend,revenue
A1,15000,800,60,2000,12000
B2,12000,200,5,1500,4000
C3,9000,90,1,800,1500
```

---

## 📈 Use Cases

* Identify products losing money
* Reduce ACOS across campaigns
* Scale high-performing listings
* Prioritize budget allocation
* Analyze entire product catalogs

---

## 🔥 Key Benefits

* Data-driven decision making
* Automated product prioritization
* Reduced advertising waste
* Increased sales and profitability
* Scalable analysis for large catalogs

---

## ⚠️ Current Limitations

* Manual data input (no API integration yet)
* No listing content analysis (title, price, images)
* No automated campaign execution
* Basic UI (Streamlit)

---

## 🚀 Roadmap

* Mercado Libre API integration
* Automated campaign adjustments
* Listing optimization (title, price, SEO)
* Advanced dashboard with visual analytics
* SaaS deployment

---

## 👤 Who Is This For?

* Mercado Libre sellers
* E-commerce operators
* Performance marketing specialists
* Agencies managing multiple products

---

## 🧩 Vision

To become a **fully automated optimization engine** that:

* Identifies opportunities
* Makes decisions
* Optimizes campaigns
* Maximizes profitability

---

## 📬 Contributing

Contributions are welcome in:

* Performance algorithms
* Ads optimization strategies
* Data integrations
* UI/UX improvements

---

## 📄 License

MIT License

## 📄 License

MIT License

