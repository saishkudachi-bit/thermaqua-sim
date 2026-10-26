import streamlit as st
import plotly.graph_objects as go
import numpy as np
from physics import (
    calculate_distillate_yield,
    calculate_specific_energy_consumption,
    calculate_salt_rejection
)

# Page configuration
st.set_page_config(
    page_title="ThermAqua | Data Center Thermal Desalination Twin",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished dark UI
st.markdown("""
<style>
    .metric-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 18px;
        border: 1px solid #2e3440;
    }
    .impact-pill {
        background: #111827;
        border-left: 4px solid #10b981;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
st.sidebar.title("Operational Controls")

preset = st.sidebar.selectbox(
    "Quick Architecture Presets",
    ["Custom Tuning", "Standard Hyperscale (10 MW)", "Mega Campus (30 MW)", "Edge AI Cluster (2 MW)"]
)

# Set defaults based on preset
if preset == "Standard Hyperscale (10 MW)":
    default_mw, default_temp, default_sal, default_eta = 10.0, 65, 70000, 0.58
elif preset == "Mega Campus (30 MW)":
    default_mw, default_temp, default_sal, default_eta = 30.0, 72, 70000, 0.65
elif preset == "Edge AI Cluster (2 MW)":
    default_mw, default_temp, default_sal, default_eta = 2.0, 55, 45000, 0.45
else:
    default_mw, default_temp, default_sal, default_eta = 10.0, 65, 70000, 0.58

it_capacity = st.sidebar.slider("IT Thermal Capacity (MW)", 1.0, 50.0, default_mw, 0.5)
coolant_temp = st.sidebar.slider("Coolant Loop Exhaust Temp (°C)", 45, 85, default_temp, 1)
salinity = st.sidebar.slider("Feed Water Salinity (ppm)", 10000, 120000, default_sal, 5000)
recovery_factor = st.sidebar.slider("Latent Heat Recovery Factor (η)", 0.20, 0.85, default_eta, 0.01)

# Physics calculation calls
daily_yield_liters = calculate_distillate_yield(it_capacity, coolant_temp, salinity, recovery_factor)
sec_val = calculate_specific_energy_consumption(recovery_factor)
salt_rej = calculate_salt_rejection(salinity)

# ----------------- HEADER & EXECUTIVE SUMMARY -----------------
st.title("💧 ThermAqua: Data Center Waste Heat Desalination Digital Twin")
st.markdown(
    "Mathematical modeling and operational simulation of sub-boiling atmospheric membrane distillation "
    "driven by AI server thermal exhaust."
)

# Top Key Performance Indicators
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label="Daily Distillate Yield",
        value=f"{daily_yield_liters:,.0f} L/day",
        delta=f"{daily_yield_liters/1000.0:,.1f} m³/day"
    )
with col2:
    st.metric(
        label="Primary Thermal Fuel Cost",
        value="$0 / year",
        delta="100% Upcycled Heat"
    )
with col3:
    st.metric(
        label="Specific Electric Demand",
        value=f"{sec_val:.2f} kWh/m³",
        delta="-75% vs MSF",
        delta_color="normal"
    )
with col4:
    st.metric(
        label="Salt Rejection Ratio",
        value=f"{salt_rej:.1f}%",
        delta="< 12 ppm TDS"
    )

st.write("---")

# ----------------- INTUITIVE PROCESS FLOW & SANKEY -----------------
st.subheader("System Mass & Energy Stream Distribution")

# Interactive Sankey diagram showing input -> module -> outputs
distillate_m3 = daily_yield_liters / 1000.0
brine_flow = distillate_m3 * 0.45
cooling_water_loop = it_capacity * 18.0

fig_sankey = go.Figure(data=[go.Sankey(
    node=dict(
        pad=18,
        thickness=22,
        line=dict(color="#111", width=0.5),
        label=[
            f"GPU Waste Heat ({it_capacity} MW @ {coolant_temp}°C)", # 0
            f"Seawater/Brine Intake ({salinity:,} ppm)",            # 1
            "ThermAqua Distillation Skid",                          # 2
            f"Pure Freshwater Output ({daily_yield_liters:,.0f} L/day)", # 3
            "Concentrated Brine Reject",                            # 4
            f"Cooled Loop Return ({coolant_temp-15}°C back to GPUs)" # 5
        ],
        color=["#ef4444", "#3b82f6", "#6366f1", "#10b981", "#f59e0b", "#06b6d4"]
    ),
    link=dict(
        source=[0, 1, 2, 2, 2],
        target=[2, 2, 3, 4, 5],
        value=[
            it_capacity * 25,
            distillate_m3 * 1.5,
            distillate_m3,
            brine_flow,
            it_capacity * 22
        ],
        color=[
            "rgba(239, 68, 68, 0.35)",
            "rgba(59, 130, 246, 0.35)",
            "rgba(16, 185, 129, 0.55)",
            "rgba(245, 158, 11, 0.50)",
            "rgba(6, 182, 212, 0.35)"
        ]
    )
)])

fig_sankey.update_layout(
    font=dict(size=13, color="white"),
    height=320,
    margin=dict(l=5, r=5, t=15, b=15),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig_sankey, use_container_width=True)

# ----------------- REAL-WORLD IMPACT BADGES -----------------
st.subheader("Real-World Impact Equivalents")
imp1, imp2, imp3 = st.columns(3)

people_served = int(daily_yield_liters / 2.5)
pools_per_year = (daily_yield_liters * 365) / 2_500_000
utility_savings = (daily_yield_liters * 365 / 1000) * 2.80  # ~$2.80 per m3 commercial water

with imp1:
    st.markdown(f"""
    <div class="impact-pill">
        <strong>Community Impact:</strong><br>
        Supplies daily drinking water for <b>{people_served:,} people</b> (at 2.5 L/day).
    </div>
    """, unsafe_allow_html=True)

with imp2:
    st.markdown(f"""
    <div class="impact-pill">
        <strong>Volume Benchmark:</strong><br>
        Produces equivalent of <b>{pools_per_year:.1f} Olympic pools</b> of clean water per year.
    </div>
    """, unsafe_allow_html=True)

with imp3:
    st.markdown(f"""
    <div class="impact-pill">
        <strong>Data Center Water Savings:</strong><br>
        Saves estimated <b>${utility_savings:,.0f} / year</b> in municipal water tariffs.
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# ----------------- TABS: BENCHMARK & LOAD SCALING -----------------
tab1, tab2, tab3 = st.tabs(["📊 Performance Benchmarking", "📈 Load Scaling Model", "🔬 4-Step Process Pipeline"])

with tab1:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("**Auxiliary Electrical Demand (kWh/m³)**")
        fig_bar = go.Figure(go.Bar(
            x=["ThermAqua (Our Model)", "Reverse Osmosis (RO)", "Multi-Stage Flash (MSF)"],
            y=[sec_val, 3.5, 4.0],
            text=[f"{sec_val:.2f} kWh/m³", "3.5 kWh/m³", "4.0 kWh/m³"],
            textposition="auto",
            marker_color=["#10b981", "#f97316", "#ef4444"]
        ))
        fig_bar.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=20, b=10),
            yaxis_title="kWh / m³",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.markdown("**Operational Parameter Matrix**")
        st.table({
            "Dimension": [
                "Primary Energy Source",
                "Additional Fuel Cost",
                "Feed Salinity Tolerance",
                "Operating Pressure",
                "Product Water Purity"
            ],
            "ThermAqua (Our Project)": [
                f"GPU Coolant ({coolant_temp}°C)",
                "$0 (Upcycled Waste Heat)",
                f"{salinity:,} ppm",
                "Ambient (1 atm)",
                "< 12 ppm TDS"
            ],
            "Traditional MSF": [
                "Fossil Fuel Boilers (100°C+)",
                "Extremely High",
                "40,000–50,000 ppm",
                "Vacuum Chambers",
                "< 25 ppm TDS"
            ]
        })

with tab2:
    st.markdown("**Distillate Production Scaling vs. IT Thermal Capacity (1 MW – 50 MW)**")
    mw_range = np.linspace(1, 50, 50)
    yields = [calculate_distillate_yield(mw, coolant_temp, salinity, recovery_factor) for mw in mw_range]

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=mw_range,
        y=yields,
        mode="lines",
        line=dict(color="#10b981", width=3),
        name="Distillate Yield"
    ))
    fig_line.add_vline(
        x=it_capacity,
        line_dash="dash",
        line_color="#ef4444",
        annotation_text=f"Current: {it_capacity:.1f} MW"
    )
    fig_line.update_layout(
        height=340,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Data Center IT Load (MW)",
        yaxis_title="Water Production (Liters / Day)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_line, use_container_width=True)

with tab3:
    st.markdown("""
    #### Physical Flow Architecture:
    1. **Direct-to-Chip Loop:** Coolant picks up heat from GPU cold plates, leaving the racks at **55°C–75°C**.
    2. **Heat Interceptor Skid:** A high-efficiency heat exchanger transfers this thermal energy to the incoming saline feed stream without cross-contaminating server loops.
    3. **Hydrophobic PTFE Membrane:** Warm brine passes over microporous Teflon membranes (0.2 µm pore size). High surface tension prevents liquid water from penetrating; pure water vapor diffuses across.
    4. **Latent Heat Condenser:** The pure vapor condenses into fresh distillate (<12 ppm TDS), transferring its condensation enthalpy back into the feed brine to maximize efficiency.
    """)