
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

from transformer import run_simulation

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="Transformer Monitoring System",
    page_icon="⚡",
    layout="wide"
)

# ------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------

st.markdown("""
<style>

.stApp{
    background-color:#F5F7FA;
}

h1{
    color:#2563EB;
    font-weight:700;
}

.metric-box{
    background:white;
    padding:15px;
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# HEADER
# ------------------------------------------------

col1,col2,col3 = st.columns([5,2,2])

with col1:
    st.title("⚡ Three-Phase Transformer Fault Analysis")

with col2:
    st.metric("System Status","ONLINE")

with col3:
    st.write(datetime.now())

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("Control Panel")

load_choice = st.sidebar.selectbox(
    "Load Condition",
    [
        "25%",
        "50%",
        "75%",
        "Full Load"
    ]
)

fault_choice = st.sidebar.selectbox(
    "Fault Type",
    [
        "Normal",
        "L-G",
        "L-L-G",
        "L-L-L-G",
        "Temperature"
    ]
)

sim_time = st.sidebar.slider(
    "Simulation Time",
    0.05,
    0.50,
    0.10
)

run_btn = st.sidebar.button(
    "▶ Run Simulation"
)

# ------------------------------------------------
# HELPERS
# ------------------------------------------------

def rms(x):
    return np.sqrt(np.mean(x**2))

def make_plot(results,key,title):

    fig = go.Figure()

    for phase in ["A","B","C"]:

        fig.add_trace(
            go.Scatter(
                x=results[phase]["time"],
                y=results[phase][key],
                mode="lines",
                name=f"Phase {phase}"
            )
        )

    fig.update_layout(
        title=title,
        template="plotly_white",
        height=450
    )

    return fig

# ------------------------------------------------
# MAIN
# ------------------------------------------------

if run_btn:

    simulation = run_simulation(
        load_choice,
        fault_choice,
        sim_time
    )

    results = simulation["results"]

    parameters = simulation["parameters"]

    phaseA = results["A"]

    # --------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------

    VrmsP = rms(
        phaseA["v_primary"]
    )

    VrmsS = rms(
        phaseA["v_secondary"]
    )

    IrmsP = rms(
        phaseA["i_primary"]
    )

    IrmsS = rms(
        phaseA["i_secondary"]
    )

    PeakP = np.max(
        np.abs(
            phaseA["i_primary"]
        )
    )

    PeakS = np.max(
        np.abs(
            phaseA["i_secondary"]
        )
    )

    RealPower = np.mean(
        phaseA["p_primary"]
    )

    ApparPower = (
        VrmsP *
        IrmsP
    )

    PF = (
        RealPower /
        ApparPower
        if ApparPower != 0
        else 0
    )

    Efficiency = (
        np.mean(
            phaseA["p_secondary"]
        ) /
        np.mean(
            phaseA["p_primary"]
        )
    ) * 100

    # --------------------------------------------
    # KPI CARDS
    # --------------------------------------------

    st.subheader("Dashboard Summary")

    c1,c2,c3,c4,c5,c6 = st.columns(6)

    c1.metric(
        "Primary RMS Voltage",
        f"{VrmsP:.2f} V"
    )

    c2.metric(
        "Secondary RMS Voltage",
        f"{VrmsS:.2f} V"
    )

    c3.metric(
        "Peak Primary Current",
        f"{PeakP:.2f} A"
    )

    c4.metric(
        "Peak Secondary Current",
        f"{PeakS:.2f} A"
    )

    c5.metric(
        "Power Factor",
        f"{PF:.3f}"
    )

    c6.metric(
        "Efficiency",
        f"{Efficiency:.2f}%"
    )

    # --------------------------------------------
    # TABS
    # --------------------------------------------

    tab1,tab2,tab3 = st.tabs(
        [
            "Dashboard",
            "Analysis",
            "Reports"
        ]
    )

    # --------------------------------------------
    # DASHBOARD
    # --------------------------------------------

    with tab1:

        r1c1,r1c2 = st.columns(2)

        with r1c1:
            st.plotly_chart(
                make_plot(
                    results,
                    "v_primary",
                    "Primary Voltage"
                ),
                use_container_width=True
            )

        with r1c2:
            st.plotly_chart(
                make_plot(
                    results,
                    "v_secondary",
                    "Secondary Voltage"
                ),
                use_container_width=True
            )

        r2c1,r2c2 = st.columns(2)

        with r2c1:
            st.plotly_chart(
                make_plot(
                    results,
                    "i_primary",
                    "Primary Current"
                ),
                use_container_width=True
            )

        with r2c2:
            st.plotly_chart(
                make_plot(
                    results,
                    "i_secondary",
                    "Secondary Current"
                ),
                use_container_width=True
            )

    # --------------------------------------------
    # ANALYSIS
    # --------------------------------------------

    with tab2:

        st.plotly_chart(
            make_plot(
                results,
                "p_primary",
                "Primary Power"
            ),
            use_container_width=True
        )

        st.plotly_chart(
            make_plot(
                results,
                "p_secondary",
                "Secondary Power"
            ),
            use_container_width=True
        )

        st.subheader(
            "Transformer Parameters"
        )

        st.dataframe(
            pd.DataFrame(
                parameters.items(),
                columns=[
                    "Parameter",
                    "Value"
                ]
            ),
            use_container_width=True
        )

        severity = {
            "Normal":"Low",
            "L-G":"Medium",
            "L-L-G":"High",
            "L-L-L-G":"Critical",
            "Temperature":"Medium"
        }

        st.subheader(
            "Fault Analysis"
        )

        st.write(
            f"Fault Type: {fault_choice}"
        )

        st.write(
            f"Severity: {severity[fault_choice]}"
        )

    # --------------------------------------------
    # REPORTS
    # --------------------------------------------

    with tab3:

        report = pd.DataFrame({
            "Parameter":[
                "Vrms Primary",
                "Vrms Secondary",
                "Irms Primary",
                "Irms Secondary",
                "Power Factor",
                "Efficiency"
            ],

            "Value":[
                VrmsP,
                VrmsS,
                IrmsP,
                IrmsS,
                PF,
                Efficiency
            ]
        })

        st.dataframe(
            report,
            use_container_width=True
        )

        export_df = pd.DataFrame({
            "Time":
            phaseA["time"],

            "Primary Voltage":
            phaseA["v_primary"],

            "Secondary Voltage":
            phaseA["v_secondary"],

            "Primary Current":
            phaseA["i_primary"],

            "Secondary Current":
            phaseA["i_secondary"]
        })

        csv = export_df.to_csv(
            index=False
        )

        st.download_button(
            "⬇ Download CSV",
            csv,
            "transformer_report.csv",
            "text/csv"
        )

else:

    st.info(
        "Select parameters and click Run Simulation."
    )

