"""Shared Streamlit styling and small UI helpers."""

from __future__ import annotations

import streamlit as st

THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&display=swap');
    .stApp {
        background: linear-gradient(165deg, #0f172a 0%, #1e1b4b 45%, #134e4a 100%);
    }
    h1, h2, h3, p, label, .stMarkdown { font-family: 'DM Sans', sans-serif !important; }
    .hero {
        padding: 1.25rem 1.5rem;
        border-radius: 16px;
        background: linear-gradient(90deg, #6366f1, #a855f7, #14b8a6);
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.35);
    }
    .hero h1 { color: white !important; margin: 0; font-size: 1.75rem; }
    .hero p { margin: 0.35rem 0 0 0; opacity: 0.95; font-size: 0.95rem; }
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.08);
        padding: 0.75rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.12);
    }
    div[data-testid="stMetric"] label { color: #cbd5e1 !important; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #f8fafc !important; }
    .card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.75rem;
    }
    .card-risk { border-left: 4px solid #f97316; }
    .card-ok { border-left: 4px solid #22c55e; }
    .card-neutral { border-left: 4px solid #38bdf8; }
    .stSlider label { color: #e2e8f0 !important; }
</style>
"""


def inject_theme() -> None:
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str) -> None:
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def reason_card(icon: str, title: str, detail: str, tone: str) -> None:
    cls = {"risk": "card-risk", "ok": "card-ok", "neutral": "card-neutral"}.get(tone, "card-neutral")
    st.markdown(
        f'<div class="card {cls}"><strong>{icon} {title}</strong><br><span style="color:#cbd5e1;font-size:0.9rem;">{detail}</span></div>',
        unsafe_allow_html=True,
    )
