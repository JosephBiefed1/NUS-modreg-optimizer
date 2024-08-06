import random
import json
import numpy as np
from free_days import select_e_learn_lectures
from visualization import visualize_timetable


def run_script():
    # Load the timetable data from the JSON file
    with open('timetables.json', 'r') as json_file:
        timetables = json.load(json_file)

    # Initialize constants
    NUM_DAYS = 5
    NUM_SLOTS = 18  # Assuming slots represent 30-minute intervals from 9 AM to 6 PM

    # Fitness function
    def fitness_function(individual):
        schedule = np.zeros((NUM_DAYS, NUM_SLOTS), dtype=int)
        for course, slots in individual.items():
            for (day, start, end) in slots:
                schedule[day, start:end] = 1
        occupied_slots = np.sum(schedule)
        gaps = 0
        lunch_penalty = 0
        free_day_penalty = 0

        for day in range(NUM_DAYS):
            day_schedule = schedule[day]
            in_class = False
            for slot in range(NUM_SLOTS):
                if day_schedule[slot] == 1 and not in_class:
                    in_class = True
                elif day_schedule[slot] == 0 and in_class:
                    in_class = False
                    gaps += 1
            # Check for mandatory lunch break
            if any(day_schedule[2:11]) and not (day_schedule[2:11] == 0).any():
                lunch_penalty += 1

        # Check if the free day has any classes
        for day in FREE_DAY:
            if np.any(schedule[day]):
                free_day_penalty = 1000  # Large penalty for having classes on the free day

        num_days_with_classes = np.sum(np.any(schedule, axis=1))
        return occupied_slots - gaps - num_days_with_classes - lunch_penalty * 10 - free_day_penalty

    # Initialize population
    def initialize_population(timetable, population_size):
        population = []
        course_options = list(timetable.items())
        for _ in range(population_size):
            individual = {}
            for course, options in course_options:
                slots = []
                if options["Tutorials"]:
                    valid_tutorials = [t for t in options["Tutorials"] if t[0] not in FREE_DAY]
                    if valid_tutorials:
                        slots.append(tuple(random.choice(valid_tutorials)))
                if options["Lectures"]:
                    valid_lectures = [l for l in options["Lectures"] if l[0] not in FREE_DAY]
                    if valid_lectures:
                        slots.append(tuple(random.choice(valid_lectures)))

                individual[course] = slots
            population.append(individual)
        return population

    # Crossover function
    def crossover(parent1, parent2):
        child1, child2 = {}, {}
        for course in parent1.keys():
            if random.random() > 0.5:
                child1[course] = parent1[course]
                child2[course] = parent2[course]
            else:
                child1[course] = parent2[course]
                child2[course] = parent1[course]
        return child1, child2

    # Mutation function
    def mutate(individual, mutation_rate, timetable):
        for course in individual.keys():
            if random.random() < mutation_rate:
                slots = []
                if timetable[course]["Tutorials"]:
                    valid_tutorials = [t for t in timetable[course]["Tutorials"] if t[0] not in FREE_DAY]
                    if valid_tutorials:
                        slots.append(tuple(random.choice(valid_tutorials)))
                if timetable[course]["Lectures"]:
                    valid_lectures = [l for l in timetable[course]["Lectures"] if l[0] not in FREE_DAY]
                    if valid_lectures:
                        slots.append(tuple(random.choice(valid_lectures)))
                individual[course] = slots
        return individual

    # Genetic algorithm
    def genetic_algorithm(timetable, population_size=100, generations=1000, mutation_rate=0.01):
        population = initialize_population(timetable, population_size)
        for generation in range(generations):
            population = sorted(population, key=fitness_function, reverse=True)
            next_generation = population[:population_size // 2]
            while len(next_generation) < population_size:
                parent1, parent2 = random.sample(next_generation, 2)
                child1, child2 = crossover(parent1, parent2)
                child1 = mutate(child1, mutation_rate, timetable)
                child2 = mutate(child2, mutation_rate, timetable)
                next_generation += [child1, child2]
            population = next_generation
        best_individual = max(population, key=fitness_function)
        return best_individual, fitness_function(best_individual)

    # Run the genetic algorithm

    #select free days
    selected_e_learn_lectures = select_e_learn_lectures(timetables)
    print("Selected E-learn Lectures:", selected_e_learn_lectures)

    FREE_DAY = set()
    for options in selected_e_learn_lectures.values():
        FREE_DAY.add(options[0])
    # The day that should be free (e.g., day 3)



    converter = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4}

    other_free_days = input("Any other day you want to be free? Example: Monday. If no, add None: ")


    if other_free_days.lower() == 'none' or not other_free_days:
        pass
    else:
        try:
            x = converter[other_free_days.lower()]
            FREE_DAY.add(x)
        except KeyError:
            print("Invalid day provided")
    best_schedule, best_fitness = genetic_algorithm(timetables)

    print("Best Schedule:", best_schedule)
    print("Best Fitness:", best_fitness)

    visualize_timetable(best_schedule, selected_e_learn_lectures)
    