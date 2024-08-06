import random
import numpy as np
import json






def select_e_learn_lectures(timetables):
    NUM_DAYS = 5

    e_learn_lectures = {}
    day_slots = {day: [] for day in range(NUM_DAYS)}
    
    timetable = {}
    for mod in timetables:
        if len(timetables[mod]['E-Learn Lecture']) != 0:
            timetable[mod] = timetables[mod]['E-Learn Lecture']
            
    # Group e-learning lectures by day
    for course, options in timetable.items():
        if options:
            for option in options:
                day = option[0]
                day_slots[day].append((course, option))

    # Select non-overlapping lectures from the same day
    for day, slots in day_slots.items():
        selected_slots = []
        for course, option in slots:
            if not any(start < option[2] and option[1] < end for _, (d, start, end) in selected_slots):
                selected_slots.append((course, option))
                e_learn_lectures[course] = option

    # Randomly select remaining lectures
    for course, options in timetable.items():
        if course not in e_learn_lectures and options:
            e_learn_lectures[course] = random.choice(options)

    return e_learn_lectures


    

