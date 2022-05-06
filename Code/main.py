import sys
from settings import chunk_IO
from PyQt5.QtWidgets import QApplication

from gui import GUI


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
