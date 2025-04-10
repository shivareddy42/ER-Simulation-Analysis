# 🚑 ER Operations Simulation Dashboard



## Overview

The **ER Operations Simulation Dashboard** is an interactive web application that models Emergency Room (ER) operations using a discrete-event simulation built with **SimPy**. The dashboard integrates real-world ER data (sourced from a Kaggle dataset) with dynamic visualizations and key performance metrics. Users can adjust simulation parameters such as the number of doctors and nurses, patient arrival rate, and simulation duration to evaluate how these factors impact patient wait times, throughput, and resource utilization.

This project is inspired by the research of **Dr. Vishnu Prabhu** on healthcare systems modeling and data-driven decision making. It provides insights into operational challenges such as ED crowding and helps explore strategies to improve resource allocation.

## Features

- **Interactive Parameter Tuning:** Adjust critical parameters (number of doctors, nurses, patient arrival rate, simulation duration) using intuitive sliders.
- **Real-time Simulation:** Run a SimPy-based simulation that processes patients through stages (registration, triage, medical consultation) with time-series tracking.
- **Dynamic Visualizations:** 
  - **Histogram of Patient Wait Times:** Explore the distribution of wait times.
  - **Line Chart of Queue Lengths:** Visualize how the number of patients in queues changes over the simulation.
- **Additional EDA Insights:** Expandable section displaying static exploratory data analysis (EDA) plots (e.g., wait time by hospital, urgency, correlation heatmap) for additional context.
- **Key Metrics Display:** Dynamic metric cards show average wait time, total patients treated, and resource utilization percentages.
- **Clean, Responsive UI:** Built with Streamlit and Plotly to ensure a sleek and user-friendly experience.


## Data Source

The simulation uses a cleaned version of real-world ER data from a Kaggle dataset.  
**Dataset Link:** [ER Wait Time Dataset on Kaggle](https://www.kaggle.com/datasets/rivalytics/er-wait-time)  
*(Ensure you have rights to use the data as per Kaggle terms.)*

## Installation and Setup

1. **Clone this repository:**

   ```bash
   git clone https://github.com/shivareddy42/ER-Simulation-Analysis.git
   cd ER-Simulation-Analysis

