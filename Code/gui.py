from PyQt5 import QtWidgets, QtCore, QtGui


class GUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Varausjärjestelmä"
        self.width = 1000
        self.height = 500
        # Single monitor
        #self.left = int((1920-self.width)/2)
        # Dual monitor
        self.left = int(1920+(1920-self.width)/2)
        self.top = int((1080-self.height)/2)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        x = 20
        y = 10

        # Sport dropdown
        sport_l = QtWidgets.QLabel(self)
        sport_l.setText("Laji: ")
        sport_l.move(x+1, y)

        spdd = QtWidgets.QComboBox(self)
        spdd.setGeometry(x, y+30, 120, 20)
        spdd.addItems(["", "Tennis", "Sulkapallo", "Padel", "Squash", "Pöytätennis"])
        spdd.setCurrentText("")

        # Text boxes for contact info
        name_l = QtWidgets.QLabel(self)
        name_l.setText("Name: ")
        name_l.move(x+1, y+50)

        date_l = QtWidgets.QLabel(self)
        date_l.setText("Date: ")
        date_l.move(x+1, y+110)

        time_l = QtWidgets.QLabel(self)
        time_l.setText("Time: ")
        time_l.move(x+1, y+170)

        name = QtWidgets.QLineEdit(self)
        name.move(x, y+80)
        date = QtWidgets.QLineEdit(self)
        date.move(x, y+140)
        time = QtWidgets.QLineEdit(self)
        time.move(x, y+200)

        # Vakiovuoro checkbox
        checkbox = QtWidgets.QCheckBox("Vakiovuoro", self)
        checkbox.move(x+1, y+235)

        # Frequency
        frq_l = QtWidgets.QLabel(self)
        frq_l.setText("Toistettavuus: ")
        frq_l.move(x+1, y+260)

        frq = QtWidgets.QComboBox(self)
        frq.setGeometry(x, y+290, 80, 20)
        frq.addItems(["", "Viikko", "Kuukausi"])
        frq.setCurrentText("")

        count = QtWidgets.QLineEdit(self)
        count.setGeometry(x, y+323, 30, 25)

        self.text = QtWidgets.QLabel(self)
        self.text.setText("ajanjakson välein.")
        self.text.move(x+37, y+320)

        frq.currentTextChanged.connect(lambda: self.frq_change(frq.currentText()))

        # Price
        price_l = QtWidgets.QLabel(self)
        price_l.setText("Hinta: ")
        price_l.move(x+1, y+370)

        self.price_t = QtWidgets.QLineEdit(self)
        self.price_t.setText("")
        self.price_t.setReadOnly(True)
        self.price_t.setGeometry(x, y+400, 100, 40)

        spdd.currentTextChanged.connect(lambda: self.sprt_change(spdd.currentText()))

        # Reserve button
        button = QtWidgets.QPushButton("Varaa", self)
        button.setGeometry(x+150, y+400, 100, 40)
        button.setStyleSheet("background-color:#3FBA1D")

        self.show()

    def frq_change(self, value):
        if value == "":
            content = "ajanjakson"
        elif value == "Viikko":
            content = "viikon"
        elif value == "Kuukausi":
            content = "kuukauden"
        self.text.setText(content + " välein.")

    def sprt_change(self, value):
        pr = 0
        if value == "Tennis":
            pr = 30
        elif value == "Squash":
            pr = 20
        elif value == "Sulkapallo":
            pr = 15
        elif value == "Padel":
            pr = 35
        elif value == "Pöytätennis":
            pr = 10
        if pr != 0:
            self.price_t.setText(str(2*pr) + "€")
        else:
            self.price_t.setText("")

