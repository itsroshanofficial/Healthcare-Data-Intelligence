"""
Shared design system for the Healthcare Intelligence app.
Centralizes colors, CSS and small reusable HTML components so every
page in the multipage app looks and feels consistent.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# COLOR PALETTE
# ---------------------------------------------------------------------------
NAVY = "#0B2545"
NAVY_SOFT = "#13315C"
TEAL = "#0EA5A6"
TEAL_SOFT = "#CFFAFA"
BLUE = "#2563EB"
BG = "#F6F8FB"
CARD = "#FFFFFF"
BORDER = "#E4EAF1"
TEXT = "#0B2545"
MUTED = "#5B6B82"

RISK_HIGH = "#DC2626"
RISK_HIGH_BG = "#FDEDED"
RISK_MED = "#D97706"
RISK_MED_BG = "#FEF6E7"
RISK_LOW = "#16A34A"
RISK_LOW_BG = "#EAFBF1"


def _risk_colors(level: str):
    level = (level or "").lower()
    if level.startswith("high"):
        return RISK_HIGH, RISK_HIGH_BG
    if level.startswith("med"):
        return RISK_MED, RISK_MED_BG
    return RISK_LOW, RISK_LOW_BG


# ---------------------------------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------------------------------
def inject_global_css():
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .stApp {{
            background: {BG} !important;
            color: {TEXT} !important;
        }}
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {NAVY} 0%, {NAVY_SOFT} 55%, #0E2F52 100%) !important;
            border-right: 1px solid rgba(255,255,255,0.06);
        }}
        section[data-testid="stSidebar"] * {{
            color: #EAF2FF !important;
        }}
        /* Sidebar nav links */
        section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"],
        section[data-testid="stSidebar"] li a {{
            border-radius: 10px !important;
            margin: 2px 8px !important;
            padding: 8px 12px !important;
            transition: background 0.15s ease;
        }}
        section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"]:hover,
        section[data-testid="stSidebar"] li a:hover {{
            background: rgba(255,255,255,0.08) !important;
        }}
        section[data-testid="stSidebar"] a[aria-current="page"] {{
            background: linear-gradient(90deg, {TEAL} 0%, rgba(37,99,235,0.55) 100%) !important;
            font-weight: 700 !important;
        }}
        section[data-testid="stSidebar"] hr {{
            border-color: rgba(255,255,255,0.12) !important;
        }}
        #MainMenu, footer {{ visibility: hidden; }}

        .block-container {{ padding-top: 1.6rem !important; padding-bottom: 3rem !important; }}

        h1, h2, h3 {{ color: {NAVY} !important; font-weight: 800 !important; }}
        p, span, label, div {{ color: {TEXT}; }}
        .subtle {{ color: {MUTED} !important; font-size: 0.95rem; }}

        /* Buttons */
        div.stButton > button, div.stFormSubmitButton > button {{
            width: 100%;
            border-radius: 12px !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, {TEAL} 0%, {BLUE} 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            height: 3rem !important;
            box-shadow: 0 6px 16px rgba(14,165,166,0.25);
            transition: transform 0.15s ease;
        }}
        div.stButton > button:hover, div.stFormSubmitButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 10px 22px rgba(14,165,166,0.35);
        }}

        /* Generic card */
        .card {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 20px 22px;
            box-shadow: 0 2px 10px rgba(11,37,69,0.04);
            margin-bottom: 16px;
        }}

        /* KPI card */
        .kpi {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 16px 18px;
            box-shadow: 0 2px 10px rgba(11,37,69,0.04);
        }}
        .kpi .label {{ color: {MUTED}; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }}
        .kpi .value {{ color: {NAVY}; font-size: 1.9rem; font-weight: 800; line-height: 1.2; }}
        .kpi .delta {{ font-size: 0.82rem; font-weight: 700; }}

        /* Feature nav card */
        .feature-card {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 18px;
            padding: 22px 20px 14px 20px;
            box-shadow: 0 2px 10px rgba(11,37,69,0.05);
            height: 100%;
        }}
        .feature-icon {{
            width: 52px; height: 52px; border-radius: 14px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.6rem; margin-bottom: 10px;
            background: linear-gradient(135deg, {TEAL_SOFT} 0%, #E7F0FF 100%);
        }}
        .feature-title {{ font-weight: 800; color: {NAVY}; font-size: 1.05rem; margin-bottom: 4px; }}
        .feature-desc {{ color: {MUTED}; font-size: 0.88rem; margin-bottom: 10px; min-height: 40px; }}

        /* Badges */
        .badge {{ padding: 4px 12px; border-radius: 20px; font-weight: 700; font-size: 0.8rem; display:inline-block; }}
        .badge-high {{ background:{RISK_HIGH_BG}; color:{RISK_HIGH}; }}
        .badge-med  {{ background:{RISK_MED_BG};  color:{RISK_MED}; }}
        .badge-low  {{ background:{RISK_LOW_BG};  color:{RISK_LOW}; }}

        /* Result panel */
        .result-panel {{
            border-radius: 16px;
            padding: 22px;
            margin-top: 10px;
            border-left: 7px solid;
        }}

        .app-footer {{
            text-align:center; color:{MUTED}; font-size: 0.78rem; margin-top: 30px;
            border-top: 1px solid {BORDER}; padding-top: 14px;
        }}

        div[data-testid="stMetricValue"] {{ color: {NAVY} !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# HERO ISOMETRIC HOSPITAL ILLUSTRATION (hand-built SVG, no external assets)
# ---------------------------------------------------------------------------
def _hospital_svg_markup(width: int = 260) -> str:
    return f"""
    <svg width="{width}" height="{int(width*0.82)}" viewBox="0 0 320 260" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="skyGlow" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#1E4FBF"/>
          <stop offset="100%" stop-color="#0EA5A6"/>
        </linearGradient>
        <linearGradient id="wallFront" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="#FFFFFF"/>
          <stop offset="100%" stop-color="#DCE7F5"/>
        </linearGradient>
        <linearGradient id="wallSide" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="#B9CBEA"/>
          <stop offset="100%" stop-color="#93AEDD"/>
        </linearGradient>
        <linearGradient id="roofTop" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#0B2545"/>
          <stop offset="100%" stop-color="#13315C"/>
        </linearGradient>
      </defs>

      <ellipse cx="160" cy="235" rx="140" ry="16" fill="#0B2545" opacity="0.08"/>

      <!-- Main isometric building block -->
      <g>
        <polygon points="60,150 160,100 260,150 260,210 160,240 60,210" fill="url(#wallFront)"/>
        <polygon points="160,100 260,150 260,210 160,180" fill="url(#wallSide)"/>
        <polygon points="60,150 160,100 260,150 160,180" fill="url(#roofTop)"/>

        <!-- windows front -->
        <g fill="#0EA5A6" opacity="0.85">
          <rect x="78" y="165" width="18" height="24" rx="3"/>
          <rect x="108" y="178" width="18" height="24" rx="3"/>
          <rect x="138" y="191" width="18" height="24" rx="3"/>
        </g>
        <g fill="#2563EB" opacity="0.55">
          <rect x="178" y="191" width="16" height="22" rx="3"/>
          <rect x="206" y="178" width="16" height="22" rx="3"/>
          <rect x="234" y="165" width="16" height="22" rx="3"/>
        </g>

        <!-- medical cross -->
        <g>
          <rect x="148" y="118" width="24" height="8" rx="2" fill="#FFFFFF"/>
          <rect x="156" y="110" width="8" height="24" rx="2" fill="#FFFFFF"/>
        </g>
      </g>

      <!-- small side building -->
      <polygon points="15,190 60,168 60,210 15,232" fill="url(#wallFront)" opacity="0.9"/>
      <polygon points="15,190 60,168 105,190 60,212" fill="url(#roofTop)" opacity="0.9"/>

      <!-- ambulance cross accent -->
      <circle cx="285" cy="70" r="26" fill="url(#skyGlow)" opacity="0.18"/>
      <circle cx="40" cy="55" r="16" fill="url(#skyGlow)" opacity="0.15"/>
    </svg>
    """


def hospital_svg(width: int = 260) -> str:
    """
    Returns an <img> tag with the illustration embedded as a base64 data URI.
    Rendering it as an <img> (instead of a raw inline <svg>) avoids the blank/
    black-box rendering issue some browsers show for complex inline SVG with
    nested <defs>/gradients injected via st.markdown's unsafe HTML.
    """
    import base64
    svg_markup = _hospital_svg_markup(width)
    encoded = base64.b64encode(svg_markup.encode("utf-8")).decode("utf-8")
    height = int(width * 0.82)
    return (
        f'<img src="data:image/svg+xml;base64,{encoded}" '
        f'width="{width}" height="{height}" alt="Hospital illustration" '
        f'style="display:block;" />'
    )


def hero_banner(title_html: str, subtitle: str, badge_text: str = "AI Decision-Support Prototype"):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(120deg, {NAVY} 0%, {NAVY_SOFT} 55%, {TEAL} 130%);
            border-radius: 22px; padding: 28px 30px; margin-bottom: 22px;
            display:flex; align-items:center; justify-content:space-between; gap: 20px;
            box-shadow: 0 12px 30px rgba(11,37,69,0.25);
        ">
          <div style="flex:1; min-width: 240px;">
            <span style="background: rgba(255,255,255,0.16); color:#EAF2FF; padding:5px 14px;
                  border-radius: 20px; font-size:0.75rem; font-weight:700; letter-spacing:0.03em;">
                  🏥 {badge_text}</span>
            <div style="color:#FFFFFF; font-size:1.7rem; font-weight:800; margin-top:14px; line-height:1.35;">
                {title_html}
            </div>
            <div style="color:#D7E6FF; margin-top:8px; font-size:0.98rem; max-width: 520px;">
                {subtitle}
            </div>
          </div>
          <div style="flex-shrink:0;">{hospital_svg(220)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(icon: str, title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:14px; margin-bottom: 6px;">
            <div style="font-size:2rem;">{icon}</div>
            <div>
                <div style="font-size:1.6rem; font-weight:800; color:{NAVY};">{title}</div>
                <div class="subtle">{subtitle}</div>
            </div>
        </div>
        <hr style="border-top:1px solid {BORDER}; margin: 14px 0 22px 0;">
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str = "", delta_color: str = TEAL):
    delta_html = f'<div class="delta" style="color:{delta_color};">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="kpi">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def result_panel(risk_level: str, probability: float, message: str, extra_html: str = ""):
    color, bg = _risk_colors(risk_level)
    st.markdown(
        f"""
        <div class="result-panel" style="background:{bg}; border-color:{color};">
            <span class="badge" style="background:{color}; color:white;">{probability*100:.1f}% probability</span>
            <h3 style="color:{color}; margin:10px 0 6px 0;">{risk_level} Risk</h3>
            <p style="color:{NAVY}; font-weight:500; margin-bottom:8px;">{message}</p>
            {extra_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer():
    st.markdown(
        """
        <div class="app-footer">
            🏥 Healthcare Data Intelligence — AI decision-support prototype trained on the
            Diabetes 130-US Hospitals dataset. Not a certified medical device; predictions must
            be validated by qualified clinicians before any real-world use.
        </div>
        """,
        unsafe_allow_html=True,
    )
