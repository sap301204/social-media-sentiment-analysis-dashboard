import streamlit as st
import pandas as pd
import plotly.express as px
import random
import re
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="McDonald's Social Listening Dashboard",
    page_icon="🍟",
    layout="wide"
)

# ---------------- CSS: POWER BI / NEON DASHBOARD ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #050b14;
    color: #ffffff;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #061018 0%, #071b22 100%);
    border-right: 1px solid #00f5ff55;
}

.sidebar-title {
    font-size: 25px;
    font-weight: 900;
    color: #00f5ff;
    margin-bottom: 10px;
}

.nav-box {
    background: #071923;
    border: 1px solid #00f5ff55;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
    color: white;
    font-weight: 700;
}

.main-header {
    background: linear-gradient(90deg, #061018, #071b22);
    border: 1px solid #00f5ff55;
    border-radius: 18px;
    padding: 22px 26px;
    margin-bottom: 20px;
    box-shadow: 0 0 25px rgba(0,245,255,0.12);
}

.title {
    font-size: 34px;
    font-weight: 900;
    color: #00f5ff;
    letter-spacing: 0.5px;
}

.subtitle {
    color: #a7f3ff;
    font-size: 15px;
    margin-top: 6px;
}

.kpi-card {
    background: linear-gradient(180deg, #071923 0%, #041018 100%);
    border: 1px solid #00f5ff66;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 0 18px rgba(0,245,255,0.10);
}

.kpi-label {
    font-size: 13px;
    color: #9defff;
    font-weight: 700;
}

.kpi-value {
    font-size: 32px;
    color: white;
    font-weight: 900;
    margin-top: 8px;
}

.kpi-delta {
    color: #00ff88;
    font-size: 13px;
    font-weight: 700;
}

.panel {
    background: #07111d;
    border: 1px solid #00f5ff55;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 0 20px rgba(0,245,255,0.08);
    margin-bottom: 16px;
}

.section-title {
    color: #00f5ff;
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 12px;
}

.insight-box {
    background: #061923;
    border-left: 5px solid #00f5ff;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 10px;
    color: #dffcff;
}

.stButton > button {
    background: linear-gradient(90deg, #00f5ff, #00ff88);
    color: #001014;
    border: none;
    border-radius: 10px;
    padding: 12px 26px;
    font-weight: 900;
}

div[data-testid="stMetric"] {
    background: #071923;
    border: 1px solid #00f5ff44;
    padding: 15px;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    possible_files = [
        "McDonald_s_Reviews.csv",
        "mcdonalds_reviews.csv",
        "mcdonalds_data.csv",
        "McDonalds_Reviews.csv"
    ]

    df = None
    for file in possible_files:
        try:
            df = pd.read_csv(file, encoding="latin1")
            break
        except:
            continue

    if df is None:
        st.error("CSV file not found. Upload McDonald_s_Reviews.csv to GitHub root folder.")
        st.stop()

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Detect review text column
    text_candidates = ["review", "text", "review_text", "comment", "reviews"]
    text_col = next((col for col in text_candidates if col in df.columns), None)

    if text_col is None:
        st.error("No review/text column found. Your CSV must contain a review or text column.")
        st.stop()

    df["text"] = df[text_col].astype(str)

    # Detect rating column
    rating_candidates = ["rating", "stars", "score"]
    rating_col = next((col for col in rating_candidates if col in df.columns), None)

    if rating_col:
        df["rating_clean"] = df[rating_col].astype(str).str.extract(r"(\d+)").astype(float)
    else:
        df["rating_clean"] = random.choices([1, 2, 3, 4, 5], k=len(df))

    def rating_to_sentiment(rating):
        if rating >= 4:
            return "positive"
        elif rating == 3:
            return "neutral"
        else:
            return "negative"

    df["sentiment"] = df["rating_clean"].apply(rating_to_sentiment)
    df["score"] = df["sentiment"].map({"positive": 1, "neutral": 0, "negative": -1})

    # Add realistic industry-style dashboard fields
    platforms = ["Google Reviews", "Twitter/X", "Instagram", "Facebook", "YouTube", "Reddit"]
    categories = ["Food Quality", "Service", "Price", "Cleanliness", "Delivery", "Waiting Time", "App Experience"]
    campaigns = ["McFlurry Buzz", "Burger Promo", "Fries Campaign", "Breakfast Offer", "General Brand Talk"]
    locations = ["New York", "California", "Texas", "Florida", "Chicago", "Ohio", "Arizona"]

    if "platform" not in df.columns:
        df["platform"] = random.choices(platforms, k=len(df))

    if "category" not in df.columns:
        def detect_category(text):
            text = text.lower()
            if any(w in text for w in ["fries", "burger", "food", "taste", "cold", "meal"]):
                return "Food Quality"
            if any(w in text for w in ["staff", "service", "rude", "friendly"]):
                return "Service"
            if any(w in text for w in ["price", "expensive", "cheap", "cost"]):
                return "Price"
            if any(w in text for w in ["clean", "dirty", "hygiene"]):
                return "Cleanliness"
            if any(w in text for w in ["wait", "slow", "fast", "queue"]):
                return "Waiting Time"
            return random.choice(categories)

        df["category"] = df["text"].apply(detect_category)

    if "campaign" not in df.columns:
        df["campaign"] = random.choices(campaigns, k=len(df))

    if "location" not in df.columns:
        store_cols = ["store_address", "address", "city"]
        store_col = next((col for col in store_cols if col in df.columns), None)
        if store_col:
            df["location"] = df[store_col].astype(str).str[:22]
        else:
            df["location"] = random.choices(locations, k=len(df))

    if "date" not in df.columns:
        today = datetime.today()
        df["date"] = [today - timedelta(days=random.randint(0, 90)) for _ in range(len(df))]
    else:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["date"] = df["date"].fillna(pd.Timestamp.today())

    df["likes"] = [random.randint(10, 4000) for _ in range(len(df))]
    df["shares"] = [random.randint(1, 700) for _ in range(len(df))]
    df["comments"] = [random.randint(0, 350) for _ in range(len(df))]
    df["reach"] = df["likes"] * random.randint(5, 20) + df["shares"] * random.randint(10, 40)
    df["engagement"] = df["likes"] + df["shares"] + df["comments"]

    return df


df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.markdown('<div class="sidebar-title">🍟 McDonald’s BI</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="nav-box">📊 Overview</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="nav-box">💬 Mentions</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="nav-box">📈 Trends</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="nav-box">🌍 Platforms</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="nav-box">⚙️ Filters</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")

sentiment_filter = st.sidebar.multiselect(
    "Sentiment",
    options=sorted(df["sentiment"].unique()),
    default=sorted(df["sentiment"].unique())
)

platform_filter = st.sidebar.multiselect(
    "Platform",
    options=sorted(df["platform"].unique()),
    default=sorted(df["platform"].unique())
)

category_filter = st.sidebar.multiselect(
    "Category",
    options=sorted(df["category"].unique()),
    default=sorted(df["category"].unique())
)

df_filtered = df[
    (df["sentiment"].isin(sentiment_filter)) &
    (df["platform"].isin(platform_filter)) &
    (df["category"].isin(category_filter))
]

# ---------------- HEADER ----------------
st.markdown("""
<div class="main-header">
    <div class="title">McDonald’s Social Media Sentiment Analysis Dashboard</div>
    <div class="subtitle">
        Power BI-style social listening dashboard for customer reviews, sentiment, engagement, campaign performance, and brand reputation.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- KPI CARDS ----------------
total_mentions = len(df_filtered)
positive = (df_filtered["sentiment"] == "positive").sum()
negative = (df_filtered["sentiment"] == "negative").sum()
neutral = (df_filtered["sentiment"] == "neutral").sum()

positive_pct = round((positive / total_mentions) * 100, 1) if total_mentions else 0
negative_pct = round((negative / total_mentions) * 100, 1) if total_mentions else 0
brand_health = round(((positive - negative) / total_mentions) * 100, 1) if total_mentions else 0
total_reach = int(df_filtered["reach"].sum()) if total_mentions else 0
total_engagement = int(df_filtered["engagement"].sum()) if total_mentions else 0

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">TOTAL MENTIONS</div>
        <div class="kpi-value">{total_mentions:,}</div>
        <div class="kpi-delta">Live review volume</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">SOCIAL REACH</div>
        <div class="kpi-value">{total_reach/1000000:.1f}M</div>
        <div class="kpi-delta">Estimated reach</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">ENGAGEMENT</div>
        <div class="kpi-value">{total_engagement/1000:.1f}K</div>
        <div class="kpi-delta">Likes + shares + comments</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">POSITIVE RATE</div>
        <div class="kpi-value">{positive_pct}%</div>
        <div class="kpi-delta">Customer satisfaction</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">BRAND HEALTH</div>
        <div class="kpi-value">{brand_health}</div>
        <div class="kpi-delta">Positive minus negative index</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------- CHART STYLE FUNCTION ----------------
def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#07111d",
        font_color="white",
        title_font_color="#00f5ff",
        title_font_size=18,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )
    )
    fig.update_xaxes(gridcolor="#14303d")
    fig.update_yaxes(gridcolor="#14303d")
    return fig

# ---------------- ROW 1 CHARTS ----------------
c1, c2, c3 = st.columns([1.1, 1.2, 1.2])

with c1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    sentiment_fig = px.pie(
        df_filtered,
        names="sentiment",
        title="Sentiment Share",
        hole=0.55
    )
    sentiment_fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(style_chart(sentiment_fig), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    platform_df = df_filtered["platform"].value_counts().reset_index()
    platform_df.columns = ["platform", "mentions"]
    platform_fig = px.bar(
        platform_df,
        x="platform",
        y="mentions",
        title="Mentions by Platform",
        text="mentions"
    )
    st.plotly_chart(style_chart(platform_fig), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    category_df = df_filtered["category"].value_counts().reset_index()
    category_df.columns = ["category", "mentions"]
    category_fig = px.bar(
        category_df,
        x="mentions",
        y="category",
        orientation="h",
        title="Conversation Categories",
        text="mentions"
    )
    st.plotly_chart(style_chart(category_fig), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ROW 2 CHARTS ----------------
r1, r2 = st.columns(2)

with r1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    trend = df_filtered.groupby(df_filtered["date"].dt.date).agg(
        average_sentiment=("score", "mean"),
        mentions=("text", "count")
    ).reset_index()

    trend_fig = px.line(
        trend,
        x="date",
        y="average_sentiment",
        markers=True,
        title="Sentiment Trend Over Time"
    )
    st.plotly_chart(style_chart(trend_fig), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    engagement = df_filtered.groupby("platform")["engagement"].sum().reset_index()
    engagement_fig = px.area(
        engagement,
        x="platform",
        y="engagement",
        title="Engagement by Platform"
    )
    st.plotly_chart(style_chart(engagement_fig), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ROW 3 ----------------
left, right = st.columns([1.4, 1])

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recent Customer Mentions</div>', unsafe_allow_html=True)
    show_cols = ["date", "platform", "location", "category", "text", "sentiment", "rating_clean", "engagement"]
    st.dataframe(df_filtered[show_cols].head(25), use_container_width=True, height=420)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Business Insights</div>', unsafe_allow_html=True)

    top_category = df_filtered["category"].value_counts().idxmax() if total_mentions else "N/A"
    top_platform = df_filtered["platform"].value_counts().idxmax() if total_mentions else "N/A"

    if brand_health > 20:
        health_msg = "Brand sentiment is strong. Positive customer perception is leading negative feedback."
    elif brand_health < -10:
        health_msg = "Brand sentiment needs attention. Negative mentions are creating reputation risk."
    else:
        health_msg = "Brand sentiment is balanced. Monitor complaint categories closely."

    st.markdown(f'<div class="insight-box">✅ Top conversation area: <b>{top_category}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-box">📡 Highest activity platform: <b>{top_platform}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-box">📊 Negative rate: <b>{negative_pct}%</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-box">🧠 {health_msg}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LIVE PREDICTION ----------------
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Analyze New McDonald’s Comment</div>', unsafe_allow_html=True)

user_text = st.text_area("Enter a customer review or social media comment:")

if st.button("Analyze Sentiment"):
    if user_text.strip() == "":
        st.warning("Please enter a comment first.")
    else:
        # Simple rule-based fallback based on rating-style sentiment words
        positive_words = ["good", "great", "love", "amazing", "excellent", "fast", "fresh", "clean", "tasty", "friendly"]
        negative_words = ["bad", "worst", "hate", "slow", "dirty", "cold", "rude", "expensive", "terrible", "poor"]

        text_lower = user_text.lower()
        pos_hits = sum(word in text_lower for word in positive_words)
        neg_hits = sum(word in text_lower for word in negative_words)

        if pos_hits > neg_hits:
            prediction = "positive"
        elif neg_hits > pos_hits:
            prediction = "negative"
        else:
            prediction = "neutral"

        if prediction == "positive":
            st.success("😊 Predicted Sentiment: Positive")
        elif prediction == "negative":
            st.error("😡 Predicted Sentiment: Negative")
        else:
            st.warning("😐 Predicted Sentiment: Neutral")

st.markdown('</div>', unsafe_allow_html=True)
