import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="ThermAqua | AI Thermal Desalination Twin",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Cyber/Industrial Glassmorphic Theme
st.markdown("""
<style>
    .kpi-box {
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.12);
        backdrop-filter: blur(10px);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        transition: transform 0.2s ease;
    }
    .kpi-box:hover {
        transform: translateY(-4px);
        border-color: #38bdf8;
    }
    .kpi-title {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .kpi-val {
        font-size: 32px;
        font-weight: 800;
        margin: 6px 0;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .kpi-badge {
        font-size: 12px;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-green { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }
    .badge-blue { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid #0284c7; }
    
    .infocard {
        background: #0f172a;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #1e293b;
        text-align: center;
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
st.sidebar.image("https://img.icons8.com/fluency/96/water-drop.png", width=60)
st.sidebar.title("🎛️ Mission Control")

preset = st.sidebar.selectbox(
    "⚡ One-Click Scenarios",
    ["Standard Hyperscale (10 MW)", "Mega AI Campus (30 MW)", "Edge Node (2 MW)", "Manual Tuning"]
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
coolant_temp = st.sidebar.slider("🌡️ GPU Coolant Temp (°C)", 45, 85, int(default_temp), 1)
salinity = st.sidebar.slider("🧂 Saltiness of Intake (ppm)", 10000, 120000, int(default_sal), 5000)
recovery_factor = st.sidebar.slider("♻️ Heat Recycling Efficiency (η)", 0.20, 0.85, float(default_eta), 0.01)

# Run calculation
daily_yield_liters = calc_distillate_yield(it_capacity, coolant_temp, salinity, recovery_factor)
sec_val = calc_specific_energy(recovery_factor)

# Calculations for human equivalents
people_supplied = int(daily_yield_liters / 2.5)
bottles_per_min = int(daily_yield_liters / (24 * 60 * 0.5))
water_savings_usd = (daily_yield_liters * 365 / 1000) * 2.80

# ----------------- APP HEADER -----------------
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🌊 ThermAqua Digital Twin</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>Transforming AI Server Heat into Pure Water with Zero Extra Fuel</p>", unsafe_allow_html=True)
st.write("")

# ----------------- HERO GLASSMORPHIC KPI CARDS -----------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-title">Freshwater Made</div>
        <div class="kpi-val">{daily_yield_liters:,.0f} L</div>
        <span class="kpi-badge badge-blue">💧 {daily_yield_liters/1000:,.1f} m³ Every Day</span>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-title">Primary Fuel Cost</div>
        <div class="kpi-val" style="background: linear-gradient(90deg, #10b981, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">$0</div>
        <span class="kpi-badge badge-green">🌱 100% Waste Heat Powered</span>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-title">Power Needed</div>
        <div class="kpi-val">{sec_val:.2f}</div>
        <span class="kpi-badge badge-blue">⚡ kWh / m³ (Pumps Only)</span>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-title">Water Cleanliness</div>
        <div class="kpi-val" style="background: linear-gradient(90deg, #38bdf8, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">99.9%</div>
        <span class="kpi-badge badge-green">✨ Ultra-Pure (&lt;12 ppm)</span>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------- VISUAL GAUGES & TANK MONITOR -----------------
st.markdown("### 🎚️ Live Visual Telemetry")

g1, g2, g3 = st.columns([1.2, 1.2, 1.4])

with g1:
    # Coolant Temperature Gauge
    fig_temp = go.Figure(go.Indicator(
        mode="gauge+number",
        value=coolant_temp,
        title={'text': "GPU Coolant Temp (°C)", 'font': {'size': 16, 'color': '#94a3b8'}},
        gauge={
            'axis': {'range': [40, 90], 'tickcolor': "white"},
            'bar': {'color': "#ef4444"},
            'steps': [
                {'range': [40, 55], 'color': "rgba(59, 130, 246, 0.2)"},
                {'range': [55, 75], 'color': "rgba(16, 185, 129, 0.2)"},
                {'range': [75, 90], 'color': "rgba(239, 68, 68, 0.2)"}
            ],
            'threshold': {
                'line': {'color': "yellow", 'width': 3},
                'thickness': 0.75,
                'value': coolant_temp
            }
        }
    ))
    fig_temp.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
    st.plotly_chart(fig_temp, use_container_width=True)

with g2:
    # Thermal Energy Input Gauge
    fig_mw = go.Figure(go.Indicator(
        mode="gauge+number",
        value=it_capacity,
        title={'text': "Captured IT Heat (MW)", 'font': {'size': 16, 'color': '#94a3b8'}},
        gauge={
            'axis': {'range': [0, 50], 'tickcolor': "white"},
            'bar': {'color': "#818cf8"},
            'steps': [
                {'range': [0, 15], 'color': "rgba(99, 102, 241, 0.15)"},
                {'range': [15, 35], 'color': "rgba(99, 102, 241, 0.3)"},
                {'range': [35, 50], 'color': "rgba(99, 102, 241, 0.5)"}
            ]
        }
    ))
    fig_mw.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
    st.plotly_chart(fig_mw, use_container_width=True)

with g3:
    # Visual Water Reservoir Tank
    tank_fill = min(daily_yield_liters / 1_000_000.0 * 100, 100.0)
    fig_tank = go.Figure()
    fig_tank.add_trace(go.Bar(
        x=["Storage Buffer"],
        y=[daily_yield_liters],
        marker=dict(
            color='#0284c7',
            line=dict(color='#38bdf8', width=2)
        ),
        width=0.35,
        text=[f"🌊 {daily_yield_liters:,.0f} L"],
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(size=16, color="white", family="Arial Black")
    ))
    fig_tank.update_layout(
        height=260,
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(range=[0, 1_000_000], title="Daily Production Volume (Liters)", color="#94a3b8"),
        xaxis=dict(showticklabels=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_tank, use_container_width=True)

st.write("---")

# ----------------- VISUAL REAL-WORLD IMPACT (ICON INFOGRAPHICS) -----------------
st.markdown("### 🌍 Real-World Impact (What this actually means)")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="infocard">
        <div style="font-size: 38px;">👥</div>
        <b style="font-size: 20px; color: #38bdf8;">{people_supplied:,}</b><br>
        <span style="color: #94a3b8; font-size: 13px;">People Provided Drinking Water Daily</span>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="infocard">
        <div style="font-size: 38px;">🍾</div>
        <b style="font-size: 20px; color: #34d399;">{bottles_per_min:,} / min</b><br>
        <span style="color: #94a3b8; font-size: 13px;">Equivalent 500ml Water Bottles Produced</span>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="infocard">
        <div style="font-size: 38px;">🏊‍♂️</div>
        <b style="font-size: 20px; color: #818cf8;">{(daily_yield_liters * 365) / 2_500_000:.1f} Pools</b><br>
        <span style="color: #94a3b8; font-size: 13px;">Olympic Swimming Pools Filled Annually</span>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="infocard">
        <div style="font-size: 38px;">💰</div>
        <b style="font-size: 20px; color: #facc15;">${water_savings_usd:,.0f}</b><br>
        <span style="color: #94a3b8; font-size: 13px;">Saved Every Year in Municipal Water Bills</span>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# ----------------- INTERACTIVE BENCHMARKING -----------------
st.markdown("### 📊 Why ThermAqua Beats Traditional Methods")

b1, b2 = st.columns([1.2, 1])

with b1:
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=["ThermAqua (Our Model)", "Reverse Osmosis (RO)", "Thermal Distillation (MSF)"],
        y=[sec_val, 3.5, 4.0],
        marker_color=["#10b981", "#f97316", "#ef4444"],
        text=[f"{sec_val:.2f} kWh/m³", "3.5 kWh/m³", "4.0 kWh/m³"],
        textposition="outside",
        textfont=dict(color="white")
    ))
    fig_comp.update_layout(
        title="Electricity Required to Make 1,000 Liters (Lower is Better)",
        title_font=dict(color="#cbd5e1", size=14),
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        yaxis=dict(title="Electricity Used (kWh/m³)", color="#94a3b8", range=[0, 5]),
        xaxis=dict(color="#94a3b8"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_comp, use_container_width=True)

with b2:
    st.markdown("""
    <div style="background:#0f172a; border-radius:12px; padding:22px; border:1px solid #1e293b; height: 100%;">
        <h4 style="color:#38bdf8; margin-top:0;">💡 The Big Picture:</h4>
        <ul style="color:#cbd5e1; line-height: 1.7; font-size:14px; margin-bottom:0;">
            <li><b>Zero Burned Fuel:</b> Uses 100% free server exhaust heat instead of coal or gas boilers.</li>
            <li><b>No High-Pressure Jamming:</b> RO plants force salt water through membranes at 70 times atmospheric pressure. ThermAqua operates at gentle atmospheric pressure.</li>
            <li><b>No Filter Clogging:</b> Can easily handle salty brine water at <b>70,000+ ppm</b> without membrane rupture.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)