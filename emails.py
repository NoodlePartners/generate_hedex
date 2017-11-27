from rand import Rand

class Emails(object):
    
    domains = [
        "gmail.com",
        "yahoo.com",
        "aol.com",
        "mail.com",
        "hotmail.com",
        "outlook.com",
        "inbox.com",
        "mail.com"
    ]

    n_domains = domains.__len__()

    _percent_gnfi = 30
    _percent_numbers = 90
    _max_number = 39
        
    @classmethod
    def get_email(self, given_name, family_name):
        if Rand.get(100) < self._percent_gnfi:
            email = given_name + family_name[0]
        else:
            email = given_name[0] + family_name
        email = email.lower()
        if Rand.get(100) < self._percent_numbers:
            email += str(Rand.get(self._max_number)+1)
        email += "@" + self.domains[Rand.get(self.n_domains)]
        
        return email


    _max_u_number = 999
    _u_domain = "swigmore.edu"

    @classmethod
    def get_u_email(self, given_name, family_name):
        id = (given_name[0] + family_name[0] + "%03d" %  (Rand.get(self._max_number)+1)).lower()
        email = id + "@" + self._u_domain
        return {"email": email, "id": id}
