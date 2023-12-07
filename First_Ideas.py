class Patient:
    def __init__(self, call_date, call_time, category, appointment_date, 
                 appointment_time, scan_duration):
        self.call_date = call_date
        self.call_time = call_time
        self.category = category #can you see this?
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.scan_duration = scan_duration

    def display_info(self):
        print(f"Patient Category: {self.category}")
        print(f"Call Date and Time: {self.call_date} at {self.call_time}")
        print(f"Appointment Date and Time: {self.appointment_date} at {self.appointment_time}")
        print(f"Scan Duration: {self.scan_duration} hours")
        
    def get_appointement(self):
        appointment_date = min(call_date + 1, next_available_slot)
        appointment_time = [appointment_date, next_available_slot]

class Machine:
    def __init__(self, current_patient, next_available_slot):
        self.current_patient = current_patient
        self.next_available_slot = next_available_slot

next_available_slot = [date]

# Creating instances
patient_1 = Patient(1, 8.23, 1, 2, 8, 1)
patient_2 = Patient(1, 9.3, 2, 2, 9, 0.5)

# Calling patients
patient_1.display_info()
patient_2.display_info()

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
