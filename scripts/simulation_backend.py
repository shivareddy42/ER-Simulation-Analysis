import simpy
import numpy as np
import pandas as pd
import os

def run_er_simulation(num_doctors, num_nurses, arrival_rate, sim_time=240):
    """
    Runs a discrete-event simulation of an emergency room for a given simulation time.
    Uses service time distributions (registration, triage, medical consultation) derived from real data.
    Returns overall metrics along with time-series data (wait times and queue lengths).
    
    Parameters:
      - num_doctors: Number of doctors available.
      - num_nurses: Number of nurses available.
      - arrival_rate: Patient arrival rate (patients per hour).
      - sim_time: Simulation time in minutes (default is 240 minutes = 4 hours).
    """
    # Load the cleaned dataset from disk. (Adjust the path to your cleaned ER data.)
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))  # This file's directory
    DATA_PATH = os.path.join(THIS_DIR, "..", "data", "cleaned_er_data.csv")

    df = pd.read_csv(DATA_PATH)

    
    # Use the preprocessed columns (ensure these match your preprocessing code)
    REGISTRATION_MEAN = df['Time_to_Registration'].mean()
    TRIAGE_MEAN = df['Time_to_Triage'].mean()
    MEDICAL_PRO_MEAN = df['Time_to_Medical_Professional'].mean()
    
    # Lists to record results from simulation
    wait_times = []         # individual patient wait times
    queue_lengths = []      # total number in queue (nurse+doctor) over time
    time_points = []        # time points at which queue lengths are recorded
    resource_usage = {'doctor': 0, 'nurse': 0}

    def patient(env, nurses, doctors):
        arrival = env.now
        # Registration process (handled by a nurse)
        with nurses.request() as req:
            yield req
            duration = np.random.exponential(REGISTRATION_MEAN)
            yield env.timeout(duration)
            resource_usage['nurse'] += duration
        
        # Triage process (also handled by a nurse)
        with nurses.request() as req:
            yield req
            duration = np.random.exponential(TRIAGE_MEAN)
            yield env.timeout(duration)
            resource_usage['nurse'] += duration
        
        # Medical consultation (handled by a doctor)
        with doctors.request() as req:
            yield req
            duration = np.random.exponential(MEDICAL_PRO_MEAN)
            yield env.timeout(duration)
            resource_usage['doctor'] += duration
        
        # Record the wait time (from arrival until end of consultation)
        wait_times.append(env.now - arrival)
    
    def generate_patients(env, nurses, doctors):
        while True:
            # Interarrival time (in minutes). (60/arrival_rate gives avg time between arrivals)
            inter_arrival = np.random.exponential(60 / arrival_rate)
            yield env.timeout(inter_arrival)
            env.process(patient(env, nurses, doctors))
    
    def monitor(env, nurses, doctors):
        # Record the combined length of both nurse and doctor queues every 5 minutes
        while True:
            total_queue = len(nurses.queue) + len(doctors.queue)
            time_points.append(env.now)
            queue_lengths.append(total_queue)
            yield env.timeout(5)  # record every 5 minutes

    # Create the simulation environment
    env = simpy.Environment()
    nurses = simpy.Resource(env, capacity=num_nurses)
    doctors = simpy.Resource(env, capacity=num_doctors)
    env.process(generate_patients(env, nurses, doctors))
    env.process(monitor(env, nurses, doctors))
    
    # Run simulation for sim_time minutes (default 4 hours)
    env.run(until=sim_time)
    
    # Calculate overall simulation metrics
    avg_wait = np.mean(wait_times) if wait_times else 0
    throughput = len(wait_times)
    doctor_util = resource_usage['doctor'] / (sim_time * num_doctors) if sim_time and num_doctors else 0
    nurse_util = resource_usage['nurse'] / (sim_time * num_nurses) if sim_time and num_nurses else 0

    return {
        'Average Wait Time (min)': round(avg_wait, 2),
        'Total Patients Treated': throughput,
        'Doctor Utilization (%)': round(doctor_util * 100, 2),
        'Nurse Utilization (%)': round(nurse_util * 100, 2),
        'All Wait Times': wait_times,
        'Time Points': time_points,
        'Queue Lengths': queue_lengths
    }
