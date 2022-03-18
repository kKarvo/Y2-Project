import sys
from PyQt5.QtWidgets import QApplication

from gui import GUI

def main():

    global app
    app = QApplication(sys.argv)
    gui = GUI()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()