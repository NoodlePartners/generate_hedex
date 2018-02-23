#!/usr/bin/python
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

def generate_form_csv(n):
    i = 0
    rows = []
    while i < n:
        name_x = Names.get_name()
        given_name = name_x["given_name"]
        family_name = name_x["family_name"]
        row = {
            "first_name": given_name,
            "last_name": family_name,
            "email": Emails.get_email(given_name, family_name),
            "birthdate": Rand.get_date_in_range(_birthday_start_date, _birthday_n_days),
            "phone": Addresses.get_phone(True),
            "utmSource": Rand.pick((("Web Search",70),("Social",30))),
            "utmMedium": "Web",
            "utmCampaign": "Campaign %d" % Rand.get(1000),
            "utmTerm": Rand.pick((("CGU",70),("Online",30))),
            "utmContent": Rand.pick((("hello",60),("world",40))),
            "sourceClickId": str(Rand.get(10000000)),
            "highestLevelofEducation": Rand.pick((("High School",10),("Associate's",10),("Bachelor's in Progress",20),("Bachelor's",30),("Master's in progress",10),("Master's",10), ("Doctorate",10))),
            "testScoreStatus": Rand.pick((("Taken",40),("Registered",30),("Not Registered",30))),
            "yearsOfWorkExperience": Rand.pick((("0-1 years",20),("2-3 years",30),("3 or more years",50))),
            "urlOnSubmission": "http://www.google.com",
            "marketingSourceAdditionalId": str(Rand.get(1000000)),
            "cookieSourceAdditionalId": str(Rand.get(1000000))
        }
        rows.append(row)
        i += 1
    return rows

# ---------------------

if sys.argv.__len__()<2:
    sys.stderr.write("number of records?\n")
else:
    sys.stdout.write(json.dumps(generate_form_csv(int(sys.argv[1])),indent=None))
    sys.stdout.write("\n")

