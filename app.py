import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="ThermAqua | AI Thermal Desalination Twin",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- APPLE LIQUID GLASS & ACTIVE FLUID BACKGROUND -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');

    /* Dynamic Liquid Fluid Background */
    @keyframes liquidMotion {
        0% { background-position: 0% 40%; }
        50% { background-position: 100% 60%; }
        100% { background-position: 0% 40%; }
    }

    .stApp {
        background: radial-gradient(circle at 15% 20%, rgba(14, 116, 144, 0.45), transparent 45%),
                    radial-gradient(circle at 85% 80%, rgba(2, 132, 199, 0.35), transparent 50%),
                    radial-gradient(circle at 50% 50%, rgba(3, 105, 161, 0.25), transparent 60%),
                    linear-gradient(135deg, #020617 0%, #031326 35%, #051d36 70%, #020b18 100%) !important;
        background-size: 220% 220% !important;
        animation: liquidMotion 18s ease infinite !important;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
    }

    /* Apple Liquid Glass Container */
    .apple-glass {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(28px) saturate(190%);
        -webkit-backdrop-filter: blur(28px) saturate(190%);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-top: 1px solid rgba(255, 255, 255, 0.38);
        border-radius: 22px;
        padding: 22px 20px;
        box-shadow: 0 16px 40px -12px rgba(0, 0, 0, 0.5), 
                    inset 0 1px 1px 0 rgba(255, 255, 255, 0.2),
                    inset 0 -1px 1px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }

    .apple-glass:hover {
        transform: translateY(-4px) scale(1.008);
        border-color: rgba(56, 189, 248, 0.35);
        border-top-color: rgba(255, 255, 255, 0.55);
        box-shadow: 0 24px 50px -10px rgba(14, 165, 233, 0.28),
                    inset 0 1px 2px 0 rgba(255, 255, 255, 0.35);
    }

    /* Liquid Glass Typography */
    .glass-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        color: #94a3b8;
        margin-bottom: 4px;
    }

    .glass-val-liquid {
        font-size: 33px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 6px 0;
        background: linear-gradient(180deg, #ffffff 15%, #bae6fd 85%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .glass-badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 11.5px;
        font-weight: 500;
        backdrop-filter: blur(12px);
    }
    .badge-cyan {
        background: rgba(14, 165, 233, 0.16);
        border: 1px solid rgba(56, 189, 248, 0.32);
        color: #7dd3fc;
    }
    .badge-green {
        background: rgba(16, 185, 129, 0.16);
        border: 1px solid rgba(52, 211, 153, 0.32);
        color: #6ee7b7;
    }

    /* Apple-style Infographic Pill Cards */
    .apple-pill-card {
        background: rgba(15, 23, 42, 0.45);
        backdrop-filter: blur(24px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-top: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 18px;
        padding: 20px 16px;
        text-align: center;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease;
    }
    .apple-pill-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.3);
    }

    div[data-testid="stSidebar"] {
        background: rgba(3, 10, 20, 0.72) !important;
        backdrop-filter: blur(30px) saturate(180%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
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

def calc_avoided_fuel_cost(it_mw, temp_c):
    # Calculates equivalent thermal fuel cost if this energy was purchased via industrial natural gas boilers
    # Benchmark: $48.50 per MWh_thermal (at 85% boiler efficiency) scaled by thermodynamic temperature grade
    annual_thermal_mwh = it_mw * 24.0 * 365.0
    temp_grade_exergy = (temp_c / 65.0) ** 1.15
    avoided_cost_usd = annual_thermal_mwh * 48.50 * temp_grade_exergy
    return avoided_cost_usd

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.markdown("### 🎛️ Architecture Presets")

preset = st.sidebar.selectbox(
    "Select Configuration",
    ["Standard Hyperscale (10 MW)", "Mega AI Campus (30 MW)", "Edge Node (2 MW)", "Manual Custom Tuning"]
)

if preset == "Standard Hyperscale (10 MW)":
    default_mw, default_temp, default_sal, default_eta = 10.0, 65, 70000, 0.58
elif preset == "Mega AI Campus (30 MW)":
    default_mw, default_temp, default_sal, default_eta = 30.0, 72, 70000, 0.65
elif preset == "Edge Node (2 MW)":
    default_mw, default_temp, default_sal, default_eta = 2.0, 55, 45000, 0.45
else:
    default_mw, default_temp, default_sal, default_eta = 10.0, 65, 70000, 0.58

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Operating Parameters")
it_capacity = st.sidebar.slider("IT Thermal Capacity (MW)", 1.0, 50.0, float(default_mw), 0.5)
coolant_temp = st.sidebar.slider("Coolant Loop Exhaust Temp (°C)", 45, 85, int(default_temp), 1)
salinity = st.sidebar.slider("Feed Water Salinity (ppm)", 10000, 120000, int(default_sal), 5000)
recovery_factor = st.sidebar.slider("Latent Heat Recovery Factor (η)", 0.20, 0.85, float(default_eta), 0.01)

# Real-time calculations
daily_yield_liters = calc_distillate_yield(it_capacity, coolant_temp, salinity, recovery_factor)
sec_val = calc_specific_energy(recovery_factor)
avoided_fuel_annual = calc_avoided_fuel_cost(it_capacity, coolant_temp)
daily_thermal_mwh = it_capacity * 24.0

# Human-readable equivalents
people_supplied = int(daily_yield_liters / 2.5)
bottles_per_min = int(daily_yield_liters / (24 * 60 * 0.5))
pools_per_year = (daily_yield_liters * 365) / 2_500_000
water_savings_usd = (daily_yield_liters * 365 / 1000) * 2.80

# ----------------- MAIN LIQUID GLASS INTERFACE -----------------
st.markdown("<h1 style='text-align: center; font-weight: 700; letter-spacing: -1px; margin-bottom: 2px;'>💧 ThermAqua Digital Twin</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7dd3fc; font-size: 16px; margin-bottom: 28px;'>Sub-Boiling Atmospheric Membrane Desalination Driven by AI Server Thermal Exhaust</p>", unsafe_allow_html=True)

# 4 Dynamic Liquid Glass Telemetry Cards
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="apple-glass">
        <div class="glass-label">Daily Distillate Yield</div>
        <div class="glass-val-liquid">{daily_yield_liters:,.0f} L</div>
        <div class="glass-badge-pill badge-cyan">🌊 {daily_yield_liters/1000:,.1f} m³ / day</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="apple-glass">
        <div class="glass-label">Fuel Cost Avoided</div>
        <div class="glass-val-liquid" style="background: linear-gradient(180deg, #ffffff 15%, #86efac 85%, #22c55e 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">${avoided_fuel_annual/1_000_000:.2f}M / yr</div>
        <div class="glass-badge-pill badge-green">🌱 $0 Paid (100% Upcycled)</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="apple-glass">
        <div class="glass-label">Specific Electric Demand</div>
        <div class="glass-val-liquid">{sec_val:.2f}</div>
        <div class="glass-badge-pill badge-cyan">⚡ kWh/m³ (Pumps Only)</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="apple-glass">
        <div class="glass-label">Permeate Purity</div>
        <div class="glass-val-liquid">99.9%</div>
        <div class="glass-badge-pill badge-green">✨ &lt; 12 ppm TDS</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------- DUAL-AXIS HEAT-TO-WATER CONVERSION DYNAMICS -----------------
st.markdown("### 🔄 Energy Dissipation & Clean Water Generation Trajectory")
st.markdown("<p style='color: #94a3b8; font-size: 14px; margin-top: -8px;'>Directly correlates GPU server heat dissipated (MWh/day) with distilled water production across cluster capacity.</p>", unsafe_allow_html=True)

mw_axis = np.linspace(1, 50, 60)
water_axis = [calc_distillate_yield(mw, coolant_temp, salinity, recovery_factor) for mw in mw_axis]
heat_mwh_axis = mw_axis * 24.0

fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

# Water Generation Smooth Spline Area
fig_dual.add_trace(
    go.Scatter(
        x=mw_axis,
        y=water_axis,
        name="Freshwater Output (L/day)",
        mode="lines",
        line=dict(color="#38bdf8", width=3.5, shape="spline"),
        fill="tozeroy",
        fillcolor="rgba(56, 189, 248, 0.10)"
    ),
    secondary_y=False
)

# Heat Energy Intercepted (Right Axis)
fig_dual.add_trace(
    go.Scatter(
        x=mw_axis,
        y=heat_mwh_axis,
        name="Thermal Energy Intercepted (MWh/day)",
        mode="lines",
        line=dict(color="#fb923c", width=2.5, dash="dash", shape="spline")
    ),
    secondary_y=True
)

# Interactive Pulsing Operating Point Marker
fig_dual.add_trace(
    go.Scatter(
        x=[it_capacity],
        y=[daily_yield_liters],
        mode="markers+text",
        name="Active Working Point",
        marker=dict(
            color="#34d399",
            size=15,
            line=dict(color="#ffffff", width=2.5)
        ),
        text=[f"  📍 {daily_yield_liters:,.0f} L/day @ {it_capacity:.1f} MW"],
        textposition="top center",
        textfont=dict(color="#6ee7b7", size=13, family="SF Pro Display, Arial Black")
    ),
    secondary_y=False
)

fig_dual.update_layout(
    height=370,
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(color="#e2e8f0", size=12)
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(6, 18, 36, 0.45)",
    hovermode="x unified"
)

fig_dual.update_xaxes(
    title_text="Data Center IT Capacity (MW)",
    color="#94a3b8",
    gridcolor="rgba(255, 255, 255, 0.05)",
    showline=False
)
fig_dual.update_yaxes(
    title_text="Clean Distillate Produced (Liters / Day)",
    color="#38bdf8",
    gridcolor="rgba(56, 189, 248, 0.06)",
    showline=False,
    secondary_y=False
)
fig_dual.update_yaxes(
    title_text="Heat Dissipated (MWh / Day)",
    color="#fb923c",
    gridcolor="rgba(251, 146, 60, 0.06)",
    showline=False,
    secondary_y=True
)

st.plotly_chart(fig_dual, use_container_width=True)

# ----------------- REAL-WORLD IMPACT GLASS PILLS -----------------
st.markdown("### 🌍 Real-World Environmental Equivalency")

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.markdown(f"""
    <div class="apple-pill-card">
        <div style="font-size: 30px; margin-bottom: 2px;">👥</div>
        <div style="font-size: 22px; font-weight: 700; color: #7dd3fc;">{people_supplied:,}</div>
        <div style="color: #94a3b8; font-size: 12.5px; margin-top: 4px;">People Daily Drinking Water</div>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown(f"""
    <div class="apple-pill-card">
        <div style="font-size: 30px; margin-bottom: 2px;">🍼</div>
        <div style="font-size: 22px; font-weight: 700; color: #86efac;">{bottles_per_min:,} / min</div>
        <div style="color: #94a3b8; font-size: 12.5px; margin-top: 4px;">500ml Bottled Water Rate</div>
    </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown(f"""
    <div class="apple-pill-card">
        <div style="font-size: 30px; margin-bottom: 2px;">🏊‍♂️</div>
        <div style="font-size: 22px; font-weight: 700; color: #a5b4fc;">{pools_per_year:.1f} Pools</div>
        <div style="color: #94a3b8; font-size: 12.5px; margin-top: 4px;">Olympic Pools Filled / Year</div>
    </div>
    """, unsafe_allow_html=True)

with p4:
    st.markdown(f"""
    <div class="apple-pill-card">
        <div style="font-size: 30px; margin-bottom: 2px;">💵</div>
        <div style="font-size: 22px; font-weight: 700; color: #fde047;">${water_savings_usd:,.0f}</div>
        <div style="color: #94a3b8; font-size: 12.5px; margin-top: 4px;">Annual Utility Bill Saved</div>
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
    <div class="apple-glass" style="height: 88%;">
        <b style="color: #38bdf8; font-size: 16px;">Core Engineering Advantage:</b>
        <p style="color: #cbd5e1; font-size: 13.5px; line-height: 1.6; margin-top: 8px;">
            • <b>Zero Primary Fuel:</b> Upcycles <b>{daily_thermal_mwh:.0f} MWh/day</b> of free GPU server exhaust heat, avoiding <b>${avoided_fuel_annual/1_000_000:.2f}M / yr</b> in boiler gas tariffs.<br>
            • <b>Atmospheric Pressure:</b> Operates at 1 atm without requiring high-pressure 70-bar pumps like Reverse Osmosis.<br>
            • <b>Brine Tolerant:</b> Handles <b>{salinity:,} ppm</b> feed salinity without fouling microporous PTFE membrane pores.
        </p>
    </div>
    """, unsafe_allow_html=True)