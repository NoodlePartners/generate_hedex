from names import Names
from addresses import Addresses
from emails import Emails
from rand import Rand
import sys

def p(x):
    sys.stdout.write(x)

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
    data["Former Last Name"] = name["birth_name"]

    u_email = Emails.get_u_email(given_name, family_name)
    data["Community Email"] = u_email["email"]

    data["Preferred Name"] = name["preferred_name"]

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
