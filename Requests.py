from operator import pos
import requests
import os
import gc
from dotenv import load_dotenv
load_dotenv()
from ScheduleManager import isClassClashing

baseURL = "https://openapi.data.uwaterloo.ca/v3/ClassSchedules"

def schedule_request(term, args):
    headers = {'x-api-key': os.getenv('OPEN_DATA_API_KEY')}
    coursePayloadsFetched = []

    for i in range(1,8):
        subject = f"subject_{i}"
        catalog_number = f"catalog_number_{i}"
        if args[subject] is not None and args[catalog_number] is not None:
            try:
                subjectName = args[subject].upper()
                catalogNumber = args[catalog_number].upper()
                course_name = f"{subjectName} {catalogNumber}"
                response = requests.get(f"{baseURL}/{term}/{subjectName}/{catalogNumber}", headers = headers)
                if response.status_code == 200:
                    coursePayloadsFetched.append([course_name, createCoursePayloadFromCourseSchedule(response.json())])
                else:
                    return ['Error: Try again later']
            except requests.exceptions.RequestException:
                return ['Error: Try again later']
        else:
            break
    return createClassSchedule(coursePayloadsFetched)


def createClassSchedule(coursePayloads):
    
    def areCoursesClashing(course1, course2):
        for courseComponentName1 in course1:
            for courseComponent1 in course1[courseComponentName1]: 
                for courseComponentName2 in course2:
                    for courseComponent2 in course2[courseComponentName2]:
                        if isClassClashing(courseComponent1["scheduleData"], courseComponent2["scheduleData"]):
                            return True
        return False

    classScheduleListToReturn = []

    for coursePayload in coursePayloads:
        if classScheduleListToReturn == []:
            for course in courseToAdd(coursePayload[1]):
                classScheduleListToReturn.append({coursePayload[0]: course})
        else:
            temporaryClassScheduleList = classScheduleListToReturn
            classScheduleListToReturn = []
            for classSchedule in temporaryClassScheduleList:
                for courseNameInSchedule in classSchedule:
                    for course in courseToAdd(coursePayload[1]):
                        if not areCoursesClashing(classSchedule[courseNameInSchedule], course):
                            newClassSchedule = classSchedule.copy()
                            newClassSchedule[coursePayload[0]] = course
                            classScheduleListToReturn.append(newClassSchedule)

    tutorialClassListToReturn = {}
    for coursePayload in coursePayloads:
        if "TUT" in coursePayload[1]:
            tutorialClassListToReturn[coursePayload[0]] = coursePayload[1]["TUT"]

    finalDictToReturn = {"length": len(classScheduleListToReturn),"classSchedules": classScheduleListToReturn, "tutorialClasses": tutorialClassListToReturn}

    return finalDictToReturn

def createCoursePayloadFromCourseSchedule(inputSchedule):

    courseComponentKeysToExclude = [
        "classSection",
        "maxEnrollmentCapacity",
        "enrolledStudents",
        "courseId",
        "courseOfferNumber",
        "sessionCode",
        "termCode",
        "classNumber",
        "associatedClassCode",
        "enrollConsentCode",
        "enrollConsentDescription",
        "dropConsentCode",
        "dropConsentDescription",
    ]

    courseComponentScheduleDataKeysToExclude = [
        "classSection",
        "courseId",
        "courseOfferNumber",
        "sessionCode",
        "termCode",
        "classMeetingNumber",
        "classMeetingDayPatternCode",
        "instructorRoleCode",
        "instructorUniqueIdentifier"
    ]

    def removeScheduleDataKeys(courseComponent):
        if courseComponent['scheduleData'] is not None:
            for i in range(len(courseComponent['scheduleData'])):
                for courseComponentScheduleDataKey in courseComponentScheduleDataKeysToExclude:
                    if courseComponentScheduleDataKey in courseComponent['scheduleData'][i]:
                        del courseComponent['scheduleData'][i][courseComponentScheduleDataKey]
        if courseComponent['instructorData'] is not None:
            for i in range(len(courseComponent['instructorData'])):
                for courseComponentScheduleDataKey in courseComponentScheduleDataKeysToExclude:
                    if courseComponentScheduleDataKey in courseComponent['instructorData'][i]:
                        del courseComponent['instructorData'][i][courseComponentScheduleDataKey]
        return courseComponent

    coursePayloadDictionary = {}

    for inputCourseComponent in inputSchedule:

        courseComponent = { key:inputCourseComponent[key] for key in inputCourseComponent if key not in courseComponentKeysToExclude}
        courseComponent = removeScheduleDataKeys(courseComponent)

        if courseComponent['courseComponent'] in coursePayloadDictionary:
            coursePayloadDictionary[courseComponent['courseComponent']].append(courseComponent)
        else:
            coursePayloadDictionary[courseComponent['courseComponent']] = [courseComponent]

    return coursePayloadDictionary

def courseToAdd(coursePayload):

    def isCourseAndCourseComponentClashing(course, externalCourseComponent):
        for courseComponentName in course:
            for courseComponent in course[courseComponentName]:
                if isClassClashing(courseComponent["scheduleData"], externalCourseComponent["scheduleData"]):
                    return True
        return False

    listOfCourseComponentsOffered = []
    courseListToReturn = []

    for courseComponentName in coursePayload:
        listOfCourseComponentsOffered.append(courseComponentName)

    if "TUT" in listOfCourseComponentsOffered:
        listOfCourseComponentsOffered.remove("TUT")

    for courseComponentName in listOfCourseComponentsOffered:
        if courseComponentName == "TST":
            if courseListToReturn == []:
                courseListToReturn.append({courseComponentName: coursePayload[courseComponentName]})
            else:
                temporaryCourseList = courseListToReturn
                courseListToReturn = []
                for course in temporaryCourseList:
                    newCourse = course.copy()
                    newCourse[courseComponentName] = coursePayload[courseComponentName]
                    courseListToReturn.append(newCourse)
        else:
            if courseListToReturn == []:
                for course in coursePayload[courseComponentName]:
                    courseListToReturn.append({courseComponentName: [course]})
            else:
                temporaryCourseList = courseListToReturn
                courseListToReturn = []
                for courseComponent in coursePayload[courseComponentName]:
                    for course in temporaryCourseList:
                        if not isCourseAndCourseComponentClashing(course, courseComponent):
                            newCourse = course.copy()
                            newCourse[courseComponentName] = [courseComponent]
                            courseListToReturn.append(newCourse)
    return courseListToReturn
        
'''
    courseComponent = {
        "courseComponent": "TST",
        "scheduleData": [],
        ...
    }

    course = {
        "TST": [
            courseComponent_1,
            ...
            ],
        "LEC": [
            courseComponent_1,
            ],
        ...
    }

    coursePayload = {
        "TST": [
            courseComponent_1,
            ...
            courseComponent_n
            ],
        "LEC": [
            courseComponent_1,
            ...
            courseComponent_n
            ],
        ...
    }

    courseSchedule = {
        courseComponent_1,
        ...
        courseComponent_n
    }
'''
