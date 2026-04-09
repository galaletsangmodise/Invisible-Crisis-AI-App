import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import plotly.express as px
from datetime import datetime
import random
from faker import Faker
import requests
import os
from dotenv import load_dotenv

load_dotenv()

if 'new_data' not in st.session_state:
    st.session_state.new_data = []

fake = Faker()

st.set_page_config(page_title="Invisible Crisis AI", layout="wide")

st.title("Invisible Crisis AI — Command Center")
st.caption("AI-powered early warning system for communities")


@st.cache_data
def load_data():
    df = pd.read_csv("reports.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()
df['timestamp'] = pd.to_datetime(df['timestamp'])

issues = [
    "Water smells strange",
    "Feeling sick after drinking tap water",
    "Taxi overloaded again",
    "Power outage for hours",
    "Headache and nausea",
    "Crime suspicious activity",
    "Road damaged badly"
]
zones = ["Zone A", "Zone B", "Zone C"]


if st.sidebar.button("Simulate Incoming Reports"):
    st.session_state.new_data = []
    for _ in range(5):
        st.session_state.new_data.append({
            "timestamp": datetime.now(),
            "location": random.choice(zones),
            "text": random.choice(issues)
        })
    st.success("New reports received!")


if st.session_state.new_data:
    new_df = pd.DataFrame(st.session_state.new_data)
    df = pd.concat([df, new_df], ignore_index=True)


def classify_issue(text):
    text = str(text).lower()
    if "water" in text or "sick" in text:
        return "Health"
    elif "taxi" in text or "crime" in text:
        return "Safety"
    elif "electricity" in text or "road" in text or "power" in text:
        return "Infrastructure"
    return "Other"


df["category"] = df["text"].apply(classify_issue)


def risk_score(text):
    text = str(text).lower()
    score = 1
    if "sick" in text or "danger" in text:
        score += 2
    if "overloaded" in text or "crime" in text:
        score += 2
    return score

df["risk_score"] = df["text"].apply(risk_score)


location_stats = df.groupby("location").agg(
    risk_total=("risk_score", "sum"),
    reports=("text", "count")
).reset_index()

threshold = location_stats["risk_total"].mean()

location_stats["risk_level"] = location_stats["risk_total"].apply(
    lambda x: "High Risk" if x > threshold else "Normal"
)


col1, col2, col3 = st.columns(3)
col1.metric("Total Reports", len(df))
col2.metric("High Risk Zones", len(location_stats[location_stats["risk_level"] == "High Risk"]))
col3.metric("Categories Detected", df["category"].nunique())


coords = {
    "Zone A": (-26.2, 27.9),
    "Zone B": (-26.3, 27.8),
    "Zone C": (-26.1, 27.7)
}


location_stats = location_stats[location_stats["location"].isin(coords)]
location_stats["lat"] = location_stats["location"].apply(lambda x: coords[x][0])
location_stats["lon"] = location_stats["location"].apply(lambda x: coords[x][1])

fig = px.density_mapbox(
    location_stats,
    lat="lat",
    lon="lon",
    z="risk_total",
    radius=25,
    center=dict(lat=-26.2, lon=27.8),
    zoom=9,
    mapbox_style="open-street-map"
)
st.plotly_chart(fig, use_container_width=True)


st.subheader("Incident Trends Over Time")
trend = df.groupby(df["timestamp"].dt.date).size().reset_index(name="count")
trend_fig = px.line(trend, x="timestamp", y="count")
st.plotly_chart(trend_fig, use_container_width=True)


st.subheader("Crisis Alerts")
alerts = location_stats[location_stats["risk_level"] == "High Risk"]

if not alerts.empty:
    for _, row in alerts.iterrows():
        st.error(f"{row['location']} is at HIGH RISK ({row['reports']} reports)")
else:
    st.success("No critical risks detected")


st.subheader("What Should We Do?")

if st.button("Generate Response Plan"):
    try:
        summary = df.tail(20)['text'].tolist()
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral-small",
                "messages": [
                    {"role": "system", "content": "You are a crisis management expert."},
                    {"role": "user", "content": f"Based on these reports: {summary}, suggest urgent actions."}
                ]
            }
        )
        result = response.json()
        st.success(result['choices'][0]['message']['content'])
    except Exception as e:
        st.warning(f"Error: {e}")


st.subheader("Submit Community Report")

user_text = st.text_input("Describe issue")
user_location = st.selectbox("Location", ["Zone A", "Zone B", "Zone C"])

if st.button("Submit"):
    new_entry = pd.DataFrame([{
        "timestamp": datetime.now(),
        "location": user_location,
        "text": user_text
    }])
    
    updated = pd.concat([df, new_entry], ignore_index=True)
    updated.to_csv("reports.csv", index=False)
    st.success("Report submitted successfully!")


