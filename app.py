import streamlit as st
import plotly.graph_objects as go
from physics import run_simulation

st.set_page_config(
    page_title="ThermAqua | Digital Twin & Simulation",
    page_icon="💧",
    layout="wide"
)

st.title("💧 ThermAqua: Data Center Waste Heat Desalination Digital Twin")
st.markdown(
    "Mathematical modeling and operational simulation of sub-boiling atmospheric membrane distillation "
    "driven by AI server thermal exhaust."
)

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.header("Data Center Operational Inputs")

it_load = st.sidebar.slider(
    "IT Thermal Capacity (MW)",
    min_value=1.0,
    max_value=50.0,
    value=10.0,
    step=0.5
)

coolant_temp = st.sidebar.slider(
    "Coolant Loop Exhaust Temp (°C)",
    min_value=50,
    max_value=75,
    value=65,
    step=1
)

feed_salinity = st.sidebar.slider(
    "Feed Water Salinity (ppm)",
    min_value=30000,
    max_value=100000,
    value=70000,
    step=5000
)

recovery_factor = st.sidebar.slider(
    "Latent Heat Recovery Factor (η)",
    min_value=0.30,
    max_value=0.85,
    value=0.58,
    step=0.01
)

# ---------------- EXECUTE MODEL ----------------
data = run_simulation(it_load, recovery_factor, coolant_temp, feed_salinity)

# ---------------- KEY METRIC CARDS ----------------
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    label="Daily Distillate Yield",
    value=f"{data['daily_yield_liters']:,.0f} L/day",
    delta=f"{data['daily_yield_m3']:,.1f} m³/day"
)
c2.metric(
    label="Primary Thermal Fuel Cost",
    value=f"${data['fuel_cost']:.0f} / year",
    delta="100% Upcycled Heat"
)
c3.metric(
    label="Specific Electric Demand",
    value=f"{data['thermaqua_sec']:.2f} kWh/m³",
    delta="-75% vs MSF",
    delta_color="inverse"
)
c4.metric(
    label="Salt Rejection Ratio",
    value=f"{data['salt_rejection']}%",
    delta=f"< {data['product_tds']:.0f} ppm TDS"
)

st.divider()

# ---------------- VISUAL ANALYTICS ----------------
tab1, tab2 = st.tabs(["📊 Performance Benchmarking", "📈 Load Scaling Model"])

with tab1:
    chart_col, table_col = st.columns([1, 1])

    with chart_col:
        fig_elec = go.Figure(data=[
            go.Bar(
                x=["ThermAqua (Our Model)", "Reverse Osmosis (RO)", "Multi-Stage Flash (MSF)"],
                y=[data["thermaqua_sec"], data["ro_sec"], data["msf_sec"]],
                marker_color=["#00CC96", "#FFA15A", "#EF553B"],
                text=[
                    f"{data['thermaqua_sec']} kWh/m³",
                    f"{data['ro_sec']} kWh/m³",
                    f"{data['msf_sec']} kWh/m³"
                ],
                textposition="auto"
            )
        ])
        fig_elec.update_layout(
            title="Auxiliary Electrical Demand (kWh/m³)",
            yaxis_title="kWh / m³",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig_elec, use_container_width=True)

    with table_col:
        st.subheader("Operational Parameter Matrix")
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
                f"> {feed_salinity:,} ppm",
                "Ambient (1 atm)",
                f"< {data['product_tds']:.0f} ppm TDS"
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
    st.subheader("Yield Scaling Across Server Load (1 MW – 50 MW)")
    fig_scale = go.Figure()
    fig_scale.add_trace(go.Scatter(
        x=data["mw_range"],
        y=data["scaled_yields"],
        mode="lines",
        name="ThermAqua Yield",
        line=dict(color="#00CC96", width=3)
    ))
    fig_scale.add_vline(
        x=it_load,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Current: {it_load} MW"
    )
    fig_scale.update_layout(
        title="Distillate Production Scaling vs. IT Thermal Capacity",
        xaxis_title="Data Center IT Load (MW)",
        yaxis_title="Water Production (Liters / Day)",
        template="plotly_white",
        height=450
    )
    st.plotly_chart(fig_scale, use_container_width=True)