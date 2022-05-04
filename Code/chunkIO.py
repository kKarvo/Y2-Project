from io import StringIO
from customer import Customer
from reservation import Reservation


class ChunkIO:

    def __init__(self):
        f = open('data.txt', 'r')
        self.lines = f.readlines()
        self.customerlist = []
        self.reservationlist = []

    def read_save_file(self):
        for line in self.lines:
            line = line.rstrip()
            input = StringIO(line)
            try:
                chunk_name = self.get_chunk_name(input)
                chunk_size = self.get_chunk_size(input)
                while chunk_name != 'END':
                    if chunk_name == 'NAM':
                        name = self.read_fully(chunk_size, input)
                    elif chunk_name == 'NUM':
                        num = self.read_fully(chunk_size, input)
                    elif chunk_name == 'EML':
                        email = self.read_fully(chunk_size, input)
                    elif chunk_name == 'DAT':
                        date = self.read_fully(chunk_size, input)
                    elif chunk_name == 'TIM':
                        time = self.read_fully(chunk_size, input)
                    elif chunk_name == 'SPO':
                        try:
                            sport_number = int(self.read_fully(chunk_size, input))
                        except ValueError:
                            print("Save file corrupted.")
                    elif chunk_name == 'LEN':
                        try:
                            length = int(self.read_fully(chunk_size, input))
                        except ValueError:
                            print("Save file corrupted.")
                    elif chunk_name == 'PRC':
                        try:
                            price = int(self.read_fully(chunk_size, input))
                        except ValueError:
                            print("Save file corrupted.")
                    chunk_name = self.get_chunk_name(input)
                    chunk_size = self.get_chunk_size(input)
                reservation = Reservation()
                reservation.set_variables(sport_number, date, time, price, length)
                if not self.check_reservation(reservation):
                    self.reservationlist.append(reservation)
                    self.add_customer(name, email, num, reservation)
            except:
                print("Empty file.")

    def get_customers(self):
        return self.customerlist

    def get_reservations(self):
        return self.reservationlist

    def add_customer(self, name, email, num, reservation):
        is_new_in_list = False
        if len(self.customerlist) == 0:
            newcustomer = Customer(name, email, num)
            newcustomer.add_reservation(reservation)
            self.customerlist.append(newcustomer)
        else:
            for x in self.customerlist:
                if x.get_name() == name and x.get_num() == num and x.get_email() == email:
                    is_new_in_list = True
                    x.add_reservation(reservation)
                    break
            if not is_new_in_list:
                newcustomer = Customer(name, email, num)
                newcustomer.add_reservation(reservation)
                self.customerlist.append(newcustomer)

    def check_reservation(self, reservation):
        date = str(reservation.get_day())+str(reservation.get_month())+str(reservation.get_year())
        time = str(reservation.get_hour()) + str(reservation.get_minute())
        starttime = reservation.get_hour()*60+reservation.get_minute()
        endtime = starttime + reservation.get_length()
        sport = reservation.get_sport()
        is_date_time_taken = False
        for x in self.reservationlist:
            list_date = str(x.get_day()) + str(x.get_month()) + str(x.get_year())
            list_time = str(x.get_hour()) + str(x.get_minute())
            list_starttime = x.get_hour()*60+x.get_minute()
            list_endttime = list_starttime + x.get_length()
            list_sport = x.get_sport()
            if date == list_date and list_starttime <= starttime < list_endttime and sport == list_sport:
                is_date_time_taken = True
                break
            elif date == list_date and starttime <= list_starttime < endtime and sport == list_sport:
                is_date_time_taken = True
                break
        return is_date_time_taken

    def read_fully(self, count, input):
        chars = input.read(count)
        if len(chars) != count:
            raise OSError("Unexpected end of file.")
        return ''.join(chars)

    def get_chunk_name(self, input):
        return ''.join(input.read(3))

    def get_chunk_size(self, input):
        return int(''.join(input.read(2)))
