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
    
# Machine initialization
machine1 = Machine()
machine2 = Machine()

# Mean durations of scans:
# Type 1: 0.43 -> 30 mins 0.5
# Type 2: 0.67 -> 45 mins 0.75

slot_duration_t1 = 0.5
slot_duration_t2 = 0.75

# Read data from CSV file
df = pd.read_csv(r'C:\Users\matth\OneDrive\Dokumente\ScanRecords.csv') # Change path

# Creating instances
patients = []
for _, row in df.iterrows():
    call_date = int(row['Date'].split('-')[2])  # Extract day from the date
    call_time = row['Time']
    category = 1 if row['PatientType'] == 'Type 1' else 2
    scan_duration = row['Duration']

    patient = Patient(call_date, call_time, category, None, None, scan_duration)
    patients.append(patient)

# Assigning patients
for patient in patients:
    if patient.category == 1:
        schedule_appointment(machine1, patient, slot_duration_t1)
    else:
        schedule_appointment(machine2, patient, slot_duration_t2)
    
# Calculating overtime
# The sum of surplus is  total overtime
overtime_m1 = np.sum(machine1.surplus)
overtime_m2 = np.sum(machine2.surplus)

# Display information after assignment
print("Machine 1 finishes on the following times:")
for day, surplus in enumerate(machine1.surplus):
    print(f"Day {day + 1}: {17 + surplus}")
print(f"The total overtime for machine 1 in this month was {overtime_m1} hours.")

print("Machine 2 finishes on the following times:")
for day, surplus in enumerate(machine2.surplus):
    print(f"Day {day + 1}: {17 + surplus}")
print(f"The total overtime for machine 2 in this month was {overtime_m2} hours.")
