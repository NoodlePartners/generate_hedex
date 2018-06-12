#!/usr/bin/python3
from names import Names
from addresses import Addresses
from emails import Emails
from rand import Rand
from dates import Dates
from hashlib import sha256, sha1
import sys
import datetime
import json

_birthday_start_date = "1990-10-10"
_birthday_n_days = 5 * 365

_u_domain = "cgu.edu"
# _u_domain = "tulane.edu"

programs = ["MS in Information Systems & Technology (Online)",
            "MS in Marketing Analytics (Online)",
            "MS in Evaluation & Applied Research (Online)"]
# programs = ["MPS - Information Technology Management (Online)"]
n_programs = programs.__len__()

terms = ["Summer 2018", "Fall 2018", "Spring 2019"]
n_terms = terms.__len__()

# See make_application if you want to change this
docs = ["Resume/CV","Statement of Purpose","Transcript: %s","Reference: %s %s, %s"]

# Set this to True to add " TEST" to the end of person names
add_test_to_names = True

# -----------------------------------------

file_types = [
    "Catalog_Sections",
    "Catalog_Terms",
    "FacultyStaff_AdvisingRelationship",
    "FacultyStaff_Staff",
    "FacultyStaff_Teaching",
    "StudentRecords_StudentEnrollments",
    "StudentRecords_Students",
    "StudentRecords_StudentTerms"
]

columns = {}
columns["Catalog_Sections"] = []
columns["Catalog_Terms"] = []
columns["FacultyStaff_AdvisingRelationship"] = []
columns["FacultyStaff_Staff"] = []
columns["FacultyStaff_Teaching"] = []
columns["StudentRecords_StudentEnrollments"] = []
columns["StudentRecords_Students"] = []
columns[""] = []

if add_test_to_names:
    _name_extra = " TEST"
else:
    _name_extra = ""

def get_program(i):
    return programs[i%n_programs]


def print_row(f, r):
    f.write('"'+'","'.join(r)+"\"\n")


def get_noodle_crm_id():
    return sha1(str.encode('{}'.format(datetime.datetime.utcnow().timestamp()))).hexdigest()


