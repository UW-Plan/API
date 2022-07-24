import requests
from API_KEY import API_KEY

def courses_request(term, subject, catalog_number):
    headers = {'x-api-key': API_KEY}
    response = requests.get(f"https://openapi.data.uwaterloo.ca/v3/ClassSchedules/1229/{subject}/{catalog_number}", headers = headers)
    return response.json()