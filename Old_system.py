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


    def display_info(self):
        print(f"Patient Category: {self.category}")
        print(f"Call Date and Time: {self.call_date} at {self.call_time}")
        print(f"Appointment Date and Time: {self.appointment_date} at {self.appointment_time}")
        print(f"Scan Duration: {self.scan_duration} hours")

        
class Machine:
    def __init__(self):
        self.current_patient = None
        self.next_available_slot = np.full([num_days + 1,1],8, dtype=float)
        self.surplus = np.zeros([num_days + 1,1], dtype=float)

def schedule_appointment(machine, patient, slot_duration):
    patient.appointment_date = patient.call_date + 1
    patient.appointment_time = machine.next_available_slot[patient.appointment_date]
    machine.next_available_slot[patient.appointment_date] += slot_duration
    if patient.scan_duration > slot_duration:
        machine.surplus[patient.appointment_date] += patient.scan_duration - slot_duration   # difference between actual duration and slot time = surplus

def generate_data(num_days, start_time, end_time, mean_num_type1, mean_num_type2,
                  mean_duration_type1, shape_duration_type2, std_duration_type1,
                  scale_duration_type2, lambda_tbc_type1, mean_tbc_type2, std_tbc_type2):
    
    np.random.seed(42) # for reproducibility
    data = []
    
    for day in range(1, num_days + 1):
        current_time = start_time
        
        while current_time < end_time:
            # Generate number of type1 calls a day
            num_type1 = np.random.poisson(mean_num_type1)
            # Generate call times
            call_intervals_type1 = np.random.exponential(1/lambda_tbc_type1, size=num_type1)
            for interval in call_intervals_type1:
                current_time += interval
                if start_time <= current_time <= end_time:
                    call_date = day
                    call_time = current_time
                    category = 1
                    scan_duration = np.random.normal(mean_duration_type1, std_duration_type1)
                    data.append([call_date, call_time, category, None, None, scan_duration])
                else:
                    break
        
        current_time = start_time
        
        while current_time < end_time:
            num_type2 = np.random.poisson(mean_num_type2)
            call_intervals_type2 = np.random.normal(mean_tbc_type2, std_tbc_type2, num_type2)
            for interval in call_intervals_type2:
                current_time += interval
                if start_time <= current_time <= end_time:
                    call_date = day
                    call_time = current_time
                    category = 2
                    scan_duration = np.random.gamma(shape_duration_type2, scale_duration_type2)
                    data.append([call_date, call_time, category, None, None, scan_duration])
                else:
                    break
            
    return pd.DataFrame(data, columns=['Day', 'Time', 'PatientType', 'AppointmentDate', 'AppointmentTime', 'Duration'])

def calculate_overtime(machine, machine_name, end_time):
    # Initialize overtime
    overtime_total = 0
    
    # Print overtime for each day and total overtime
    print(f"{machine_name} finishes with a delay of:")
    for day, surplus in enumerate(machine.surplus):
        surplus_day = machine.next_available_slot[day][0] + surplus[0] - end_time
        if surplus_day > 0:
            overtime_total += surplus_day
            print(f"Day {day + 1}: {surplus_day} hours")
        else:
            surplus_day = 0
            print(f"Day {day + 1}: {surplus_day} hours")
    print(f"The total overtime for {machine_name} this month was {overtime_total} hours.\n")

# Generating data
num_days = 31
start_time = 8                      # assuming calls can be made between 8 AM and 5 PM
end_time = 17
mean_num_type1 = 16.47826
mean_num_type2 = 12.87234
mean_duration_type1 = 0.43
std_duration_type1 = 0.09777424
shape_duration_type2 = 1.136300 
scale_duration_type2 = 1.731915
lambda_tbc_type1 = 1.835622         # tbc = time between calls
mean_tbc_type2 = 0.8666245
std_tbc_type2 = 0.3114448

# Machine initialization
machine1 = Machine()
machine2 = Machine()

# Slot_durations
slot_duration_t1 = 0.2
slot_duration_t2 = 0.2

data_df = generate_data(num_days, start_time, end_time, mean_num_type1, mean_num_type2,
                        mean_duration_type1, shape_duration_type2, std_duration_type1,
                        scale_duration_type2, lambda_tbc_type1, mean_tbc_type2, std_tbc_type2)

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
calculate_overtime(machine1, "Machine 1", end_time)
calculate_overtime(machine2, "Machine 2", end_time)
