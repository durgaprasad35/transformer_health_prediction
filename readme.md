## This can predict the transformer health
⚡ Three-Phase Transformer Fault Analysis and Monitoring System

A professional industrial-grade Streamlit web application for simulating, monitoring, and analyzing the performance of a three-phase transformer under various loading and fault conditions using mathematical modeling and numerical simulation.

📌 Project Overview

This project simulates a three-phase transformer using electrical differential equations and numerical methods. The application enables users to analyze transformer behavior under different operating conditions and fault scenarios without relying on datasets or machine learning models.

All outputs are generated dynamically using:

Transformer equivalent circuit modeling
Mutual inductance coupling
Magnetizing branch modeling
Three-phase AC supply simulation
Numerical solution using SciPy's solve_ivp

The application provides interactive visualization, fault diagnosis, performance metrics, and report generation through a modern Streamlit dashboard.

🎯 Objectives
Simulate transformer behavior under varying loads.
Analyze transformer performance during faults.
Monitor voltage, current, and power waveforms.
Evaluate transformer efficiency and power quality.
Provide fault diagnosis and recommendations.
Create an industrial-style monitoring dashboard.
🏗 System Architecture
User Input
     │
     ▼
Streamlit Dashboard
     │
     ▼
Transformer Mathematical Model
     │
     ▼
SciPy Differential Equation Solver
     │
     ▼
Simulation Results
     │
     ▼
Visualization & Analysis
⚙️ Features
Load Condition Simulation

The application supports:

Load Condition	Description
25% Load	Lightly loaded transformer
50% Load	Half-load operation
75% Load	High-load operation
Full Load	Rated transformer operation
Fault Simulation

The following transformer faults can be simulated:

Fault Type	Description
Normal	Healthy transformer
L-G	Line-to-Ground Fault
L-L-G	Line-to-Line-to-Ground Fault
L-L-L-G	Three-Phase-to-Ground Fault
Temperature	Overheating Fault
🔬 Mathematical Model

The transformer is modeled using:

Primary Winding
Resistance (R₁)
Inductance (L₁)
Secondary Winding
Resistance (R₂)
Leakage Inductance
Magnetizing Branch
Core Resistance (Rm)
Magnetizing Inductance (Lm)
Mutual Coupling

Mutual inductance is calculated using:

where:

M = Mutual Inductance
k = Coupling Coefficient
L₁ = Primary Inductance
L₂ = Secondary Inductance
🧮 Numerical Solution

The system differential equations are solved using:

SciPy Solver
solve_ivp()

Method Used:

RK45

The simulation computes:

Primary Voltage
Secondary Voltage
Primary Current
Secondary Current
Magnetizing Current
Input Power
Output Power
📊 Dashboard Features
Summary Cards

The dashboard displays:

Primary RMS Voltage
Secondary RMS Voltage
Peak Primary Current
Peak Secondary Current
Transformer Efficiency
Power Factor
Interactive Visualizations
Voltage Analysis
Primary Voltage (Phase A, B, C)
Secondary Voltage (Phase A, B, C)
Current Analysis
Primary Current
Secondary Current
Power Analysis
Input Power
Output Power

All graphs are interactive and powered by Plotly.

🩺 Fault Diagnosis System

The application automatically identifies fault severity.

Fault Type	Severity
Normal	Low
L-G	Medium
L-L-G	High
L-L-L-G	Critical
Temperature	Medium
💡 Recommendations Engine

The system provides recommendations based on detected faults.

L-G Fault
Inspect insulation and grounding system.
L-L-G Fault
Inspect phase insulation and conductor integrity.
L-L-L-G Fault
Immediately disconnect transformer and inspect windings.
Temperature Fault
Check cooling system and winding temperature.
📈 Power Quality Analysis

The dashboard computes:

RMS Voltage
RMS Current
Real Power
Apparent Power
Power Factor
Transformer Efficiency
📁 Project Structure
Transformer-Fault-Analysis/
│
├── app.py
├── transformer.py
├── requirements.txt
├── README.md
│
└── reports/
🛠 Technologies Used
Frontend
Streamlit
Visualization
Plotly
Numerical Computation
NumPy
SciPy
Data Processing
Pandas
Reporting
ReportLab
Plotting
Matplotlib
📦 Installation
Clone Repository
git clone <repository-url>
Navigate to Project
cd Transformer-Fault-Analysis
Install Dependencies
pip install -r requirements.txt
▶ Running the Application

Start the Streamlit server:

streamlit run app.py

The application will open automatically in your browser.

📋 Requirements
streamlit
numpy
pandas
scipy
plotly
matplotlib
reportlab
🧪 Validation Test Cases
Normal Operation
Load: Full Load
Fault: Normal

Expected:

Balanced three-phase voltages
Healthy status
Stable currents
L-G Fault
Load: Full Load
Fault: L-G

Expected:

Increased current
Medium severity
L-L-L-G Fault
Load: Full Load
Fault: L-L-L-G

Expected:

Critical severity
Highest fault impact
📚 Educational Applications

This project can be used for:

Power System Analysis
Transformer Fault Studies
Electrical Engineering Laboratories
Academic Research
Numerical Simulation Learning
SCADA Dashboard Development
🚀 Future Enhancements
Real-time IoT sensor integration
Transformer digital twin
Harmonic analysis
Live SCADA connectivity
Cloud-based monitoring
Predictive maintenance analytics
Historical simulation storage
Multi-transformer monitoring
👨‍💻 Author

Durgaprasad Naradala

Electrical Engineering / Power Systems Project

📜 License

This project is developed for educational and research purposes.

⚡ "Simulating Transformer Intelligence Through Mathematical Modeling and Real-Time Visualization" ⚡
