import json
from model_call import grade

def grade_shoe(image_bytes):
    raw_response = grade(image_bytes)
    data = json.loads(raw_response)
    return data


#TODO: Add more custimazation options for grade parsing and UI

def parse_grade(score):
    print(score)
    if score <= 3:
        return 1.0
    elif score <= 5:
        return 2.0
    elif score <= 7:
        return 3.0
    elif score < 8.5:
        return 4.0
    else:
        print('!')
        return 5.0
    