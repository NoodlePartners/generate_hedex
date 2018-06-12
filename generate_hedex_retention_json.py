#!/usr/bin/python3
from names import Names
from addresses import Addresses
from emails import Emails
from rand import Rand
from dates import Dates
from words import Words
import sys
import json
import datetime

tenantId = "WFU"
cut_date = datetime.datetime.strptime("2018-09-01", "%Y-%m-%d")
subjectCode = "ECO"
n_faculty = 30
n_staff = 10
n_students = 150
university_email_domain = "wfu.edu"
university_phone_format = "+1 336-758-%04d"
university_address_1 = "1834 Wake Forest Road"
university_city = "Winston-Salem"
university_state = "SC"
university_postal_code = "27106"
university_country = "USA"

# -----------------------------------------

def _make_batch(key, arr):
    return {"tenantId": tenantId, key: arr}


def _assemble_datetime(year, _mm_dd):
    return datetime.datetime.strptime(("%d%s"%(year,_mm_dd)), "%Y-%m-%d")


def _x_day_after(dd, n):
    return dd+datetime.timedelta(days = (n-dd.weekday())%7)


def _monday_after(dd):
    return _x_day_after(dd, 0)


def _friday_after(dd):
    return _x_day_after(dd, 4)


retention_catalog_terms = []
def generate_retention_catalog_terms():
    term_data = (("S", "-01-02", "-05-20"), ("X", "-06-01", "-08-20"), ("F", "-09-01", "-12-15"))
    i = 0
    terms = []
    while i < 12:
        j = i%3
        year = 2016 + ((i-j)/3)
        term_vals = term_data[j]
        startDate = _monday_after(_assemble_datetime(year, term_vals[1]))
        addDropEndDate = startDate + datetime.timedelta(days = 21)
        endDate = _friday_after(_assemble_datetime(year, term_vals[2]))
        termCode = "%d%s" % (year, term_vals[0])
        status = "A" if startDate > cut_date else "I"
        i += 1
        x = {
            "termCode": termCode,
            "status": status,
            "acadYear": "%d" % year,
            "addDropEndDate": addDropEndDate.strftime("%Y-%m-%d")
        }
        y = dict(x)
        y.update({
            "startDate": startDate.strftime("%Y-%m-%d"),
            "endDate": endDate.strftime("%Y-%m-%d"),
        })
        retention_catalog_terms.append(y)
        y = dict(x)
        y.update({
            "startDate": startDate.strftime("%Y-%m-%d"),
            "endDate": endDate.strftime("%Y-%m-%d"),
            "sessionCode": termCode + "-SUB",
            "sessionStatus": status,
            "sessionStartDate": (startDate+datetime.timedelta(days=14)).strftime("%Y-%m-%d"),
            "sessionEndDate": (endDate-datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
        })
        retention_catalog_terms.append(y)
    return _make_batch("terms", retention_catalog_terms)


retention_catalog_sections = []
def generate_retention_catalog_sections():
    for tt in retention_catalog_terms:
        if tt.get("status") != "A" or not tt.get("sessionCode"):
            continue
        n_courses = 5 + Rand.get(10)
        i = 0
        while i < n_courses:
            i += 1
            sectionCourseNumber = 100+Rand.get(900)
            title_prefix = "Intro to " if sectionCourseNumber < 200 else ""
            x = {
                "termCode": tt["termCode"],
                "sessionCode": tt["sessionCode"],
                "sisSectionId": "S%05d" % Rand.get(99999),
                "lmsSectionId": "L%05d" % Rand.get(99999),
                "sectionRefNum": Rand.get(99999),
                "subjectCode": subjectCode,
                "sectionCourseNumber": 100+Rand.get(900),
                "sectionNumber": 1+Rand.get(9),
                "nonTermIndicator": False,
                "sectionTitle": title_prefix + " ".join(Words.get_n(Rand.get(3)+1)),
                "sectionLevel": "Graduate",
                "sectionStatus": "A",
                "sectionStartDate": tt["sessionStartDate"],
                "sectionEndDate": tt["sessionEndDate"],
                "sectionInstMethod": "Online",
                "Crosslisting": []
            }
            retention_catalog_sections.append(x)
    return _make_batch("sections", retention_catalog_sections)


def _start_person(name):
    return {
        "personSisId": "S%09d" % Rand.get(999999999),
        "personLmsId": "L%09d" % Rand.get(999999999),
        "lastName": name["family_name"],
        "firstName": name["given_name"],
        "middleName": None,
        "preferredName": name["preferred_given_name"],
        "prefix": name["prefix"],
        "suffix": name["suffix"],
        "alternateIDs": [],
        "gender": name["gender"],
        "personStatus": "A",
        "personRequestingAgentMergedId": None
    }


retention_facultystaff_staff = []
def generate_retention_facultystaff_staff():
    u_building_format = "%s " + Words.get() + " Hall"
    n = n_staff + n_faculty
    i = 0
    while i < n:
        i += 1
        name = Names.get_name()
        x = _start_person(name)
        u_email = Emails.get_u_email(name["given_name"], name["family_name"], u_domain=university_email_domain)
        u_phone = university_phone_format % Rand.get(9999)
        x.update({
            "PersonAddresses": [
                {
                "addressType": "OFFICE",
                "addressLine1": university_address_1,
                "addressLine2": u_building_format % (Rand.get(600)+100),
                "addressLine3": None,
                "city": university_city,
                "state": university_state,
                "postalCode": university_postal_code,
                "county": None,
                "country": university_country,
                "preferredResidenceIndicator": False,
                "preferredMailingAddressIndicator": None,
                "addressStartDate": None,
                "addressEndDate": None
                }
            ],
            "PersonPhones": [
                {
                "phoneNumber": u_phone,
                "phoneType": "OFFICE",
                "phoneExtension": None
                }
            ],
            "PersonEmails": [
                {
                "emailAddress": u_email,
                "emailAddressType": "INSTITUTION",
                "preferredEmailIndicator": True
                }
            ],
            "StaffItems": {
                "facInd": i > n_staff,
                "advInd": False,
                "staffInd": i <= n_staff,
            }
        })
        retention_facultystaff_staff.append(x)
    return _make_batch("staff", retention_facultystaff_staff)


retention_studentrecords_students = []
def generate_retention_studentrecords_students():
    i = 0
    while i < n_students:
        i += 1
        name = Names.get_name()
        x = _start_person(name)
        personSisId = x["personSisId"]
        personLmsId = x["personLmsId"]
        email = Emails.get_email(name["given_name"], name["family_name"])
        phone = Addresses.get_phone(prefix=True)
        address = Address.get_address()
        birth_address = Address.get_address()
        latino = Rand.get_bool(10)
        address_line_1 = address["building_number"]+" " + address["street_name"]
        if address["apt"]:
            address_line_1 += " Apt " + address["apt"]
        x.update({
            "dateOfBirth": "string",
            "formerFirstName": "string",
            "formerLastName": "string",
            "placeOfBirth": "%s, %s %s" % (birth_address["city"], birth_address["state"], birth_address["country"]),
            "maritalStatus": name["marital_status"],
            "religiousPreference": "string",
            "veteranStatus": None,
            "ipedsHispanic/Latino": latino,
            "ethnicity": "Latino" if latino else "Non-latino",
            "listOfRaces": Rand.pick((("White",50), ("Black",20), ("Asian",10), ("White|Black",7), ("While|Asian",3), ("Black|Asian",2), ("N/A",15), ("Other",3)))
            "languagesSpoken": Rand.pick((("English",80), ("English|Spanish",15), ("English|Serbian", 5)))
            "primaryLanguage": "English",
            "alienStatus": None,
            "countryOfCitizenship": "USA",
            "countryOfResidence": address["country"],
            "alienRegistrationNumber": None,
            "immigrationStatus": "Citizen",
            "visaType": None,
            "personOriginationCode": None,
            "personOriginationDate": None,
            "personSourceCode": None,
            "PersonAddresses": [
                {
                "addressType": "HOME",
                "addressLine1": address_line_1
                "addressLine2": None,
                "addressLine3": None,
                "city": address["city"],
                "state": address["state"],
                "postal_code": address["postal_code"],
                "county": address["county"],
                "country": address["country"],
                "preferredResidenceIndicator": True,
                "preferredMailingAddressIndicator": True
                }
            ],
            "PersonPhones": [
                {
                "phoneNumber": phone,
                "phoneType": "Mobile",
                "phoneExtension": None
                }
            ],
            "PersonEmails": [
                {
                "emailAddress": email,
                "emailAddressType": "PERSONAL",
                "preferredEmailIndicator": True
                }
            ],
            "StudentItems": {
                "studentCurrentStatus": "A",
                "studentTermItems": studentTermItems
            }
        })
        studentTermItems = []
        credits = 0
        for term in retention_catalog_terms:
            if term["startDate"] > cut_date:
                break
            credits += Rand.get(10) + 10
            studentTermItems.append({
                "personSisId": personSisId,
                "personLmsId": personLmsId,
                "termCode": term["termCode"],
                "enrollmentDate": "2017-07-25",
                "enrollmentTerm": "2017F",
                "anticipatedGradDate": "2019-05-25",
                "anticipatedGradTerm": "2019S",
                "cummGpa": (Rand.get(20)+2.0)/10.0,
                "totalHours": credits*3,
                "totalCredit": credits,
                "firstGenerationStudent": None,
                "firstTimeStudent": None,
                "currAcadStanding": "string",
                "totalWithdrawls": 0,
                "creditsOnTrack": "string",
                "estCreditsToGraduate": "Unknown Type: float",
                "currentFaHold": "string",
                "currentBursarHold": "string",
                "primaryProgramCode": "string",
                "primaryProgramLevel": "string",
                "primaryDegreeCode": "string",
                "primaryMajor1": "string",
                "primaryMajor2": "string",
                "primaryConcentration1": "string",
                "primaryConcentration2": "string",
                "primaryMinor1": "string",
                "primaryMinor2": "string",
                "secondaryProgramCode": "string",
                "secondaryProgramLevel": "string",
                "secondaryDegreeCode": "string",
                "secondaryMajor1": "string",
                "secondaryMajor2": "string",
                "secondaryConcentration1": "string",
                "secondaryConcentration2": "string",
                "secondaryMinor1": "string",
                "secondarysMinor2": "string",
                "studentStatus": "string"
            })

        x["StudentItems"]["studentTermItems"] = studentTermItems


# Generate all files
files = ((generate_retention_catalog_terms, "Retention_Catalog_Term"),
         (generate_retention_catalog_sections, "Retention_Catalog_Sections"),
         (generate_retention_facultystaff_staff, "Retention_FacultyStaff_Staff")
         (generate_retention_studentrecords_students, "Retention_StudentRecords_Students")
        )

def generate_all_files():
    for proc, fn in files:
        val = proc()
        with open('%s_%s.json'%(fn,datetime.datetime.now().strftime("%Y%m%d%H%M%S")), "w") as f:
            json.dump(val, f, indent=2)

generate_all_files()
