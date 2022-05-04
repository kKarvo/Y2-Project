
class Reservation:

    def __init__(self):
        self.sport = 0
        self.day = 0
        self.month = 0
        self.year = 0
        self.hour = 0
        self.minute = 0
        self.price = 0
        self.length = 0

    def set_variables(self, sport, date, time, price, length):
        self.sport = sport
        self.price = price
        self.length = length
        datestring = date.split(".")
        if len(datestring) == 3:
            try:
                i = 0
                for x in datestring:
                    datestring[i] = int(x)
                    i += 1
            except ValueError:
                print("Date format error.")
            if datestring[0] < 10:
                datestring[0] = '0' + str(datestring[0])
            if datestring[1] < 10:
                datestring[1] = '0' + str(datestring[1])
            datestring[0] = str(datestring[0])
            datestring[1] = str(datestring[1])
            datestring[2] = str(datestring[2])
            date_components = "".join(datestring)
        else:
            date_components = "".join(date.split("."))
        if len(date_components) != 8:
            print("Date format error.")
            raise ValueError
        try:
            self.day = int(date_components[0:2])
        except ValueError:
            print("Date format error.")
        try:
            self.month = int(date_components[2:4])
        except ValueError:
            print("Date format error.")
        try:
            self.year = int(date_components[4:8])
        except ValueError:
            print("Date format error.")
        time_components = "".join(time.split(":"))
        if len(time_components) != 4:
            print("Time format error.")
            raise ValueError
        try:
            self.hour = int(time_components[0:2])
        except ValueError:
            print("Time format error.")
        try:
            self.minute = int(time_components[2:4])
        except ValueError:
            print("Time format error.")

    def get_sport(self):
        return self.sport

    def get_day(self):
        return self.day

    def get_month(self):
        return self.month

    def get_year(self):
        return self.year

    def get_hour(self):
        return self.hour

    def get_minute(self):
        return self.minute

    def get_price(self):
        return self.price

    def get_length(self):
        return self.length

    def return_date(self):
        ret = ''
        if self.day < 10:
            ret += '0'
        ret += str(self.day)
        if self.month < 10:
            ret += '0'
        ret += str(self.month) + str(self.year)
        return ret

    def return_time(self):
        ret = ''
        if self.hour < 10:
            ret += '0'
        ret += str(self.hour)
        if self.minute < 10:
            ret += '0'
        ret += str(self.minute)
        return ret

    def return_price(self):
        ret = ''
        if self.price < 100:
            ret += '02'
        else:
            ret += str(len(str(self.price)))
        if self.price < 10:
            ret += '0'
        ret += str(self.price)
        ret = ret.split(".")[0]
        return ret

    def return_len(self):
        ret = ''
        if self.length < 100:
            ret += '02'
        else:
            ret += '0' + str(len(str(self.length)))
        ret += str(self.length)
        return ret
