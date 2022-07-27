import requests
import json
import math


class RateMyProfScraper:
    def __init__(self, schoolid):
        self.UniversityId = schoolid
        self.professorlist = self.createprofessorlist()
        self.indexnumber = False

    # creates List object that include basic information on all Professors from the IDed University
    def createprofessorlist(self):
        tempprofessorlist = []
        num_of_prof = self.GetNumOfProfessors(self.UniversityId)
        num_of_pages = math.ceil(num_of_prof / 20)
        i = 1
        while (i <= num_of_pages):  # the loop insert all professor into list
            page = requests.get("http://www.ratemyprofessors.com/filter/professor/?&page=" + str(
                i) + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                self.UniversityId))
            temp_jsonpage = json.loads(page.content)
            temp_list = temp_jsonpage['professors']
            tempprofessorlist.extend(temp_list)
            i += 1
        return tempprofessorlist

    # function returns the number of professors in the university of the given ID.
    def GetNumOfProfessors(self, id):
        page = requests.get(
            "http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                id))  # get request for page
        temp_jsonpage = json.loads(page.content)
        num_of_prof = temp_jsonpage[
            'remaining'] + 20  # get the number of professors at William Paterson University
        return num_of_prof

    def SearchProfessor(self, ProfessorName):
        self.indexnumber = self.GetProfessorIndex(ProfessorName)
        self.PrintProfessorInfo()
        return self.indexnumber

    # function searches for professor in list
    def GetProfessorIndex(self, ProfessorName):
        for i in range(0, len(self.professorlist)):
            if (ProfessorName == (self.professorlist[i]['tFname'] + " " + self.professorlist[i]['tLname'])):
                return i
        return False  # Return False is not found

    def PrintProfessorInfo(self):  # print search professor's name and RMP score
        if self.indexnumber == False:
            print("error")
        else:
            print(self.professorlist[self.indexnumber])

    # print search professor's name and RMP score
    def PrintProfessorDetail(self, key):
        if self.indexnumber == False:
            print("error")
            return "error"
        else:
            print(self.professorlist[self.indexnumber][key])
            return self.professorlist[self.indexnumber][key]


universityOfWaterloo = RateMyProfScraper(1490)  # 1490 is UW SID
professorList = universityOfWaterloo.professorlist
print(professorList[0])


sample = {'tDept': 'Mathematics', 'tSid': '1490', 'institution_name': 'University of Waterloo',
          'tFname': 'Lei Lei', 'tMiddlename': '', 'tLname': 'Zeng', 'tid': 1753851, 'tNumRatings': 18,
          'rating_class': 'average', 'contentType': 'TEACHER', 'categoryType': 'PROFESSOR', 'overall_rating': '3.2'}


# WilliamPatersonUniversity.SearchProfessor("Cyril Ku")
# WilliamPatersonUniversity.PrintProfessorDetail("overall_rating")

# MassInstTech = RateMyProfScraper(580)
# MassInstTech.SearchProfessor("Robert Berwick")
# MassInstTech.PrintProfessorDetail("overall_rating")
