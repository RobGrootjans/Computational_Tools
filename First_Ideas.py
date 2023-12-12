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
        machine.surplus += patient.scan_duration - slot_duration
    
# Machine initialization
machine1 = Machine()
machine2 = Machine()

# Old system
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

'''
next_available_slot = [date]

# Mean durations of scans:
# Type 1: 0.43 -> 30 mins 0.5
# Type 2: 0.67 -> 45 mins 0.75

# difference between actual duration and slot time = surplus
# sum of surplus is overtime

class Simulation:
    def __init__(self):
        self.current_time = 0 # Start simulation at the current time
        self.patient_queue = []  # Queue for incoming patients
        self.machines = [Machine(), Machine()]  # Two MRI machines

    def schedule_next_event(self):
        # Logic to determine the next event based on the current state of the system
        # This may involve determining the next patient arrival, scan start, etc.
        pass

    def run_simulation(self, end_time):
        while self.current_time < end_time:
            # Execute the next scheduled event
            self.schedule_next_event()
            # Advance the simulation time to the next event
            self.current_time = self.next_event_time

    def handle_patient_arrival(self, patient):
        # Logic to handle a new patient arriving and scheduling an appointment
        pass

    def handle_scan_start(self, machine):
        # Logic to handle the start of a scan on a machine
        pass

    def handle_scan_finish(self, machine):
        # Logic to handle the completion of a scan on a machine
        pass

# Example usage:
simulation = Simulation()

# Creating instances of the Patient class
patient_1 = Patient(datetime(2023, 8, 1, 8, 23), "Type_1", datetime(2023, 8, 2, 8, 0), 1)
patient_2 = Patient(datetime(2023, 8, 1, 9, 30), "Type_2", datetime(2023, 8, 2, 9, 0), 0.5)

# Enqueue patients for simulation
simulation.patient_queue.extend([patient_1, patient_2])

# Run the simulation for a specific time duration
end_time = datetime(2023, 8, 3, 17, 0)  # Example end time
simulation.run_simulation(end_time)
'''
