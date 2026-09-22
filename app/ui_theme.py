"""Streamlit styling — dark glass dashboard."""

from __future__ import annotations

import streamlit as st

THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');
    .stApp {
        background: radial-gradient(ellipse at 20% 0%, #1e3a5f 0%, #0f172a 40%, #020617 100%);
    }
    h1, h2, h3, p, label, .stMarkdown { font-family: 'Outfit', sans-serif !important; }
    .hero {
        padding: 1.5rem 1.75rem;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(99,102,241,0.9), rgba(168,85,247,0.85), rgba(20,184,166,0.8));
        color: white;
        margin-bottom: 1.25rem;
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.4);
        border: 1px solid rgba(255,255,255,0.15);
    }
    .hero h1 { color: white !important; margin: 0; font-size: 2rem; font-weight: 700; }
    .hero p { margin: 0.5rem 0 0 0; opacity: 0.95; font-size: 1.05rem; line-height: 1.45; }
    .baseline-pill {
        display: inline-block;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 999px;
        padding: 0.35rem 0.85rem;
        margin: 0.2rem;
        font-size: 0.85rem;
        color: #e2e8f0;
    }
    .card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 16px;
        padding: 1rem 1.15rem;
        margin-bottom: 0.75rem;
    }
    .card-risk { border-left: 4px solid #fb923c; }
    .card-ok { border-left: 4px solid #4ade80; }
    .card-neutral { border-left: 4px solid #38bdf8; }
    .whatif {
        background: linear-gradient(145deg, rgba(88,28,135,0.35), rgba(15,23,42,0.8));
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 0.65rem;
        border: 1px solid rgba(167,139,250,0.25);
    }
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.06);
        padding: 0.85rem;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    div[data-testid="stMetric"] label { color: #94a3b8 !important; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #f1f5f9 !important; }
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
        f'<div class="card {cls}"><strong>{icon} {title}</strong><br>'
        f'<span style="color:#cbd5e1;font-size:0.92rem;line-height:1.45;">{detail}</span></div>',
        unsafe_allow_html=True,
    )


def baseline_pills(sleep: float, hr: float, steps: float) -> None:
    st.markdown(
        f'<span class="baseline-pill">🌙 Your norm {sleep:.1f}h sleep</span>'
        f'<span class="baseline-pill">❤️ {hr:.0f} bpm</span>'
        f'<span class="baseline-pill">🚶 {steps:,.0f} steps</span>',
        unsafe_allow_html=True,
    )
