import pickle
from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication
import os

dirname, filename = os.path.split(os.path.realpath(__file__))
Form, Window = uic.loadUiType(dirname+"\\calender.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


def save_to_file():
    global start_date, calc_date, description, dirname
    data_to_save = {"start": start_date, "end": calc_date, "desc": description}
    file1 = open(dirname+"\\text.txt", "wb")
    pickle.dump(data_to_save, file1)
    file1.close()
    task = """schtasks /create /tr "python """ + os.path.realpath(
        __file__) + """" /tn "Расписание с элементами напоминания" /sc MINUTE /mo {} /ed 29/04/2021 /F""".format(perem)
    os.system('chcp 65001')
    os.system(task)

def read_from_file():
    global start_date, calc_date, description, now_date, dirname
    try:
        file1 = open(dirname+"\\text.txt", "rb")
        data_to_load = pickle.load(file1)
        file1.close()
        start_date = data_to_load["start"]
        calc_date = data_to_load["end"]
        description = data_to_load["desc"]
        form.calendarWidget.setSelectedDate(calc_date)
        form.dateEdit.setDate(calc_date)
        form.plainTextEdit.setPlainText(description)
        delta_days_left = start_date.daysTo(now_date)
        delta_days_right = now_date.daysTo(calc_date)
        days_total = start_date.daysTo(calc_date)
        procent = int(delta_days_left * 100 / days_total)
        form.progressBar.setProperty("value", procent)
    except:
        print()


def on_click():
    global calc_date, description, start_date
    start_date = now_date
    calc_date = form.calendarWidget.selectedDate()
    description = form.plainTextEdit.toPlainText()
    save_to_file()


def on_click_calendar():
    global start_date, calc_date
    form.dateEdit.setDate(form.calendarWidget.selectedDate())
    calc_date = form.calendarWidget.selectedDate()
    delta_days = start_date.daysTo(calc_date)
    form.label.setText("Осталось: %s дн." % delta_days)


def on_dateedit_change():
    global start_date, calc_date
    form.calendarWidget.setSelectedDate(form.dateEdit.date())
    calc_date = form.dateEdit.date()
    delta_days = start_date.daysTo(calc_date)
    form.label.setText("Осталось: %s дн." % delta_days)


form.pushButton.clicked.connect(on_click)
form.calendarWidget.clicked.connect(on_click_calendar)
form.dateEdit.dateChanged.connect(on_dateedit_change)

start_date = form.calendarWidget.selectedDate()
now_date = form.calendarWidget.selectedDate()
calc_date = form.calendarWidget.selectedDate()
description = form.plainTextEdit.toPlainText()
read_from_file()

form.label_2.setText("Сегодня : %s" % start_date.toString('dd.MM.yyyy'))
on_click_calendar()

app.exec_()