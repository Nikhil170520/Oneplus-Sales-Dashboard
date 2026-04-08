# 🔴 OnePlus India Sales Dashboard

> **Kalaiworks Data Analyst Interview Task** — Streamlit dashboard built with dummy OnePlus sales data (Jan 2024 – Mar 2025).

---

## 📊 Dashboard Features

| Section | Charts |
|---|---|
| **KPI Row** | Transactions · Units Sold · Total Revenue · Avg Order Value · Avg Rating |
| **Row 1** | Quantity by Day of Month (line) · Sales by City India (bubble map) |
| **Row 2** | Revenue by OnePlus Model (bar) · Transactions by Payment Method (donut) · Revenue by Channel (bar) |
| **Row 3** | Customer Ratings (bar) · Sales by Day of Week (bar) · Monthly Revenue Trend (line) |
| **Sidebar** | Filters: Month · Year · Model · Channel · Payment Method |

---

## 📱 Dummy Dataset Details

- **Records:** 8,000 transactions
- **Period:** January 2024 – March 2025
- **Models:** OnePlus 13, OnePlus 12R, OnePlus Nord 4, OnePlus 12, OnePlus Nord CE4, OnePlus Open
- **Cities:** Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Kolkata, Pune, Ahmedabad, Jaipur, Lucknow
- **Payment Methods:** UPI, Debit Card, Cash, Credit Card, EMI
- **Channels:** OnePlus Store, Amazon, Flipkart, Croma, Reliance Digital

---

## 🚀 Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/oneplus-sales-dashboard
cd oneplus-sales-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub (set as **Public**)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** → Connect GitHub → Select `app.py` → **Deploy**
4. Get your live link: `https://YOUR_USERNAME-oneplus-sales-dashboard-app-XXXX.streamlit.app`

---

## 🛠️ Tech Stack

- **Python 3.11**
- **Streamlit** — App framework
- **Plotly** — Interactive charts (scatter, bar, pie, line, mapbox)
- **Pandas / NumPy** — Data generation & manipulation

---

*Built for the Kalaiworks Data Analyst Interview · 2024*
