import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.set_page_config(
    page_title="Social Media Sentiment Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #020617 100%);
    color: white;
}

.main-title {
    font-size: 52px;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}

.sub-title {
    font-size: 18px;
    color: #cbd5e1;
    margin-bottom: 35px;
}

.card {
    background: rgba(255, 255, 255, 0.08);
    padding: 25px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 12px 35px rgba(0,0,0,0.35);
}

.result-box {
    padding: 25px;
    border-radius: 18px;
    font-size: 28px;
    font-weight: 800;
    text-align: center;
    margin-top: 20px;
}

.positive {
    background: linear-gradient(135deg, #16a34a, #22c55e);
}

.negative {
    background: linear-gradient(135deg, #dc2626, #f97316);
}

.neutral {
    background: linear-gradient(135deg, #475569, #64748b);
}

.stButton > button {
    background: linear-gradient(90deg, #38bdf8, #a78bfa);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 28px;
    font-weight: 700;
}

textarea {
    border-radius: 15px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Social Media Sentiment Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Analyze social media comments, tweets, and reviews using NLP + Machine Learning.</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card"><h3>📌 NLP Pipeline</h3><p>Text cleaning, TF-IDF vectorization, and sentiment classification.</p></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><h3>🤖 ML Model</h3><p>Logistic Regression model trained for positive, negative, and neutral sentiment.</p></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card"><h3>📊 Business Insight</h3><p>Helps brands understand customer emotions and feedback quickly.</p></div>', unsafe_allow_html=True)

st.write("")
st.write("")

option = st.radio("Choose Input Type", ["Single Text", "CSV Upload"], horizontal=True)

if option == "Single Text":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    text = st.text_area("Enter a social media comment, tweet, or review:")

    if st.button("Analyze Sentiment"):
        if text.strip() == "":
            st.warning("Please enter some text first.")
        else:
            vec = vectorizer.transform([text])
            prediction = model.predict(vec)[0]

            if prediction == "positive":
                st.markdown(f'<div class="result-box positive">😊 Positive Sentiment</div>', unsafe_allow_html=True)
            elif prediction == "negative":
                st.markdown(f'<div class="result-box negative">😡 Negative Sentiment</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="result-box neutral">😐 Neutral Sentiment</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    uploaded_file = st.file_uploader("Upload CSV file with a column named `text`")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if "text" not in df.columns:
            st.error("CSV must contain a column named `text`.")
        else:
            df["Prediction"] = model.predict(vectorizer.transform(df["text"]))

            total = len(df)
            positive = (df["Prediction"] == "positive").sum()
            negative = (df["Prediction"] == "negative").sum()
            neutral = (df["Prediction"] == "neutral").sum()

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Comments", total)
            c2.metric("Positive", positive)
            c3.metric("Negative", negative)
            c4.metric("Neutral", neutral)

            st.write("")
            st.dataframe(df, use_container_width=True)

            fig = px.pie(
                df,
                names="Prediction",
                title="Sentiment Distribution",
                hole=0.45
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )
            st.plotly_chart(fig, use_container_width=True)

            bar = px.bar(
                df["Prediction"].value_counts().reset_index(),
                x="Prediction",
                y="count",
                title="Sentiment Count"
            )
            bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )
            st.plotly_chart(bar, use_container_width=True)
