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
university_country = "US"

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
        x.update(
            {
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
                    "facInd": i <= n_faculty,
                    "advInd": False,
                    "staffInd": i > n_staff,
                }
            }
        )
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
        address = Addresses.get_address()
        birth_address = Addresses.get_address()
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
            "listOfRaces": Rand.pick((("White",50), ("Black",20), ("Asian",10), ("White|Black",7), ("While|Asian",3), ("Black|Asian",2), ("N/A",15), ("Other",3))),
            "languagesSpoken": Rand.pick((("English",80), ("English|Spanish",15), ("English|Serbian", 5))),
            "primaryLanguage": "English",
            "alienStatus": None,
            "countryOfCitizenship": "US",
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
                    "addressLine1": address_line_1,
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
                "studentCurrentStatus": "Enrolled"
            }
        })
        studentTermItems = []
        credits = 0
        cut_date_str = cut_date.strftime("%Y-%m-%d")
        for term in retention_catalog_terms:
            if not term.get("sessionStartDate"):
                continue
            if term["startDate"] > cut_date_str:
                break
            credits += Rand.get(10) + 10
            problem = Rand.get_bool(80)
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
                "currAcadStanding": "Enrolled",
                "totalWithdrawls": 0,
                "creditsOnTrack": not problem,
                "estCreditsToGraduate": 120-credits,
                "currentFaHold": problem,
                "currentBursarHold": Rand.get_bool(50) if problem else False,
                "primaryProgramCode": Words.get(),
                "primaryProgramLevel": "Graduate",
                "primaryDegreeCode": "MS",
                "primaryMajor1": None,
                "primaryMajor2": None,
                "primaryConcentration1": None,
                "primaryConcentration2": None,
                "primaryMinor1": None,
                "primaryMinor2": None,
                "secondaryProgramCode": None,
                "secondaryProgramLevel": None,
                "secondaryDegreeCode": None,
                "secondaryMajor1": None,
                "secondaryMajor2": None,
                "secondaryConcentration1": None,
                "secondaryConcentration2": None,
                "secondaryMinor1": None,
                "secondarysMinor2": None,
                "studentStatus": None
            })
        x["StudentItems"]["studentTermItems"] = studentTermItems
        retention_studentrecords_students.append(x)
    return _make_batch("students", retention_studentrecords_students)


def _generate_enrollment(output_array, person_array, n_person, enrollmentType, n_members_avg):
    for section in retention_catalog_sections:
        i = 0
        used = set([])
        if n_members_avg == 1:
            n_members = 1
        else:
            n_members = n_members_avg + Rand.get(5) - 2
        while i < n_members:
            i += 1
            k = Rand.get(n_person)
            while k in used:
                k = Rand.get(n_person)
            person = person_array[k]
            x = {
                "enrollmentType": enrollmentType,
                "personSisId": person["personSisId"],
                "personLmsId": person["personLmsId"],
                "sisSectionId": section["sisSectionId"],
                "lmsSectionId": section["lmsSectionId"],
                "termCode": section["termCode"],
                "sectionRefNum": section["sectionRefNum"],
                "subjectCode": section["subjectCode"],
                "sectionCourseNumber": section["sectionCourseNumber"],
                "sectionNumber": section["sectionNumber"],
                "nonTermIndicator": section["nonTermIndicator"],
                "enrollStatus": "A",
                "enrollStatusDate": section["sectionStartDate"],
            }
            output_array.append(x)


retention_facultystaff_teaching = []
def generate_retention_facultystaff_teaching():
    _generate_enrollment(retention_facultystaff_teaching, retention_facultystaff_staff, n_faculty, "Faculty", 1)
    for e in retention_facultystaff_teaching:
        e.update({"enrollType": "Primary"})
    return _make_batch("teaching", retention_facultystaff_teaching)


def _get_grade():
    return Rand.pick((("A+",5),("A",5),("A-",5),("B+",20),("B",20),("B-",20),("C+",8),("C",4),("C-",3),("F",10)))


retention_studentrecords_studentenrollments = []
def generate_retention_studentrecords_studentenrollments():
    _generate_enrollment(retention_studentrecords_studentenrollments, retention_studentrecords_students, retention_studentrecords_students.__len__(), "Student", 10)
    for e in retention_studentrecords_studentenrollments:
        e.update({
            "currentGrade": _get_grade(),
            "enrollType": "Graded",
            "midTermGrade": "string",
            "midtermGradeScheme": "A-F",
            "midTermGradeDate": e["enrollStatusDate"],
            "finalGrade": _get_grade(),
            "finalGradeDate": e["enrollStatusDate"],
            "finalGradeScheme": "A-F",
            "creditsAttempted": 5,
            "creditsEarned": 5
        })
    return _make_batch("studentEnrollments", retention_studentrecords_studentenrollments)


retention_facultystaff_advisingrelationship = []
def generate_retention_facultystaff_advisingrelationship():
    n = retention_facultystaff_staff.__len__()
    cut_date_str = cut_date.strftime("%Y-%m-%d")
    for term in retention_catalog_terms:
        if term.get("sessionStartDate"):
            continue
        if term["startDate"] > cut_date_str:
            break
        for student in retention_studentrecords_students:
            j = Rand.get(n)
            advisor = retention_facultystaff_staff[j]
            retention_facultystaff_advisingrelationship.append({
                "advrId": advisor["personSisId"],
                "studentId": student["personSisId"],
                "advrTermCode": term["termCode"],
                "advrType": "Faculty" if j<n_faculty else "Staff",
                "advrStatusInd": "A",
                "advrTermStart": term["startDate"],
                "advrTermEnd": term["endDate"]
            })
    return _make_batch("advisors", retention_facultystaff_advisingrelationship)


