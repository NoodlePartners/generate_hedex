#!/usr/bin/python
from names import Names
from addresses import Addresses
from emails import Emails
from rand import Rand
from dates import Dates
import sys
import json
import datetime


isoformat = "%Y-%m-%dT%H:%M-04:00"

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
        # "religiousPreference": "",
        "veteranStatus": "",
        "ipedsHispanicLatino": True,
        "ethnicity": "",
        "listOfRaces": "",
        "languagesSpoken": "",
        "primaryLanguage": "",
        "alienStatus": "",
        "countryOfCitizenship": "",
        "countryOfResidence": "",
        "alienRegistrationNumber": "",
        "immigrationStatus": "",
        "visaType": "",
#        "personOriginationCode": "string",
#        "personOriginationDate": "string",
#        "personSourceCode": "string",
        "PersonAddresses": [],
        "PersonPhones": [],
        "PersonEmails": [],
        "PersonRelations": [],
#        "PersonEducation": [],  Might not be added if the person isn't an applicant
#        "PersonTestScores": [], Might not be added if the person isn't an applicant
        "PersonProspect": {},
#        "PersonApplicant": {} Might not be added if the person isn't an applicant
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
    # res["religiousPreference"] = ""
    res["veteranStatus"] = ""
    # res["ethnicity"] = ""
    res["listOfRaces"] = Rand.pick((("White",65),("Black",15),("Asian",10),("White|Black",5),("White|Asian",3),("Black|Asian",1)))
    lspok = Rand.pick((("English",80),("English|Chinese",14),("English|Russian",6)))
    if Rand.get_bool(8): # is from Mexico
        res["ipedsHispanicLatino"] = True
        plang = "Spanish"
        lspok = "Spanish|" + lspok 
        ccit = "MX"
        if Rand.get_bool(25):
            astat = None
            cres = "MX"
            anum = None
        else:
            astat = "J1"
            cres = "US"
            anum = "INS"+("%06d"%Rand.get(1000000))
    else:
        res["ipedsHispanicLatino"] = Rand.get_bool(15)
        plang = "English"
        if Rand.get_bool(20):
            lspok += "|Spanish"
        ccit = "US"
        astat = None
        cres = "US"
        anum = None
    res["countryOfCitizenship"] = cres
    res["languagesSpoken"] = lspok
    res["primaryLanguage"] = plang
    res["countryOfCitizenship"] = ccit
    res["alienStatus"] = astat
    res["countryOfResidence"] = cres
    res["alienRegistrationNumber"] = anum
    res["immigrationStatus"] = astat
    res["visaType"] = astat
    # res["personOriginationCode"] = ""
    # res["personOriginationDate"] = ""
    # res["personSourceCode"] = ""
    res["alternateIDs"] = generate_alternate_ids()
    res["PersonAddresses"] = generate_person_addresses()
    res["PersonPhones"] = generate_person_phones()
    res["PersonEmails"] = generate_person_emails(given_name, family_name)
    res["PersonRelations"] = generate_person_relations()
    res["PersonProspect"] = generate_person_prospect()
    person_applicant = generate_person_applicant()
    if person_applicant:
        res["PersonApplicant"] = person_applicant
        res["PersonTestScores"] = generate_person_test_scores()
        res["PersonEducation"] = generate_person_educations()
    
    return res


def generate_alternate_ids():
    ai = {
        "personAlternateId": "%d"%(Rand.get(999999)+1000000),
        "personAlternateIdType": "Acme"
    }
    return [ai]


