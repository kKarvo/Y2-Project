import sys
from PyQt5.QtWidgets import QApplication

from io import StringIO
from customer import Customer
from reservation import Reservation

from gui2 import GUI


def read_save_file():
    # Initializes a list of customers based on 'data.txt'
    customer_list = []
    reservation_list = []
    f = open('data.txt', 'r')
    lines = f.readlines()
    i = 0
    for line in lines:
        line = line.rstrip()
        input = StringIO(line)
        try:
            chunk_name = get_chunk_name(input)
            chunk_size = get_chunk_size(input)
            while chunk_name != 'END':
                if chunk_name == 'NAM':
                    name = read_fully(chunk_size, input)
                elif chunk_name == 'NUM':
                    num = read_fully(chunk_size, input)
                elif chunk_name == 'EML':
                    email = read_fully(chunk_size, input)
                elif chunk_name == 'DAT':
                    date = read_fully(chunk_size, input)
                elif chunk_name == 'TIM':
                    time = read_fully(chunk_size, input)
                elif chunk_name == 'SPO':
                    try:
                        sport_number = int(read_fully(chunk_size, input))
                    except ValueError:
                        print("Save file corrupted.")
                elif chunk_name == 'PRC':
                    try:
                        price = int(read_fully(chunk_size, input))
                    except ValueError:
                        print("Save file corrupted.")
                chunk_name = get_chunk_name(input)
                chunk_size = get_chunk_size(input)
            reservation = Reservation()
            reservation.set_variables(sport_number, date, time, price)
            reservation_list.append(reservation)
            is_new_in_list = False
            if len(customer_list) == 0:
                newcustomer = Customer(name, email, num)
                newcustomer.add_reservation(reservation)
                customer_list.append(newcustomer)
            else:
                for x in customer_list:
                    if x.get_name() == name and x.get_num() == num and x.get_email() == email:
                        is_new_in_list = True
                        x.add_reservation(reservation)
                if not is_new_in_list:
                    newcustomer = Customer(name, email, num)
                    newcustomer.add_reservation(reservation)
                    customer_list.append(newcustomer)
        except:
            print("Reading data file failed.")
    return customer_list


def read_fully(count, input):
    chars = input.read(count)
    if len(chars) != count:
        raise OSError("Unexpected end of file.")
    return ''.join(chars)


def get_chunk_name(input):
    return ''.join(input.read(3))


def get_chunk_size(input):
    return int(''.join(input.read(2)))

def main():
    customer_list = read_save_file()

    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()