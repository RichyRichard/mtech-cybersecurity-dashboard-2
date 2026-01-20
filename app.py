# =========================================================
# Advanced Social Media Privacy & Security Dashboard
# M.Tech Mini Project | Visualization using Highcharts Concepts
# Streamlit + Python
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import requests
import random
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------------------------------------------------
# DATA FETCHER (Ethical + Open Data)
# ---------------------------------------------------------

class SocialMediaDataFetcher:

    def fetch_twitter_trends(self):
        # Ethical simulated Twitter trends (no personal data)
        data = [
            {"trend": "#DataPrivacy", "volume": 14000, "category": "Technology"},
            {"trend": "#CyberSecurity", "volume": 22000, "category": "Technology"},
            {"trend": "#OnlineSafety", "volume": 9000, "category": "Social"},
            {"trend": "#DigitalEthics", "volume": 6000, "category": "Education"},
            {"trend": "#GDPR", "volume": 12000, "category": "Legal"},
            {"trend": "#Phishing", "volume": 8000, "category": "Security"},
        ]
        return pd.DataFrame(data)

    def fetch_github_security_data(self):
        # Live GitHub Security Advisories (Open API)
        url = "https://api.github.com/advisories"
        try:
            response = requests.get(url, timeout=10)
            advisories = response.json()[:15]
            records = []

            for a in advisories:
                records.append({
                    "severity": a.get("severity", "medium").capitalize(),
                    "published": pd.to_datetime(a.get("published_at")),
                    "summary": a.get("summary", "")[:80],
                    "cvss": random.uniform(4.0, 9.5)
                })

            return pd.DataFrame(records)

        except Exception:
            return pd.DataFrame()

    def fetch_location_privacy_data(self):
        # Synthetic anonymized location risk data
        data = []
        for _ in range(80):
            data.append({
                "hour": random.randint(0, 23),
                "day": random.randint(1, 30),
                "privacy_risk": random.randint(10, 95)
            })
        return pd.DataFrame(data)

    def fetch_phishing_timeline(self):
        months = pd.date_range("2023-06-01", "2024-03-01", freq="M")
        rows = []

        for m in months:
            rows.append({
                "month": m,
                "incidents": random.randint(80, 200),
                "detection_rate": random.uniform(0.6, 0.9)
            })

        return pd.DataFrame(rows)

# ---------------------------------------------------------
# VISUALIZATION (Highcharts-style via Plotly)
# ---------------------------------------------------------

class Visualizer:

    def twitter_bubble(self, df):
        fig = px.scatter(
            df,
            x="category",
            y="volume",
            size="volume",
            color="category",
            hover_name="trend",
            title="Twitter Privacy & Security Trends"
        )
        fig.update_layout(height=450)
        return fig

    def security_timeline(self, df):
        df["month"] = df["published"].dt.to_period("M").astype(str)
        grouped = df.groupby(["month", "severity"]).size().unstack(fill_value=0)

        fig = go.Figure()
        for sev in grouped.columns:
            fig.add_bar(x=grouped.index, y=grouped[sev], name=sev)

        fig.update_layout(
            barmode="stack",
            title="GitHub Security Incidents Timeline",
            xaxis_title="Month",
            yaxis_title="Number of Incidents",
            height=450
        )
        return fig

    def privacy_heatmap(self, df):
        pivot = df.pivot_table(
            values="privacy_risk",
            index="hour",
            columns="day",
            aggfunc="mean"
        )

        fig = go.Figure(
            data=go.Heatmap(
                z=pivot.values,
                colorscale="Viridis"
            )
        )

        fig.update_layout(
            title="Location Privacy Risk Heatmap",
            xaxis_title="Day of Month",
            yaxis_title="Hour of Day",
            height=450
        )
        return fig

    def phishing_trend(self, df):
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(
                x=df["month"],
                y=df["incidents"],
                name="Phishing Incidents",
                line=dict(width=3)
            ),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(
                x=df["month"],
                y=df["detection_rate"] * 100,
                name="Detection Rate (%)",
                line=dict(width=3)
            ),
            secondary_y=True
        )

        fig.update_layout(
            title="Phishing Incidents vs Detection Rate",
            height=450
        )

        fig.update_yaxes(title_text="Incidents", secondary_y=False)
        fig.update_yaxes(title_text="Detection Rate (%)", secondary_y=True)

        return fig

# ---------------------------------------------------------
# STREAMLIT DASHBOARD
# ---------------------------------------------------------

def main():
    st.set_page_config(
        page_title="Social Media Privacy & Security Dashboard",
        layout="wide"
    )

    st.title("🛡️ Advanced Social Media Privacy & Security Dashboard")
    st.markdown("""
    **M.Tech Mini Project – Visualization using Highcharts Concepts**  
    Course: *Ethical Issues in Information Technology*
    """)

    fetcher = SocialMediaDataFetcher()
    viz = Visualizer()

    tab1, tab2, tab3, tab4 = st.tabs([
        "🐦 Twitter Trends",
        "🛡️ Security Incidents",
        "📍 Location Privacy",
        "🎣 Phishing Analysis"
    ])

    with tab1:
        df = fetcher.fetch_twitter_trends()
        st.plotly_chart(viz.twitter_bubble(df), use_container_width=True)

    with tab2:
        df = fetcher.fetch_github_security_data()
        st.plotly_chart(viz.security_timeline(df), use_container_width=True)

    with tab3:
        df = fetcher.fetch_location_privacy_data()
        st.plotly_chart(viz.privacy_heatmap(df), use_container_width=True)

    with tab4:
        df = fetcher.fetch_phishing_timeline()
        st.plotly_chart(viz.phishing_trend(df), use_container_width=True)

    st.markdown("""
    ---
    ### Ethical Compliance
    - No personal or identifiable user data
    - Aggregated & anonymized datasets
    - Educational & research-only usage
    - Demonstrates privacy–utility tradeoff
    """)

# ---------------------------------------------------------
# APP ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
