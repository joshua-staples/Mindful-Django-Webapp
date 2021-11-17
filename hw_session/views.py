from django.http import request
from django.shortcuts import render, redirect
from .models import Hw_Data, Session_Data
from .forms import Sessionform
from canvasapi import Canvas
import threading
import json
import random
from datetime import datetime
import calendar


#------------------------------------------------------------------------------
# Gets all of the assignments for a given course
#------------------------------------------------------------------------------
def getCourseAssignments(course, results, lock):
    assignmentList = []
    results[course.id] = {
        "courseName": '',
        "assignments": []
        }
    
    # Get all upcoming assignments from canvas
    assignments = course.get_assignments(bucket='upcoming')

    # Loop through and populate assignmentList with data
    for assignment in assignments:
        assignmentList.append({
            "name" : assignment.name,
            "due_date" : assignment.due_at,
            "course" : course.name,
            "submitted" : assignment.has_submitted_submissions
        })

    # Any time we modify shared results obj use lock for protection
    with lock:
        results[course.id]['courseName'] = course.name
        # We only want the assignments that haven't been submitted yet
        results[course.id]['assignments'] = list(filter(lambda a: a['submitted'] == False, assignmentList))


#------------------------------------------------------------------------------
# Starts a thread for each course to get its assignments.
# The assignments are put into the results object as the threads
# rejoin the main thread. The results object is then returned.
# A lock is used to protect the results obj from race conditions.
#------------------------------------------------------------------------------
def getAllAssignments(courses):
    courseThreads = []
    results = {}
    lock = threading.Lock()

    # Create a thread for each course
    for course in courses:
        thread = threading.Thread(target=getCourseAssignments, args=(course, results, lock))
        courseThreads.append(thread)

    # Start each thread
    for thread in courseThreads:
        thread.start()

    # Wait for each thread to complete
    for thread in courseThreads:
        thread.join()

    return results


#------------------------------------------------------------------------------
# gets all hwdata and creates instances of Hw_Data data model class
#------------------------------------------------------------------------------
def getHWData():
    with open('./hw_session/static/accessToken.json') as file:
        # Get the user info from accessToken file
        userInfo = json.load(file)

    # Set up the canvas object
    API_URL = "https://byui.instructure.com"
    API_KEY = userInfo["token"]
    canvas = Canvas(API_URL, API_KEY)

    # Get the user from canvas object
    myUserID = userInfo["user_id"]
    user = canvas.get_user(myUserID)
    print(f"Getting {user.name}'s information...")


    # Gets all courses that the user is actively enrolled in
    courses = user.get_courses(enrollment_state="active")

    # Get all of the upcoming unsubmitted assignments for the user
    results = getAllAssignments(courses)
    tasks = []

    for course in results:
        for assignment in results[course]['assignments']:
            hw = Hw_Data(
                name=assignment['name'], 
                due_date=assignment['due_date'], 
                course=assignment['course'], 
                submitted=assignment['submitted'],
                )
            print('hw:', hw)
            hw.save()
            tasks.append(hw)
    return tasks


def refreshHwData():
    tasks = []
    hourOfReload = 0
    curHour = (datetime.now().hour % 12)
    print("curHour: ", curHour)
    allHwData = Hw_Data.objects.all()
    for assignment in allHwData:
        tasks.append(assignment)
        dateTimeOfReload = assignment.loaded_at
        hourOfReload = ((dateTimeOfReload.hour + 5) % 12)
        print("hourOfReload: ", hourOfReload)
    
    if curHour == hourOfReload:
        print("No need to reload")
        return tasks
    else:
        print("Reloaded Data")
        Hw_Data.objects.all().delete()
        return getHWData()

# Create your views here.
def home(request):
    if request.method == "POST":
        session_form = Sessionform(request.POST)
        if session_form.is_valid():
            session_form.save()
            print("Session form saved to DB")
        return redirect("/dashboard")
    #here

    hw_data = refreshHwData()
    for i in hw_data:
        print('---------------------------------------------')
        #Get the due date of the assignment to manipulate it
        reformed_datetime = str(i.due_date)
        assignment = str(i.name)
        print(assignment)

        #Parse the due date
        reformed_datetime = reformed_datetime.split(' ')
        time_due_str = reformed_datetime[1]
        time_due_str1 = time_due_str.split(':')

        # To get the hour right 
        hour = (int(time_due_str1[0]) + 5) % 12
        if hour == 0:
            hours = 12
            hour_due_str = str(hours)
            
        else:
            hours = hour
            hour_due_str = str(hours)
        # time = datetime()
        time = (hour_due_str + ':' + time_due_str1[1])

        #Getting the Month and day of the year 
        date_due = reformed_datetime[0]
        date_due = date_due.split('-')
        parsed_year, parsed_month, parsed_day = int(date_due[0]), int(date_due[1]), int(date_due[2])
        datetime_dueDate = datetime(parsed_year, parsed_month, parsed_day)
        # print(datetime_dueDate)

        dayNumber = calendar.weekday(parsed_year, parsed_month, parsed_day)
        days =["Monday", "Tuesday", "Wednesday", "Thursday",
                            "Friday", "Saturday", "Sunday"]
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        # print(parsed_month)
        final_month = (months[parsed_month -1])
        final_day = (days[dayNumber])
        i.due_date = final_day + ', ' + final_month + ' ' + str(parsed_year) + ' - ' + time
        print(str(i.due_date))

    context = {
        "hw_data" : hw_data,
        "session_form" : Sessionform()
    }
    return render(request, 'hw_session/index.html', context)


def create_session(request):
    return render(request, 'hw_session/running.html', context={})