def generate_person_address():
    res = {
        "addressType": 0,
        "addressLine1": "",
        "addressLine2": "",
        "addressLine3": "",
        "city": "",
        "state": "",
        "postalCode": "",
        "county": "",
        "country": "",
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

hold_terms = []
program_of_interest = "MSW"

def generate_prospect_program_interest():
    # Generate 
    if hold_terms.__len__()>1:
        x = hold_terms[0]
    else:
        x = ""
    while True:
        term = Rand.pick((("Summer 2018",50),("Fall 2018",40),("Spring 2019",10)))
        if term != x:
            break
    hold_terms.append(term)
    res = {
        "prospectAcademicLevel": "Masters",
        "prospectAcademicProgram": program_of_interest,
        # "prospectMajor": "",
        "prospectFinancialAidIntent": False,
        "prospectFullTimePartTimeIntent": "Part Time",
        "prospectInterestedProgramStatus": "",
        "prospectStartTerm": term,
        # "prospectStartDate": "",
        # "prospectStudentType": "",
        "residentOrCommuterIntent": False
    }
    return res


def generate_prospect_program_interests():
    global hold_terms
    hold_terms = []
    res = []
    n = Rand.pick(((1,80),(2,20)))
    i = 0
    while i<n:
        i += 1
        res.append(generate_prospect_program_interest())
    return res


def generate_source_ids():
    res = [{
        "sourceId": "%d"%(Rand.get(1000000)+1000000),
        "sourceIdType": "CMS"
    }]
    return res


def generate_prospect_source(term):
    res = {
        "sourceProgramOfInterest": program_of_interest,
        "sourceStartTerm": term,
        # "sourceStartDate": None,
        "sourceIds": [],
        "sourceCode": "X" + ("%06d"%Rand.get(1000000)),
        "sourceDateTime": Dates.get_date_in_range("2017-10-01", 45),
        "sourceDetail": "X" + ("%06d"%Rand.get(1000000)),
        "sourceMedium": Rand.pick((("Web Search",70),("Social",30))),
        "sourceClickId": Rand.get(100000000)
    }
    res["sourceIds"] = generate_source_ids()
    return res


def generate_prospect_sources():
    res = []
    m = hold_terms.__len__()
    j = 0
    while j<m:
        term = hold_terms[j]
        j += 1
        n = Rand.pick(((1,50),(2,25),(3,13),(4,12)))
        i = 0
        while i<n:
            res.append(generate_prospect_source(term))
            i += 1
    return res


def generate_activity_ids():
    res = [{
        "activityId": "%d"%(Rand.get(1000000)+1000000),
        "activityIdType": "Acme"
    }]
    return res


def generate_prospect_activity(program, term, vendor, coachId, channel, initiator, startDatetime, status, disposition, notes, resultingStatus):
    res = {
        "activityProgramOfInterest": program,
        "activityProgramStartTerm": term,
        # "activityProgramStartDate": "",
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
    res = []
    m = hold_terms.__len__()
    j = 0
    while j<m:
        term = hold_terms[j]
        j += 1
        vendor = "Acme"
        coachId = "C" + ("%03d"%Rand.get(1000))
        channel = Rand.pick((("phone",75),("email",15),("text",10)))
        initiator = "coach"
        status = "complete"
        startDatetime_dt = datetime.datetime.strptime("2017-02-10T09:38", "%Y-%m-%dT%H:%M")
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
            res.append(generate_prospect_activity(program_of_interest, term, vendor, coachId, channel, initiator,
                                                startDatetime, status, disposition, notes, resultingStatus))
            startDatetime_dt += datetime.timedelta(1, 3600) # 25 hours later
            i += 1
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


def generate_prospect_rating(term):
    res = {
        "ratingProgramOfInterest": program_of_interest,
        "ratingStartTerm": term,
        # "ratingStartDate": "",
        "ratingType": "demographic score",
        "ratingScore": Rand.get(4)
    }        
    return {}


def generate_prospect_ratings():
    res = []
    m = hold_terms.__len__()
    j = 0
    while j<m:
        term = hold_terms[j]
        j += 1
        res.append(generate_prospect_rating(term))
    return res


def generate_person_prospect():
    dt = []
    last = Dates.get_date_in_range("2017-10-01", 45, False)
    dt.append(last)
    for j in (1,4,6):        
        last += datetime.timedelta(Rand.get(j)+1)
        dt.append(last)
    res = {
        "ProspectProgramInterests": [],
        "highlyDesirable": Rand.pick((("High",20),("Medium",50),("Low",30))),
        "prospectComments": "hello, world!",
        "prospectAdmissionsCounselor": "L"+("%06d"%Rand.get(1000000)),
        "prospectExtracurricularInterests": Rand.pick((("Kayaking",20),("Skiing",20),("Swimming",20),("Fencing",20),("Baseball",20))),
        # "prospectContinuedInterestIndicators": "string",
        "athleticProspectIndicator": Rand.get_bool(20),
        "prospectStatus": "active",
        "prospectLegacy": Rand.get_bool(20),
        "optOutFields": "",
        "currentRecruitmentVendor": "Acme",
        "currentRecruitmentCoachID": "L"+("%06d"%Rand.get(1000000)),
        "createdDateTime": dt[0].strftime(isoformat),
        "firstCommunicationType": Rand.pick((("Phone",70),("Email",30))),
        "firstContactedDateTime": dt[1].strftime(isoformat),
        "firstCommunicatedDateTime": dt[2].strftime(isoformat),
        "lastCommunicatedDateTime": dt[3].strftime(isoformat),
        "totalMissedAttemptsAfterCommunicated": 0,
        "totalAttemptsToContact": 3+Rand.get(4),
        "totalAttemptsToCommunicate": 7+Rand.get(4),
        "totalAttemptsToContactAfterCommunicate": 3,
        "leadQuality": Rand.get(4),
        "nextCommunicationObjective": "try to close",
        "ProspectSources": [],
        "ProspectActivity": [],
        "ProspectEvents": [],
        "ProspectRatings": []
    }
    # ProspectProgramInterests must be first
    res["ProspectProgramInterests"] = generate_prospect_program_interests()
    res["ProspectSources"] = generate_prospect_sources()
    res["ProspectActivity"] = generate_prospect_activities()
    res["ProspectEvents"] = generate_prospect_events()
    return res


def generate_application_alternate_ids():
    res = [{
        "applicationAlternateId": "%d"%(Rand.get(1000000)+1000000),
        "applicationAlternateIdType": "SIS"
    }]
    return res


def generate_application_check_list_item():
    res = {
        "checklistItemCode": Rand.pick((("Letter of Reference from " +
                                         Rand.pick((("John Doe",25),
                                                    ("Jane Poe",25),
                                                    ("Joe Blow",25),
                                                    ("Jill Crow",25))),50),
                                        ("Transcript from " + 
                                         Rand.pick((("Malcolm S White University",25),
                                                    ("Springfield University",25),
                                                    ("State University of Euphoria",25),
                                                    ("Rummidge College",25))),50))),
        "checklistItemStatus": Rand.pick((("Received",50),("Waived",10),("Awaiting",40))),
        "checklistItemDate": Dates.get_date_in_range("2017-10-01",45),
        # "checklistItemAssignedDate": "",
        # "checklistItemInstance": "string",
        # "checklistItemComment": "string",
        # "checklistItemFaYear": 0
    }
    return res


def generate_application_check_list_items():
    res = []
    n = Rand.get(3)+3
    i = 0
    while i<n:
        res.append(generate_application_check_list_item())
        i += 1
    return res


def generate_application_financial_aid():
    res = {
        "financialAidStatus": "applied",
        "financialAidType": "grant",
        # "financialAidAwardAmount": "Unknown Type: double",
        # "financialAidAwardYear": "string",
        "fafsaFiled": True
    }
    return res
        

def generate_application_financial_aids(f):
    res = []
    if f:
        res.append(generate_application_financial_aid())
    return res


hold_admitted = False
hold_admitted_date = ""
hold_admitted_date_dt = None


def generate_person_application(term):
    global hold_admitted
    global hold_admitted_date
    global hold_admitted_date_dt
    res = {
        "applicationSisId": "",
        "applicationCRMId": "",
        "applicationAlternateIds": [],
        # "applicationAlternateId": None,
        # "applicationAlternateIdType": None,
        "intentToApplyForFinancialAid": True,
        "applicationType": "",
        "startTerm": "",
        "academicProgram": "",
        "academicProgramCatalog": "",
        "academicLevel": "",
        "location": "",
        "campus": "",
        "college": "",
        # "additionalMajors": "",
        # "intendedAreaOfStudy": "",
        "applicantProspectStatusDate": "",
        "currentApplicationStatus": "",
        "currentApplicationStatusDate": "",
        "applicationStarted": "",
        "applicationStartedDate": "",
        "applicationCompleted": "",
        "applicationCompletedDate": "",
        "applicationSubmitted": "",
        "applicationSubmittedDate": "",
        # "decision": "",
        # "decisionDate": "",
        # "withdrawalDate": "",
        # "withdrawalReason": "",
        # "admitStatus": "",
        "degreeSought": "",
        "applicationComments": "",
        # "influencedToApply": "",
        "fullTimePartTimeIntent": "",
        "applicationFeeReceiptIndicator": True,
        "applicationFeeReceiptDate": "",
        "ApplicationCheckListItems": [],
        "ApplicationFinancialAid": []
    }
    status = Rand.pick((("started",60),("submitted",30),("completed",10)))
    applicationStartedDate_dt = Dates.get_date_in_range("2017-10-15", 40, False)
    applicationStartedDate = applicationStartedDate_dt.strftime(isoformat)
    applicationStarted = "Yes"
    if status=="started":
        feePaid = False
        applicationStarted = "Yes"
        currentStatusDate = applicationStartedDate
        applicationSubmittedDate = ""
        applicationCompletedDate = ""
        applicationSubmitted = "No"
        applicationCompleted = "No"
    else:
        applicationSubmittedDate_dt = applicationStartedDate_dt + datetime.timedelta(Rand.get(7)+1)
        applicationSubmittedDate = applicationSubmittedDate_dt.strftime(isoformat)
        feePaid = True
        applicationSubmitted = "Yes"
        if status=="completed":
            applicationCompletedDate_dt = applicationSubmittedDate_dt + datetime.timedelta(Rand.get(7)+1)
            applicationCompletedDate = applicationCompletedDate_dt.strftime(isoformat)
            currentStatusDate = applicationCompletedDate
            applicationCompleted = "Yes"
        else:
            currentStatusDate = applicationSubmittedDate
            applicationCompletedDate = ""
            applicationCompleted = "No"
    financialAidIntent = Rand.get_bool(20)
    res["applicationSisId"] = "A"+"%d"%(Rand.get(1000000)+1000000)
    res["applicationCRMId"] = "A"+"%d"%(Rand.get(1000000)+1000000)
    res["applicationAlternateIds"] = generate_application_alternate_ids()
    res["intentToApplyForFinancialAid"] = financialAidIntent
    res["applicationType"] = "normal"
    res["startTerm"] = term
    res["academicProgram"] = program_of_interest
    # res["academicProgramCatalog"] = ""
    res["academicLevel"] = "Masters"
    res["location"] = "online"
    res["campus"] = "online"
    res["college"] = "SSW"
    # res["additionalMajors"] = ""
    # res["intendedAreaOfStudy"] = ""
    # res["applicantProspectStatusDate"] = ""
    res["applicantProspectStatusDate"] = currentStatusDate
    res["applicationStarted"] = applicationStarted
    res["applicationStartedDate"] = applicationStartedDate
    res["applicationCompleted"] = applicationCompleted
    res["applicationCompletedDate"] = applicationCompletedDate
    res["applicationSubmitted"] = applicationSubmitted
    res["applicationSubmittedDate"] = applicationSubmittedDate
    # Only one of the applications can be admitted
    if not hold_admitted and applicationCompleted == "Yes" and Rand.get_bool(80):
        decision = Rand.pick((("admitted", 90), ("rejected", 10)))
        decisionDate_dt = applicationCompletedDate_dt + datetime.timedelta(Rand.get(7)+1)
        decisionDate = decisionDate_dt.strftime(isoformat)
        if decision == "admitted":
            hold_admitted = True
            hold_admitted_date = decisionDate
            hold_admitted_date_dt = decisionDate_dt
    else:
        decision = ""
        decisionDate = ""
    res["decision"] = decision
    res["decisionDate"] = decisionDate
    if applicationSubmitted == "Yes" and decision == "" and Rand.get_bool(10):
        withdrawalDate_dt = applicationSubmittedDate_dt + datetime.timedelta(Rand.get(7)+1)
        withdrawalDate = withdrawalDate_dt.strftime(isoformat)
        withdrawalReason = Rand.pick((("financial", 40), ("family", 60)))
        status = "withdrawn"
        currentStatusDate = withdrawalDate
        admitStatus = Rand.pick((("admitted",90),("open",10)))
    else:
        withdrawalDate = ""
        withdrawalReason = ""
        admitStatus = ""
    res["withdrawalDate"] = withdrawalDate
    res["withdrawalReason"] = withdrawalReason
    res["currentApplicationStatus"] = status
    res["currentApplicationStatusDate"] = currentStatusDate
    res["admitStatus"] = admitStatus
    res["degreeSought"] = program_of_interest
    res["applicationComments"] = ""
    # res["influencedToApply"] = ""
    res["fullTimePartTimeIntent"] = Rand.pick((("Part Time",80),("Full Time",20)))
    res["applicationFeeReceiptIndicator"] = feePaid
    res["applicationFeeReceiptDate"] = applicationSubmittedDate

    res["ApplicationCheckListItems"] = generate_application_check_list_items()
    res["ApplicationFinancialAid"] = generate_application_financial_aids(financialAidIntent)
    return res


def generate_person_applications():
    # Most prospects don't actually apply
    if hold_terms.__len__() < 2:
        n = Rand.pick(((0,65),(1,35)))
    else:
        n = Rand.pick(((0,60),(1,35),(2,5)))
    res = []
    i = 0
    while i < n:
        res.append(generate_person_application(hold_terms[i]))
        i += 1
    return res


def generate_person_applicant():
    global hold_admitted
    global hold_admitted_date
    global hold_admitted_date_dt
    # This has to go first, as it picks the hold_admitted value
    hold_admitted = False
    hold_admitted_date = ""
    hold_admitted_date_dt = None
    person_applications = generate_person_applications()
    
    if person_applications.__len__() == 0:
        return None

    if hold_admitted:
        applicantEnrolled = Rand.get_bool(80)
        applicantEnrolledDate = (hold_admitted_date_dt +  datetime.timedelta(Rand.get(7)+1)).strftime(isoformat)
    else:
        applicantEnrolled = False
        applicantEnrolledDate = ""

    res = {
        "housingDesiredIndicator": False,
        "admissionsCounselor": "L" + ("%06d"%Rand.get(1000000)),
        "applicantProspectStatus": "normal",
        "applicantAdmitted": hold_admitted,
        "applicantAdmittedDate": hold_admitted_date,
        "applicantEnrolled": False,
        "applicantEnrolledDate": applicantEnrolledDate,
        # "extracurricularInterests": "string",
        # "continuedInterestIndicators": "string",
        # "careerGoals": "string",
        # "educationalGoals": "string",
        # "applicantComments": "string",
        "legacy": Rand.get_bool(20),
        # "officialOffCampusVisitDate": "string",
        # "officialOnCampusVisitDate": "string",
        # "unofficialVisitDate": "string",
        # "applicantMisc1": "string",
        # "applicantMisc2": "string",
        # "applicantMisc3": "string",
        # "applicantMisc4": "string",
        # "restrictions": "string",
        "PersonApplications": person_applications
    }
    
    return res


# ---------------------

if sys.argv.__len__()<2:
    sys.stderr.write("number of records?\n")
else:
    sys.stdout.write(json.dumps(generate_hedex(int(sys.argv[1])),indent=None))
    sys.stdout.write("\n")

