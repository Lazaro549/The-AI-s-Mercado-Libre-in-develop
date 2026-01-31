# Mercado Libre AI – Engineering & Machine Learning Overview

This repository provides a **developer-focused overview** of how Mercado Libre designs, builds, and operates **Artificial Intelligence and Machine Learning systems at scale** across its marketplace ecosystem (Search, Ads, Payments, Risk).

> ⚠️ Disclaimer  
> This document is based on public information, engineering talks, and industry best practices.  
> It does **not** include proprietary code, models, or internal documentation.

---

## 🔐 Authentication Flow (OAuth 2.0)

The following diagram illustrates the **OAuth 2.0 Authorization Code flow** used by the Mercado Libre API, showing how users securely authorize third-party applications to act on their behalf.

<p align="center">
  <img 
    src="https://github.com/user-attachments/assets/b45a6d31-01c7-4224-8a65-4ead984138b0"
    width="600"
    alt="Mercado Libre OAuth Authorization Code Flow"
  />
</p>

**Flow summary:**
1. The application redirects the user to Mercado Libre.
2. The user authenticates on Mercado Libre.
3. The user authorizes the application.
4. The application receives an authorization code.
5. The code is exchanged for an access token.
6. The user is redirected back to the application with access granted.

---

## 🎯 Problem Space

Mercado Libre operates one of the largest marketplaces in Latin America, facing challenges such as:

- Millions of concurrent searches
- Real-time ranking with strict latency constraints (<100ms)
- Product and ad competition
- Fraud and abuse prevention
- Conversion and monetization optimization

AI at Mercado Libre is **core infrastructure**, not a feature.

---

## 🧠 Core ML Domains

### 1. Search & Ranking (Marketplace Core)

**Problem**  
Rank millions of listings while maximizing relevance, conversion, and user satisfaction.

**Technical approach**
- Learning-to-Rank models
- Heavy feature engineering
- Real-time inference

**Common features**
- Historical CTR
- Conversion rate (CVR)
- Price competitiveness
- Shipping speed and cost
- Seller reputation
- Listing content quality

> Engineering insight:  
> The ranking system optimizes long-term user satisfaction, not just immediate sales.

---

### 2. NLP & Content Intelligence

**Problem**  
Understand and process massive volumes of unstructured text.

**Technical approach**
- Transformer-based models (BERT-like)
- Semantic embeddings
- Text classification and similarity models

**Use cases**
- Automatic product categorization
- Search-query ↔ listing matching
- Spam and policy violation detection

---

### 3. Mercado Ads (Product Ads)

**Problem**  
Monetize traffic without degrading user experience.

**Technical approach**
- CTR and CVR prediction models
- Second-price auction system
- Ad ranking based on bid and quality



