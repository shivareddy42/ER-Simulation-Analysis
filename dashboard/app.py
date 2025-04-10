import os
import sys

# Add the project root directory to sys.path so we can import from 'scripts'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")
sys.path.append(project_root)

import streamlit as st
import plotly.express as px
import pandas as pd
from scripts.simulation_backend import run_er_simulation

# Build the path to the "plots" folder relative to this file (app.py)
plots_dir = os.path.join(current_dir, "..", "plots")

# -------------------------------
# Dashboard Title & Description
# -------------------------------
st.markdown("<h1 style='text-align: center; color: #2F4F4F;'>🚑 ER Operations Simulation Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""
This interactive dashboard simulates Emergency Room operations based on real-world data.  
Adjust the parameters in the sidebar below and click **Run Simulation** to view results, including key metrics and dynamic visualizations.
""")

# -------------------------------
# Sidebar: Simulation Parameters
# -------------------------------
st.sidebar.header("Simulation Parameters")
num_doctors = st.sidebar.slider("Number of Doctors", 1, 10, 3)
num_nurses = st.sidebar.slider("Number of Nurses", 1, 10, 5)
arrival_rate = st.sidebar.slider("Patient Arrival Rate (patients per hour)", 1, 60, 10)
sim_duration = st.sidebar.slider("Simulation Duration (minutes)", 60, 480, 240)

# -------------------------------
# Run Simulation Button and Results
# -------------------------------
if st.sidebar.button("Run Simulation"):
    with st.spinner("Running simulation, please wait..."):
        results = run_er_simulation(num_doctors, num_nurses, arrival_rate, sim_time=sim_duration)
    
    # Divider
    st.markdown("---")
    
    # -------------------------------
    # Display Key Simulation Metrics
    # -------------------------------
    st.subheader("Simulation Results (Key Metrics)")
    col1, col2 = st.columns(2)
    col1.metric("Average Wait Time (min)", results['Average Wait Time (min)'])
    col2.metric("Patients Treated", results['Total Patients Treated'])
    
    col3, col4 = st.columns(2)
    col3.metric("Doctor Utilization (%)", results['Doctor Utilization (%)'])
    col4.metric("Nurse Utilization (%)", results['Nurse Utilization (%)'])
    
    # Divider
    st.markdown("---")
    
    # -------------------------------
    # Plot 1: Histogram of All Wait Times
    # -------------------------------
    st.subheader("Patient Wait Time Distribution")
    if results['All Wait Times']:
        fig_hist = px.histogram(
            pd.DataFrame({'Wait Time (min)': results['All Wait Times']}),
            x="Wait Time (min)",
            nbins=20,
            title="Histogram of Patient Wait Times",
            template="plotly_white"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.write("No wait time data available.")
    
    # Divider
    st.markdown("---")
    
    # -------------------------------
    # Plot 2: Queue Length over Time
    # -------------------------------
    st.subheader("Queue Length Over Time")
    if results['Time Points'] and results['Queue Lengths']:
        df_queue = pd.DataFrame({
            'Time (min)': results['Time Points'],
            'Total Queue Length': results['Queue Lengths']
        })
        fig_line = px.line(
            df_queue,
            x="Time (min)",
            y="Total Queue Length",
            title="ER Queue Length Over Simulation Time",
            markers=True,
            template="plotly_white"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.write("No queue data available.")
    
    # Divider
    st.markdown("---")
    
    # -------------------------------
    # Additional EDA Plots from Prior Analysis
    # -------------------------------
    with st.expander("📊 More EDA Plots"):
        st.markdown("These static plots, generated during the exploratory data analysis phase, provide additional insights into the ER dataset.")
        st.image(os.path.join(plots_dir, "avg_wait_time_by_hospital.png"), caption="Average Wait Time by Hospital", use_container_width=True)
        st.image(os.path.join(plots_dir, "avg_wait_time_by_urgency.png"), caption="Average Wait Time by Urgency Level", use_container_width=True)
        st.image(os.path.join(plots_dir, "correlation_heatmap.png"), caption="Correlation Heatmap", use_container_width=True)

# -------------------------------
# About Section (Always Visible)
# -------------------------------
with st.expander("ℹ️ About This Dashboard"):
    st.markdown("""
    **Overview:**  
    This interactive dashboard simulates Emergency Room (ER) operations using a discrete-event simulation model (SimPy).  
    Users can adjust parameters such as the number of doctors, nurses, patient arrival rate, and simulation duration.  
    The simulation computes key metrics (average wait times, throughput, resource utilization) and dynamically generates visualizations 
    (a histogram of patient wait times and a time-series chart of queue lengths) for analysis.
    
    **Data Source:**  
    The simulation uses cleaned real-world ER data from a Kaggle dataset.
    
    **Developed by:**  
    Shiva Reddy Peddireddy  
    **Inspired by:**  
    Dr. Vishnu Prabhu’s research on healthcare systems modeling and data-driven decision making.
    """)
