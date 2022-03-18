import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class GUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajanvarausjärjestelmä")
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 3)
        layout.setColumnStretch(4, 1)
        self.setGeometry(2210, 290, 1340, 500)
        # Add widgets to the layout'
        sport_l = QtWidgets.QLabel(self)
        sport_l.setText("Laji: ")

        spdd = QtWidgets.QComboBox(self)
        spdd.addItems(
            ["", "Tennis (30€/h)", "Sulkapallo (14€/h)", "Padel (34€/h)", "Squash (14€/h)", "Pöytätennis (10€/h)"])
        spdd.setCurrentText("")

        layout.addWidget(sport_l, 0, 0, 1, 2)
        layout.addWidget(spdd, 1, 0, 1, 2)

        # Text boxes for contact info
        name_l = QtWidgets.QLabel(self)
        name_l.setText("Nimi: ")
        email_l = QtWidgets.QLabel(self)
        email_l.setText("E-Mail: ")
        num_l = QtWidgets.QLabel(self)
        num_l.setText("Puhelinnumero: ")
        date_l = QtWidgets.QLabel(self)
        date_l.setText("Varauksen pvm (pp.kk.vvvv): ")
        time_l = QtWidgets.QLabel(self)
        time_l.setText("Aika (HH:MM): ")
        name = QtWidgets.QLineEdit(self)
        email = QtWidgets.QLineEdit(self)
        num = QtWidgets.QLineEdit(self)
        date = QtWidgets.QLineEdit(self)
        time = QtWidgets.QLineEdit(self)

        layout.addWidget(name_l, 2, 0, 1, 2)
        layout.addWidget(name, 3, 0, 1, 2)
        layout.addWidget(email_l, 4, 0, 1, 2)
        layout.addWidget(email, 5, 0, 1, 2)
        layout.addWidget(num_l, 6, 0, 1, 2)
        layout.addWidget(num, 7, 0, 1, 2)
        layout.addWidget(date_l, 8, 0, 1, 2)
        layout.addWidget(date, 9, 0, 1, 2)
        layout.addWidget(time_l, 10, 0, 1, 2)
        layout.addWidget(time, 11, 0, 1, 2)

        # Vakiovuoro checkbox
        self.vakiovuoro = QtWidgets.QCheckBox("Vakiovuoro", self)
        layout.addWidget(self.vakiovuoro, 12, 0, 1, 1)
        self.vakiovuoro.stateChanged.connect(lambda: self.sprt_change(spdd.currentText()))

        # Racket rent
        self.rrent = QtWidgets.QCheckBox("Mailavuokra", self)
        layout.addWidget(self.rrent, 12, 1, 1, 1)
        self.rrent.stateChanged.connect(lambda: self.sprt_change(spdd.currentText()))

        # Frequency
        frq_l = QtWidgets.QLabel(self)
        frq_l.setText("Toistettavuus: ")

        frq = QtWidgets.QComboBox(self)
        frq.addItems(["", "Viikko", "Kuukausi"])
        frq.setCurrentText("")

        count = QtWidgets.QLineEdit(self)

        self.text = QtWidgets.QLabel(self)
        self.text.setText("ajanjakson välein.")

        frq.currentTextChanged.connect(lambda: self.frq_change(frq.currentText()))

        layout.addWidget(frq_l, 13, 0, 1, 1)
        layout.addWidget(frq, 14, 0, 1, 1)
        layout.addWidget(count, 15, 0, 1, 1)
        layout.addWidget(self.text, 15, 1, 1, 1)

        # Price
        price_l = QtWidgets.QLabel(self)
        price_l.setText("Hinta: ")

        self.price_t = QtWidgets.QLineEdit(self)
        self.price_t.setText("")
        self.price_t.setReadOnly(True)

        layout.addWidget(price_l, 16, 0, 1, 1)
        layout.addWidget(self.price_t, 17, 0, 1, 1)

        spdd.currentTextChanged.connect(lambda: self.sprt_change(spdd.currentText()))

        # Reserve button
        button = QtWidgets.QPushButton("Varaa", self)
        button.setStyleSheet("background-color:#3FBA1D")

        layout.addWidget(button, 17, 1, 1, 1)

        # Calendar
        self.calendar = QtWidgets.QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.selectionChanged.connect(self.calendar_date)
        layout.addWidget(self.calendar, 0, 3, 17, 2)

        self.chosendate = QtWidgets.QLabel(self)
        self.chosendate.setText(str(self.calendar.selectedDate().toPyDate()))
        layout.addWidget(self.chosendate, 0, 2, 1, 1)

        # Today
        self.today = QtWidgets.QPushButton("Tänään")
        layout.addWidget(self.today, 17, 4, 1, 1)
        self.today.clicked.connect(lambda: self.to_today())



        self.show()

    def frq_change(self, value):
        if value == "":
            content = "ajanjakson"
        elif value == "Viikko":
            content = "viikon"
        elif value == "Kuukausi":
            content = "kuukauden"
        self.text.setText(content + " välein.")

    def to_today(self):
        self.calendar.setSelectedDate(QtCore.QDate.currentDate())

    def calendar_date(self):
        date = self.calendar.selectedDate()
        datestring = str(date.toPyDate())

        self.chosendate.setText(datestring)

    def sprt_change(self, value):
        pr = 0
        raq = ""
        if value == "Tennis (30€/h)":
            pr = 30
            raq = 3
        elif value == "Squash (14€/h)":
            pr = 14
            raq = 3
        elif value == "Sulkapallo (14€/h)":
            pr = 14
            raq = 3
        elif value == "Padel (34€/h)":
            pr = 34
            raq = 4
        elif value == "Pöytätennis (10€/h)":
            pr = 10
            raq = 2
        elif value == "":
            pr = 0
            raq = 0
        if pr != 0:
            self.price_t.setText(str(pr) + "€")
            self.rrent.setText("Mailavuokra " + str(raq) + "€")
        else:
            self.price_t.setText("")
            self.rrent.setText("Mailavuokra")
        if self.rrent.isChecked():
            pr += raq
            self.price_t.setText(str(pr) + "€")
        if self.vakiovuoro.isChecked():
            self.price_t.setText(str(pr) + "€/krt")
