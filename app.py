import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

# Load model
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.title("Social Media Sentiment Analysis Dashboard")

option = st.radio("Select Input Type", ["Single Text", "CSV Upload"])

# ---- Single Text ----
if option == "Single Text":
    text = st.text_area("Enter text")

    if st.button("Analyze"):
        vec = vectorizer.transform([text])
        prediction = model.predict(vec)[0]
        st.success(f"Prediction: {prediction}")

# ---- CSV Upload ----
else:
    file = st.file_uploader("Upload CSV with 'text' column")

    if file:
        df = pd.read_csv(file)
        df['Prediction'] = model.predict(vectorizer.transform(df['text']))

        st.write(df.head())

        fig = px.pie(df, names='Prediction', title='Sentiment Distribution')
        st.plotly_chart(fig)