def _copy_enrollment(e):
    return {
        "personSisId": e["personSisId"],
        "personLmsId": e["personLmsId"],
        "sisSectionId": e["sisSectionId"],
        "lmsSectionId": e["lmsSectionId"],
        "termCode": e["termCode"],
        "sectionRefNum": e["sectionRefNum"],
        "subjectCode": e["subjectCode"],
        "sectionCourseNumber": e["sectionCourseNumber"],
        "sectionNumber": e["sectionNumber"]
    }


retention_engagement_assignments = []
def generate_retention_engagement_assignments():
    for e in retention_studentrecords_studentenrollments:
        n = 10
        i = 0
        while i < n:
            i += 1
            assignGrade = _get_grade()
            assignScore = Rand.get(11)
            x = _copy_enrollment(e)
            x.update({
                "assignmentLmsId": "LA%09d"%Rand.get(1000000000),
                "submissionVersionId": 1,
                "assignType": Rand.pick((("Term Paper",20),("Quiz",40),("Midterm Exam",10),("Final Exam",10),("Forum Post",20))),
                "assignTitle": " ".join(Words.get_n(Rand.get(3)+1)),
                "assignDueDate": e["enrollStatusDate"],
                "assignGrade": assignGrade,
                "assignGradeScheme": "A-F",
                "assignScore": assignScore,
                "assignScoreScheme": "0-10",
                "assignHiScore": assignScore,
                "assignLoScore": assignScore,
                "assignFirstAttmpt": assignScore,
                "assignLastAttmpt": assignScore,
                "assignAvgAttmpt": assignScore,
                "assignNumAttempt": 1
            })
            retention_engagement_assignments.append(x)
    return _make_batch("assignments", retention_engagement_assignments)


retention_engagement_engagementactivity = []
def generate_retention_engagement_engagementactivity():
    for e in retention_studentrecords_studentenrollments:
        engagementStatus = Rand.pick((("None", 10),("Low",20),("Medium",50),("High",20)))
        if engagementStatus == "None":
            lmsLastAccessDate = None
            lmsTotalTime = 0
            lmsTotalLogin = 0
        elif engagementStatus == "Low":
            lmsLastAccessDate = e["enrollStatusDate"]
            lmsTotalTime = "00-00-%d" % (Rand.get(39)+20)
            lmsTotalLogin = Rand.get(10) + 10
        elif engagementStatus == "Medium":
            lmsLastAccessDate = e["enrollStatusDate"]
            lmsTotalTime = "00-%d-20" % (Rand.get(5)+7)
            lmsTotalLogin = Rand.get(10) + 30
        else:
            lmsLastAccessDate = e["enrollStatusDate"]
            lmsTotalTime = "02-%d-20" % (Rand.get(49)+10)
            lmsTotalLogin = Rand.get(10) + 50
        x = _copy_enrollment(e)
        x.update({
            "engagementStatus": engagementStatus,
            "lmsLastAccessDate": lmsLastAccessDate,
            "lmsTotalTime": lmsTotalTime,
            "lmsTotalLogin": lmsTotalLogin
        })
        retention_engagement_engagementactivity.append(x)
    return _make_batch("engagementActivity", retention_engagement_engagementactivity)


retention_engagement_attendance = []
def generate_retention_engagement_attendance():
    for e in retention_studentrecords_studentenrollments:
        totalAttendanceEvents = 8 + Rand.get(4)
        attendanceStatus = Rand.pick((("Red", 10),("Yellow",30),("Green",60)))
        if attendanceStatus == "Red":
            totalTardyEvents = Rand.get(3)
            totalAbsentEvents = totalAttendanceEvents - totalTardyEvents - Rand.get(4)
        elif attendanceStatus == "Yellow":
            totalAbsentEvents = totalAttendanceEvents - 4 - Rand.get(3)
            totalTardyEvents = Rand.get(2)
        else:
            totalAbsentEvents = Rand.get(3)
            totalTardyEvents = Rand.get(2)
        x = _copy_enrollment(e)
        x.update({
            "attendanceStatus": attendanceStatus,
            "totalAttendanceEvents": totalAttendanceEvents,
            "totalAbsentEvents": totalAbsentEvents,
            "totalTardyEvents": totalTardyEvents
        })
        retention_engagement_attendance.append(x)
    return _make_batch("attendance", retention_engagement_attendance)


# Generate all files
files = ((generate_retention_catalog_terms, "Retention_Catalog_Term"),
         (generate_retention_catalog_sections, "Retention_Catalog_Sections"),
         (generate_retention_facultystaff_staff, "Retention_FacultyStaff_Staff"),
         (generate_retention_studentrecords_students, "Retention_StudentRecords_Students"),
         (generate_retention_facultystaff_teaching, "Retention_FacultyStaff_Teaching"),
         (generate_retention_studentrecords_studentenrollments, "Retention_StudentRecords_StudentEnrollments"),
         (generate_retention_facultystaff_advisingrelationship, "Retention_FacultyStaff_AdvisingRelationship"),
         (generate_retention_engagement_assignments, "Retention_Engagement_Assignments"),
         (generate_retention_engagement_engagementactivity, "Retention_Engagement_EngagementActivity"),
         (generate_retention_engagement_attendance, "Retention_Engagement_Attendance")
        )

def generate_all_files():
    for proc, fn in files:
        val = proc()
        with open('%s_%s.json'%(fn,datetime.datetime.now().strftime("%Y%m%d%H%M%S")), "w") as f:
            json.dump(val, f, indent=2)

generate_all_files()
