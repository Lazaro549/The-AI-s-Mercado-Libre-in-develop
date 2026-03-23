# 🚀 AI Mercado Libre Optimizer

AI-powered tool designed to **analyze listings, optimize ad campaigns, and increase sales on Mercado Libre** using data-driven decisions.

---

## 🎯 Problem

Most Mercado Libre sellers:

* Invest in ads without knowing if they are profitable
* Don’t understand why they are not making sales
* Fail to properly optimize campaigns
* Lose money due to high ACOS

---

## 💡 Solution

This project automatically analyzes your listings and campaigns to:

* Detect performance issues
* Identify which products to scale or pause
* Optimize advertising investment (Ads)
* Improve CTR, conversion rate, and profitability

---

## 📊 Key Metrics Analyzed

The tool is based on core Mercado Ads metrics:

* **Impressions** → visibility
* **Clicks** → user interest
* **CTR** → ability to attract clicks
* **Conversion Rate** → sales generated
* **ACOS** → advertising profitability

---

## ⚙️ How It Works

### 1. Input (product data)

```json id="en1"
{
  "impressions": 12000,
  "clicks": 150,
  "sales": 3,
  "ad_spend": 900,
  "revenue": 3000
}
```

---

### 2. Automatic Analysis

The system:

* Calculates key metrics
* Detects performance issues
* Evaluates profitability (ACOS)
* Analyzes bidding strategy

---

### 3. Output (actionable decisions)

Example result:

* Problem: Low CTR
* Cause: Low search attractiveness
* Actions:

  * Optimize title
  * Improve main image
  * Adjust price

---

## 🧠 System Modules

### 📦 analyzer/

Handles performance analysis:

* `metrics.py` → CTR, conversion, and ACOS calculations
* `diagnosis.py` → issue detection
* `recommendations.py` → actions to improve sales

---

### 💰 ads/

Advertising optimization:

* `acos_optimizer.py` → profitability control
* `bidding_logic.py` → bidding strategy (CPC & visibility)

---

### 🚀 app.py

System entry point:

* Integrates analysis + Ads
* Generates full diagnostics
* Suggests business actions

---

## ▶️ How to Use

1. Clone the repository:

```bash id="en2"
git clone https://github.com/Lazaro549/The-AI-s-Mercado-Libre-in-develop.git
cd The-AI-s-Mercado-Libre-in-develop
```

2. Run the analysis:

```bash id="en3"
python app.py
```

3. Interpret results:

* Detected problems
* Recommendations
* Ads strategy
* Investment adjustments

---

## 📈 Use Cases

* Identify products losing money
* Reduce ACOS in campaigns
* Scale profitable products
* Improve low-performing listings

---

## 🔥 Benefits

* Data-driven decisions
* Automated campaign optimization
* Reduced wasted ad spend
* Increased sales and profitability

---

## ⚠️ Current Limitations

* Not connected to Mercado Libre API
* Manual data input
* No listing content analysis yet
* No visual interface

---

## 🚀 Roadmap

* Integration with real data
* Interactive dashboard
* Product scoring system
* Product ranking (winners vs losers)
* Listing optimization (SEO for Mercado Libre)

---

## 👤 Who Is This For?

* Mercado Libre sellers
* Users running Mercado Ads campaigns
* Businesses looking to scale online sales

---

## 🧩 Project Vision

To become an intelligent system that:

* Automates campaign decisions
* Optimizes listings
* Maximizes sales with the lowest possible ACOS

---

## 📬 Contributions

You can contribute by improving:

* Analysis algorithms
* Ads strategies
* API integrations
* Visual interfaces

---

## 📄 License

MIT License

