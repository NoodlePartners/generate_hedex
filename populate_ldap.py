import ldap, os, csv
from passlib.hash import ldap_sha256_crypt

class PopulateLdap(object):
    # LDAP params
    ldap_host = "ldap://poc-ldap.noodle-partners.com"
    # trick: "ldap://x.y.com" -> ".x.y.com" -> ["", "x", "y", "com"] -> ",dc=x,dc=y,dc=com" 
    ldap_dc_suffix = ",dc=".join(ldap_host.replace("ldap://", ".").split("."))
    ldap_username = "cn=admin" + ldap_dc_suffix
    ldap_ou = 'Users'
    ldap_user_dn_suffix = ",ou=" + ldap_ou + ldap_dc_suffix
    ldap_password = "c0nceptPr0of"


    # Mapping for spreadsheet (copied from make_users), added email
    renamed = {
        "First Name": "firstname",
        "Last Name": "lastname",
        "Former Last Name": "",
        "Community Email": "email",
        "Preferred Name": "",
        "Primary Email": "",
        "2ndary Email": "",
        "Telephone Number": "phone",
        "Home Address": "address",
        "City": "city",
        "State": "state",
        "Country": "country",
        "Apt #": "address2",
        "Current Zipcode": "zip",
        "Unique ID": "external_user_id",
        "Username": "",
        "Date of Birth": "birthdate",
        "Gender": "gender",
        "Country of Birth": "",
        "Zip Code of Birth": "",
        "Race": "",
        "First Generation College?": "",
        "Marital Status": "",
        "Highest Level of Education for Parents": "",
        "Hours Per Week Working": "",
        "Parent's Income Level": "",
        "Parent's Marital Status": "",
        "Number of Children": "",
        "Number of Siblings": "",
        "Highest Educational Attainment of Sibling": "",
        "Military Status Military Service": "",
        "Highest Military Rank": "",
        "Military Spouse?": "",
        "Employer": "",
        "Application": "",
        "Application Writing Samples": "",
        "Documents": "",
        "Application Date": "",
        "Accepted Date": "",
        "Community Join Date": "",
        "Highest Level of Education": "",
        "Application (lead source)": "",
        "High School Attended": "",
        "Learning Disability?": "",
        "Emotional Disturbances?": "",
        "Has dropped out in past?": "",
        "High School Grade Point Average": "",
        "Status": "",
        "Last Program Change": "",
        "Transfer Credit Evaluation": "",
    }

    con = None

    @classmethod
    def connect(self):
        try:
            self.con = ldap.initialize(self.ldap_host)
            self.con.simple_bind_s(self.ldap_username, self.ldap_password)
        except Exception as e:
            print "Unable to connect to %s, user %s" % (self.ldap_host, self.ldap_username)
            print e.__repr__()
            exit(1)

    @classmethod
    def populate_ldap(self):
        self.connect()
        with open('test1.csv', 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            i = 0
            for row in csvreader:
                i += 1
                if i == 1:
                    names = []
                    for val in row:
                        names.append(val)
                else:
                    user_info = {}
                    j = 0
                    for val in row:
                        if type(val) == unicode:
                            vv = val.encode("utf-8")
                        elif type(val) == str:
                            vv = val
                        else:
                            vv = str(val)
                        if names[j] in self.renamed:
                            col = self.renamed[names[j]]
                        if col:
                            user_info[col] = vv
                        j += 1
                    self.create_user(user_info["external_user_id"],
                        user_info["email"],
                        user_info["firstname"],
                        user_info["lastname"],
                        "password")

    @classmethod
    def create_user(self, uid, email, first_name, last_name, password):

        if not uid or not email or not first_name or not last_name or not password:
            print "missing data for %s %s" % (uid, email)
            
        print "%s %s %s %s %s" % (uid, email, first_name, last_name, password)
        
        full_name = "%s %s" % (first_name, last_name)
        
        user_dn = self._get_user_dn(uid)
        user_record = [
                       ('objectclass', ['person', 'organizationalPerson', 'inetOrgPerson']),
                       ('mail', [email]),('cn', [full_name] ),('displayName', [full_name] ),
                       ('sn', [last_name] ),('userpassword', [ldap_sha256_crypt.encrypt(password)]),
                       ('ou', ['Users']),
                       ]

        print user_dn.__repr__()
        print user_record.__repr__()
        
        try:            
            rs = self.con.add_s(user_dn, user_record)
        except ldap.ALREADY_EXISTS:
            print 'error: ldap.ALREADY_EXISTS: %s' % user_dn
        except ldap.LDAPError, e:
            print 'error in create_user: %s' % user_dn
            print e.__repr__()

        return None


    @classmethod
    def _get_user_dn(self, uid):        
        return 'uid=' + uid + self.ldap_user_dn_suffix
