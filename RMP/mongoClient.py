from pymongo import MongoClient
from RMP import professorList

# RUN docker-compose file in MONGO folder first using "docker-compose up"

client = MongoClient("mongodb://UW_PLAN:password@localhost:27018")
db = client.professors
x = 0
for i in professorList:
    if i["tMiddlename"] != "":
        name = i["tFname"].lower() + " " + i["tMiddlename"].lower() + " "+ i['tLname'].lower()
    else:
        name = i["tFname"].lower() + " " + i['tLname'].lower()
    
    entries = {'tDept': i["tDept"],
                'name': name,
               'tFname': i["tFname"],
               'tMiddlename': i["tMiddlename"],
               'tLname': i['tLname'],
               'tNumRatings': i["tNumRatings"],
               'classRatings': i["rating_class"],
               'designation': i['categoryType'],
               'prof_rating': i['overall_rating']}
    x += 1
    result = db.data.insert_one(entries)
    print('Created {0} of {1} as {2}'.format(
        x, len(professorList), result.inserted_id))

print("done")
