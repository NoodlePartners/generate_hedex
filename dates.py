from rand import Rand
import datetime

class Dates(object):

    @classmethod
    def get_date_in_range(self, middle_s, n_days, return_string=True):
        middle = datetime.datetime.strptime(middle_s, "%Y-%m-%d")
        r = Rand.get(2*n_days + 1) - n_days
        picked = middle + datetime.timedelta(days = r)
        if return_string:
            val = picked.strftime("%Y-%m-%d")
        else:
            val = picked
        return val
