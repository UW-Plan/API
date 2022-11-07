import datetime

def isClassClashing(scheduleData1, scheduleData2):
    for class1 in scheduleData1:
        for class2 in scheduleData2:
            if hasSimilarMeetingWeekPattern(class1, class2):
                if hasClashingDates(class1, class2):
                    class1StartTime = datetime.datetime.fromisoformat(class1["classMeetingStartTime"])
                    class1EndTime = datetime.datetime.fromisoformat(class1["classMeetingEndTime"])
                    class2StartTime = datetime.datetime.fromisoformat(class2["classMeetingStartTime"])
                    class2EndTime = datetime.datetime.fromisoformat(class2["classMeetingEndTime"])
                    if hasTimeClashing(class1StartTime, class1EndTime, class2StartTime, class2EndTime):
                        return True
                else:
                    return False
    return False


def hasSimilarMeetingWeekPattern(class1, class2):
    meetingWeekPatternArrayClass1 = list(class1["classMeetingWeekPatternCode"])
    meetingWeekPatternArrayClass2 = list(class2["classMeetingWeekPatternCode"])
    for i in range(7):
        if meetingWeekPatternArrayClass1[i] == 'Y' and meetingWeekPatternArrayClass2[i] == 'Y':
            return True
    return False

def hasTimeClashing(startTime1, endTime1, startTime2, endTime2):
    if startTime1 <= startTime2 and endTime1 <= endTime2 and endTime1 <= startTime2:
        return False
    elif startTime2 <= startTime1 and endTime2 <= endTime1 and endTime2 <= startTime1:
        return False
    else:
        return True

def hasClashingDates(scheduleData1, scheduleData2):
    scheduleStartDate1 = datetime.datetime.fromisoformat(scheduleData1["scheduleStartDate"])
    scheduleEndDate1 = datetime.datetime.fromisoformat(scheduleData1["scheduleEndDate"])
    scheduleStartDate2 = datetime.datetime.fromisoformat(scheduleData2["scheduleStartDate"])
    scheduleEndDate2 = datetime.datetime.fromisoformat(scheduleData2["scheduleEndDate"])
    
    if scheduleStartDate1 <= scheduleStartDate2 and scheduleEndDate1 >= scheduleEndDate2:
        return True
    elif scheduleStartDate2 <= scheduleStartDate1 and scheduleEndDate2 >= scheduleEndDate1:
        return True
    else:
        return False


# scheduleData1 = [
#                     {
#                         "courseId": "006878",
#                         "courseOfferNumber": 1,
#                         "sessionCode": "1",
#                         "classSection": 101,
#                         "termCode": "1229",
#                         "classMeetingNumber": 1,
#                         "scheduleStartDate": "2022-10-17T00:00:00",
#                         "scheduleEndDate": "2022-10-17T00:00:00",
#                         "classMeetingStartTime": "2022-08-01T19:00:00",
#                         "classMeetingEndTime": "2022-08-01T20:50:00",
#                         "classMeetingDayPatternCode": "M",
#                         "classMeetingWeekPatternCode": "YNNNNNN",
#                         "locationName": ""
#                     },
#                     {
#                         "courseId": "006878",
#                         "courseOfferNumber": 1,
#                         "sessionCode": "1",
#                         "classSection": 101,
#                         "termCode": "1229",
#                         "classMeetingNumber": 2,
#                         "scheduleStartDate": "2022-11-14T00:00:00",
#                         "scheduleEndDate": "2022-11-14T00:00:00",
#                         "classMeetingStartTime": "2022-08-01T19:00:00",
#                         "classMeetingEndTime": "2022-08-01T20:50:00",
#                         "classMeetingDayPatternCode": "M",
#                         "classMeetingWeekPatternCode": "YNNNNNN",
#                         "locationName": ""
#                     }
#                 ]

# scheduleData2 = [
#                     {
#                         "courseId": "006878",
#                         "courseOfferNumber": 1,
#                         "sessionCode": "1",
#                         "classSection": 6,
#                         "termCode": "1229",
#                         "classMeetingNumber": 1,
#                         "scheduleStartDate": "2022-09-07T00:00:00",
#                         "scheduleEndDate": "2022-12-06T00:00:00",
#                         "classMeetingStartTime": "2022-08-01T10:30:00",
#                         "classMeetingEndTime": "2022-08-01T11:20:00",
#                         "classMeetingDayPatternCode": "MWF",
#                         "classMeetingWeekPatternCode": "YNYNYNN",
#                         "locationName": "RCH 204"
#                     }
#                 ]

# print(isClassClashing(scheduleData1, scheduleData2))

