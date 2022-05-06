import unittest
from io import StringIO
from customer import Customer
from reservation import Reservation
from chunkIO import ChunkIO


class Test(unittest.TestCase):

    def test_add_customer(self):
        self.name = 'Teemu Teekkari'
        self.email = 'teemu.teekkari@aalto.fi'
        self.num = 1234567890
        self.reservation = Reservation()
        self.customerlist = []
        actual = Customer(self.name, self.email, self.num)
        actual.add_reservation(self.reservation)
        ChunkIO.add_customer(self, self.name, self.email, self.num, self.reservation)
        x = ChunkIO.get_customers(self)[0]
        assert 'Teemu Teekkari' == x.get_name() and 'teemu.teekkari@aalto.fi' == x.get_email() and self.reservation == x.get_reservations()[0] and 1234567890 == x.get_num()

    def test_set_variables(self):
        sport = 1
        price = 30
        length = 60
        date = '1.1.2022'
        time = '10:15'
        Reservation.set_variables(self, sport, date, time, price, length)
        assert 1 == Reservation.get_sport(self) and 30 == Reservation.get_price(self) and 60 == Reservation.get_length(self)
        assert 1 == Reservation.get_day(self) and 1 == Reservation.get_month(self) and 2022 == Reservation.get_year(self)
        assert 10 == Reservation.get_hour(self) and 15 == Reservation.get_minute(self)

    def test_read_fully(self):
        test_data = 'NAM13TeemuTeekkariNUM100101231234EML23teemu.teekkari@aalto.fiDAT0812062025TIM040915SPO0203LEN0260PRC0214END00'
        self.input = StringIO(test_data)
        x = ChunkIO.read_fully(self, 15, self.input)
        assert 'NAM13TeemuTeekk' == x

    def test_get_chunk_name_and_size(self):
        test_data = 'NUM100101231234'
        self.input = StringIO(test_data)
        x = ChunkIO.get_chunk_name(self, self.input)
        y = ChunkIO.get_chunk_size(self, self.input)
        assert 'NUM' == x and 10 == y

    def close_silently(self, r):
        try:
            r.close()
        except OSError:
            """ignore"""


if __name__ == "__main__":
    unittest.main()
