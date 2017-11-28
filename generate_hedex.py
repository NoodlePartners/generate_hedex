from names import Names
from addresses import Addresses
from emails import Emails
from rand import Rand
import sys
import json
import datetime

def p(x):
    sys.stdout.write(x)

def generate_simple_json():
    # Number of rows to generate
    n = 100
    rows = []

    i = 0
    while i < n:
        i += 1

        name_x = Names.get_name()
        given_name = name_x["given_name"]
        family_name = name_x["family_name"]
        birth_family_name = name_x["birth_family_name"]
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
        if birth_family_name:
            formname["Maiden"] = "%s %s" % (given_name, birth_family_name)
        personRecord["formname"] = formname

        full = {
            "First": given_name,
            "Last": family_name
        }
        if name_x["preferred_given_name"]:
            full["Nickname"] = name_x["preferred_given_name"]
        name = {}
        name["Full"] = full
        if birth_family_name:
            name["Maiden"] = {
                "First": given_name,
                "Last": birth_family_name
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


def p_row(columns, data=None):
    vals = []
    for col in columns:
        if data:
            x = data[col]
        else:
            x = col
        if type(x) in [str, unicode]:
            val = '"' + x.encode("utf-8") + '"'
        else:
            val = str(x)
        vals.append(val)
    p(",".join(vals)+"\n")


def generate_csv():
    # This is what we are trying to generate
    columns = [
        "First Name",
        "Last Name",
        "Former Last Name",
        "Community Email",
        "Preferred Name",
        "Primary Email",
        "2ndary Email",
        "Telephone Number",
        "Home Address",
        "City",
        "State",
        "Country",
        "Apt #",
        "Current Zipcode",
        "Unique ID",
        "Username",
        "Date of Birth",
        "Gender",
        "Country of Birth",
        "Zip Code of Birth",
        "Race",
        "First Generation College?",
        "Marital Status",
        "Highest Level of Education for Parents",
        "Hours Per Week Working",
        "Parent's Income Level",
        "Parent's Marital Status",
        "Number of Children",
        "Number of Siblings",
        "Highest Educational Attainment of Sibling",
        "Military Status",
        "Military Service",
        "Highest Military Rank",
        "Military Spouse?",
        "Employer",
        "Application",
        "Application Writing Samples",
        "Documents",
        "Application Date",
        "Accepted Date",
        "Community Join Date",
        "Highest Level of Education",
        "Application (lead source)",
        "High School Attended",
        "Learning Disability?",
        "Emotional Disturbances?",
        "Has dropped out in past?",
        "High School Grade Point Average",
        "Status",
        "Last Program Change",
        "Transfer Credit Evaluation"
    ]
    n_columns = columns.__len__()

    # Number of rows to generate
    n = 100

    # Print header
    p_row(columns)

    data_template = {}
    for col in columns:
        data_template[col] = ""

    i = 0
    while i < n:
        i += 1

        data = dict(data_template) # clone the template

        name = Names.get_name()
        given_name = name["given_name"]
        family_name = name["family_name"]
        data["First Name"] = given_name
        data["Last Name"] = family_name
        data["Former Last Name"] = name["birth_family_name"]

        u_email = Emails.get_u_email(given_name, family_name)
        data["Community Email"] = u_email["email"]

        data["Preferred Name"] = name["preferred_given_name"]

        data["Primary Email"] = Emails.get_email(given_name, family_name)
        data["2ndary Email"] = Emails.get_email(given_name, family_name)

        data["Telephone Number"] = Addresses.get_phone()

        address = Addresses.get_address()
        data["Home Address"] = address["address1"]
        data["City"] = address["city"]
        data["State"] = address["state"]
        data["Country"] = address["country"]
        data["Apt #"] = address["apt"]
        data["Current Zipcode"] = address["postal_code"]

        data["Date of Birth"] = Rand.get_date_in_range("1990-10-10", 365*3)

        data["Unique ID"] = u_email["id"]

        data["Username"] = u_email["email"]

        data["Gender"] = name["gender"]

        birth_address = Addresses.get_address()
        data["Country of Birth"] = birth_address["country"]
        data["Zip Code of Birth"] = birth_address["postal_code"]

        data["Race"] = Rand.pick([
            ["White non hispanic", 60],
            ["Hispanic", 20],
            ["Black", 12],
            ["Asian or Pacific Islander", 3],
            ["Other or N/A", 5]
        ])

        data["First Generation College?"] = Rand.pick([
            ["N", 70],
            ["Y", 30]
        ])

        data["Marital Status"] = name["marital_status"]

        data["Highest Level of Education for Parents"] = Rand.pick([
            ["No High School Diploma", 5],
            ["High School", 20],
            ["Some College", 20],
            ["Associates Degree", 10],
            ["Bachelors Degree", 30],
            ["Post Graduate", 10]
        ])

        data["Hours Per Week Working"] = Rand.pick([
            [0, 30],
            [5, 25],
            [10, 20],
            [20, 20],
            [40, 5],
        ])

        data["Parent's Income Level"] = Rand.pick([
            ["<$30,000", 5],
            ["$30,000-$45,000", 10],
            ["$45,000-$60,000", 15],
            ["$60,000-$90,000", 20],
            ["$90,000-$120,000", 25],
            ["$120,000-$180,000", 20],
            [">$180,000", 5]
        ])

        data["Parent's Marital Status"] = Rand.pick([
            ["S", 5],
            ["M", 50],
            ["D", 45]
        ])

        data["Number of Children"] = Rand.pick([
            [0, 80],
            [1, 12],
            [2, 5],
            [3, 2],
            [4, 1]
        ])

        t = Rand.pick([
            [0, 20],
            [1, 40],
            [2, 20],
            [3, 15],
            [4, 5]
        ])

        data["Number of Siblings"] = t

        if t == 0:
            data["Highest Level of Education of Sibling"] = ""

        else:
            data["Highest Level of Education of Sibling"] = Rand.pick([
                ["No High School Diploma", 30],
                ["High School", 25],
                ["Some College", 20],
                ["Associates Degree", 5],
                ["Bachelors Degree", 15],
                ["Post Graduate", 5]
            ])

        # TODO!
        data["Military Status"] = "N"
        data["Military Service"] = ""
        data["Highest Military Rank"] = ""

        data["Military Spouse?"] = Rand.pick([
            ["N", 90],
            ["Y", 10]
        ])

        employer = Names.get_name()
        data["Employer"] = employer["family_name"] + " Inc."

        # TODO!
        data["Application"] = ""
        data["Application Writing Samples"] = ""
        data["Documents"] = ""

        data["Application Date"] = Rand.get_date_in_range("2014-06-01", 180)

        data["Accepted Date"] = "2015-04-07"

        data["Community Join Date"] = "2015-09-07"

        data["Highest Level of Education"] = Rand.pick([
            ["Bachelors Degree", 90],
            ["Post Graduate", 10]
        ])

        data["Application (lead source)"] = Rand.pick([
            ["Google", 40],
            ["Web site", 30],
            ["Noodle.com", 15],
            ["Yahoo", 10],
            ["Bing", 5]
        ])

        data["High School Attended"] = Names.get_high_school_name()

        data["Learning Disability?"] = Rand.pick([
            ["N", 95],
            ["Y", 5]
        ])

        data["Emotional Disturbances?"] = Rand.pick([
            ["N", 95],
            ["Y", 5]
        ])

        data["Has dropped out in past?"] = Rand.pick([
            ["N", 85],
            ["Y", 15]
        ])

        data["High School Grade Point Average"] = float(Rand.get(25))/10.0 + 2.0

        data["Status"] = "Active"
        
        # TODO!
        data["Last Program Change"] = ""
        data["Transfer Credit Evaluation"] = ""

        p_row(columns, data)


def generate_hedex(n):
    # HEDEX GET response, from Swagger Documents
    res = {
        "tenantId": "1234567",
        "batchId": "123",
        # "batchGroupId": "string",
        # "batchTransactionStatus": "SUCCESS",
        # "batchTransactionStatusMessage": "string",
        # "batchDataSourceAgents": "string",
        "admissionsPerson": []
    }
    # Make n addmissionsPersons
    aps = []
    i = 0
    while i < n:
        ap = generate_admissions_person()
        ap["itemSequenceNumber"] = i
        aps.append(ap)
        i += 1
    res["admissionsPerson"] = aps
    return res



_birthday_start_date = "1990-10-10"
_birthday_n_days = 5 * 365

def generate_admissions_person():
    
    res = {
        "itemSequenceNumber": 0,
        "personSisId": "",
        "personCRMId": "",
        "lastName": "",
        "firstName": "",
        "middleName": "",
        "preferredName": "",
        "prefix": "",
        "suffix": "",
        "socialSecurityNumber": None,
        "alternateIDs": [],
        "gender": "",
        "dateOfBirth": "",
        "formerFirstName": "",
        "formerLastName": "",
        "placeOfBirth": "",
        "maritalStatus": "",
        "religiousPreference": "",
        "veteranStatus": "",
        "ipedsHispanicLatino": True,
        "ethnicity": "",
        "listOfRaces": "",
        "languagesSpoken": "",
        "primaryLanguage": "string",
        "alienStatus": "string",
        "countryOfCitizenship": "string",
        "countryOfResidence": "string",
        "alienRegistrationNumber": "string",
        "immigrationStatus": "string",
        "visaType": "string",
        "personOriginationCode": "string",
        "personOriginationDate": "string",
        "personSourceCode": "string",
        "PersonAddresses": [],
        "PersonPhones": [],
        "PersonEmails": [],
        "PersonRelations": [],
        "PersonEducation": [],
        "PersonTestScores": [],
        "PersonProspect": {},
        "PersonApplicant": {},
        "PersonApplications": []
    }
        
    res["personSisId"] = "%d"%(Rand.get(999999)+1000000)
    res["personCRMId"] = "%d"%(Rand.get(999999)+1000000)

    name_x = Names.get_name()
    given_name = name_x["given_name"]
    family_name = name_x["family_name"]
    res["lastName"] = family_name
    res["firstName"] = given_name
    res["preferredName"] = name_x["preferred_given_name"]
    res["formerFirstName"] = name_x["birth_given_name"]
    res["formerLastName"] = name_x["birth_family_name"]
    res["prefix"] = name_x["prefix"]
    res["suffix"] = name_x["suffix"]
    res["gender"] = name_x["gender"]
    res["dateOfBirth"] = Rand.get_date_in_range(_birthday_start_date, _birthday_n_days)
    addr_x = Addresses.get_address()
    res["placeOfBirth"] = addr_x["city"]+", "+addr_x["state"]+" "+addr_x["country"]
    res["maritalStatus"] = name_x["marital_status"]

    res["alternateIDs"] = generate_alternate_ids()
    res["PersonAddresses"] = generate_person_addresses()
    res["PersonPhones"] = generate_person_phones()
    res["PersonEmails"] = generate_person_emails(given_name, family_name)
    res["PersonRelations"] = generate_person_relations()
    res["PersonEducation"] = generate_person_educations()
    res["PersonProspect"] = generate_person_prospect()
    res["PersonApplicant"] = generate_person_applicant()
    
    
    return res


def generate_alternate_ids():
    ai = {
        "personAlternateId": "%d"%(Rand.get(999999)+1000000),
        "personAlternateIdType": "FPS"
    }
    return [ai]


def generate_person_address():
    res = {
        "addressType": 0,
        "addressLine1": "string",
        "addressLine2": "",
        "addressLine3": "",
        "city": "string",
        "state": "string",
        "postalCode": "string",
        "county": "string",
        "country": "string",
        "preferredResidenceIndicator": True,
        "preferredMailingAddressIndicator": True,
        # "addressStartDate": "string",
        # "addressEndDate": "string"
    }
    address_x = Addresses.get_address()
    if address_x["apt"]:
        apt = " Apt " + address_x["apt"]
    else:
        apt = ""
    line1 = address_x["building_number"] + " " + address_x["street_name"] + apt
    res["addressLine1"] = line1
    res["city"] = address_x["city"]
    res["state"] = address_x["state"]
    res["county"] = address_x["county"]
    res["country"] = address_x["country"]
    res["postalCode"] = address_x["postal_code"]
    return res


_percent_with_secondary_address = 20

def generate_person_addresses():
    res = [generate_person_address()]
    if Rand.get_bool(_percent_with_secondary_address):
        x = generate_person_address()
        x["preferredResidenceIndicator"] = False
        x["preferredMailingAddressIndicator"] = False
        res.append(x)
    return res


_percent_with_home_phone = 20
_percent_with_work_phone = 20

def generate_person_phones():
    res = []
    for typep in (("mobile",100), ("home", _percent_with_home_phone), ("work", _percent_with_work_phone)):
        if Rand.get_bool(typep[1]):
            res.append({
                "phoneNumber": Addresses.get_phone(True),
                "phoneType": typep[0],
                "phoneExtension": 0
            })
    return res


_percent_with_work_email = 30

def generate_person_emails(given_name, family_name):
    res = []
    res.append({
        "emailAddress": Emails.get_u_email(given_name, family_name)["email"],
        "emailAddressType": "university",
        "preferredEmailIndicator": True
    })
    res.append({
        "emailAddress": Emails.get_email(given_name, family_name),
        "emailAddressType": "home",
        "preferredEmailIndicator": True
    })
    if Rand.get_bool(_percent_with_work_email):
        res.append({
            "emailAddress": Emails.get_email(given_name, family_name),
            "emailAddressType": "home",
            "preferredEmailIndicator": True
        })
    return res


def generate_person_relation():
    res = {
        "typeOfRelationship": "string",
        "relationGender": "string",
        "relationPrefix": "string",
        "relationSuffix": "string",
        "relationFirstName": "string",
        "relationLastName": "string",
        "relationDeceased": True,
        "relationSourceCode": "string",
        "RelationAddresses": [
            {
                "relationAddressType": "string",
                "relationAddressLine1": "string",
                "relationAddressLine2": "string",
                "relationAddressLine3": "string",
                "relationAddressCity": "string",
                "relationAddressState": "string",
                "relationAddressPostalCode": "string",
                "relationAddressCountry": "string"
            }
        ],
        "RelationPhones": [
            {
                "relationPhoneNumber": "string",
                "relationPhoneType": "string",
                "relationPhoneExtension": 0
            }
        ],
        "RelationEmails": [
            {
                "relationEmailAddress": "string",
                "relationEmailAddressType": "string"
            }
        ]
    }
    return {} # TODO


def generate_person_relations():
    return [] # TODO


def generate_person_education():
    res = {
        "institutionAttendedCeebCode": "string",
        "institutionAttendedFiceCode": "string",
        "institutionAttendedName": "string",
        "institutionAttendedAddressLine1": "string",
        "institutionAttendedAddressLine2": "string",
        "institutionAttendedAddressLine3": "string",
        "institutionAttendedCity": "string",
        "institutionAttendedState": "string",
        "institutionAttendedPostalCode": "string",
        "institutionAttendedCountry": "string",
        "institutionAttendedType": "string",
        "institutionAttendedStartDate": "string",
        "institutionAttendedEndDate": "string",
        "institutionAttendedStartYears": 0,
        "institutionAttendedEndYears": 0,
        "institutionAttendedTranscriptDate": "string",
        "institutionAttendedTranscriptType": "string",
        "institutionAttendedTranscriptStatus": "string",
        "institutionAttendedCreditsEarned": "Unknown Type: float",
        "institutionAttendedGpa": "Unknown Type: float",
        "institutionAttendedClassRankPercentage": "Unknown Type: float",
        "institutionAttendedClassRankNumerator": 0,
        "institutionAttendedClassRankDenominator": 0,
        "institutionAttendedGraduationType": "string",
        "institutionAttendedTypeOfEducation": "string",
        "institutionAttendedDiplomaReceived": True,
        "EducationCredentials": [
            {
                "credentialInstitutionId": "string",
                "institutionAttendedDegreeObtained": "string",
                "institutionAttendedDegreeDate": "string",
                "institutionAttendedCcdsObtained": "string",
                "institutionAttendedCcdDates": "string",
                "institutionAttendedMajor": "string",
                "institutionAttendedMinor": "string",
                "institutionAttendedSpecialization": "string"
            }
        ]
    }
        
    return {} #TODO


def generate_person_educations():
    return [] #TODO


def generate_person_test_scores():
    tests = ((50,(("SATM",100,800),("SATV",100,800))),
             (45,(("ACTE",1,36),("ACTM",1,36),("ACTR",1,36),("ACTS",1,36))),
             (15,(("GREV",130,170),("GREQ",130,170),("GREW",0,6))))
    res = []
    for test in tests:
        if Rand.get_bool(test[0]):
            for sect in test[1]:
                score = Rand.get(sect[2]-sect[1]+1) + sect[1]
                res.append(
                    {
                        "testName": sect[0],
                        "testDate": Rand.get_date_in_range('2016-01-01',365),
                        "testScore": score,
                        "testStatus": "official",
                        "testSource": "transcript"
                    }
                )
    return res


def generate_prospect_program_interest():
    res = {
        "prospectAcademicLevel": "Masters",
        "prospectAcademicProgram": "MSW",
        "prospectMajor": "",
        "prospectFinancialAidIntent": False,
        "prospectFull-Time/PartTimeIntent": "Part Time",
        "prospectInterestedProgramStatus": "",
        "prospectStartTerm": "Spring 2018",
        "prospectStartDate": "",
        "prospectStudentType": "",
        "residentOrCommuterIntent": False
    }


def generate_prospect_program_interests():
    return [generate_prospect_program_interest()]


def generate_prospect_source():
    res = {
        "sourceCode": "",
        "sourceDateTime": "",
        "sourceDetail": "",
        "sourceMedium": "",
        "sourceClickId": Rand.get(100000000)
    }
    return res #TODO


def generate_prospect_sources():
    return [] #TODO


def generate_activity_ids():
    res = [{
        "activityId": "%d"%(Rand.get(1000000)+1000000),
        "activityIdType": "FPS"
    }]


def generate_prospect_activity(program, term, vendor, coachId, channel, initiator, startDatetime, status, disposition, notes, resultingStatus):
    res = {
        "activityProgramOfInterest": program,
        "activityProgramStartTerm": term,
        "activityProgramStartDate": "",
        "activityCoachingVendor": vendor,
        "activityCoachID": coachId,
        "activityIDs": [],
        "activityChannel": channel,
        "activityInitiator": initiator,
        "activityStartDatetime": startDatetime,
        "activityStatus": status,
        "activityDisposition": disposition,
        "notes": notes,
        "resultingProspectStatus": resultingStatus,
        "optOutFields": ""
    }
    res["activityIDs"] = generate_activity_ids()
    return res
        

def generate_prospect_activities():
    program = "MSW"
    term = Rand.pick((("Spring 2018",70),("Summer 2018",10),("Fall 2018",20)))
    vendor = "FPS"
    coachId = "C" + ("%03d"%Rand.get(1000))
    channel = Rand.pick((("phone",75),("email",15),("text",10)))
    initiator = "coach"
    status = "complete"
    startDatetime_dt = datetime.datetime.strptime("2017-02-10T09:38", "%Y-%m-%dT%H:%M")
    res = []
    n = Rand.get(11)
    i = 0
    while(i<n):
        activityStartDatetime = startDatetime_dt.strftime("%Y-%m-%d")
        if i == n-1:
            disposition = "closed"
            resultingStatus = "closed"
        else:
            disposition = "open"
            resultingStatus = "open"
        notes = "Spoke on " + activityStartDatetime
        startDatetime = startDatetime_dt.strftime("%Y-%m-%dT%H:%M-04:00")
        res.append(generate_prospect_activity(program, term, vendor, coachId, channel, initiator,
                                              startDatetime, status, disposition, notes, resultingStatus))
        startDatetime_dt += datetime.timedelta(1, 3600) # 25 hours later
        i+=1
    return res


def generate_prospect_event():
    res = {
        "eventAttended": "Jazz Party",
        "eventDetails": "Held at the Erin Rose Bar",
        "eventAttendedDate": "2017-06-15"
    }
    return res


_percent_attended_party = 10

def generate_prospect_events():
    res = []
    if Rand.get_bool(_percent_attended_party):
        res.append(generate_prospect_event())
    return []


def generate_prospect_rating():
    res = {
        "ratingProgramOfInterest": "MSW",
        "ratingStartTerm": "Sprint 2018",
        "ratingStartDate": "",
        "ratingType": "demographic score",
        "ratingScore": Rand.get(4)
    }        
    return {}


def generate_prospect_ratings():
    res = [generate_prospect_rating()]
    return res


def generate_person_prospect():
    res = {
        "ProspectProgramInterests": [],
        "highlyDesirable": "string",
        "prospectComments": "string",
        "prospectAdmissionsCounselor": "string",
        "prospectExtracurricularInterests": "string",
        "prospectContinuedInterestIndicators": "string",
        "athleticProspectIndicator": True,
        "prospectStatus": "string",
        "prospectLegacy": True,
        "optOutFields": "string",
        "currentRecruitmentVendor": "string",
        "currentRecruitmentCoachID": "string",
        "createdDateTime": "2017-11-22T17:06:02.617Z",
        "firstCommunicationType": "2017-11-22T17:06:02.617Z",
        "firstContactedDateTime": "2017-11-22T17:06:02.617Z",
        "firstCommunicatedDateTime": "2017-11-22T17:06:02.617Z",
        "lastCommunicatedDateTime": "2017-11-22T17:06:02.617Z",
        "totalMissedAttemptsAfterCommunicated": 0,
        "totalAttemptsToContact": 0,
        "totalAttemptsToCommunicate": 0,
        "totalAttemptsToContactAfterCommunicate": 0,
        "leadQuality": 0,
        "nextCommunicationObjective": "string",
        "ProspectSources": [],
        "ProspectActivity": [],
        "ProspectEvents": [],
        "ProspectRatings": []
    }
    res["ProspectSources"] = generate_prospect_sources()
    res["ProspectActivity"] = generate_prospect_activities()
    res["ProspectEvents"] = generate_prospect_events()
    return res


def generate_person_applicant():
    res = {
        "housingDesiredIndicator": True,
        "admissionsCounselor": "string",
        "applicantProspectStatus": "string",
        "extracurricularInterests": "string",
        "continuedInterestIndicators": "string",
        "careerGoals": "string",
        "educationalGoals": "string",
        "applicantComments": "string",
        "legacy": True,
        "officialOffCampusVisitDate": "string",
        "officialOnCampusVisitDate": "string",
        "unofficialVisitDate": "string",
        "applicantMisc1": "string",
        "applicantMisc2": "string",
        "applicantMisc3": "string",
        "applicantMisc4": "string",
        "restrictions": "string"
    }
    return res


def generate_person_applications():
    return [] #TODO


def generate_application_check_list_item():
    res = {
        "checklistItemCode": "string",
        "checklistItemStatus": "string",
        "checklistItemDate": "string",
        "checklistItemAssignedDate": "string",
        "checklistItemInstance": "string",
        "checklistItemComment": "string",
        "checklistItemFaYear": 0
    }        
    return {} #TODO


def generate_application_check_list_items():
    return [] #TODO


def generate_application_check_list_item():
    res = {
        "checklistItemCode": "string",
        "checklistItemStatus": "string",
        "checklistItemDate": "string",
        "checklistItemAssignedDate": "string",
        "checklistItemInstance": "string",
        "checklistItemComment": "string",
        "checklistItemFaYear": 0
    }
    return res


def generate_application_financial_aid():
    res = {
        "financialAidStatus": "string",
        "financialAidType": "string",
        "financialAidAwardAmount": "Unknown Type: double",
        "financialAidAwardYear": "string",
        "fafsaFiled": True
    }
    return res
        

def generate_application_financial_aids():
    return [] #TODO


def generate_person_application():
    res = {
        "applicationSisId": "string",
        "applicationCRMId": "string",
        "applicationAlternateId": "string",
        "applicationAlternateIdType": "string",
        "intentToApplyForFinancialAid": True,
        "applicationType": "string",
        "startTerm": "string",
        "academicProgram": "string",
        "academicProgramCatalog": "string",
        "academicLevel": "string",
        "location": "string",
        "campus": "string",
        "college": "string",
        "additionalMajors": "string",
        "intendedAreaOfStudy": "string",
        "applicantProspectStatusDate": "string",
        "currentApplicationStatus": "string",
        "currentApplicationStatusDate": "string",
        "applicationDate": "string",
        "decision": "string",
        "decisionDate": "string",
        "withdrawalDate": "string",
        "withdrawalReason": "string",
        "admitStatus": "string",
        "degreeSought": "string",
        "applicationComments": "string",
        "influencedToApply": "string",
        "fullTimePartTimeIntent": "string",
        "applicationFeeReceiptIndicator": True,
        "applicationFeeReceiptDate": "string",
        "ApplicationCheckListItems": [],
        "ApplicationFinancialAid": []
    }
    res["ApplicationCheckListItems"] = generate_application_check_list_items()
    res["ApplicationFinancialAid"] = generate_application_financial_aids()
    return res #TODO
