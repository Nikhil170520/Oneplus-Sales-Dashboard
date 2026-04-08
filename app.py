import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OnePlus Sales Dashboard",
    page_icon="Logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stSidebar"] {
    background: #0d0d0d !important;
    border-right: 1px solid #1f1f1f;
}
[data-testid="stSidebar"] * { color: #d4d4d4 !important; }
[data-testid="stSidebar"] label {
    color: #888 !important; font-size:0.72rem;
    text-transform:uppercase; letter-spacing:0.08em;
}

.main { background: #f9fafb; }

.brand {
    font-family:'Syne',sans-serif; font-weight:800; font-size:1.7rem;
    color:#eb0029; letter-spacing:-0.02em;
}
.sub-brand { font-size:0.7rem; color:#888; letter-spacing:0.12em; text-transform:uppercase; }

.kpi-wrap {
    background:white; border-radius:16px; padding:16px 18px;
    box-shadow:0 1px 4px rgba(0,0,0,0.06), 0 6px 20px rgba(0,0,0,0.05);
    border:1px solid #f0f0f0;
    display:flex; align-items:center; gap:13px;
}
.kpi-icon {
    font-size:1.6rem; width:48px; height:48px; border-radius:12px;
    display:flex; align-items:center; justify-content:center; flex-shrink:0;
}
.kpi-label {
    font-size:0.68rem; font-weight:600; text-transform:uppercase;
    letter-spacing:0.09em; color:#9ca3af; margin-bottom:2px;
}
.kpi-value {
    font-family:'Syne',sans-serif; font-size:1.4rem;
    font-weight:700; color:#111; line-height:1.1;
}
.kpi-delta { font-size:0.7rem; color:#16a34a; margin-top:2px; font-weight:500; }

.chart-box {
    background:white; border-radius:16px; padding:16px 16px 6px;
    box-shadow:0 1px 4px rgba(0,0,0,0.06), 0 6px 20px rgba(0,0,0,0.05);
    border:1px solid #f0f0f0;
}
.chart-title {
    font-family:'Syne',sans-serif; font-size:0.8rem; font-weight:700;
    color:#111; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;
}
.footer {
    text-align:center; font-size:0.7rem; color:#9ca3af;
    margin-top:2.5rem; padding-top:1rem; border-top:1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)


# ── Generate OnePlus Dataset ───────────────────────────────────────────
@st.cache_data
def generate_data():
    np.random.seed(7)
    random.seed(7)
    n = 8000
    start = datetime(2024, 1, 1)
    end   = datetime(2025, 3, 31)
    delta = (end - start).days
    dates = [start + timedelta(days=random.randint(0, delta)) for _ in range(n)]

    models = ["OnePlus 13","OnePlus 12R","OnePlus Nord 4",
              "OnePlus 12","OnePlus Nord CE4","OnePlus Open"]
    model_prices = {
        "OnePlus 13":69999,"OnePlus 12R":39999,"OnePlus Nord 4":29999,
        "OnePlus 12":64999,"OnePlus Nord CE4":24999,"OnePlus Open":139999,
    }
    model_w = [0.28,0.22,0.20,0.12,0.13,0.05]

    cities = ["Mumbai","Delhi","Bengaluru","Chennai","Hyderabad",
              "Kolkata","Pune","Ahmedabad","Jaipur","Lucknow"]
    coords = {
        "Mumbai":(19.076,72.877),"Delhi":(28.613,77.209),
        "Bengaluru":(12.972,77.594),"Chennai":(13.083,80.270),
        "Hyderabad":(17.385,78.486),"Kolkata":(22.573,88.364),
        "Pune":(18.520,73.856),"Ahmedabad":(23.023,72.572),
        "Jaipur":(26.912,75.787),"Lucknow":(26.847,80.947),
    }

    payments = ["UPI","Debit Card","Cash","Credit Card","EMI"]
    pay_w    = [0.38,0.20,0.12,0.15,0.15]

    channels = ["OnePlus Store","Amazon","Flipkart","Croma","Reliance Digital"]
    ch_w     = [0.25,0.30,0.25,0.10,0.10]

    m_list  = random.choices(models,   weights=model_w, k=n)
    c_list  = random.choices(cities,   k=n)
    p_list  = random.choices(payments, weights=pay_w,   k=n)
    ch_list = random.choices(channels, weights=ch_w,    k=n)

    df = pd.DataFrame({
        "Date":dates,"Model":m_list,"City":c_list,
        "Payment":p_list,"Channel":ch_list,
        "Quantity":np.random.randint(1,4,n),
        "Rating":np.random.choice([1,2,3,4,5],n,p=[0.03,0.07,0.15,0.45,0.30]),
        "TransactionID":[f"OP{str(i).zfill(6)}" for i in range(n)],
    })
    df["Price"]     = df["Model"].map(model_prices)
    df["Revenue"]   = df["Quantity"] * df["Price"]
    df["Month"]     = df["Date"].dt.strftime("%B")
    df["MonthNum"]  = df["Date"].dt.month
    df["Year"]      = df["Date"].dt.year
    df["Day"]       = df["Date"].dt.day
    df["DayName"]   = df["Date"].dt.strftime("%A")
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)
    df["Lat"]       = df["City"].map(lambda c: coords[c][0])
    df["Lon"]       = df["City"].map(lambda c: coords[c][1])
    return df

df_all = generate_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="brand">1+</div>'
                '<div class="sub-brand">Sales Intelligence</div>', unsafe_allow_html=True)
    st.markdown("---")

    months_ordered = ["January","February","March","April","May","June",
                      "July","August","September","October","November","December"]
    sel_months   = st.multiselect("📅 Month",   months_ordered, default=months_ordered)
    sel_years    = st.multiselect("📆 Year",    [2024,2025],    default=[2024,2025])
    sel_models   = st.multiselect("📱 Model",   sorted(df_all["Model"].unique()),   default=sorted(df_all["Model"].unique()))
    sel_channels = st.multiselect("🏪 Channel", sorted(df_all["Channel"].unique()), default=sorted(df_all["Channel"].unique()))
    sel_payments = st.multiselect("💳 Payment", sorted(df_all["Payment"].unique()), default=sorted(df_all["Payment"].unique()))
    st.markdown("---")
    st.caption("📊 OnePlus Sales · Jan 2024 – Mar 2025")

# ── Filter ───────────────────────────────────────────────────────────────────
df = df_all[
    df_all["Month"].isin(sel_months)     &
    df_all["Year"].isin(sel_years)       &
    df_all["Model"].isin(sel_models)     &
    df_all["Channel"].isin(sel_channels) &
    df_all["Payment"].isin(sel_payments)
].copy()

if df.empty:
    st.warning("⚠️ No data matches your filters. Please broaden your selection.")
    st.stop()

# ── Header ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 10])

with col1:
    st.image("d:/VS Code/projects/Oneplus_Sales/logo.png", width=50)

with col2:
    st.markdown(
        """
        <h2 style="
            font-family:Syne,sans-serif;
            font-weight:800;
            font-size:1.9rem;
            color:#eb0029;
            margin-bottom:0;">
            OnePlus India — Sales Dashboard
        </h2>
        """,
        unsafe_allow_html=True
    )
st.markdown("<br>", unsafe_allow_html=True)

# ── KPI cards ────────────────────────────────────────────────────────────────
total_txn = len(df)
total_qty = int(df["Quantity"].sum())
total_rev = df["Revenue"].sum()
avg_order = df["Revenue"].mean()
avg_rat   = df["Rating"].mean()

def kpi(icon, bg, label, value, delta=""):
    d = f"<div class='kpi-delta'>{delta}</div>" if delta else ""
    return (f'<div class="kpi-wrap">'
            f'<div class="kpi-icon" style="background:{bg}">{icon}</div>'
            f'<div><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>{d}</div></div>')

k1,k2,k3,k4,k5 = st.columns(5)
with k1: st.markdown(kpi("🛒","#fff1f2","Transactions", f"{total_txn:,}","All channels combined"), unsafe_allow_html=True)
with k2: st.markdown(kpi("📦","#f0fdf4","Units Sold",   f"{total_qty:,}","Across all models"),    unsafe_allow_html=True)
with k3: st.markdown(kpi("💰","#fffbeb","Total Revenue",f"₹{total_rev/1e7:.2f} Cr","Gross sales"), unsafe_allow_html=True)
with k4: st.markdown(kpi("📈","#f5f3ff","Avg Order",    f"₹{avg_order/1000:.1f}K","Per transaction"), unsafe_allow_html=True)
with k5: st.markdown(kpi("⭐","#fff7ed","Avg Rating",   f"{avg_rat:.2f} / 5","Customer score"),   unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Shared chart defaults ────────────────────────────────────────────────────
BASE = dict(
    paper_bgcolor="white", plot_bgcolor="white",
    margin=dict(l=8,r=8,t=8,b=8),
    font=dict(family="Inter",size=10,color="#6b7280"),
)
RED    = "#eb0029"
DARK   = "#374151"
COLORS = [RED,DARK,"#f59e0b","#10b981","#6366f1","#06b6d4"]

def card(title):
    st.markdown(f'<div class="chart-box"><div class="chart-title">{title}</div>', unsafe_allow_html=True)
def end_card():
    st.markdown("</div>", unsafe_allow_html=True)

# ── Row 1 : Line + Map ───────────────────────────────────────────────────────
r1a, r1b = st.columns([3,2], gap="medium")

with r1a:
    card("📅 Total Quantity Sold — by Day of Month")
    qty_day = df.groupby("Day")["Quantity"].sum().reset_index()
    fig = go.Figure(go.Scatter(
        x=qty_day["Day"], y=qty_day["Quantity"],
        mode="lines+markers",
        line=dict(color=RED,width=2.5),
        marker=dict(size=5,color=RED),
        fill="tozeroy", fillcolor="rgba(235,0,41,0.07)",
        hovertemplate="Day %{x}: %{y} units<extra></extra>",
    ))
    fig.update_layout(**BASE, height=210,
        xaxis=dict(title="Day of Month", gridcolor="#f3f4f6", dtick=5),
        yaxis=dict(title="Qty", gridcolor="#f3f4f6"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    end_card()

with r1b:
    card("🗺️ Total Sales by City — India Map")
    city_rev = df.groupby(["City","Lat","Lon"])["Revenue"].sum().reset_index()
    fig = px.scatter_mapbox(
        city_rev, lat="Lat", lon="Lon", size="Revenue",
        hover_name="City",
        hover_data={"Revenue":":,.0f","Lat":False,"Lon":False},
        color_discrete_sequence=[RED],
        size_max=32, zoom=4, height=225,
        mapbox_style="carto-positron",
    )
    fig.update_layout(margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    end_card()

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 2 : Model bar + Payment pie + Channel bar ────────────────────────────
r2a, r2b, r2c = st.columns([2,1.6,1.8], gap="medium")

with r2a:
    card("📱 Total Sales by OnePlus Model")
    model_rev = df.groupby("Model")["Revenue"].sum().sort_values().reset_index()
    fig = go.Figure(go.Bar(
        x=model_rev["Revenue"], y=model_rev["Model"],
        orientation="h",
        marker=dict(color=model_rev["Revenue"],
                    colorscale=[[0,"#fecdd3"],[1,RED]], showscale=False),
        text=model_rev["Revenue"].apply(lambda x: f"₹{x/1e6:.0f}M"),
        textposition="outside",
        hovertemplate="%{y}: ₹%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(**BASE, height=260,
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(gridcolor="#f3f4f6"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    end_card()

with r2b:
    card("💳 Count of Transactions by Payment Method")
    pay = df.groupby("Payment")["TransactionID"].count().reset_index()
    pay.columns = ["Payment","Count"]
    fig = go.Figure(go.Pie(
        labels=pay["Payment"], values=pay["Count"],
        hole=0.48,
        marker_colors=COLORS,
        textinfo="percent",
        textfont_size=9,
        hovertemplate="%{label}: %{value} txns (%{percent})<extra></extra>",
    ))
    fig.update_layout(**BASE, height=260, showlegend=True,
        legend=dict(orientation="v", font=dict(size=8), x=1.01, xanchor="left"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    end_card()

with r2c:
    card("🏪 Revenue by Sales Channel")
    ch = df.groupby("Channel")["Revenue"].sum().sort_values().reset_index()
    fig = go.Figure(go.Bar(
        x=ch["Revenue"], y=ch["Channel"],
        orientation="h",
        marker_color=DARK,
        text=ch["Revenue"].apply(lambda x: f"₹{x/1e6:.0f}M"),
        textposition="outside",
        hovertemplate="%{y}: ₹%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(**BASE, height=260,
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(gridcolor="#f3f4f6"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    end_card()

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 3 : Ratings + Day of week + Monthly trend ───────────────────────────
r3a, r3b, r3c = st.columns([1.4,2,2.2], gap="medium")

with r3a:
    card("⭐ Customer Ratings")
    rat = df.groupby("Rating")["TransactionID"].count().reset_index()
    rat.columns = ["Stars","Count"]
    rat["Label"] = rat["Stars"].apply(lambda x: f"{'★'*x}{'☆'*(5-x)}")
    fig = go.Figure(go.Bar(
        x=rat["Count"], y=rat["Label"],
        orientation="h",
        marker_color=["#fca5a5","#fdba74","#fcd34d","#86efac","#4ade80"],
        text=rat["Count"],
        textposition="outside",
    ))
    fig.update_layout(**BASE, height=240,
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(gridcolor="#f3f4f6"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    end_card()

with r3b:
    card("📆 Total Sales by Day Name")
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    day_rev = df.groupby("DayName")["Revenue"].sum().reindex(day_order).reset_index()
    fig = go.Figure(go.Bar(
        x=day_rev["DayName"], y=day_rev["Revenue"],
        marker=dict(color=day_rev["Revenue"],
                    colorscale=[[0,"#fecdd3"],[1,RED]], showscale=False),
        text=day_rev["Revenue"].apply(lambda x: f"₹{x/1e6:.0f}M"),
        textposition="outside",
        hovertemplate="%{x}: ₹%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(**BASE, height=240,
        xaxis=dict(tickfont=dict(size=9), gridcolor="#f3f4f6"),
        yaxis=dict(showgrid=False, showticklabels=False))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    end_card()

with r3c:
    card("📈 Monthly Revenue Trend · 2024–2025")
    monthly = df.groupby("YearMonth")["Revenue"].sum().reset_index().sort_values("YearMonth")
    fig = go.Figure(go.Scatter(
        x=monthly["YearMonth"], y=monthly["Revenue"],
        mode="lines+markers",
        line=dict(color=RED,width=2.5),
        marker=dict(size=6,color=RED,line=dict(width=1.5,color="white")),
        fill="tozeroy", fillcolor="rgba(235,0,41,0.07)",
        hovertemplate="%{x}: ₹%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(**BASE, height=240,
        xaxis=dict(tickangle=-40, tickfont=dict(size=8), gridcolor="#f3f4f6"),
        yaxis=dict(gridcolor="#f3f4f6", tickformat=".2s"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    end_card()

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer"> OnePlus India · Sales Dataset · Jan 2024 – Mar 2025 · '
    'Built with Streamlit & Plotly · Data Analyst Task</div>',
    unsafe_allow_html=True
)
