import numpy as np

class Patient:
    def __init__(self, call_date, call_time, category, appointment_date, 
                 appointment_time, scan_duration):
        self.call_date = call_date
        self.call_time = call_time
        self.category = category
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.scan_duration = scan_duration

'''
    def display_info(self):
        print(f"Patient Category: {self.category}")
        print(f"Call Date and Time: {self.call_date} at {self.call_time}")
        print(f"Appointment Date and Time: {self.appointment_date} at {self.appointment_time}")
        print(f"Scan Duration: {self.scan_duration} hours")
'''
        
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

# Creating instances  
patient1 = Patient(1, 8.23, 1, None, None, 1)
patient2 = Patient(1, 9.3, 2, None, None, 0.5)
patient3 = Patient(1, 10, 1, None, None, 2)

patients = [patient1, patient2, patient3]

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
