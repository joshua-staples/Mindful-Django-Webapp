from datetime import datetime
import pandas as pd
import json
from hw_session.models import Hw_Data, Session_Data

# Getting the current time 
today = datetime.now().day
current_hour = str(datetime.now().hour)
current_mins = str(datetime.now().minute)
full_time = round(int(current_hour) + (int(current_mins)/60),2)

def sanitize():
    """Manipulates the data store in the hw_session database to be graphable. Formats some time variables and
    performs some basic arithmatic to show differences in start and end times."""
  
    #Setting up the dataframe we are going to use

    finish_time_mins = []
    finish_time_hours = []
    finish_time_days = []
    finish_times = []

    start_time_mins = []
    start_time_hours = []
    start_time_days = []
    start_times = []
    size = []


    

    session_data = pd.DataFrame(list(Session_Data.objects.all().values()))

    #Get the time the hw session ended

    for time in session_data['finish_time']:
        fin_min = time.minute
        fin_min = fin_min/60 
        fin_day = time.date().day
        fin_hour = time.hour - 7
        if fin_hour < 0:
            fin_hour = 24 + fin_hour
            fin_day = fin_day - 1
        float_fin_time = fin_hour + fin_min
        finish_time_mins.append(fin_min)
        finish_time_hours.append(fin_hour)
        finish_time_days.append(fin_day)
        finish_times.append(float_fin_time)

    #Get the time the hw session started

    for time in session_data['start_time']:
        json_start_time = json.loads(time)
        start_day = json_start_time['day']
        start_hour = json_start_time['hour']
        start_min = json_start_time['min']

        start_min = start_min/60
        float_start_time = start_hour + start_min

        start_time_days.append(start_day)
        start_time_hours.append(start_hour)
        start_time_mins.append(start_min)
        start_times.append(float_start_time)

        
    #Add the comparison data between the start time and finish time to the session_data df
    session_data['date_day'] = finish_time_days
    session_data['fin_time_hour'] = finish_time_hours
    session_data['fin_time_minutes'] = finish_time_mins
    session_data['finish_times'] = finish_times
    session_data['start_time_hours'] = start_time_hours
    session_data['start_time_minutes'] = start_time_mins
    session_data['start_times'] = start_times
    session_data['time_spent'] = session_data['finish_times'] - session_data['start_times']
    session_data["time_limit_mins"] = session_data["time_limit_mins"]/60
    session_data["time_goal"] = session_data['time_limit_hours'] + session_data['time_limit_mins']
    session_data["time_goal_met"] =  (session_data['time_spent'] / session_data['time_goal']) * 100
    session_data["assignment_goal_met"]= session_data["completed_count"]/session_data["selected_assignment_count"]

    

    """Graphing"""


    #Creating another instance of the hw session dataframe for graphing purposes
    graphable = session_data
    graphable['time_spent_mins'] = round(graphable['time_spent'] * 60)
    #Altering some aspects of the new dataframe for graphing purposes 
    for i in graphable['time_goal_met']:
        if i > 100:
            i = 100
        else:
            pass
    
    for time in graphable['time_goal_met']:
        size.append(20)
    graphable['size'] = size

    return graphable