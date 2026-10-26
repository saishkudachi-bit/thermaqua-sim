import numpy as np

LATENT_HEAT_J_KG = 2400000.0  # Latent heat of vaporization for water (~2.4 MJ/kg)
SECONDS_PER_DAY = 86400

def run_simulation(it_load_mw: float, recovery_factor: float, coolant_temp: float, feed_salinity: int):
    total_watts = it_load_mw * 1_000_000.0

    # 1. ThermAqua Distillate Output:
    daily_yield_liters = (total_watts * recovery_factor / LATENT_HEAT_J_KG) * SECONDS_PER_DAY
    daily_yield_m3 = daily_yield_liters / 1000.0

    # 2. Baseline Comparison: Industrial Multi-Stage Flash (MSF)
    msf_daily_liters = (total_watts * 0.95 * 9.0 / LATENT_HEAT_J_KG) * SECONDS_PER_DAY
    msf_daily_m3 = msf_daily_liters / 1000.0

    # 3. Specific Electrical Consumption (SEC) in kWh/m³
    thermaqua_sec = 0.75  # 0.5 to 1.0 kWh/m³ (low-pressure pumps & control)
    ro_sec = 3.5          # Reverse Osmosis high-pressure baseline
    msf_sec = 4.0         # Industrial MSF vacuum & brine circulation

    # 4. Water Quality & Operational Cost
    fuel_cost = 0.0       # $0 additional fuel (waste heat utilization)
    salt_rejection = 99.9
    product_tds = 12.0    # Sub-15 ppm TDS

    # 5. Capacity Scaling Spectrum (1 MW to 50 MW)
    mw_range = np.linspace(1, 50, 50)
    scaled_yields = [
        (mw * 1_000_000.0 * recovery_factor / LATENT_HEAT_J_KG) * SECONDS_PER_DAY
        for mw in mw_range
    ]

    return {
        "daily_yield_liters": daily_yield_liters,
        "daily_yield_m3": daily_yield_m3,
        "msf_daily_liters": msf_daily_liters,
        "msf_daily_m3": msf_daily_m3,
        "thermaqua_sec": thermaqua_sec,
        "ro_sec": ro_sec,
        "msf_sec": msf_sec,
        "fuel_cost": fuel_cost,
        "salt_rejection": salt_rejection,
        "product_tds": product_tds,
        "mw_range": mw_range,
        "scaled_yields": scaled_yields,
    }