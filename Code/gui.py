from customer import Customer
from reservation import Reservation
from settings import chunk_IO


from PyQt5 import QtWidgets, QtCore


class GUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.is_reserved = False
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
            ["", "Tennis (30€/h)", "Sulkapallo (14€/h)", "Padel (32€/h)", "Squash (14€/h)", "Pöytätennis (10€/h)"])
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
        length_l = QtWidgets.QLabel(self)
        length_l.setText("Varauksen pituus: ")
        self.name = QtWidgets.QLineEdit(self)
        self.email = QtWidgets.QLineEdit(self)
        self.num = QtWidgets.QLineEdit(self)
        self.date = QtWidgets.QLineEdit(self)
        self.date.setText('{}.{}.{}'.format(self.calendar.selectedDate().day(), self.calendar.selectedDate().month(), self.calendar.selectedDate().year()))
        self.date.setReadOnly(True)
        self.time = QtWidgets.QLineEdit(self)
        self.length = QtWidgets.QComboBox(self)
        self.length.addItems(['', '60 min', '90 min', '120 min', '150 min', '180 min'])

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
        layout.addWidget(length_l, 10, 1, 1, 1)
        layout.addWidget(self.length, 11, 1, 1, 1)

        # Vakiovuoro checkbox
        self.vakiovuoro = QtWidgets.QCheckBox("Vakiovuoro", self)
        layout.addWidget(self.vakiovuoro, 12, 0, 1, 1)
        self.vakiovuoro.stateChanged.connect(lambda: self.sprt_change(self.spdd.currentText(), self.length.currentText()))

        # Racket rent
        self.rrent = QtWidgets.QCheckBox("Mailavuokra", self)
        layout.addWidget(self.rrent, 12, 1, 1, 1)
        self.rrent.stateChanged.connect(lambda: self.sprt_change(self.spdd.currentText(), self.length.currentText()))

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

        self.spdd.currentTextChanged.connect(lambda: self.sprt_change(self.spdd.currentText(), self.length.currentText()))
        self.length.currentTextChanged.connect(lambda: self.sprt_change(self.spdd.currentText(), self.length.currentText()))

        # Reserve button
        button = QtWidgets.QPushButton("Varaa", self)
        button.setStyleSheet("background-color:#3FBA1D")
        button.clicked.connect(lambda: self.init_reservation())
        button.clicked.connect(lambda: self.init_customer())
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

        # History button
        self.history = QtWidgets.QPushButton("Historia")
        layout.addWidget(self.history, 17, 3, 1, 1)
        self.history.clicked.connect(lambda: self.show_history())

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
        temp_date = self.calendar.selectedDate()
        string = '{}.{}.{}'.format(temp_date.day(), temp_date.month(), temp_date.year())
        self.chosendate.setText(str(self.calendar.selectedDate().toPyDate()))
        self.date.setText(string)

    def sprt_change(self, value, length):
        raq = 0
        h = 0
        if length != '':
            h = int(length.split(" ")[0])/60
        if value == "Tennis (30€/h)":
            self.pr = int(30*h)
            raq = 3
            self.sport_number = 1
        elif value == "Squash (14€/h)":
            self.pr = int(14*h)
            raq = 3
            self.sport_number = 2
        elif value == "Sulkapallo (14€/h)":
            self.pr = int(14*h)
            raq = 3
            self.sport_number = 3
        elif value == "Padel (32€/h)":
            self.pr = int(32*h)
            raq = 4
            self.sport_number = 4
        elif value == "Pöytätennis (10€/h)":
            self.pr = int(10*h)
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
        if not self.is_reserved:
            chunk_IO.add_customer(''.join(self.name.text().split(' ')), self.email.text(), self.num.text(), self.reservation)

    def init_reservation(self):
        self.is_reserved = False
        self.reservation = Reservation()
        self.len = int((self.length.currentText()).split(" ")[0])
        self.reservation.set_variables(self.sport_number, self.date.text(), self.time.text(), self.pr, self.len)
        check = chunk_IO.check_reservation(self.reservation)
        if not check:
            chunk_IO.reservationlist.append(self.reservation)
        else:
            self.is_reserved = True
            error = QtWidgets.QMessageBox()
            error.setIcon(QtWidgets.QMessageBox.Information)
            error.setWindowTitle("Invalid reservation time")
            error.setText("This time is already reserved. Please choose another time.")
            error.exec_()

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
        self.line += 'LEN' + str(self.reservation.return_len())
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
        self.length.setCurrentText("")
        print("{}c{}r".format(len(chunk_IO.get_customers()), len(chunk_IO.get_reservations())))
        if not self.is_reserved:
            f = open('data.txt', 'a')
            f.write(self.line)

    def show_history(self):
        name = ''.join(self.name.text().split(" "))
        reservations_popup = QtWidgets.QMessageBox()
        reservations_popup.setIcon(QtWidgets.QMessageBox.Question)
        reservations_popup.setWindowTitle("Varaushistoria")
        popup_text = ''
        for x in chunk_IO.customerlist:
            if name == x.get_name():
                popup_text = ''
                popup_text += "Varaukset nimellä " + self.name.text() + ":\n\n"
                reservation_list = x.get_reservations()
                for i in reservation_list:
                    if i.get_sport() == 1:
                        popup_text += "Tennis "
                    elif i.get_sport() == 2:
                        popup_text += "Squash "
                    elif i.get_sport() == 3:
                        popup_text += "Sulkapallo "
                    elif i.get_sport() == 4:
                        popup_text += "Padel "
                    elif i.get_sport() == 5:
                        popup_text += "Pöytätennis "
                    popup_text += str(i.get_day()) + "." + str(i.get_month()) + "." + str(i.get_year()) + ""
                    popup_text += ", " + str(i.get_hour()) + ":"
                    if i.get_minute() < 10:
                        popup_text += "0"
                    popup_text += str(i.get_minute()) + ", " + str(i.get_price()) + "€\n"
                break
            elif name == '':
                popup_text = "Syötä nimi jonka varaukset haluat nähdä 'Nimi:' kenttään."
                break
            else:
                popup_text = "Ei varauksia annetulla nimellä."
        if len(chunk_IO.customerlist) == 0:
            popup_text = "Ei varauksia annetulla nimellä."
        reservations_popup.setText(popup_text)
        reservations_popup.exec_()
        self.name.clear()
