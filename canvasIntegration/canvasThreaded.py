from canvasapi import Canvas
import threading
import json

def getCourseAssignments(course, results, lock):
    print(course.id)
    results[course.id] = {
        "courseName": '',
        "assignments": []
        }
    assignments = course.get_assignments(bucket='upcoming')
    for assignment in assignments:
        with lock:
            results[course.id]['courseName'] = course.name
            results[course.id]['assignments'].append(assignment.name)


def printAssignments(courses):
    courseThreads = []
    results = {}
    lock = threading.Lock()
    for course in courses:
        thread = threading.Thread(target=getCourseAssignments, args=(course, results, lock))
        courseThreads.append(thread)

    for thread in courseThreads:
        thread.start()

    for thread in courseThreads:
        thread.join()

    # print(results)

    for course in courses:
        if results[course.id]['assignments'] != []:
            print(results[course.id])

def main():
    tokenJSON = {}
    with open('accessToken.json') as file:
        tokenJSON = json.load(file)

    API_URL = "https://byui.instructure.com"
    API_KEY = tokenJSON["token"]
    canvas = Canvas(API_URL, API_KEY)
    myUserID = 167103

    user = canvas.get_user(myUserID)
    print(user)

    courses = user.get_courses()

    printAssignments(courses)

main()