import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta

st.set_page_config(
    page_title="McDonald's Dashboard",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at top left, #06222d 0%, #020812 45%, #010409 100%);
    color: #ffffff;
}

/* =======================
   SIDEBAR
======================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #03131a 0%, #02070d 100%);
    border-right: 1px solid #00eaff33;
}

.brand-block {
    padding: 12px 8px 22px 8px;
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 12px;
}

.burger-icon {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    background: linear-gradient(135deg, #00f5ff, #00ff88);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
    box-shadow: 0 0 22px rgba(0,245,255,0.28);
}

.brand-title {
    color: #00f5ff;
    font-size: 25px;
    font-weight: 900;
    letter-spacing: 0.2px;
    line-height: 1.1;
}

.brand-subtitle {
    color: #8ff6ff;
    font-size: 13px;
    font-weight: 600;
    margin-top: 8px;
    margin-left: 54px;
}

.brand-line {
    height: 1px;
    background: linear-gradient(90deg, #00eaff66, transparent);
    margin-top: 22px;
    margin-bottom: 16px;
}

/* NAVIGATION */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 13px;
    margin-top: 6px;
    margin-bottom: 8px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: #071923 !important;
    border: 1px solid #00eaff55 !important;
    border-radius: 18px !important;
    padding: 14px 16px !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
    margin: 0 !important;
    box-shadow: 0 0 16px rgba(0,245,255,0.04);
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #0a2230 !important;
    transform: translateX(3px);
    box-shadow: 0 0 18px rgba(0,245,255,0.10);
}

section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color: #ffffff !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    margin: 0 !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(90deg, #0a2230, #071923) !important;
    border-left: 5px solid #00f5ff !important;
    border-top: 1px solid #00f5ff !important;
    border-right: 1px solid #00f5ff !important;
    border-bottom: 1px solid #00f5ff !important;
    box-shadow: 0 0 18px rgba(0,245,255,0.14);
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
    color: #00f5ff !important;
}

/* FILTERS */
.sidebar-subhead {
    color: white;
    font-size: 22px;
    font-weight: 900;
    margin-top: 4px;
    margin-bottom: 14px;
}

section[data-testid="stSidebar"] .stMultiSelect label {
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 15px !important;
}

section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div {
    background: #08111c !important;
    border: 1px solid #00eaff33 !important;
    border-radius: 16px !important;
    min-height: 52px !important;
}

/* selected filter chips */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: linear-gradient(90deg, #00f5ff, #00ff88) !important;
    color: #001014 !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
}

section[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: #001014 !important;
    font-weight: 800 !important;
}

section[data-testid="stSidebar"] [data-baseweb="tag"] svg {
    color: #001014 !important;
}

/* dropdown text */
section[data-testid="stSidebar"] .stMultiSelect span {
    color: white !important;
}

