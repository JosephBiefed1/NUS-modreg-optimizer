import numpy as np

def visualize_timetable(best_schedule, e_learn_lectures):
    # Initialize constants
    NUM_DAYS = 5
    NUM_SLOTS = 18  # Assuming slots represent 30-minute intervals from 9 AM to 6 PM

    # Create a matrix for each day
    schedule_matrix = np.full((NUM_DAYS, NUM_SLOTS), ' ', dtype=str)
    for course, slots in best_schedule.items():
        for (day, start, end) in slots:
            schedule_matrix[day, start:end] = '1'

    for course, slot in e_learn_lectures.items():
        day, start, end = slot
        schedule_matrix[day, start:end] = 'H'

    # Print the schedule matrix for each day
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for i, day in enumerate(days):
        print(f"{day}:\n{schedule_matrix[i]}\n")

