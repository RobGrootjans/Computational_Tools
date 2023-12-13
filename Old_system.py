import numpy as np
import pandas as pd

class Patient:
    def __init__(self, call_date, call_time, category, appointment_date, 
                 appointment_time, scan_duration):
        self.call_date = call_date - 1 # because python uses zero-based indexing
        self.call_time = call_time
        self.category = category
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.scan_duration = scan_duration
        
class Machine:
    def __init__(self):
        self.current_patient = None
        self.next_available_slot = np.full([32,1],8, dtype=float)
        self.surplus = np.zeros([32,1], dtype=float)

def schedule_appointment(machine, patient, slot_duration):
    patient.appointment_date = patient.call_date + 1
    patient.appointment_time = machine.next_available_slot[patient.appointment_date]
    machine.next_available_slot[patient.appointment_date] += slot_duration
    if patient.scan_duration > slot_duration:
        machine.surplus[patient.appointment_date] += patient.scan_duration - slot_duration   # difference between actual duration and slot time = surplus

def generate_data(num_days, mean_num_type1, mean_num_type2, mean_duration_type1,
                  mean_duration_type2, std_duration_type1, std_duration_type2):
    np.random.seed(42) # for reproducibility
    data = []
    
    for day in range(1, num_days + 1):
        
        num_type1 = np.random.poisson(mean_num_type1)
        for _ in range(num_type1):
            call_date = day
            call_time = np.random.uniform(8, 17) # assuming calls can be made between 8 AM and 5 PM
            category = 1
            scan_duration = np.random.normal(mean_duration_type1, std_duration_type1)
            data.append([call_date, call_time, category, None, None, scan_duration])
        
        num_type2 = np.random.poisson(mean_num_type2)
        for _ in range(num_type2):
            call_date = day
            call_time = np.random.uniform(8, 17)
            category = 2
            scan_duration = np.random.normal(mean_duration_type2, std_duration_type2)
            data.append([call_date, call_time, category, None, None, scan_duration])
            
    return pd.DataFrame(data, columns=['Day', 'Time', 'PatientType', 'AppointmentDate', 'AppointmentTime', 'Duration'])

def calculate_overtime(machine, machine_name):
    # Initialize overtime
    overtime_total = 0
    
    # Print overtime for each day and total overtime
    print(f"{machine_name} finishes with a delay of:")
    for day, surplus in enumerate(machine.surplus):
        surplus_day = machine.next_available_slot[day][0] + surplus[0] - 17
        if surplus_day > 0:
            overtime_total += surplus_day
            print(f"Day {day + 1}: {surplus_day} hours")
        else:
            surplus_day = 0
            print(f"Day {day + 1}: {surplus_day} hours")
    print(f"The total overtime for {machine_name} this month was {overtime_total} hours.\n")

# Machine initialization
machine1 = Machine()
machine2 = Machine()

# Slot_durations
slot_duration_t1 = 0.5
slot_duration_t2 = 0.75

# Generating data
num_days = 31
mean_num_type1 = 16.47826
mean_num_type2 = 12.87234
mean_duration_type1 = 0.43
mean_duration_type2 = 0.67
std_duration_type1 = 0.09777424
std_duration_type2 = 0.10347673

data_df = generate_data(num_days, mean_num_type1, mean_num_type2, mean_duration_type1, mean_duration_type2, std_duration_type1, std_duration_type2)

# Creating instances and sorting patients acoording to their call time to apply FCFS
patients = []
for _, row in data_df.sort_values(by=['Day', 'Time']).iterrows():
    call_date = int(row['Day'])
    call_time = row['Time']
    category = int(row['PatientType'])
    scan_duration = row['Duration']

    patient = Patient(call_date, call_time, category, None, None, scan_duration)
    patients.append(patient)

# Assigning patients
for patient in patients:
    if patient.category == 1:
        schedule_appointment(machine1, patient, slot_duration_t1)
    else:
        schedule_appointment(machine2, patient, slot_duration_t2)

# Display information after assignment
calculate_overtime(machine1, "Machine 1")
calculate_overtime(machine2, "Machine 2")
