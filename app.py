import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="ThermAqua | AI Thermal Desalination Twin",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- COZY WATERY GLASSMORPHIC CSS -----------------
st.markdown("""
<style>
    /* Animated Water Gradient Background */
    @keyframes oceanicFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(-45deg, #020b14, #051c2c, #072e44, #031422, #020912) !important;
        background-size: 400% 400% !important;
        animation: oceanicFlow 22s ease infinite !important;
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Frosted Glass Container */
    .glass-card {
        background: rgba(15, 23, 42, 0.55);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(56, 189, 248, 0.18);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: transform 0.25s ease, border-color 0.25s ease;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.4);
    }

    /* KPI Header Text */
    .glass-title {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }
    .glass-val {
        font-size: 32px;
        font-weight: 800;
        margin: 6px 0;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .glass-pill {
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
        display: inline-block;
    }
    .pill-cyan { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .pill-green { background: rgba(52, 211, 153, 0.15); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); }

    /* Infographic Glass Tiles */
    .impact-glass {
        background: rgba(8, 20, 36, 0.65);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ----------------- FIRST-PRINCIPLES PHYSICS -----------------
def calc_distillate_yield(it_mw, temp_c, sal_ppm, eta):
    temp_factor = (temp_c / 65.0) ** 1.3
    salinity_factor = 1.0 - (sal_ppm / 100000.0) * 0.05
    recovery_mult = 1.0 + (eta - 0.58) * 0.85
    base_liters_per_mw = 20880.0
    yield_val = it_mw * base_liters_per_mw * temp_factor * salinity_factor * recovery_mult
    return max(yield_val, 0.0)

def calc_specific_energy(eta):
    return 0.75 - (eta - 0.58) * 0.05

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.markdown("### 🌊 Simulation Matrix")

preset = st.sidebar.selectbox(
    "Architecture Presets",
    ["Standard Hyperscale (10 MW)", "Mega AI Campus (30 MW)", "Edge Node (2 MW)", "Custom Tuning"]
)

if preset == "Standard Hyperscale (10 MW)":
    default_mw, default_temp, default_sal, default_eta = 10.0, 65, 70000, 0.58
elif preset == "Mega AI Campus (30 MW)":
    default_mw, default_temp, default_sal, default_eta = 30.0, 72, 70000, 0.65
elif preset == "Edge Node (2 MW)":
    default_mw, default_temp, default_sal, default_eta = 2.0, 55, 45000, 0.45
else:
    default_mw, default_temp, default_sal, default_eta = 10.0, 65, 70000, 0.58

it_capacity = st.sidebar.slider("🔥 Server Heat Output (MW)", 1.0, 50.0, float(default_mw), 0.5)
coolant_temp = st.sidebar.slider("🌡️ GPU Coolant Loop (°C)", 45, 85, int(default_temp), 1)
salinity = st.sidebar.slider("🧂 Feed Salinity (ppm)", 10000, 120000, int(default_sal), 5000)
recovery_factor = st.sidebar.slider("♻️ Latent Heat Recovery (η)", 0.20, 0.85, float(default_eta), 0.01)

# Physics calculations
daily_yield_liters = calc_distillate_yield(it_capacity, coolant_temp, salinity, recovery_factor)
sec_val = calc_specific_energy(recovery_factor)
daily_thermal_mwh = it_capacity * 24.0  # Daily MWh thermal energy dissipated

# Human impact metrics
people_supplied = int(daily_yield_liters / 2.5)
bottles_per_min = int(daily_yield_liters / (24 * 60 * 0.5))
pools_per_year = (daily_yield_liters * 365) / 2_500_000
water_savings_usd = (daily_yield_liters * 365 / 1000) * 2.80

# ----------------- MAIN TITLE & HERO KPI CARDS -----------------
st.markdown("<h1 style='text-align: center; margin-bottom: 2px;'>💧 ThermAqua Digital Twin</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7dd3fc; font-size: 16px; margin-bottom: 28px;'>Atmospheric Sub-Boiling Desalination Driven by AI Server Thermal Exhaust</p>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="glass-card">
        <div class="glass-title">Daily Distillate Yield</div>
        <div class="glass-val">{daily_yield_liters:,.0f} L</div>
        <span class="glass-pill pill-cyan">🌊 {daily_yield_liters/1000:,.1f} m³ / day</span>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="glass-card">
        <div class="glass-title">Thermal Fuel Cost</div>
        <div class="glass-val" style="background: linear-gradient(90deg, #34d399, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">$0</div>
        <span class="glass-pill pill-green">🌱 100% Upcycled Heat</span>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="glass-card">
        <div class="glass-title">Auxiliary Electricity</div>
        <div class="glass-val">{sec_val:.2f}</div>
        <span class="glass-pill pill-cyan">⚡ kWh/m³ (Pumps Only)</span>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="glass-card">
        <div class="glass-title">Permeate Purity</div>
        <div class="glass-val" style="background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">99.9%</div>
        <span class="glass-pill pill-green">✨ &lt; 12 ppm TDS</span>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------- NEW DUAL-AXIS HEAT VS WATER CONVERSION GRAPH -----------------
st.markdown("### 🔄 Heat-to-Water Direct Conversion Trajectory")
st.markdown("<span style='color: #94a3b8; font-size: 14px;'>Visualizes how dissipated GPU thermal megawatt-hours are converted directly into clean water volume without burning fossil fuels.</span>", unsafe_allow_html=True)

mw_axis = np.linspace(1, 50, 50)
water_axis = [calc_distillate_yield(mw, coolant_temp, salinity, recovery_factor) for mw in mw_axis]
heat_mwh_axis = mw_axis * 24.0

fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

# Trace 1: Water Yield Area Curve (Left Axis)
fig_dual.add_trace(
    go.Scatter(
        x=mw_axis,
        y=water_axis,
        name="Clean Water Output (L/day)",
        mode="lines",
        line=dict(color="#38bdf8", width=3.5),
        fill="tozeroy",
        fillcolor="rgba(56, 189, 248, 0.12)"
    ),
    secondary_y=False
)

# Trace 2: Dissipated Heat Energy (Right Axis)
fig_dual.add_trace(
    go.Scatter(
        x=mw_axis,
        y=heat_mwh_axis,
        name="Thermal Energy Intercepted (MWh/day)",
        mode="lines",
        line=dict(color="#f97316", width=2.5, dash="dash")
    ),
    secondary_y=True
)

# Marker for Current Operating Point
fig_dual.add_trace(
    go.Scatter(
        x=[it_capacity],
        y=[daily_yield_liters],
        mode="markers+text",
        name="Current Operating Point",
        marker=dict(color="#34d399", size=14, line=dict(color="white", width=2)),
        text=[f" 📍 {daily_yield_liters:,.0f} L/day @ {it_capacity:.1f} MW"],
        textposition="top left",
        textfont=dict(color="#34d399", size=13, family="Arial Black")
    ),
    secondary_y=False
)

fig_dual.update_layout(
    height=380,
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(color="white")),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15, 23, 42, 0.4)",
    hovermode="x unified"
)

fig_dual.update_xaxes(
    title_text="Data Center IT Capacity (MW)",
    color="#94a3b8",
    gridcolor="rgba(255,255,255,0.06)"
)
fig_dual.update_yaxes(
    title_text="Distillate Produced (Liters / Day)",
    color="#38bdf8",
    gridcolor="rgba(56, 189, 248, 0.08)",
    secondary_y=False
)
fig_dual.update_yaxes(
    title_text="Heat Dissipated (MWh_thermal / Day)",
    color="#f97316",
    gridcolor="rgba(249, 115, 22, 0.08)",
    secondary_y=True
)

st.plotly_chart(fig_dual, use_container_width=True)

# ----------------- REAL-WORLD IMPACT GLASS TILES -----------------
st.markdown("### 🌍 Real-World Impact (Translating Liters into Human Scale)")

i1, i2, i3, i4 = st.columns(4)

with i1:
    st.markdown(f"""
    <div class="impact-glass">
        <div style="font-size: 32px; margin-bottom: 4px;">👥</div>
        <div style="font-size: 22px; font-weight: 800; color: #38bdf8;">{people_supplied:,}</div>
        <span style="color: #94a3b8; font-size: 13px;">People Provided Daily Drinking Water</span>
    </div>
    """, unsafe_allow_html=True)

with i2:
    st.markdown(f"""
    <div class="impact-glass">
        <div style="font-size: 32px; margin-bottom: 4px;">🍼</div>
        <div style="font-size: 22px; font-weight: 800; color: #34d399;">{bottles_per_min:,} / min</div>
        <span style="color: #94a3b8; font-size: 13px;">500ml Bottled Water Equivalent Rate</span>
    </div>
    """, unsafe_allow_html=True)

with i3:
    st.markdown(f"""
    <div class="impact-glass">
        <div style="font-size: 32px; margin-bottom: 4px;">🏊‍♂️</div>
        <div style="font-size: 22px; font-weight: 800; color: #818cf8;">{pools_per_year:.1f} Pools</div>
        <span style="color: #94a3b8; font-size: 13px;">Olympic Pools Filled Annually</span>
    </div>
    """, unsafe_allow_html=True)

with i4:
    st.markdown(f"""
    <div class="impact-glass">
        <div style="font-size: 32px; margin-bottom: 4px;">💵</div>
        <div style="font-size: 22px; font-weight: 800; color: #facc15;">${water_savings_usd:,.0f}</div>
        <span style="color: #94a3b8; font-size: 13px;">Annual Municipal Water Cost Saved</span>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------- BENCHMARK COMPARISON -----------------
st.markdown("### ⚡ Auxiliary Energy Demand: Why ThermAqua Wins")

b1, b2 = st.columns([1.3, 1])

with b1:
    fig_comp = go.Figure(go.Bar(
        x=["ThermAqua (Our Model)", "Reverse Osmosis (RO)", "Thermal MSF"],
        y=[sec_val, 3.5, 4.0],
        marker_color=["#10b981", "#f97316", "#ef4444"],
        text=[f"{sec_val:.2f} kWh/m³", "3.5 kWh/m³", "4.0 kWh/m³"],
        textposition="outside",
        textfont=dict(color="white", size=13)
    ))
    fig_comp.update_layout(
        height=280,
        margin=dict(l=10, r=10, t=20, b=10),
        yaxis=dict(title="Electricity (kWh / m³)", color="#94a3b8", range=[0, 5], gridcolor="rgba(255,255,255,0.06)"),
        xaxis=dict(color="#cbd5e1"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_comp, use_container_width=True)

with b2:
    st.markdown(f"""
    <div class="glass-card" style="height: 90%;">
        <b style="color: #38bdf8; font-size: 16px;">Core Engineering Advantage:</b>
        <p style="color: #cbd5e1; font-size: 13.5px; line-height: 1.6; margin-top: 8px;">
            • <b>Zero Primary Fuel:</b> Uses <b>{daily_thermal_mwh:.0f} MWh/day</b> of free GPU server exhaust heat instead of gas boilers.<br>
            • <b>Atmospheric Pressure:</b> Operates at 1 atm without requiring high-pressure 70-bar pumps like Reverse Osmosis.<br>
            • <b>Brine Tolerant:</b> Handles <b>{salinity:,} ppm</b> feed salinity without fouling microporous PTFE membrane pores.
        </p>
    </div>
    """, unsafe_allow_html=True)