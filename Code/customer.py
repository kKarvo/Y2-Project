import gui2


class Customer:

    def __init__(self, name, email, num):
        self.set_name(name)
        self.email = email
        self.num = num
        self.reservation = None

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_num(self):
        return self.num
