from rand import Rand
import datetime

class Dates(object):

    @classmethod
    def get_date_in_range(self, middle_s, n_days):
        middle = datetime.datetime.strptime(middle_s, "%Y-%m-%d")
        r = Rand.get(2*n_days + 1) - n_days
        picked = middle + datetime.timedelta(days = r)
        return picked.strftime("%Y-%m-%d")
