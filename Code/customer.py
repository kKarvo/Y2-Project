

class Customer:

    def __init__(self, name, email, num):
        self.name = name
        self.email = email
        self.num = num
        self.reservations = []

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_num(self):
        return self.num

    def add_reservation(self, reservation):
        self.reservations.append(reservation)
