
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import secrets
import string
import pyperclip
import os
from PyQt5.QtCore import QTimer
from datetime import datetime

app = QApplication([])
ui = uic.loadUi("untitled.ui")

#---------------------------------------------------------------------------------------

TRIAL_FILE = "trial.txt"
SECRET_KEY = "PRO-LPMS-202625062014275"


def check_and_get_trial_minutes():
    today_str = str(datetime.now().date())

    if not os.path.exists(TRIAL_FILE):
        with open(TRIAL_FILE, "w") as f:
            f.write(f"{today_str}\n100")
        return 100

    with open(TRIAL_FILE, "r") as f:
        lines = f.read().splitlines()
        saved_date = lines[0]
        saved_minutes = lines[1]

    
    if saved_minutes == "PREMIUM":
        return "PREMIUM"

    if today_str != saved_date:
        with open(TRIAL_FILE, "w") as f:
            f.write(f"{today_str}\n100")
        return 100

    return int(saved_minutes)


minutes_left = check_and_get_trial_minutes()


def update_trial_timer():
    global minutes_left


    if minutes_left == "PREMIUM":
        if not ui.isEnabled():
            ui.setEnabled(True)
        ui.statusbar.showMessage("LPMSolo PREMIUM Версия активирована! Лимитов нет.", 0)
        ui.trialbar.setValue(100)
        trial_timer.stop()
        return

    if minutes_left > 0 and not ui.isEnabled():
        ui.setEnabled(True)

    if minutes_left > 0:
        today_str = str(datetime.now().date())
        with open(TRIAL_FILE, "w") as f:
            f.write(f"{today_str}\n{minutes_left}")

        ui.statusbar.showMessage(f"Осталось триал-времени на сегодня: {minutes_left} мин.", 0)
        ui.trialbar.setValue(minutes_left)
        minutes_left -= 1

    elif minutes_left <= 0:
        ui.setEnabled(False)
        ui.statusbar.showMessage("Ваш лимит (100 минут) на сегодня исчерпан! Введите Pro-ключ для разблокировки.", 0)
        ui.trialbar.setValue(0)
        trial_timer.stop()



def activate_pro():
    global minutes_left
    # Показываем красивое окошко ввода ключа
    text, ok = QtWidgets.QInputDialog.getText(ui, 'Активация Pro', 'Введите лицензионный ключ:')

    if ok and text == SECRET_KEY:
        minutes_left = "PREMIUM"
        today_str = str(datetime.now().date())

        with open(TRIAL_FILE, "w") as f:
            f.write(f"{today_str}\nPREMIUM")

        QtWidgets.QMessageBox.information(ui, "Успех!",
                                          "Программа успешно активирована до Pro-версии! Все ограничения сняты.")
        update_trial_timer()
    elif ok:
        QtWidgets.QMessageBox.critical(ui, "Ошибка", "Неверный ключ активации!")



trial_timer = QTimer()
trial_timer.timeout.connect(update_trial_timer)


update_trial_timer()

if minutes_left != "PREMIUM" and minutes_left > 0:
    trial_timer.start(60000)
#-------------------------------------------------------------------------------------------------

ui.actionGet_PREMIUM.triggered.connect(activate_pro)

base_char = ' | '

def generation():
    length_str = ui.lengthE.text()
    length = int(length_str)
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    ui.genResL.setText(password)
    return password

def copy():
    text = ui.genResL.text()
    pyperclip.copy(text)
    ui.statusbar.showMessage("Copy success!", 2000)

ui.genB.clicked.connect(generation)
ui.copyB.clicked.connect(copy)

# Начало работы с файлами записи и тд.
passw = ui.passEd.text()

def check(isChecked):
    ui.label_5.setEnabled(not isChecked)
    ui.custLocE.setEnabled(not isChecked)

def create_file(isChecked):
    if not isChecked:
        location = ui.custLocE.text()
        full_path = os.path.join(location, 'passwords.txt')
    else:
        full_path = "passwords.txt"
    with open(full_path, 'a', encoding='utf-8') as file:
        text_1 = ui.passEd.text()
        text_2 = ui.siteNameE.text()
        file.write(text_1 + base_char + text_2 + "\n")

    ui.passEd.setText("")
    ui.siteNameE.setText("")




ui.useDLC.toggled.connect(check)

check(ui.useDLC.isChecked())

ui.add_custB.clicked.connect(lambda: create_file(ui.useDLC.isChecked()))

# Начало работы с Magic Text

def reload_text():
    word = ui.magicE.text()
    reverted_text = word[::-1]
    ui.magicL.setText(reverted_text)

def copy_magic():
    text = ui.magicL.text()
    pyperclip.copy(text)
    ui.statusbar.showMessage("Copy success!", 2000)



ui.magicB.clicked.connect(reload_text)
ui.magic_copyB.clicked.connect(copy_magic)

# Начало работы с файлами

def setEnabledContent(isChecked):
    if isChecked:
        ui.fileT.setEnabled(False)
        ui.fileE.setEnabled(False)
    else:
        ui.fileT.setEnabled(True)
        ui.fileE.setEnabled(True)

def structureFile():
    file_path = "passwords.txt"
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding='utf-8') as file:
        lines = file.read().splitlines()


    ui.tableWidget.setRowCount(len(lines))
    ui.tableWidget.setColumnCount(2)


    for row_index, line in enumerate(lines):
        if base_char in line:
            parts = line.split(base_char)
            password_val = parts[0]
            site_val = parts[1]

            # Пихаем данные в ячейки таблицы
            ui.tableWidget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(password_val))
            ui.tableWidget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(site_val))


ui.fileC.toggled.connect(setEnabledContent)

setEnabledContent(ui.fileC.isChecked())

ui.fileOB.clicked.connect(structureFile)

def about():
    QtWidgets.QMessageBox.aboutQt(ui)
def aboutthis():
    QtWidgets.QMessageBox.about(ui, "About LPMSolo", "LPMSolo - Local Password Manager SOLO is a secure password manager that combines both fun and useful features! For example: You can generate passwords and immediately save them to a file below, then view all your passwords in a convenient format. You can also use the Magic Text section to encrypt words—you can reverse a word or restore it to its original form! \n Thank you for using our product! \n \n LPMSolo v1.0")




def exit():
    app.exit()

ui.actionAbout_QT.triggered.connect(about)
ui.actionAbout_LPMSolo.triggered.connect(aboutthis)
ui.actionExit.triggered.connect(exit)



ui.show()
app.exec_()