def get_noodle_source_id(contact_id):
    return sha256(str.encode(('{}+{}'.format(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S.%f'),contact_id)))).hexdigest()


def get_status_and_decision(decided_datetime_str):
    status = Rand.pick((
                    ("", 10),
                    ("Awaiting Submission",35),
                    ("Awaiting Payment",5),
                    ("Awaiting Materials",15),
                    ("Awaiting Decision",5),
                    ("Awaiting Confirmation",10),
                    ("Decided",20)))
    admit_date = ""
    deny_date = ""
    # The full list of decisions is
    # "Admit","Deposit Pending","Deposit Paid (Enroll)","Admit/Decline","Deny","Defer",
    # "Waitlist","Waitlist/Accept","Waitlist/Decline","Withdraw"
    # But we won't use any of the Waitlist ones because thyey aren't relevant to us
    if status == "Awaiting Confirmation" or status == "Decided":
        decision = Rand.pick((
            ("Admit",20),
            ("Deposit Pending",10),
            ("Deposit Paid (Enroll)",20),
            ("Admit/Decline",10),
            ("Deny",10),
            ("Defer",10),
            ("Withdraw",20)))
        if decision == "Deny":
            deny_date = decided_datetime_str
        elif decision != "Withdraw":
            admit_date = decided_datetime_str
    else:
        decision = ""
    
    return (status, decision, admit_date, deny_date)


def make_person(f, ref, name_x, noodle_crm_id, program, term, zip2, email1, mp1, highest_ed, years_work, has_application, has_inquiry):
    row = []
    # "Ref"
    row.append(ref)
    # "SIS ID"
    row.append("S%08d"%Rand.get(100000000))
    # "Preferred"
    row.append(name_x["preferred_given_name"])
    # "First"
    first_name = name_x["given_name"]
    row.append(first_name + _name_extra)
    # "Middle"
    row.append("")
    # "Last"
    last_name = name_x["family_name"]
    row.append(last_name + _name_extra)
    # "Suffix"
    row.append("")
    # "Alias"
    row.append("")
    # "Birthdate"
    row.append(Rand.get_date_in_range(_birthday_start_date, _birthday_n_days))
    # "Sex"
    row.append(name_x["gender"])
    # "IPEDS"
    if has_application:
        ipeds = Rand.pick((("Nonresident Alien", 20), ("Decline",20),("Asian",10),("White",25),("Hispanic of any race",15),("Black",10)))
    else:
        ipeds = "Race/Ethnicity Unknown"
    row.append(ipeds)
    # "Race"
    race = ""
    if has_application:
        if ipeds == "Nonresident Alien":
            race = "Decline"
        else:
            race = ipeds
    row.append(race)
    # "Primary Citizenship"
    if has_application:
        if ipeds == "Nonresident Alien":
            citiz = Rand.pick((("Mexico",40),("Honduras",30), ("Ukraine",15),("Kenya",15)))
        else:
            citiz = "United States"
    else:
        citiz = ""
    row.append(citiz)
    # "noodleCrmId"
    row.append(noodle_crm_id)
    # "Street 1","Street 2","City","Region","Postal","Zip Code (Stand Alone)","Country",
    address_x = Addresses.get_address()
    if has_application:
        street1 = address_x["building_number"] + " " + address_x["street_name"]
        apt = address_x["apt"]
        if not apt:
            street2 = ""
        else:
            street2 = "Apt " + apt
        city = address_x["city"]
        state = address_x["state"]
        zip1 = address_x["postal_code"]
        # zip2 is a param
        country = "United States"
    else:
        street1 = ""
        street2 = ""
        city = ""
        state = ""
        zip1 = ""
        # Since there isn't an application, there must be an inquiry
        zip2 = address_x["postal_code"]
        country = ""
    row.append(street1)
    row.append(street2)
    row.append(city)
    row.append(state)
    row.append(zip1)
    row.append(zip2)
    row.append(country)
    # "Prospect Status"
    if has_application:
        pstatus = "Applicant"
    else:
        pstatus = Rand.pick((("Prospect",90),("Inquiry",10)))
    row.append(pstatus)
    # "Initial Inquiry"
    if pstatus == "Inquiry":
        init_inq = Dates.get_date_in_range("2018-02-01",30) + " 12;15"
    else:
        init_inq = ""
    row.append(init_inq)
    # "Tags"
    contacted = False
    tags = []
    if Rand.get_bool(20):
        tags.append("Call Opt Out")
        tags.append("Email Opt Out")
        tags.append("Text Opt Out")
    else:
        if Rand.get_bool(20):
            tags.append("Call Opt Out")
        if Rand.get_bool(20):
            tags.append("Email Opt Out")
        if Rand.get_bool(20):
            tags.append("Email Opt Out")
    if Rand.get_bool(20):
        contacted = True
        tags.append("Contacted")
    if Rand.get_bool(10):
        tags.append("Test Record")
    row.append(", ".join(tags))
    # "prospectFull-Time/PartTimeIntent",
    row.append("")
    # "Anticipated Start Term",
    row.append(term)
    # "Person Updated",
    row.append("2018-03-01 12:14")
    # "Highest Level of Education"
    row.append(highest_ed)
    # "Years of Work Experience"
    row.append(years_work)
    # "Interaction Date"
    if Rand.get_bool(10):
        int_date = Dates.get_date_in_range("2018-02-01",30) + " 12;15"
    else:
        int_date = ""
    row.append(int_date)
    # "Interaction Summary",
    if int_date:
        int_sum = "test"
    else:
        int_sum = ""
    row.append(int_sum)
    # "Degree of Interest",
    row.append(program)
    # "Institution Email",
    row.append(Emails.get_u_email(first_name, last_name, u_domain=_u_domain)["email"])
    # "Device Email Address #1","Device Email Address #2","Device Email Address #3","Device Email Address #4","Device Email Address #5",
    #TODO: dry this out
    n_emails = Rand.pick(((1,70),(2,20),(3,10)))
    # email1 is a param
    if n_emails>1:
        email2 = Emails.get_email(first_name, last_name)
        if n_emails>2:
            email3 = Emails.get_email(first_name, last_name)
        else:
            email3 = ""
    else:
        email2 = ""
        email3 = ""
    row.append(email1)
    row.append(email2)
    row.append(email3)
    row.append("")
    row.append("")
    # "Device Evening Phone #1","Device Evening Phone #2","Device Evening Phone #3","Device Evening Phone #4","Device Evening Phone #5",
    if has_application:
        n_ep = Rand.pick(((1,90),(2,10)))
        ep1 = Addresses.get_phone(prefix=True)
        if n_ep>1:
            ep2 = Addresses.get_phone(prefix=True)
        else:
            ep2 = ""
    else:
        ep1 = ""
        ep2 = ""
    row.append(ep1)
    row.append(ep2)
    row.append("")
    row.append("")
    row.append("")
    # "Device Mobile Phone #1","Device Mobile Phone #2","Device Mobile Phone #3","Device Mobile Phone #4","Device Mobile Phone #5",
    n_mp = Rand.pick(((1,70),(2,20),(3,10)))
    # mp1 is a param
    if n_mp>1:
        mp2 = Addresses.get_phone(prefix=True)
        if n_mp>2:
            mp3 = Addresses.get_phone(prefix=True)
        else:
            mp3 = ""
    else:
        mp2 = ""
        mp3 = ""
    row.append(mp1)
    row.append(mp2)
    row.append(mp3)
    row.append("")
    row.append("")
    # "Device Primary Phone #1","Device Primary Phone #2","Device Primary Phone #3","Device Primary Phone #4","Device Primary Phone #5",
    if has_application:
        n_pp = Rand.pick(((1,90),(2,10)))
        pp1 = Addresses.get_phone(prefix=True)
        if n_pp>1:
            pp2 = Addresses.get_phone(prefix=True)
        else:
            pp2 = ""
    else:
        pp1 = ""
        pp2 = ""
    row.append(pp1)
    row.append(pp2)
    row.append("")
    row.append("")
    row.append("")
    # "Interaction Private Comments"
    row.append("")
    print_row(f, row)

# Sample json blob:
# {"marketingSourceAdditionalId": "426459", "sourceClickId": "8146238", "utmMedium": "Web", "sourceProgramOfInterest": "Master of Science in Evaluation and Applied Research", "sourcePrimaryId": "096a6090a09ff5c0ed3ce15fdb737e6757f23af38009fcc40a03f0b8b322a036", "sourceDateTime": "2018-02-23T19:52:44Z", "cookieSourceAdditionalId": "326435", "utmContent": "world", "utmSource": "Web Search", "postalCodeType": "INQUIRY", "postalCode": "", "sourceStartTerm": "unspecified", "testScoreStatus": "Taken", "utmCampaign": "Campaign 714", "urlOnSubmission": "http://www.google.com", "utmTerm": "CGU"}

def make_inquiry(f, ref, name_x, noodle_crm_id, program, term, zip2, email1, mp1, highest_ed, years_work):
    row = []
    # "Ref"
    row.append(ref)
    # "noodleCrmId"
    row.append(noodle_crm_id)
    # "sourcePrimaryId"
    source_primary_id = get_noodle_source_id(noodle_crm_id+"0123456789abcdef"[Rand.get(16)])
    row.append(source_primary_id)
    # "firstName"
    row.append(name_x["given_name"]+_name_extra)
    # "lastName"
    row.append(name_x["family_name"]+_name_extra)
    # "Public Comments"
    jblob = {
        "marketingSourceAdditionalId": str(Rand.get(100000)),
        "sourceClickId": str(Rand.get(10000000)),
        "sourceProgramOfInterest": program,
        "sourcePrimaryId": "%d"%(Rand.get(1000000)+1000000),
        "sourceDateTime": Dates.get_date_in_range("2018-02-01",30)+"T09:12:13Z",
        "cookieSourceAdditionalId": "%d"%(Rand.get(1000000)+1000000),
        "postalCodeType": "INQUIRY",
        "postalCode": zip2,
        "sourceStartTerm": term,
        "testScoreStatus": Rand.pick((("taken",30),("registered",40),("not registered",30))),
        "urlOnSubmission": "http://www.google.com",            
        "utmSource": Rand.pick((("Google",50),("Facebook",30),("Bing",20))),
        "utmMedium": "Web Search",
        "utmCampaign": Rand.pick((("Red", 60),("Blue",40))),
        "utmTerm": Rand.pick((("Yo", 50),("Dude",50))),
        "utmContent": "Yow!"
    }
    row.append(json.dumps(jblob).replace('"','""'))
    # "yearsOfWorkExperience",
    row.append(years_work)
    # "postalCode"
    row.append(zip2)
    # "highestLevelOfEducation"
    row.append(highest_ed)
    # "emailAddress"
    row.append(email1)
    # "phoneNumber"
    row.append(mp1)

    print_row(f, row)

datetime_format = "%Y-%m-%d %H:%M"

def make_application(f, ref, program, term):
    row = []
    # "Application ID"
    row.append("%09d"%Rand.get(1000000000))
    # "Ref"
    row.append(ref)
    # "Campus"
    row.append("Online")
    # "Academic Program"
    row.append(program)
    # "Application Status"
    created_date = datetime.datetime.strptime(Dates.get_date_in_range("2017-12-15", 30),"%Y-%m-%d")
    created_datetime = created_date + datetime.timedelta(seconds=(8*3600+Rand.get(12*3600)))
    created_datetime_str = created_datetime.strftime(datetime_format)
    submitted_datetime = created_datetime + datetime.timedelta(days=1+Rand.get(3))
    submitted_datetime_str = submitted_datetime.strftime(datetime_format)
    paid_datetime = submitted_datetime + datetime.timedelta(days=5+Rand.get(4))
    completed_datetime = paid_datetime + datetime.timedelta(days=4+Rand.get(3))
    completed_datetime_str = completed_datetime.strftime(datetime_format)
    decided_datetime = submitted_datetime + datetime.timedelta(days=2+Rand.get(4))
    decided_datetime_str = decided_datetime.strftime(datetime_format)
    status, decision, admit_date, deny_date = get_status_and_decision(decided_datetime_str)
    row.append(status)
    # "Decision"
    row.append(decision)
    # "Admit Date"
    row.append(admit_date)
    # "Deny Date"
    row.append(deny_date)
    # "App Created"
    row.append(created_datetime_str)
    # "App Submitted"
    row.append(submitted_datetime_str)
    # "App Completed"
    row.append(completed_datetime_str)
    # Get docs
    my_docs = []
    my_docs.append([docs[0],"Fulfilled"])
    my_docs.append([docs[1],"Fulfilled"])
    my_docs.append([docs[2]%Names.get_university_name(),"Fulfilled"])
    if status == "Awaiting Submission":
        n_refs = Rand.get(1)
    else:
        n_refs = 2+Rand.get(2)
    j = 0
    while j<n_refs:
        j+=1
        n_x = Names.get_name()
        my_docs.append([docs[3]%(n_x["given_name"],n_x["family_name"],Names.get_corporation_name()),"Fulfilled"])
    for d in my_docs:
        if status == "Awaiting Submission" or status == "Awaiting Payment" or status == "In Progess":
            d[1] = Rand.pick((("Missing",55),("Waived",10),("Fulfilled",35)))
        else:
            d[1] = Rand.pick((("Waived",10),("Fulfilled",90)))
    xx = {"Missing":[],"Waived":[],"Fulfilled":[]}
    for d in my_docs:
        xx[d[1]].append(d[0])
    # "All Missing Checklist Items"
    row.append("|".join(xx["Missing"]))
    # "All Waived Checklist Items"
    row.append("|".join(xx["Waived"]))
    # "All Fulfilled Checklist Items"
    row.append("|".join(xx["Fulfilled"]))
    # "Deposit Date"
    if status == "Accepted":
        deposit_datetime_str = (decided_datetime + datetime.timedelta(days=21+Rand.get(4))).strftime(datetime_format)
    else:
        deposit_datetime_str = ""
    row.append(deposit_datetime_str)
    # "Application Updated"
    if status=="Awaiting Submission":
        updated_datetime_str = created_datetime_str
    else:
        updated_datetime_str = submitted_datetime_str
    row.append(updated_datetime_str)
    # "Round Key"
    row.append("CGU")
    # "Entry Term (Application Scoped)"
    row.append(term)
    # "App FullTime/PartTimeIntent"
    row.append("")
    # "Application Fee Waiver Code"
    if Rand.get_bool(10):
        afwc = "Waive"
    else:
        afwc = ""
    row.append(afwc)
    # "Interaction Date"
    row.append(created_datetime_str)
    # "Interaction Code"
    row.append("SOURCE")

    print_row(f, row)


	#{
		#"highestLevelOfEducation": ["high school", "associate's", "bachelor's in progress", "bachelor's", "master's in progress", "master's", "doctorate"]
	#},
	#{
		#"yearsOfWorkExperience": ["0-1 years", "2-3 years", "3 or more years"]
	#},
	#{
		#"testScoreStatus": ["taken", "registered", "not registered"]
	#}

# -------
# Start!
# -------

if sys.argv.__len__()<2:
    n = 10
else:
    n = int(sys.argv[1])

if n<10:
    n = 10

# Open files, write headers
suffix = suffix = datetime.datetime.now().strftime("_%Y%m%d_01_%H%M%S.csv")
file = {}
for t in file_types:
    file[t] = open("idata_"+t+suffix, "w")
    print_row(file[t], columns[t])

i = 0
while i < n:
    i += 1
    
    # make a ref
    ref = "%09d"%Rand.get(1000000000)

    # get a name
    name_x = Names.get_name()

    # get a program
    program = get_program(i)

    # Determine if the person has an application
    # and pick the first term
    term = ""
    has_inquiry = Rand.get_bool(90)
    if not has_inquiry:
        has_application = True
        noodle_crm_id = ""
        zip2 = ""
        highest_ed = ""
        years_work = ""
    else:
        has_application = Rand.get_bool(15)
        if has_application:
            term = terms[Rand.get(n_terms)]
        noodle_crm_id = get_noodle_crm_id()
        zip2 = Addresses.get_address()["postal_code"]
        highest_ed = Rand.pick((("high school",10),("associate's",10),("bachelor's in progress",20),("bachelor's",20),("master's in progress",10),("master's",20),("doctorate",10)))
        years_work = Rand.pick((("0-1 years",30),("2-3 years",40),("3 or more years",30)))

    email1 = Emails.get_email(name_x["given_name"], name_x["family_name"])
    mp1 = Addresses.get_phone(prefix=True)

    # Make a person
    make_person(file["person"], ref, name_x, noodle_crm_id, program, term, zip2, email1, mp1, highest_ed, years_work, has_application, has_inquiry)

    if has_application:
        n_apps = Rand.pick(((1,85),(2,10),(3,5)))
        j = 0
        term_x = term
        program_x = program
        while j < n_apps:
            j += 1
            make_application(file["application"], ref, program_x, term_x)
            term_x = terms[Rand.get(n_terms)]
            program_x = get_program(i+j)

    if has_inquiry:
        n_inqs = Rand.pick(((1,60),(2,20),(3,15),(4,5)))
        j = 0
        term_x = "" # first one will have no term
        program_x = program
        while j < n_inqs:
            j += 1
            make_inquiry(file["inquiry"], ref, name_x, noodle_crm_id, program, term, zip2, email1, mp1, highest_ed, years_work)
            term_x = terms[Rand.get(n_terms)]
            program_x = get_program(i+j)
        
