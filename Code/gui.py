from reservation import Reservation
from settings import chunk_IO

from PyQt5 import QtWidgets, QtCore


class GUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.is_reserved = False
        self.setWindowTitle("Ajanvarausjärjestelmä")
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 2)
        self.layout.setColumnStretch(3, 1)
        self.layout.setColumnStretch(4, 1)
        self.setGeometry(2210-1920, 290, 1340, 500)

        self.line = ''
        self.pr = 0
        self.calendar = QtWidgets.QCalendarWidget(self)
        self.sport_number = 0

        # Sport dropdown
        sport_l = QtWidgets.QLabel("Laji: ", self)

        self.spdd = QtWidgets.QComboBox(self)
        self.spdd.addItems(
            ["", "Tennis (30€/h)", "Sulkapallo (14€/h)", "Padel (32€/h)", "Squash (14€/h)", "Pöytätennis (10€/h)"])
        self.spdd.setCurrentText("")

        self.layout.addWidget(sport_l, 0, 0, 1, 2)
        self.layout.addWidget(self.spdd, 1, 0, 1, 2)

        # Text boxes for contact info
        name_l = QtWidgets.QLabel("Nimi: ", self)
        email_l = QtWidgets.QLabel("Sähköposti: ", self)
        num_l = QtWidgets.QLabel("Puhelinnumero: ", self)
        date_l = QtWidgets.QLabel("Varauksen päivämäärä: ", self)
        time_l = QtWidgets.QLabel("Aika (HH:MM): ", self)
        length_l = QtWidgets.QLabel("Varauksen pituus: ", self)
        self.name = QtWidgets.QLineEdit(self)
        self.email = QtWidgets.QLineEdit(self)
        self.num = QtWidgets.QLineEdit(self)
        self.date = QtWidgets.QLineEdit(self)
        self.date.setText('{}.{}.{}'.format(self.calendar.selectedDate().day(), self.calendar.selectedDate().month(), self.calendar.selectedDate().year()))
        self.date.setReadOnly(True)
        self.time = QtWidgets.QLineEdit(self)
        self.length = QtWidgets.QComboBox(self)
        self.length.addItems(['', '60 min', '90 min', '120 min', '150 min', '180 min'])

        self.layout.addWidget(name_l, 2, 0, 1, 2)
        self.layout.addWidget(self.name, 3, 0, 1, 2)
        self.layout.addWidget(email_l, 4, 0, 1, 2)
        self.layout.addWidget(self.email, 5, 0, 1, 2)
        self.layout.addWidget(num_l, 6, 0, 1, 2)
        self.layout.addWidget(self.num, 7, 0, 1, 2)
        self.layout.addWidget(date_l, 8, 0, 1, 2)
        self.layout.addWidget(self.date, 9, 0, 1, 2)
        self.layout.addWidget(time_l, 10, 0, 1, 2)
        self.layout.addWidget(self.time, 11, 0, 1, 2)
        self.layout.addWidget(length_l, 10, 1, 1, 1)
        self.layout.addWidget(self.length, 11, 1, 1, 1)

        # Vakiovuoro checkbox
        self.vakiovuoro = QtWidgets.QCheckBox("Vakiovuoro", self)
        self.layout.addWidget(self.vakiovuoro, 12, 0, 1, 1)
        self.vakiovuoro.stateChanged.connect(lambda: self.sprt_change(self.spdd.currentText(), self.length.currentText()))

        # Racket rent
        self.rrent = QtWidgets.QCheckBox("Mailavuokra", self)
        self.layout.addWidget(self.rrent, 12, 1, 1, 1)
        self.rrent.stateChanged.connect(lambda: self.sprt_change(self.spdd.currentText(), self.length.currentText()))

        # Frequency
        self.frq_l = QtWidgets.QLabel("Toistettavuus: ", self)
        self.count = QtWidgets.QLineEdit(self)
        self.text = QtWidgets.QLabel("viikon välein.", self)

        self.layout.addWidget(self.frq_l, 13, 0, 1, 1)
        self.layout.addWidget(self.count, 14, 0, 1, 1)
        self.layout.addWidget(self.text, 14, 1, 1, 1)
        self.frq_l.hide()
        self.count.hide()
        self.text.hide()

        self.vakiovuoro.stateChanged.connect(lambda: self.vv_change())

        # Price
        price_l = QtWidgets.QLabel("Hinta: ", self)

        self.price_t = QtWidgets.QLineEdit(self)
        self.price_t.setText("")
        self.price_t.setReadOnly(True)

        self.layout.addWidget(price_l, 15, 0, 1, 1)
        self.layout.addWidget(self.price_t, 16, 0, 1, 1)

        self.spdd.currentTextChanged.connect(lambda: self.sprt_change(self.spdd.currentText(), self.length.currentText()))
        self.length.currentTextChanged.connect(lambda: self.sprt_change(self.spdd.currentText(), self.length.currentText()))

        # Reserve button
        button = QtWidgets.QPushButton("Varaa", self)
        button.setStyleSheet("background-color:#3FBA1D")
        button.clicked.connect(lambda: self.check_fields())

        self.layout.addWidget(button, 16, 1, 1, 1)

        # Calendar
        self.calendar.setGridVisible(True)
        self.calendar.selectionChanged.connect(self.calendar_date)
        self.layout.addWidget(self.calendar, 0, 3, 16, 2)

        self.chosendate = QtWidgets.QLabel("Varaukset:", self)
        self.layout.addWidget(self.chosendate, 0, 2, 1, 1)

        # Today button
        self.today = QtWidgets.QPushButton("Tänään")
        self.layout.addWidget(self.today, 16, 4, 1, 1)
        self.today.clicked.connect(lambda: self.to_today())

        # History button
        self.history = QtWidgets.QPushButton("Historia")
        self.layout.addWidget(self.history, 16, 3, 1, 1)
        self.history.clicked.connect(lambda: self.show_history())

        # Middle column for reservations.
        self.reservationlist = []
        self.show_reservations()

    def vv_change(self):
        # Shows and hides widgetse according to vakiovuoro checkbox
        self.frq_l.hide()
        self.count.hide()
        self.text.hide()
        if self.vakiovuoro.isChecked():
            self.frq_l.show()
            self.count.show()
            self.text.show()

    def to_today(self):
        # Sets calendar selected date to today
        self.calendar.setSelectedDate(QtCore.QDate.currentDate())

    def calendar_date(self):
        # Sets date string. Includes hiding and showing middle column reservations
        # when new date is selected.
        temp_date = self.calendar.selectedDate()
        string = '{}.{}.{}'.format(temp_date.day(), temp_date.month(), temp_date.year())
        self.date.setText(string)
        self.hide_reservations()
        self.show_reservations()

    def sprt_change(self, value, length):
        # Updates price according to sport, reservation length
        # and wether or not the user rents a racket.
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
        # Initializes customer if reservation is free.
        if not self.is_reserved:
            chunk_IO.add_customer(''.join(self.name.text().split(' ')), self.email.text(), self.num.text(), self.reservation)

    def init_reservation(self):
        # Checks if reservation overlaps with another one.
        # If not, initializes the reservation.
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
            error.setWindowTitle("Varattu ajankohta")
            error.setText("Tämä aika on jo varattu, valitse toinen.")
            error.exec_()
            return 1
        return 0

    def init_line(self):
        # Initializes line which is to be written into data.txt
        self.line = ''
        name = ''.join(self.name.text().split(" "))
        self.line += 'NAM'
        if len(name) < 10:
            self.line += '0'
        self.line += str(len(name)) + name
        self.line += 'NUM'
        if len(self.num.text()) < 10:
            self.line += '0'
        self.line += str(len(self.num.text())) + self.num.text()
        self.line += 'EML' + str(len(self.email.text())) + self.email.text()
        self.line += 'DAT08' + str(self.reservation.return_date())
        self.line += 'TIM04' + str(self.reservation.return_time())
        self.line += 'SPO020' + str(self.sport_number)
        self.line += 'LEN' + str(self.reservation.return_len())
        self.line += 'PRC' + str(self.reservation.return_price())
        self.line += 'END00\n'

    def press_res(self):
        # Clears fields, sets date to today and calls write_line().
        # Also prints current amount of customers and reservations into console.
        self.to_today()
        self.spdd.setCurrentText("")
        if self.vakiovuoro.isChecked():
            self.vakiovuoro.toggle()
        if self.rrent.isChecked():
            self.rrent.toggle()
        self.name.clear()
        self.email.clear()
        self.num.clear()
        self.date.setText('{}.{}.{}'.format(self.calendar.selectedDate().day(), self.calendar.selectedDate().month(),
                                            self.calendar.selectedDate().year()))
        self.time.clear()
        self.count.clear()
        self.length.setCurrentText("")
        self.hide_reservations()
        print("{}c{}r".format(len(chunk_IO.get_customers()), len(chunk_IO.get_reservations())))
        self.write_line()

    def show_history(self):
        # Shows the reservation history of a user.
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
                popup_text = "Ei varauksia annetulla nimellä: " + self.name.text()
        if len(chunk_IO.customerlist) == 0:
            popup_text = "Ei varauksia annetulla nimellä."
        reservations_popup.setText(popup_text)
        reservations_popup.exec_()

    def check_fields(self):
        error = QtWidgets.QMessageBox()
        error.setIcon(QtWidgets.QMessageBox.Information)
        error.setWindowTitle("Virhe")
        check = self.check_empty()
        if check == 0:
            x = self.check_vakiovuoro()
            i = 0
            if x > 0:
                while i < x:
                    temp = self.date.text().split(".")
                    temp[0] = int(temp[0])
                    temp[1] = int(temp[1])
                    temp[2] = int(temp[2])
                    date = QtCore.QDate(temp[2], temp[1], temp[0])
                    date = date.addDays(i*7)
                    date = str(date.toPyDate()).split("-")
                    self.date.setText('{}.{}.{}'.format(date[2], date[1], date[0]))
                    i += 1
                    if self.init_reservation() == 0:
                        self.init_customer()
                        self.init_line()
                        self.write_line()
                self.press_res()
                notification = QtWidgets.QMessageBox()
                notification.setIcon(QtWidgets.QMessageBox.Information)
                notification.setWindowTitle("Vakiovuoro varattu")
                notification.setText("Vakiovuoro onnistuneesti varattu seuraavaksi 3 kuukaudeksi.")
                notification.exec_()
            elif x == -1:
                error.setText("Anna vakiovuorovälille jokin arvo.")
                error.exec_()
                return 0
            else:
                if self.init_reservation() == 0:
                    self.init_customer()
                    self.init_line()
                    self.press_res()
        elif check == 1:
            error.setText("Täytä kaikki kentät.")
            error.exec_()
        elif check == 2:
            error.setText("Virheellinen aika, anna aika oikeassa muodossa (HH:MM).")
            error.exec_()
        elif check == 3:
            error.setText("Varausta ei voi tehdä mennelle päivämäärälle. Valitse uusi päivämäärä.")
            error.exec_()
        elif check == 4:
            error.setText("Varaukset täytyy tehdä 15 minuutin välein.\nEsim. klo 12:00, 12:15, 12:30 tai 12:45.")
            error.exec_()
        elif check == 5:
            error.setText("Palloiluhalli on auki 7-20.\nVaraus voi alkaa aikaisintaan klo 07:00 ja varauksen täytyy loppua viimeistään klo 20:00.")
            error.exec_()

    def check_vakiovuoro(self):
        if self.vakiovuoro.isChecked():
            try:
                x = int(self.count.text())
                j = 12/x
                k = int(j)
                return int(12/x)
            except ValueError:
                print("Count not integer.")
                return -1
        else:
            return 1

    def check_empty(self):
        if self.spdd.currentText() == '' or self.name.text() == '' or self.email.text() == '' or self.num.text() == '' or self.date.text() == '' or self.time.text() == '' or self.length.currentText() == '':
            print("Fields not filled.")
            return 1
        else:
            return self.check_date()

    def check_date(self):
        current_day = QtCore.QDate.currentDate().day()
        current_month = QtCore.QDate.currentDate().month()
        current_year = QtCore.QDate.currentDate().year()
        date_components = self.date.text().split(".")
        if int(date_components[2]) > current_year:
            return self.check_time()
        elif int(date_components[2]) == current_year and int(date_components[1]) > current_month:
            return self.check_time()
        elif int(date_components[2]) == current_year and int(date_components[1]) == current_month and int(date_components[0]) >= current_day:
            return self.check_time()
        else:
            return 3

    def check_time(self):
        time_components = self.time.text().split(":")
        if len(time_components) != 2:
            print("Invalid time!")
            return 2
        try:
            time_components[0] = int(time_components[0])
            time_components[1] = int(time_components[1])
            if 0 < time_components[0] < 24 and 0 <= time_components[1] < 60:
                # Check if reservation ends before 20:00 (20*60=1200)
                x = time_components[0] * 60 + time_components[1]
                y = int(self.length.currentText().split(" ")[0])
                if time_components[0] >= 7 and x + y <= 1200:
                    # Check if reservation is done on minutes 00, 15, 30 or 45.
                    if time_components[1] % 15 == 0:
                        return 0
                    else:
                        return 4
                else:
                    return 5
            else:
                print("Invalid time!")
                return 2
        except ValueError:
            print("Invalid time!")
            return 2

    def show_reservations(self):
        i = 0
        temp_date = self.calendar.selectedDate()
        chosendate = [temp_date.day(), temp_date.month(), temp_date.year()]
        clist = chunk_IO.get_reservations()
        for reservation in clist:
            curdate = reservation.return_date()
            reservationdate = [int(curdate[0:2]), int(curdate[2:4]), int(curdate[4:8])]
            if chosendate == reservationdate:
                curtime = reservation.return_time()
                curhour = int(curtime[0:2])
                curminute = int(curtime[2:4])
                temptime = curhour*60+curminute
                endtime = temptime + reservation.get_length()
                minute = endtime % 60
                minutestring = ''
                if minute < 10:
                    minutestring += '0'
                minutestring += str(minute)
                hour = int((endtime - minute)/60)
                if hour >= 24:
                    hour -= 24
                hourstring = ''
                if hour < 10:
                    hourstring += '0'
                hourstring += str(hour)
                x = reservation.return_sport()
                print_str = '{} {}:{}-{}:{}'.format(x, curtime[0:2], curtime[2:4], hourstring, minutestring)
                label = QtWidgets.QLabel(print_str, self)
                self.reservationlist.append(label)
                self.layout.addWidget(label, i+1, 2, 1, 1)
                i += 1

    def hide_reservations(self):
        for i in self.reservationlist:
            i.hide()

    def write_line(self):
        f = open('data.txt', 'a')
        b = open('data.txt', 'r')
        lines = b.readlines()
        if self.line not in lines:
            f.write(self.line)
