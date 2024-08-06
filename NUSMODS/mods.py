import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
from scraper import scraper
from df_generate import generate_df
import re
from itertools import chain
pd.set_option('display.max_columns', None)


def mod_info():
    
        
    def get_units(df, mods):
        return df[df['moduleCode'].isin(mods)]['moduleCredit'].astype(int).sum()
        

    def check_similar(arr, arr2):
        #check common mods between common_curr and second_major
        uncommon = []
        common = []

        for i in arr:
            if isinstance(i, list):  # Check if the item is a list
                for j in i:
                    if j not in arr2:
                        uncommon.append(j)
                    else:
                        common.append(j)
            else:
                if i not in arr2:
                    uncommon.append(i)
                else:
                    common.append(i)
        #might need to remove variations//remove last letters 
        uncommon = [x.replace(' ', '') for x in uncommon]
        common = [x.replace(' ', '') for x in common]


        return common
    
    df = generate_df()
    
    # Scrape common curriculums
    common_curr, second_common_curr, second_elec_curr = scraper()
    
    
    
    
    common_curr = [x.replace(' ', '') if isinstance(x, str) else x for x in common_curr]
    second_common_curr = [x.replace(' ', '') if isinstance(x, str) else x for x in second_common_curr]
    second_elec_curr = [x.replace(' ', '') if isinstance(x, str) else x for x in second_elec_curr]
        
   
    
    def check_prerequisite(df, mods):
        
        return df[df['moduleCode'].isin(mods) & df['prerequisite'].notna()][['moduleCode', 'prerequisite']]    

    # Function to extract prerequisites
    def extract_prerequisites(sentence, course_set):
        # Initialize an empty list to store the prerequisites
        prerequisites = set()
        
        # Remove punctuation and split the sentence into words
        words = re.findall(r'\b\w+\b', sentence)
        
        # Check each word to see if it is in the set of course names
        for word in words:
            if word in course_set:
                prerequisites.add(word)
        
        return prerequisites

    
    def update_prerequisite(df, mods, prerequisites):
        # Continue looping until all prerequisites are found
        while True:
            return_df = check_prerequisite(df, mods)
            
            all_found = True
            
            for i in range(len(return_df)):
                prerequisite_sentence = return_df.iloc[i]['prerequisite']
                prerequisite = extract_prerequisites(prerequisite_sentence, course_names)
                
                if not prerequisite.issubset(prerequisites):
                    prerequisites.update(prerequisite)
                    all_found = False
            
            if all_found:
                break
                
            mods = list(prerequisites)

        
        return prerequisites
    
    def split_semesters(df):
        set_1 = set()
        set_2 = set()
        set_3 = set()
        set_both = set()
        set_unknown = set()

        for i in range(len(df)):
            if len(df.loc[i, 'semesterData']) > 0:
                if len(df.loc[i, 'semesterData']) >1:
                    set_both.add(df.loc[i, 'moduleCode'])
                elif len(df.loc[i, 'semesterData']) == 1:
                    sem_num = df.loc[i, 'semesterData'][0]['semester']
                    module_code = df.loc[i, 'moduleCode']
                    
                    if str(sem_num) == '1':
                        set_1.add(module_code)
                    elif str(sem_num) == '2': 
                        set_2.add(module_code)
                    elif str(sem_num) == '3':
                        set_3.add(module_code)
                    else:
                        set_unknown.add(module_code)
                else:
                    set_unknown.add(module_code)
        return set_1, set_2, set_3, set_both, set_unknown

    
    
    
    course_names = set(df['moduleCode'])

    df = generate_df()
    #common mods?????
    mods = common_curr + second_common_curr + second_elec_curr
    units = get_units(df, mods)
    print(units,"MCs")

    

    set_prerequisites = update_prerequisite(df, mods, set())
    set_prerequisites = {item: None for item in set_prerequisites}

    # Assuming 'set_prerequisites' is the dictionary you want to update
    for module_code in set_prerequisites.copy():
        sum = 0
        for i in df.loc[df['moduleCode'] == module_code, 'workload'].sum():
            sum += i

        set_prerequisites[module_code] = sum

    mc_prerequisite = {}  # Initialize an empty dictionary

    for module_code in set_prerequisites.keys():
        total_module_credit = df.loc[df['moduleCode'] == module_code, 'moduleCredit'].sum()
        mc_prerequisite[module_code] = total_module_credit



    

    # Create a dictionary based on unique values of mc_prerequisite
    unique_values = set(mc_prerequisite.values())
    unique_dict = {value: [] for value in unique_values}

    # Add moduleCode key from mc_prerequisite to the dictionary based on set_prerequisites value
    for module_code, total_module_credit in mc_prerequisite.items():
        unique_dict[total_module_credit].append(module_code)

    # Sort the dictionary based on set_prerequisites value from small to big
    sorted_unique_dict = {key: unique_dict[key] for key in sorted(unique_dict.keys())}

    # Create separate dictionaries for each row
    separate_dicts = []
    for total_module_credit, module_codes in sorted_unique_dict.items():
        row_dict = {
            "Units": total_module_credit,
            "Modules": module_codes
        }
        separate_dicts.append(row_dict)


    for i in range(len(separate_dicts)):
        separate_dicts[i]['Modules'] = {module_code: set_prerequisites.get(module_code) for module_code in separate_dicts[i]['Modules']}
    
    #rearrange
    for i in range(len(separate_dicts)):
       separate_dicts[i]['Modules'] = {k: v for k, v in sorted(separate_dicts[i]['Modules'].items(), key=lambda item: item[1])}

    
    for module in separate_dicts:
        print(f"Total Units: {module['Units']}")
        for code, credit in module['Modules'].items():
            print(f"  - {code}: Workload {credit} hrs")
        print()
    
    print("Total MCs:", get_units(df, set_prerequisites))

    common_mods_FMA_SMA = []
    common_mods_FMA_SMI = []
    common_mods_SMA_SMI = []
    common_mods_FMA_SMA.append(check_similar(common_curr, second_common_curr))
    common_mods_FMA_SMI.append(check_similar(common_curr, second_elec_curr))
    common_mods_SMA_SMI.append(check_similar(second_common_curr, second_elec_curr))
    module_set_1 = set(chain.from_iterable(common_mods_FMA_SMA))
    module_set_2 = set(chain.from_iterable(common_mods_FMA_SMI))
    module_set_3 = set(chain.from_iterable(common_mods_SMA_SMI))

    print("___________________________________________________________")
    print("Common modules between First Major and Second:", module_set_1)
    print("Total MCs:", get_units(df, module_set_1))
    print("Common modules between First Major and Second Minor:", module_set_2)
    print("Total MCs:", get_units(df, module_set_2))
    print("Common modules between Second Major and Second Minor:", module_set_3)
    print("Total MCs:", get_units(df, module_set_3))
    print("___________________________________________________________")

    ##split mods into sem 1 and/or sem2:
    #set is sem1, set2 is sem2, set3 is special term, set_both is both 1 and 2, set_unknown is sem data not known
    set1, set2, set3, set_both, set_unknown = split_semesters(df)

    print("For Overlapping modules")
    print('Modules In all semesters:', set_both.intersection(module_set_1), set_both.intersection(module_set_2), set_both.intersection(module_set_3))
    print('Modules In unknown semesters:', set_unknown.intersection(module_set_1), set_unknown.intersection(module_set_2), set_unknown.intersection(module_set_3))
    print("Modules Only in Semester 1:", set1.intersection(module_set_1), set1.intersection(module_set_2), set1.intersection(module_set_3))
    print("Modules Only in Semester 2:", set2.intersection(module_set_1), set2.intersection(module_set_2), set2.intersection(module_set_3))
    print("Modules Only in Special Term:", set3.intersection(module_set_1), set3.intersection(module_set_2), set3.intersection(module_set_3))

    print("___________________________________________________________")
    print("For Common Curriculum Modules")
    print('Modules In all semesters:', set_both.intersection(set(set_prerequisites.keys())))
    print('Modules In unknown semesters:', set_unknown.intersection(set(set_prerequisites.keys())))
    print("Modules Only in Semester 1:", set1.intersection(set(set_prerequisites.keys())))
    print("Modules Only in Semester 2:", set2.intersection(set(set_prerequisites.keys())))
    print("Modules Only in Special Term:", set3.intersection(set(set_prerequisites.keys())))

    print("___________________________________________________________")
