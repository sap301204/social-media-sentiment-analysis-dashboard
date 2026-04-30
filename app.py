import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="McDonald's Sentiment Dashboard",
    page_icon="🍔",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("mcdonalds_data.csv")
df["date"] = pd.to_datetime(df["date"])

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
    color: white;
}

.main-title {
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(90deg, #facc15, #ef4444);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #cbd5e1;
    font-size: 18px;
    margin-bottom: 25px;
}

.card {
    background: rgba(255,255,255,0.07);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}

.stButton > button {
    background: linear-gradient(90deg, #facc15, #ef4444);
    color: black;
    font-weight: 800;
    border-radius: 12px;
    padding: 12px 30px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">🍔 McDonald’s Sentiment Intelligence Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Track customer emotions, brand reputation, and social media feedback using NLP + Machine Learning.</div>',
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("Dashboard Filters")

sentiment_filter = st.sidebar.multiselect(
    "Select Sentiment",
    options=df["sentiment"].unique(),
    default=df["sentiment"].unique()
)

df_filtered = df[df["sentiment"].isin(sentiment_filter)]

# ---------------- KPI CARDS ----------------
total_mentions = len(df_filtered)
positive_mentions = (df_filtered["sentiment"] == "positive").sum()
negative_mentions = (df_filtered["sentiment"] == "negative").sum()
neutral_mentions = (df_filtered["sentiment"] == "neutral").sum()

positive_rate = round((positive_mentions / total_mentions) * 100, 2) if total_mentions else 0
negative_rate = round((negative_mentions / total_mentions) * 100, 2) if total_mentions else 0

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Mentions", total_mentions)
k2.metric("Positive Mentions", positive_mentions, f"{positive_rate}%")
k3.metric("Negative Mentions", negative_mentions, f"{negative_rate}%")
k4.metric("Neutral Mentions", neutral_mentions)

st.write("")

# ---------------- CHARTS ROW 1 ----------------
col1, col2 = st.columns(2)

with col1:
    pie = px.pie(
        df_filtered,
        names="sentiment",
        title="Positive vs Negative vs Neutral",
        hole=0.45
    )
    pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    st.plotly_chart(pie, use_container_width=True)

with col2:
    sentiment_count = df_filtered["sentiment"].value_counts().reset_index()
    sentiment_count.columns = ["sentiment", "count"]

    bar = px.bar(
        sentiment_count,
        x="sentiment",
        y="count",
        title="Sentiment Mentions Count",
        text="count"
    )
    bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    st.plotly_chart(bar, use_container_width=True)

# ---------------- TREND CHART ----------------
trend = df_filtered.groupby(df_filtered["date"].dt.date)["score"].mean().reset_index()
trend.columns = ["date", "average_sentiment_score"]

line = px.line(
    trend,
    x="date",
    y="average_sentiment_score",
    markers=True,
    title="Sentiment Trend Over Time"
)
line.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)
st.plotly_chart(line, use_container_width=True)

# ---------------- DATA TABLE ----------------
st.subheader("📋 Recent McDonald’s Mentions")
st.dataframe(df_filtered.head(25), use_container_width=True)

# ---------------- LIVE PREDICTION ----------------
st.subheader("🔍 Analyze New McDonald’s Comment")

user_text = st.text_area("Enter a customer comment, tweet, or review:")

if st.button("Analyze Sentiment"):
    if user_text.strip() == "":
        st.warning("Please enter a comment first.")
    else:
        vec = vectorizer.transform([user_text])
        prediction = model.predict(vec)[0]

        if prediction == "positive":
            st.success("😊 Predicted Sentiment: Positive")
        elif prediction == "negative":
            st.error("😡 Predicted Sentiment: Negative")
        else:
            st.warning("😐 Predicted Sentiment: Neutral")
