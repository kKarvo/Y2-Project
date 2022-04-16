from customer import Customer
from reservation import Reservation

from PyQt5 import QtWidgets, QtCore


class GUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajanvarausjärjestelmä")
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 1)
        self.setGeometry(2210-1920, 290, 1340, 500)

        self.line = ''
        self.pr = 0
        self.calendar = QtWidgets.QCalendarWidget(self)
        self.sport_number = 0

        # Sport dropdown
        sport_l = QtWidgets.QLabel(self)
        sport_l.setText("Laji: ")

        self.spdd = QtWidgets.QComboBox(self)
        self.spdd.addItems(
            ["", "Tennis (30€/h)", "Sulkapallo (14€/h)", "Padel (34€/h)", "Squash (14€/h)", "Pöytätennis (10€/h)"])
        self.spdd.setCurrentText("")

        layout.addWidget(sport_l, 0, 0, 1, 2)
        layout.addWidget(self.spdd, 1, 0, 1, 2)

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
        self.name = QtWidgets.QLineEdit(self)
        self.email = QtWidgets.QLineEdit(self)
        self.num = QtWidgets.QLineEdit(self)
        self.date = QtWidgets.QLineEdit(self)
        self.time = QtWidgets.QLineEdit(self)

        layout.addWidget(name_l, 2, 0, 1, 2)
        layout.addWidget(self.name, 3, 0, 1, 2)
        layout.addWidget(email_l, 4, 0, 1, 2)
        layout.addWidget(self.email, 5, 0, 1, 2)
        layout.addWidget(num_l, 6, 0, 1, 2)
        layout.addWidget(self.num, 7, 0, 1, 2)
        layout.addWidget(date_l, 8, 0, 1, 2)
        layout.addWidget(self.date, 9, 0, 1, 2)
        layout.addWidget(time_l, 10, 0, 1, 2)
        layout.addWidget(self.time, 11, 0, 1, 2)

        # Vakiovuoro checkbox
        self.vakiovuoro = QtWidgets.QCheckBox("Vakiovuoro", self)
        layout.addWidget(self.vakiovuoro, 12, 0, 1, 1)
        self.vakiovuoro.stateChanged.connect(lambda: self.sprt_change(self.spdd.currentText()))

        # Racket rent
        self.rrent = QtWidgets.QCheckBox("Mailavuokra", self)
        layout.addWidget(self.rrent, 12, 1, 1, 1)
        self.rrent.stateChanged.connect(lambda: self.sprt_change(self.spdd.currentText()))

        # Frequency
        self.frq_l = QtWidgets.QLabel(self)
        self.frq_l.setText("Toistettavuus: ")

        self.frq = QtWidgets.QComboBox(self)
        self.frq.addItems(["", "Viikko", "Kuukausi"])
        self.frq.setCurrentText("")

        self.count = QtWidgets.QLineEdit(self)

        self.text = QtWidgets.QLabel(self)
        self.text.setText("ajanjakson välein.")

        layout.addWidget(self.frq_l, 13, 0, 1, 1)
        layout.addWidget(self.frq, 14, 0, 1, 1)
        layout.addWidget(self.count, 15, 0, 1, 1)
        layout.addWidget(self.text, 15, 1, 1, 1)
        self.frq_l.hide()
        self.frq.hide()
        self.count.hide()
        self.text.hide()

        self.frq.currentTextChanged.connect(lambda: self.frq_change(self.frq.currentText()))
        self.vakiovuoro.stateChanged.connect(lambda: self.vv_change())

        # Price
        price_l = QtWidgets.QLabel(self)
        price_l.setText("Hinta: ")

        self.price_t = QtWidgets.QLineEdit(self)
        self.price_t.setText("")
        self.price_t.setReadOnly(True)

        layout.addWidget(price_l, 16, 0, 1, 1)
        layout.addWidget(self.price_t, 17, 0, 1, 1)

        self.spdd.currentTextChanged.connect(lambda: self.sprt_change(self.spdd.currentText()))

        # Reserve button
        button = QtWidgets.QPushButton("Varaa", self)
        button.setStyleSheet("background-color:#3FBA1D")
        button.clicked.connect(lambda: self.init_customer())
        button.clicked.connect(lambda: self.init_reservation())
        button.clicked.connect(lambda: self.init_line())
        button.clicked.connect(lambda: self.press_res())

        layout.addWidget(button, 17, 1, 1, 1)

        # Calendar
        self.calendar.setGridVisible(True)
        self.calendar.selectionChanged.connect(self.calendar_date)
        layout.addWidget(self.calendar, 0, 3, 17, 2)

        self.chosendate = QtWidgets.QLabel(self)
        self.chosendate.setText(str(self.calendar.selectedDate().toPyDate()))
        layout.addWidget(self.chosendate, 0, 2, 1, 1)

        # Today button
        self.today = QtWidgets.QPushButton("Tänään")
        layout.addWidget(self.today, 17, 4, 1, 1)
        self.today.clicked.connect(lambda: self.to_today())

    def vv_change(self):
        self.frq_l.hide()
        self.frq.hide()
        self.count.hide()
        self.text.hide()
        if self.vakiovuoro.isChecked():
            self.frq.show()
            self.frq_l.show()
            self.count.show()
            self.text.show()

    def frq_change(self, value):
        content = ""
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
        self.chosendate.setText(str(self.calendar.selectedDate().toPyDate()))

    def sprt_change(self, value):
        raq = 0
        if value == "Tennis (30€/h)":
            self.pr = 30
            raq = 3
            self.sport_number = 1
        elif value == "Squash (14€/h)":
            self.pr = 14
            raq = 3
            self.sport_number = 2
        elif value == "Sulkapallo (14€/h)":
            self.pr = 14
            raq = 3
            self.sport_number = 3
        elif value == "Padel (34€/h)":
            self.pr = 34
            raq = 4
            self.sport_number = 4
        elif value == "Pöytätennis (10€/h)":
            self.pr = 10
            raq = 2
            self.sport_number = 5
        elif value == "":
            self.pr = 0
            raq = 0
        if self.pr != 0:
            self.price_t.setText(str(self.pr) + "€")
            self.rrent.setText("Mailavuokra " + str(raq) + "€")
        elif self.pr == 0:
            self.price_t.setText("")
            self.rrent.setText("Mailavuokra")
        if self.rrent.isChecked():
            self.pr += raq
            self.price_t.setText(str(self.pr) + "€")
        if self.vakiovuoro.isChecked():
            self.price_t.setText(str(self.pr) + "€/krt")

    def init_customer(self):
        self.temp_customer = Customer(self.name.text(), self.email.text(), self.num.text())

    def init_reservation(self):
        self.reservation = Reservation()
        self.reservation.set_variables(self.sport_number, self.date.text(), self.time.text(), self.pr)
        self.temp_customer.add_reservation(self.reservation)


    def init_line(self):
        self.line = ''
        i = 0
        name = ''.join(self.name.text().split(" "))
        self.line += 'NAM'
        if len(name) < 10:
            self.line += '0'
        self.line += str(len(name)) + name
        self.line += 'NUM10' + str(self.num.text())
        self.line += 'EML' + str(len(self.email.text())) + self.email.text()
        self.line += 'DAT08' + str(self.reservation.return_date())
        self.line += 'TIM04' + str(self.reservation.return_time())
        self.line += 'SPO020' + str(self.sport_number)
        self.line += 'PRC' + str(self.reservation.return_price())
        self.line += 'END00\n'

    def press_res(self):
        # Clear fields
        self.spdd.setCurrentText("")
        self.frq.setCurrentText("")
        if self.vakiovuoro.isChecked():
            self.vakiovuoro.toggle()
        if self.rrent.isChecked():
            self.rrent.toggle()
        self.name.clear()
        self.email.clear()
        self.num.clear()
        self.date.clear()
        self.time.clear()
        self.count.clear()
        f = open('data.txt', 'a')
        f.write(self.line)
