import requests
import json
from datetime import datetime, timedelta
import numpy as np
import copy

from itertools import combinations

def save_timetables():
    print("Selecting timetables.......................")
    #mods = ['ES1103', 'CS1010E', 'MA1511', 'MA1512', 'EG1311', 'EE1111A']
    try:
        with open('select_mods.txt', 'r') as file:
            content = file.read().strip()  # Read and strip any extra whitespace
            mods = eval(content)  # Convert the string to a list
            
    except FileNotFoundError:
        print("The file 'select_mods.txt' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("Selected:", mods)
    acadYear = '2024-2025'
    timetables = {module: {'Tutorials': [], 'Lectures': [], 'E-Learn Lecture': []} for module in mods}

    for moduleCode in mods:
        req_str = f'https://api.nusmods.com/v2/{acadYear}/modules/{moduleCode}.json'
        try:
            output = requests.get(req_str)
            output.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            
            if output.text.strip():  # Check if response body is not empty
                response = output.json()
            else:
                print(f"No content in response for {moduleCode}")
                continue
            
            tutorials = []
            lectures = []
            e_learn_lec = []

            sem = "1"
            sem_dict = {'1': 0, '2': 1, '4': 2}
            
            semester = response.get('semesterData', [])[sem_dict[sem]]
            for timetable in semester.get('timetable', []):
                dayOfWeek = timetable.get('day')
                lesson_type = timetable.get('lessonType')
                if lesson_type == 'Tutorial' or lesson_type == 'Laboratory':
                    tutorials.append((dayOfWeek,timetable['startTime'], timetable['endTime']))
                elif lesson_type == 'Sectional Teaching' or lesson_type=='Lecture':
                    if str(timetable.get('venue', 'sssssss')).lower()[:7] == 'e-learn':
                        e_learn_lec.append((dayOfWeek,timetable['startTime'], timetable['endTime']))
                    else:
                        lectures.append((dayOfWeek,timetable['startTime'], timetable['endTime']))
                
            
                else:
                    print(f"Unknown lesson type: {lesson_type}")
                    
                
                        
            timetables[moduleCode]['Tutorials'] = tutorials
            timetables[moduleCode]['Lectures'] = lectures
            timetables[moduleCode]['E-Learn Lecture'] = e_learn_lec

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {moduleCode}: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for {moduleCode}: {e}")





    # Define the converter function
    def converter(day, start, end):
        day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}
        day = day_map.get(day, -1)
        
        if day == -1:
            raise ValueError("Invalid day provided")

        # Define the time format
        time_format = "%H%M"

        # Parse the time strings into datetime objects
        time1 = datetime.strptime(start, time_format)
        time2 = datetime.strptime(end, time_format)

        time0900 = datetime.strptime("0900", time_format)
        # Calculate the time difference
        start_index = (time1 - time0900).seconds // 1800
        end_index = (time2 - time0900).seconds // 1800

        return day, start_index, end_index



    # Convert the timetable entries
    for module in timetables:
        for session_type in ["Lectures", "Tutorials", "E-Learn Lecture"]:
            for i, session in enumerate(timetables[module][session_type]):
                day, start_time, end_time = session
                timetables[module][session_type][i] = converter(day, start_time, end_time)




    # Save the converted timetable back to the JSON file (optional)
    with open('timetables.json', 'w') as json_file:
        json.dump(timetables, json_file, indent=4)

    print("Timetables saved to timetables.json")
    print("_____________________________________________________________________________")
