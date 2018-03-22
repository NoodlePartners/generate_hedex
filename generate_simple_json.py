#!/usr/bin/python3
from names import Names
from addresses import Addresses
from emails import Emails
from rand import Rand
import sys
import json

def p(x):
    sys.stdout.write(x)

# Number of rows to generate
n = 100
rows = []

i = 0
while i < n:
    i += 1

    name_x = Names.get_name()
    given_name = name_x["given_name"]
    family_name = name_x["family_name"]
    birth_name = name_x["birth_name"]
    u_email_x = Emails.get_u_email(given_name, family_name)
    email1 = Emails.get_email(given_name, family_name)
    email2 = Emails.get_email(given_name, family_name)
    phone_number1 = Addresses.get_phone()
    phone_number2 = Addresses.get_phone()
    address_x = Addresses.get_address()
    birth_address_x = Addresses.get_address()

    row = {}

    personRecord = {}

    personRecord["SourceGUID"] = {"sourceID": u_email_x["id"]}

    formname = {}
    formname["Full"] = "%s %s" % (given_name, family_name)
    if birth_name:
        formname["Maiden"] = "%s %s" % (given_name, birth_name)
    personRecord["formname"] = formname

    full = {
        "First": given_name,
        "Last": family_name
    }
    if name_x["preferred_name"]:
        full["Nickname"] = name_x["preferred_name"]
    name = {}
    name["Full"] = full
    if birth_name:
        name["Maiden"] = {
            "First": given_name,
            "Last": birth_name
        }

    personRecord["name"] = name

    mailing_primary = {
        "StreetNumber": address_x["building_number"],
        "StreetName": address_x["street_name"],
        "City": address_x["city"],
        "StatePr": address_x["state"],
        "Country": address_x["country"],
        "Postcode": address_x["postal_code"]
    }
    if address_x["apt"]:
        mailing_primary["ApartmentNumber"] = address_x["apt"]
    personRecord["Mailing_Primary"] = mailing_primary

    personRecord["contactinfo"] = {
        "EmailPrimary": email1,
        "Mobile": phone_number1,
        "Telephone": phone_number2
    }

    Primary = {}
    Primary["eventDate"] = {
        "Create": "2015-11-28T12:00:00-05:00",
        "Update": "2015-12-17T12:00:00-05:00",
        "Enroll": "2016-02-12T12:00:00-05:00",
        "Birth": Rand.get_date_in_range("1990-10-10", 365*3) +
            "T12:00:00-06:00"
    }
    Primary["gender"] = "female" if name_x["gender"]=="F" else "male"
    Primary["demographicInfo"] = {
        "Ethnicity": Rand.pick([
            ["White non hispanic", 60],
            ["Hispanic", 20],
            ["Black", 12],
            ["Asian or Pacific Islander", 3],
            ["Other or N/A", 5]
        ])
    }
    
    demographics = {}
    demographics["Primary"] = Primary

    personRecord["demographics"] = demographics

    row["personRecord"] = personRecord

    rows.append(row)

p(json.dumps(rows, indent=2))
