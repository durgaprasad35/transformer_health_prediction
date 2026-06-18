import math

import numpy as np
from scipy.integrate import solve_ivp


def _normalize_load_choice(load_choice):
    normalized = str(load_choice).strip().lower()
    load_map = {
        "1/4": 0.25,
        "25%": 0.25,
        "1/2": 0.5,
        "50%": 0.5,
        "3/4": 0.75,
        "75%": 0.75,
        "full": 1.0,
        "full load": 1.0,
    }

    if normalized not in load_map:
        raise ValueError(
            "Invalid load_choice. Expected one of: 1/4, 1/2, 3/4, full, 25%, 50%, 75%, Full Load."
        )

    return normalized, load_map[normalized]


def _normalize_fault_choice(fault_choice):
    normalized = str(fault_choice).strip().lower()
    fault_map = {
        "normal": "normal",
        "none": "normal",
        "l-g": "l-g",
        "l-l-g": "l-l-g",
        "l-l-l-g": "l-l-l-g",
        "temperature": "temperature",
    }

    return fault_map.get(normalized, "normal")


def run_simulation(load_choice, fault_choice, sim_time):
    load_choice_normalized, load_multiplier = _normalize_load_choice(load_choice)
    fault_choice_normalized = _normalize_fault_choice(fault_choice)

    Np_nominal = 1200
    Ns_nominal = 600
    turns_ratio = Np_nominal / Ns_nominal

    R1 = 0.3
    L1 = 0.6
    R2 = 0.05
    L2_leak = 0.015
    L_load_nominal = 0.002
    R_load_nominal = 8.0

    scale_factor = 1 / load_multiplier
    R_load_eff = R_load_nominal * scale_factor
    L_load_eff = L_load_nominal * scale_factor

    R2_total = R2 + R_load_eff
    L2_total = L2_leak + L_load_eff

    Rm = 500.0
    Lm = 100.0
    k = 0.98
    M = k * math.sqrt(L1 * L2_total)

    V1_rms = 240
    V2_rms = V1_rms / turns_ratio
    f = 50
    omega = 2 * math.pi * f

    if load_multiplier == 1.0:
        Z2_total = complex(R2_total, omega * L2_total)
        absZ2 = abs(Z2_total)
        I2_full = V2_rms / absZ2
        I1_full = I2_full / turns_ratio
    else:
        R_load_full = R_load_nominal
        L_load_full = L_load_nominal
        R2_full = R2 + R_load_full
        L2_full = L2_leak + L_load_full
        Z2_full = complex(R2_full, omega * L2_full)
        absZ2_full = abs(Z2_full)
        I2_full = V2_rms / absZ2_full
        I1_full = I2_full / turns_ratio

    I1_base = I1_full
    I2_base = I2_full

    if fault_choice_normalized == "l-g":
        R1 *= 2
    elif fault_choice_normalized == "l-l-g":
        L2_total *= 1.5
    elif fault_choice_normalized == "l-l-l-g":
        R2_total *= 2
    elif fault_choice_normalized == "temperature":
        Rm *= 1.8

    V1_peak = V1_rms * math.sqrt(2)
    t_start = 0
    t_end = float(sim_time)
    if t_end <= 0:
        raise ValueError("sim_time must be greater than 0.")
    t_eval = np.linspace(t_start, t_end, 2000)

    phases = {
        "A": 0,
        "B": -120,
        "C": 120,
    }

    def transformer_system_with_shunt(t, x, phase_deg, R1, L1, M, R2_total, L2_total, Rm, Lm):
        phase_rad = np.deg2rad(phase_deg)
        v1 = V1_peak * np.sin(2 * np.pi * f * t + phase_rad)
        i1, i_m, i2 = x
        A = np.array([[L1, M], [M, L2_total]])
        b = np.array([v1 - R1 * i1, -R2_total * i2])
        det = L1 * L2_total - M**2
        invA = (1 / det) * np.array([[L2_total, -M], [-M, L1]])
        di1_dt, di2_dt = invA @ b
        di_m_dt = (v1 - Rm * i_m) / Lm
        return [di1_dt, di_m_dt, di2_dt]

    raw_results = {}
    for phase, angle in phases.items():
        sol = solve_ivp(
            transformer_system_with_shunt,
            [t_start, t_end],
            [0, 0, 0],
            args=(angle, R1, L1, M, R2_total, L2_total, Rm, Lm),
            t_eval=t_eval,
            method="RK45",
        )
        raw_results[phase] = sol

    results = {}
    for phase, angle in phases.items():
        sol = raw_results[phase]
        t_vals = sol.t
        i1 = sol.y[0]
        i_m = sol.y[1]
        i2 = sol.y[2]
        i_primary_total = i1 + i_m
        phase_rad = np.deg2rad(angle)
        v_primary = V1_peak * np.sin(2 * np.pi * f * t_vals + phase_rad)
        p_primary = v_primary * i_primary_total
        di2_dt = np.gradient(i2, t_vals)
        v_secondary = R2_total * i2 + L2_total * di2_dt
        p_secondary = v_secondary * i2
        i1_pu = i1 / I1_base
        i_m_pu = i_m / I1_base
        i_primary_total_pu = i_primary_total / I1_base
        i2_pu = i2 / I2_base

        results[phase] = {
            "time": t_vals,
            "v_primary": v_primary,
            "v_secondary": v_secondary,
            "i_primary": i_primary_total,
            "i_secondary": i2,
            "i_series": i1,
            "i_magnetizing": i_m,
            "p_primary": p_primary,
            "p_secondary": p_secondary,
        }

        _ = (i1_pu, i_m_pu, i_primary_total_pu, i2_pu, load_choice_normalized)

    parameters = {
        "Turns Ratio": turns_ratio,
        "Primary Resistance": R1,
        "Primary Inductance": L1,
        "Secondary Resistance": R2_total,
        "Secondary Inductance": L2_total,
        "Mutual Inductance": M,
        "Magnetizing Resistance": Rm,
        "Magnetizing Inductance": Lm,
    }

    return {
        "results": results,
        "parameters": parameters,
    }


if __name__ == "__main__":
    simulation = run_simulation(
        load_choice="Full Load",
        fault_choice="Normal",
        sim_time=0.1,
    )

    print("Simulation completed successfully")