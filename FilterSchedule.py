def removeMergedClassSchedules(classScheduleList, classSchedulesToRemove):
    del classScheduleList[0]
    for classSchedule in classSchedulesToRemove:
        classScheduleList.remove(classSchedule)
    return classScheduleList

filteredClassScheduleList = []

def mergeClassSchedules(classSchedule, classScheduleList):
    for classScheduleToMerge in classScheduleList:
        for i in range(len(classSchedule)):
            for course in classScheduleToMerge:
                classSchedule[i]["TUT"].extend(course["TUT"])
    filteredClassScheduleList.append(classSchedule)

def courseHasDifferentNonTutorialClassTimings(course1, course2):
    courseComponentName1List = []
    courseComponentName2List = []

    for courseComponentName in course1:
        courseComponentName1List.append(courseComponentName)

    for courseComponentName in course2:
        courseComponentName2List.append(courseComponentName)
    
    if set(courseComponentName1List) != set(courseComponentName2List):
        return True
    else:
        if "TUT" not in courseComponentName1List:
            return True
        else:
            for courseComponentName in course1:
                if courseComponentName != "TUT":
                    if course1[courseComponentName] != course2[courseComponentName]:
                        return True
            return False

def classScheduleHasSameNonTutorialClass(classSchedule1, classSchedule2):
    if len(classSchedule1) == len(classSchedule2):
        for i in range(len(classSchedule1)):
            if courseHasDifferentNonTutorialClassTimings(classSchedule1[i], classSchedule2[i]):
                return False
        return True
    else:   
        return False

def filterClassSchedules(classScheduleList):

    while classScheduleList:
        print(len(classScheduleList))

        classSchedulesToMerge = []
        for classSchedule in  classScheduleList[1:]:
            if classScheduleHasSameNonTutorialClass(classSchedule, classScheduleList[0]):
                classSchedulesToMerge.append(classSchedule)
                
        print(len(classSchedulesToMerge))

        mergeClassSchedules(classScheduleList[0], classSchedulesToMerge)
        classScheduleList = removeMergedClassSchedules(classScheduleList, classSchedulesToMerge)
                    
    return filteredClassScheduleList




''''''''''''


def schedule_request(term, args):
    headers = {'x-api-key': os.getenv('OPEN_DATA_API_KEY')}
    coursePayloadsFetched = []

    for i in range(1,8):
        subject = f"subject_{i}"
        catalog_number = f"catalog_number_{i}"
        if args[subject] is not None:
            try:
                response = requests.get(f"{baseURL}/{term}/{args[subject]}/{args[catalog_number]}", headers = headers)
                coursePayloadsFetched.append(createCoursePayloadFromCourseSchedule(response.json()))
            except requests.exceptions.RequestException:
                return ['Error: Try again later']
        else:
            break
    # return coursePayloadsFetched
    listTo = createClassSchedule(coursePayloadsFetched)
    # print(listTo[0])
    return listTo


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
            for course in courseToAdd(coursePayload):
                classScheduleListToReturn.append([course])
        else:
            temporaryClassScheduleList = classScheduleListToReturn
            classScheduleListToReturn = []
            for classSchedule in temporaryClassScheduleList:
                for courseInSchedule in classSchedule:
                    for course in courseToAdd(coursePayload):
                        if not areCoursesClashing(courseInSchedule, course):
                            newClassSchedule = classSchedule.copy()
                            newClassSchedule.append(course)
                            classScheduleListToReturn.append(newClassSchedule)
        print("Completed 1 coursePayload")
    print("Completed all coursePayloads ... about to return")
    return classScheduleListToReturn



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

