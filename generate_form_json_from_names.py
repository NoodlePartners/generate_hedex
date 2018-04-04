#!/usr/bin/python3
from names import Names
from addresses import Addresses
from emails import Emails
from rand import Rand
from dates import Dates
import sys
import json
import datetime

_birthday_start_date = "1990-10-10"
_birthday_n_days = 5 * 365

data_rows = [
    ("First","Last","Birthdate","Postal","Mobile Phone","Email"),
    ("Kelsey","Brown","","","+1 935-226-0970","kbrown24@aol.com"),
    ("Matthew TEST","Burris TEST","2000-01-21","97204-3735","212-555-1212","mburris@technolutions.com"),
    ("Jake (Test - Non-Admin)","Campbell (Test - Non-Admin)","1985-04-08","97204-3734","212-555-1213","harold.campbell@cgu.edu"),
    ("Jake (Test)","Campbell (Test)","1985-04-08","97204-3733","212-555-1214","Jake.Campbell@cgu.edu"),
    ("Nick TEST","Conte TEST","2000-02-29","SW1A 2AA","212-555-1215","nconte@technolutions.com"),
    ("Nick TEST","Conte TEST","2000-02-29","06510-1804","212-555-1216","nconte@technolutions.com"),
    ("Timothy","Council","1984-02-09","","212-555-1217","timothycouncil@gmail.com"),
    ("Steve TEST","Dailey TEST","2000-11-22","06510-1804","212-555-1218","sdailey@technolutions.com"),
    ("King TEST","Eliza TEST","2001-06-25","06510-1804","212-555-1219","eking@technolutions.com"),
    ("Jonathan","Fisher","","","+1 654-417-8765","jfisher38@mail.com"),
    ("Andrew","Flock TEST","2000-01-22","97204-3735","212-555-1220","dflock@technolutions.com"),
    ("Drew","Flock TEST","2000-01-22","97204-3735","212-555-1221","dflock@technolutions.com"),
    ("Nathan TEST","Gault TEST","2000-01-20","06510-1804","212-555-1222","ngault@technolutions.com"),
    ("Erin TEST","Gore TEST","2000-02-22","69006","212-555-1223","egore@technolutions.com"),
    ("Misti Test","Hatfield Test","1976-07-04","91765-1169","212-555-1224","mistiw7421@aol.com"),
    ("Alexandra","Jackson","","","+1 981-596-3441","ajackson34@inbox.com"),
    ("Alex","Jenkins","","","+1 366-232-7749","ajenkins17@outlook.com"),
    ("Trevor TEST","Johnson TEST","2000-01-20","06510-1804","212-555-1225","tjohnson@technolutions.com"),
    ("Eliza TEST","King TEST","2001-06-25","06510-1804","212-555-1226","eking@technolutions.com"),
    ("Hayley","Kiruki","1982-02-15","","+1 909-607-9043","hayleykiruki@yahoo.com"),
    ("Hayley","Kiruki","","","212-555-1227","hayley.kiruki@cgu.edu"),
    ("Hayley Test","Kiruki Test","1982-02-15","91711-5909","212-555-1228","hayley.kiruki@cgu.edu"),
    ("Hayley Test","Kiruki Test","","","212-555-1229","hayley.kiruki@cgu.edu"),
    ("Dustin","Lee","","","+1 935-566-5893","dustinl2@gmail.com"),
    ("Casey","Martinez","","","+1 349-678-7805","caseym16@yahoo.com"),
    ("Alan","Mlynek","","","212-555-1230","amlynek@noodle.com"),
    ("Brittany","Murphy","","","+1 581-952-1627","bmurphy23@gmail.com"),
    ("Brent","Postlethweight","1988-06-21","","212-555-1231","bpostlethweight@noodle.com"),
    ("Emily TEST","Toops TEST","2000-01-19","06510-1804","212-555-1232","etoops@technolutions.com"),
    ("Emily TEST","Toops TEST","2000-01-19","06510-1804","212-555-1233","etoops@technolutions.com"),
    ("Paul TEST","Turchan TEST","2000-03-04","SW1A 2AA","212-555-1234","pturchan@technolutions.com"),
    ("Chris TEST","Volpe TEST","2001-08-14","06510-1804","212-555-1235","cvolpe@technolutions.com"),
    ("Nicholas","Ward","","","+1 316-530-4004","nicholasw23@outlook.com"),
    ("Alex","Williams","","","212-555-1236","awilliams@technolutions.com"),
    ("Alex TEST","Williams TEST","2001-07-25","69006","212-555-1237","awilliams@technolutions.com"),
    ("Misti TEST","Williamson TEST","1976-07-04","92823-6333","212-555-1238","mistiw76@gmail.com")
]

def generate_form_json():
    rows = []
    for r in data_rows:
        row = {
            "first_name": r[0],
            "last_name": r[1],
            "email": r[5],
            "birthdate": r[2],
            "phone": r[4],
            "zipcode": r[3],
            "utmSource": Rand.pick((("Web Search",70),("Social",30))),
            "utmMedium": "Web",
            "utmCampaign": "Campaign %d" % Rand.get(1000),
            "utmTerm": Rand.pick((("CGU",70),("Online",30))),
            "utmContent": Rand.pick((("hello",60),("world",40))),
            "sourceClickId": str(Rand.get(10000000)),
            "highestLevelOfEducation": Rand.pick((("High School",10),("Associate's",10),("Bachelor's in Progress",20),("Bachelor's",30),("Master's in progress",10),("Master's",10), ("Doctorate",10))),
            "testScoreStatus": Rand.pick((("Taken",40),("Registered",30),("Not Registered",30))),
            "yearsOfWorkExperience": Rand.pick((("0-1 years",20),("2-3 years",30),("3 or more years",50))),
            "urlOnSubmission": "http://www.google.com",
            "marketingSourceAdditionalId": str(Rand.get(1000000)),
            "cookieSourceAdditionalId": str(Rand.get(1000000))
        }
        rows.append(row)
    return rows

# ---------------------

sys.stdout.write(json.dumps(generate_form_json(),indent=2))
sys.stdout.write("\n")

