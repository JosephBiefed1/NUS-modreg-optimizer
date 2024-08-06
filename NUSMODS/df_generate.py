import json
import pandas as pd



def generate_df():
    with open('data.json', 'r', encoding='utf-8') as f:

        
        data = json.load(f)
    
    df = pd.DataFrame(data)
    #filter out engineering and cs modules
    """ 
    arr = []
    input = ['College of Design and Engineering', 'Computing', 'Multi Disciplinary Programme']

    for i in range(len(data)):
        if (data[i]['faculty'] in input):
        
            arr.append(data[i])  

    filter_arr =[]
    input = [
    'CDE Dean"s Office', 
    'Centre of Engl Lang Comms', 
    'Computer Science',
    'Computing and Engineering Programme',
    'Electrical and Engineering Programme',
    'Mathematics',
    'Physics'

    ]
    for i in data:
        if (i['department'] in input):
            filter_arr.append(i)

     
    with open('filter.json', 'w', encoding='utf-8') as f:
        json.dump(filter_arr, f)

     
    #filter out engineering and cs modules
    #filter out engineering and cs modules

    # Create the DataFrame using list comprehensions with default values
    df = pd.DataFrame({
    'moduleCode': [item.get('moduleCode', 'Unknown') for item in data],
    'description': [item.get('description', 'No description') for item in data],
    'MCredit': [item.get('moduleCredit', 0) for item in data],
    'department': [item.get('department', 'Unknown') for item in data],
    'faculty': [item.get('faculty', 'Unknown') for item in data],
    'workload_1': [item.get('workload', [None]*5)[0] if item.get('workload') and len(item['workload']) > 0 else None for item in data],
    'workload_2': [item.get('workload', [None]*5)[1] if item.get('workload') and len(item['workload']) > 1 else None for item in data],
    'workload_3': [item.get('workload', [None]*5)[2] if item.get('workload') and len(item['workload']) > 2 else None for item in data],
    'workload_4': [item.get('workload', [None]*5)[3] if item.get('workload') and len(item['workload']) > 3 else None for item in data],
    'workload_5': [item.get('workload', [None]*5)[4] if item.get('workload') and len(item['workload']) > 4 else None for item in data],
    'prerequisites': [item.get('prerequisites', 'None') for item in data],
    'preclusion': [item.get('preclusion', 'None') for item in data],
    'co-requisites': [item.get('co-requisites', 'None') for item in data]
    })

    #create prerequisite columns
    #need to filter the prerequisite into readable texts


    """

    df.to_csv('data.csv', index=False)

    return df