/* apply button */
section[data-testid="stSidebar"] .stButton > button,
section[data-testid="stSidebar"] .stFormSubmitButton > button {
    width: 100%;
    background: linear-gradient(90deg, #00f5ff, #00ff88);
    color: #001014;
    border-radius: 14px;
    font-weight: 900;
    font-size: 16px;
    border: none;
    padding: 13px 18px;
    margin-top: 12px;
}

section[data-testid="stSidebar"] .stButton > button:hover,
section[data-testid="stSidebar"] .stFormSubmitButton > button:hover {
    box-shadow: 0 0 25px rgba(0,245,255,0.30);
    transform: translateY(-1px);
}

/* MAIN CONTENT */
.main-card {
    background: linear-gradient(135deg, #061923, #030b12);
    border: 1px solid #00eaff55;
    border-radius: 22px;
    padding: 26px;
    margin-bottom: 24px;
    box-shadow: 0 0 28px rgba(0,245,255,0.10);
}

.title {
    font-size: 36px;
    font-weight: 900;
    color: #00f5ff;
}

.subtitle {
    font-size: 15px;
    color: #b8f7ff;
    margin-top: 8px;
}

.kpi {
    background: linear-gradient(180deg, #071923, #020b10);
    border: 1px solid #00eaff66;
    border-radius: 18px;
    padding: 20px;
    min-height: 135px;
    box-shadow: 0 0 22px rgba(0,245,255,0.08);
}

.kpi-label {
    color: #8ff6ff;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
}

.kpi-value {
    color: white;
    font-size: 32px;
    font-weight: 900;
    margin-top: 10px;
}

.kpi-note {
    color: #00ff88;
    font-size: 13px;
    font-weight: 700;
    margin-top: 8px;
}

.panel {
    background: #06111d;
    border: 1px solid #00eaff44;
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 22px;
    box-shadow: 0 0 24px rgba(0,245,255,0.08);
}

.section-title {
    font-size: 24px;
    font-weight: 900;
    color: #00f5ff;
    margin-bottom: 16px;
}

.mention-card {
    background: linear-gradient(90deg, #071923, #041018);
    border-left: 5px solid #00f5ff;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
}

.mention-text {
    font-size: 15px;
    color: white;
    font-weight: 600;
}

.mention-meta {
    font-size: 12px;
    color: #a7f3ff;
    margin-top: 8px;
}

.insight {
    background: #061e29;
    border-left: 5px solid #00ffcc;
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 14px;
    color: white;
    font-weight: 650;
}

.analyzer-box {
    background: linear-gradient(135deg, #081b24, #030b12);
    border: 1px solid #00eaff66;
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 0 35px rgba(0,245,255,0.12);
}

.stButton > button {
    background: linear-gradient(90deg, #00f5ff, #00ff88);
    color: #001014;
    border: none;
    border-radius: 14px;
    padding: 14px 34px;
    font-weight: 900;
    font-size: 16px;
}

textarea {
    border-radius: 18px !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
# DATA LOADER
# =========================
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
        except Exception:
            continue

    if df is None:
        st.error("CSV file not found. Upload your McDonald's reviews CSV in the project folder.")
        st.stop()

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    text_candidates = ["review", "text", "review_text", "comment", "reviews"]
    text_col = next((col for col in text_candidates if col in df.columns), None)

    if text_col is None:
        st.error("No review/text column found in dataset.")
        st.stop()

    df["text"] = df[text_col].astype(str)

    rating_candidates = ["rating", "stars", "score"]
    rating_col = next((col for col in rating_candidates if col in df.columns), None)

    if rating_col:
        df["rating_clean"] = df[rating_col].astype(str).str.extract(r"(\d+)").astype(float)
        df["rating_clean"] = df["rating_clean"].fillna(3)
    else:
        df["rating_clean"] = random.choices([1, 2, 3, 4, 5], k=len(df))

    def rating_to_sentiment(r):
        if r >= 4:
            return "positive"
        elif r == 3:
            return "neutral"
        return "negative"

    df["sentiment"] = df["rating_clean"].apply(rating_to_sentiment)
    df["score"] = df["sentiment"].map({"positive": 1, "neutral": 0, "negative": -1})

    platforms = ["Google Reviews", "Twitter/X", "Instagram", "Facebook", "YouTube", "Reddit"]
    campaigns = ["McFlurry Buzz", "Burger Promo", "Fries Campaign", "Breakfast Offer", "General Brand Talk"]

    df["platform"] = random.choices(platforms, k=len(df))
    df["campaign"] = random.choices(campaigns, k=len(df))

    def detect_category(text):
        text = text.lower()
        if any(w in text for w in ["burger", "fries", "food", "meal", "taste", "cold"]):
            return "Food Quality"
        if any(w in text for w in ["staff", "service", "rude", "friendly"]):
            return "Service"
        if any(w in text for w in ["price", "expensive", "cheap", "cost"]):
            return "Price"
        if any(w in text for w in ["clean", "dirty", "hygiene"]):
            return "Cleanliness"
        if any(w in text for w in ["wait", "slow", "fast", "queue"]):
            return "Waiting Time"
        return random.choice(["Food Quality", "Service", "Price", "Cleanliness", "Waiting Time"])

    df["category"] = df["text"].apply(detect_category)

    if "store_address" in df.columns:
        df["location"] = df["store_address"].astype(str).str[:24]
    elif "address" in df.columns:
        df["location"] = df["address"].astype(str).str[:24]
    else:
        df["location"] = random.choices(["New York", "California", "Texas", "Florida", "Chicago"], k=len(df))

    today = datetime.today()
    df["date"] = [today - timedelta(days=random.randint(0, 90)) for _ in range(len(df))]

    df["likes"] = [random.randint(20, 5000) for _ in range(len(df))]
    df["shares"] = [random.randint(1, 900) for _ in range(len(df))]
    df["comments_count"] = [random.randint(0, 500) for _ in range(len(df))]
    df["reach"] = df["likes"] * 12 + df["shares"] * 35
    df["engagement"] = df["likes"] + df["shares"] + df["comments_count"]

    return df


df = load_data()


# =========================
# SIDEBAR BRAND
# =========================
st.sidebar.markdown("""
<div class="brand-block">
    <div class="brand-row">
        <div class="burger-icon">🍔</div>
        <div class="brand-title">McDonald’s Pulse</div>
    </div>
    <div class="brand-subtitle">Product Intelligence Dashboard</div>
    <div class="brand-line"></div>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR NAVIGATION
# =========================
page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Mentions",
        "Trends",
        "Platforms",
        "Analyzer"
    ],
    label_visibility="collapsed"
)

# =========================
# SIDEBAR FILTERS WITH APPLY BUTTON
# =========================
st.sidebar.markdown('<div class="sidebar-subhead">Filters</div>', unsafe_allow_html=True)

if "sentiment_filter" not in st.session_state:
    st.session_state.sentiment_filter = sorted(df["sentiment"].unique())

if "platform_filter" not in st.session_state:
    st.session_state.platform_filter = sorted(df["platform"].unique())

if "category_filter" not in st.session_state:
    st.session_state.category_filter = sorted(df["category"].unique())

with st.sidebar.form("filter_form"):
    temp_sentiment = st.multiselect(
        "Sentiment",
        sorted(df["sentiment"].unique()),
        default=st.session_state.sentiment_filter
    )

    temp_platform = st.multiselect(
        "Platform",
        sorted(df["platform"].unique()),
        default=st.session_state.platform_filter
    )

    temp_category = st.multiselect(
        "Category",
        sorted(df["category"].unique()),
        default=st.session_state.category_filter
    )

    apply_filter = st.form_submit_button("Apply filter")

if apply_filter:
    st.session_state.sentiment_filter = temp_sentiment
    st.session_state.platform_filter = temp_platform
    st.session_state.category_filter = temp_category

df_filtered = df[
    (df["sentiment"].isin(st.session_state.sentiment_filter)) &
    (df["platform"].isin(st.session_state.platform_filter)) &
    (df["category"].isin(st.session_state.category_filter))
]


# =========================
# HELPERS
# =========================
def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#07111d",
        font_color="white",
        title_font_color="#00f5ff",
        title_font_size=20,
        margin=dict(l=20, r=20, t=55, b=25),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="white")),
    )
    fig.update_xaxes(gridcolor="#12313d", zerolinecolor="#12313d")
    fig.update_yaxes(gridcolor="#12313d", zerolinecolor="#12313d")
    return fig


def render_kpis(data):
    total = len(data)
    positive = (data["sentiment"] == "positive").sum()
    negative = (data["sentiment"] == "negative").sum()
    positive_pct = round((positive / total) * 100, 1) if total else 0
    brand_health = round(((positive - negative) / total) * 100, 1) if total else 0
    reach = int(data["reach"].sum()) if total else 0
    engagement = int(data["engagement"].sum()) if total else 0

    cols = st.columns(5)
    kpis = [
        ("TOTAL MENTIONS", f"{total:,}", "Live review volume"),
        ("SOCIAL REACH", f"{reach/1_000_000:.1f}M", "Estimated brand reach"),
        ("ENGAGEMENT", f"{engagement/1000:.1f}K", "Likes + shares + comments"),
        ("POSITIVE RATE", f"{positive_pct}%", "Customer satisfaction"),
        ("BRAND HEALTH", f"{brand_health}", "Positive minus negative")
    ]

    for col, item in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-label">{item[0]}</div>
                <div class="kpi-value">{item[1]}</div>
                <div class="kpi-note">{item[2]}</div>
            </div>
            """, unsafe_allow_html=True)


# =========================
# HEADER
# =========================
st.markdown("""
<div class="main-card">
    <div class="title">McDonald’s Social Media Sentiment Intelligence</div>
    <div class="subtitle">
        Premium analytics for customer sentiment, platform activity, engagement tracking, and brand health.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# PAGES
# =========================
if page == "Overview":
    render_kpis(df_filtered)
    st.write("")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        fig = px.pie(
            df_filtered,
            names="sentiment",
            title="Sentiment Share",
            hole=0.65,
            color="sentiment",
            color_discrete_map={
                "positive": "#00ff88",
                "neutral": "#00f5ff",
                "negative": "#ff3b5c"
            }
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        cat = df_filtered.groupby(["category", "sentiment"]).size().reset_index(name="mentions")
        fig = px.bar(
            cat,
            x="category",
            y="mentions",
            color="sentiment",
            title="Category-wise Sentiment",
            barmode="group",
            color_discrete_map={
                "positive": "#00ff88",
                "neutral": "#00f5ff",
                "negative": "#ff3b5c"
            }
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Mentions":
    st.markdown('<div class="section-title">Recent Customer Mentions</div>', unsafe_allow_html=True)

    top_mentions = df_filtered.sort_values("date", ascending=False).head(18)

    for _, row in top_mentions.iterrows():
        sentiment_color = {
            "positive": "#00ff88",
            "neutral": "#00f5ff",
            "negative": "#ff3b5c"
        }.get(row["sentiment"], "#00f5ff")

        st.markdown(f"""
        <div class="mention-card" style="border-left-color:{sentiment_color};">
            <div class="mention-text">“{str(row['text'])[:240]}”</div>
            <div class="mention-meta">
                {row['date'].strftime('%d %b %Y')} • {row['platform']} • {row['category']} • {row['location']} • Sentiment: <b>{row['sentiment']}</b> • Engagement: {row['engagement']:,}
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "Trends":
    trend = df_filtered.groupby(df_filtered["date"].dt.date).agg(
        average_sentiment=("score", "mean"),
        engagement=("engagement", "sum")
    ).reset_index()

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        fig = px.line(
            trend,
            x="date",
            y="average_sentiment",
            title="Sentiment Trend Over Time",
            markers=True
        )
        fig.update_traces(line_color="#00ff88", line_width=3)
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        fig = px.area(
            trend,
            x="date",
            y="engagement",
            title="Engagement Trend",
            markers=True
        )
        fig.update_traces(line_color="#00f5ff", fillcolor="rgba(0,245,255,0.22)")
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Platforms":
    platform_data = df_filtered.groupby("platform").agg(
        mentions=("text", "count"),
        engagement=("engagement", "sum"),
        reach=("reach", "sum")
    ).reset_index()

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        fig = px.bar(
            platform_data,
            x="platform",
            y="mentions",
            title="Mentions by Platform",
            text="mentions"
        )
        fig.update_traces(marker_color="#00f5ff")
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        fig = px.scatter(
            platform_data,
            x="reach",
            y="engagement",
            size="mentions",
            color="platform",
            title="Reach vs Engagement",
            size_max=55
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Analyzer":
    left, right = st.columns([1.2, 1])

    with left:
        st.markdown('<div class="analyzer-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Analyze New McDonald’s Comment</div>', unsafe_allow_html=True)

        user_text = st.text_area(
            "Enter a customer review, tweet, or social media comment:",
            height=170,
            placeholder="Example: The fries were fresh but the service was slow..."
        )

        if st.button("Analyze Sentiment"):
            if user_text.strip() == "":
                st.warning("Please enter a comment first.")
            else:
                text = user_text.lower()
                positive_words = ["good", "great", "love", "amazing", "excellent", "fast", "fresh", "clean", "tasty", "friendly", "best"]
                negative_words = ["bad", "worst", "hate", "slow", "dirty", "cold", "rude", "expensive", "terrible", "poor", "late"]

                pos_hits = sum(w in text for w in positive_words)
                neg_hits = sum(w in text for w in negative_words)

                if pos_hits > neg_hits:
                    st.success("Positive sentiment detected")
                elif neg_hits > pos_hits:
                    st.error("Negative sentiment detected")
                else:
                    st.warning("Neutral sentiment detected")

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        total = len(df_filtered)
        negative = (df_filtered["sentiment"] == "negative").sum()
        top_category = df_filtered["category"].value_counts().idxmax() if total else "N/A"
        top_platform = df_filtered["platform"].value_counts().idxmax() if total else "N/A"
        neg_rate = round((negative / total) * 100, 1) if total else 0

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">AI Business Insights</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight">Top issue/category: <b>{top_category}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight">Most active platform: <b>{top_platform}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight">Negative feedback rate: <b>{neg_rate}%</b></div>', unsafe_allow_html=True)
        st.markdown('<div class="insight">Recommended action: monitor service speed, pricing issues, and food quality complaints.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
