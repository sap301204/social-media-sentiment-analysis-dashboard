# 🍔 McDonald’s Social Media Sentiment Intelligence Dashboard

A premium Power BI-style social media sentiment analysis dashboard built using Python, Streamlit, Plotly, and NLP-based sentiment analytics.

This project analyzes McDonald’s customer reviews and social media-style feedback to identify positive, negative, and neutral sentiment, track brand health, monitor platform activity, and generate business insights.

---

## Project Overview

Social media platforms and review websites contain thousands of customer opinions about brands. Manually analyzing these reviews is time-consuming and inefficient.

This project solves that problem by creating an interactive dashboard that helps analyze customer feedback for McDonald’s using sentiment analysis and business intelligence visualizations.

The dashboard is designed to simulate how real companies monitor:

- Customer satisfaction
- Brand reputation
- Negative feedback
- Product/service complaints
- Platform-wise engagement
- Category-wise customer issues
- Social media trends

---

## Objective

The main objective of this project is to build an industry-oriented sentiment intelligence dashboard that can classify and visualize customer opinions as:

- Positive
- Negative
- Neutral

The project also converts customer reviews into business-level insights using interactive charts and KPI cards.

---

## Key Features

- McDonald’s brand-focused sentiment dashboard
- Power BI-style sidebar navigation
- Customer sentiment classification
- Brand health score
- Total mentions tracking
- Social reach and engagement metrics
- Category-wise sentiment analysis
- Platform-wise engagement analysis
- Sentiment trend over time
- Recent customer mentions section
- New comment sentiment analyzer
- Interactive filters for sentiment, platform, and category
- Premium dark dashboard UI

---

## Dashboard Sections

### Overview
Displays key business KPIs such as total mentions, social reach, engagement, positive rate, and brand health.

### Mentions
Shows recent customer reviews and social media-style feedback with sentiment, platform, category, location, and engagement.

### Trends
Displays sentiment trend and engagement trend over time.

### Platforms
Shows platform-wise mentions, reach, and engagement performance.

### Analyzer
Allows users to enter a new McDonald’s-related comment and predict whether the sentiment is positive, negative, or neutral.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data cleaning and processing |
| Plotly | Interactive data visualizations |
| Streamlit | Dashboard development |
| NLP | Text-based sentiment understanding |
| Kaggle Dataset | Customer review data |
| GitHub | Project hosting and proof of work |
| Streamlit Cloud | Dashboard deployment |

---

## Dataset

The project uses the **McDonald’s Store Reviews dataset from Kaggle**.

The dataset contains customer reviews related to McDonald’s stores. These reviews are used to analyze customer sentiment and generate business insights.

Dataset used:

 text

The dashboard also creates additional simulated industry-style fields such as:

Platform
Category
Campaign
Location
Likes
Shares
Comments
Reach
Engagement

These fields help make the dashboard more realistic and similar to real-world social media analytics tools.

Sentiment Logic

Customer ratings are converted into sentiment labels:

Rating	Sentiment
4–5 stars	Positive
3 stars	Neutral
1–2 stars	Negative

For the live comment analyzer, rule-based NLP keywords are used to classify new text input.

Project Workflow
Customer Reviews
        ↓
Data Cleaning
        ↓
Rating-to-Sentiment Conversion
        ↓
Feature Engineering
        ↓
Business Metrics Calculation
        ↓
Interactive Dashboard
        ↓
Insights and Sentiment Analysis
Folder Structure
social-media-sentiment-analysis-dashboard/
│
├── app.py
├── McDonald_s_Reviews.csv
├── sentiment_analysis.ipynb
├── requirements.txt
├── README.md
├── model.pkl
├── vectorizer.pkl
└── images/

McDonald_s_Reviews.csv
