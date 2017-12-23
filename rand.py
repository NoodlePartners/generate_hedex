import random
import datetime

class Rand(object):

    # random number generator
    rand = random.SystemRandom()

    @classmethod
    def get(self, n):
        return int(self.rand.random() * n)


    @classmethod
    def pick(self, vals):
        s = 0
        for val in vals:
            s += val[1]
        t = self.get(s)
        p = 0
        for val in vals:
            p += val[1]
            if t < p:
                return val[0]
        return vals[vals.__len__()-1][0]


    @classmethod
    def get_date_in_range(self, middle_s, n_days):
        middle = datetime.datetime.strptime(middle_s, "%Y-%m-%d")
        r = Rand.get(2*n_days + 1) - n_days
        picked = middle + datetime.timedelta(days = r)
        return picked.strftime("%Y-%m-%d")


    @classmethod
    def get_bool(self, percent):
        return self.pick(((False, 100-percent),(True, percent)))
