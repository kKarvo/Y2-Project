import sys
from settings import chunk_IO
from PyQt5.QtWidgets import QApplication

from io import StringIO
from customer import Customer
from reservation import Reservation
from chunkIO import ChunkIO

from gui import GUI


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
    # customer_list = read_save_file()

    chunk_IO.read_save_file()

    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()

    print("{}c{}r".format(len(chunk_IO.get_customers()), len(chunk_IO.get_reservations())))

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
