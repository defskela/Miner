import sys
from PyQt5.QtGui import QIcon, QFont  # добавление картинок и менять шрифт
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QInputDialog  # стандартные диалоги
from random import randrange  # генерация бомб
from PyQt5.QtCore import Qt, QSize  # ПКМ, задать размеры картинки
from PyQt5 import uic
from threading import Timer  # считать время игры
import sqlite3  # БД с занесением имени юзера и его времени до победы. Защита от повторов имён


# conn = sqlite3.connect('projectpassword.db')  #  СОЗДАНИЕ МОЕЙ БД С ПАРОЛЯМИ
# cur = conn.cursor()
# cur.execute("""CREATE TABLE IF NOT EXISTS users(
#    username TEXT,
#    password TEXT);
# """)
# conn.commit()
# DELETE from users

# conn = sqlite3.connect('project.db')  #  СОЗДАНИЕ МОЕЙ БД С ИНФОЙ ОБ ИГРЕ
# cur = conn.cursor()
# cur.execute("""CREATE TABLE IF NOT EXISTS users(
#    username TEXT,
#    time INTEGER);
# """)
# conn.commit()
# DELETE from users


class Lose(QWidget):  # класс, который выводится при победе \ поражении
    def __init__(self):
        global winlose  # победа \ поражение
        global val  # размеры поля игры, если пользователь использовал QSlider
        global flag  # размеры поля игры, если пользователь использовал QRadioButton
        super().__init__()
        uic.loadUi('Lose.ui', self)
        self.appendd.clicked.connect(self.dob)  # добавление юзера в БД
        self.nazad1.clicked.connect(self.defnazad1)  # возврат на выбор режима
        self.restarting1.clicked.connect(self.restart1)  # начать заново в том же режиме
        self.nameuser = ''
        if flag == 0:  # флаг = 0 при размере поля 5х5
            self.lvl = '5x5'
        elif flag == 1:  # флаг = 1 при размере поля 9х9
            self.lvl = '9x9'
        elif flag == 2:  # флаг = 2 при размере поля 10х10
            self.lvl = '10x10'
        else:  # пользователь выбрал режимы, больше, чем 10x10
            self.lvl = f'{val}x{val}'
        con1 = sqlite3.connect('project.db')
        cur1 = con1.cursor()
        self.champion = cur1.execute(f"""SELECT username FROM users
        WHERE level = '{self.lvl}' ORDER BY time""").fetchone()  # имя юзера с наименьшим временем
        if self.champion:  # если хоть кто-то играл в этот режим
            self.label_4.setText(str(*self.champion))
            self.label_4.setFont(QFont("Times", 10, QFont.Bold))  # меняем шрифт
        if winlose == 0:  # winlose = 0 при поражении
            self.setWindowTitle('Поражение')
            self.pushButton.setIcon(QIcon('Бомбочка.png'))
            self.pushButton.resize(50, 50)
            self.pushButton.setIconSize(QSize(50, 50))
            self.label.setText('ВЫ ПРОИГРАЛИ')
            self.lineEdit.setEnabled(False)  # нельзя ввести имя победителя
            self.appendd.setEnabled(False) # нельзя ввести имя победителя
        elif winlose == 1:  # winlose = 1 при победе
            self.setWindowTitle('Победа')
            self.pushButton.setIcon(QIcon('ПОБЕДА.png'))
            self.pushButton.resize(50, 50)
            self.pushButton.setIconSize(QSize(50, 50))
            self.label.setText('УРА! ПОБЕДА!')
        self.label.setFont(QFont("Times", 14, QFont.Bold))
        self.label.adjustSize()  # подстраиваем размеры

    def defnazad1(self):  # функция отвечает за возврат на выбор режима
        ex1.show()
        c.hide()

    def restart1(self):  # рестарт
        global a  # иначе свернется
        global flag
        global val
        if flag == 0:
            a = Sapper(5)  # подается размер поля в формате NxN
            a.show()
        elif flag == 1:
            a = Sapper(9) # подается размер поля в формате NxN
            a.show()
        elif flag == 2:
            a = Sapper(10) # подается размер поля в формате NxN
            a.show()
        elif flag == -1:
            a = Sapper(val) # подается размер поля в формате valXval
            a.show()
        c.hide()  # cкрываем окно выбора режима

    def dob(self):  # добавление юзера в БД
        global clock  # время, за которое юзер сыграл
        con2 = sqlite3.connect('project.db')  # БД с инфой об игре: ник, время, лвл
        cur2 = con2.cursor()
        conpass = sqlite3.connect('projectpassword.db')  # БД с паролями
        curpass = conpass.cursor()
        # print(list(cur.execute("""SELECT username from users""")))  # вывод всех имен пользователей
        if self.lineEdit.text() != '':
            # проверка, есть ли такое имя в БД
            if (self.lineEdit.text(),) in curpass.execute(f"""SELECT username FROM users"""):
                self.UppUser()
                # print([(self.password,)])
                # print(list(curpass.execute(f"""SELECT password from users
                # WHERE username = '{self.lineEdit.text()}'""")))
                if [(self.password,)] == list(curpass.execute(f"""SELECT password from users
                WHERE username = '{self.lineEdit.text()}'""")):
                    if val == 10:
                        if flag == 0:
                            cur2.execute(f"""UPDATE users
                            SET time = {clock}, level = '5x5'
                            WHERE username = '{self.lineEdit.text()}'""")
                            self.errorz.setText('Данные успешно обновлены')
                        elif flag == 1:
                            cur2.execute(f"""UPDATE users
                            SET time = {clock}, level = '9x9'
                            WHERE username = '{self.lineEdit.text()}'""")
                            self.errorz.setText('Данные успешно обновлены')
                        elif flag == 2:
                            cur2.execute(f"""UPDATE users
                            SET time = {clock}, level = '10x10'
                            WHERE username = '{self.lineEdit.text()}'""")
                            self.errorz.setText('Данные успешно обновлены')
                        else:
                            cur2.execute(f"""UPDATE users
                            SET time = {clock}, level = '{val}x{val}'
                            WHERE username = '{self.lineEdit.text()}'""")
                            self.errorz.setText('Данные успешно обновлены')
                else:
                    self.errorz.setText('Неверный пароль')
            else:
                self.NewUser()
                self.errorz.setText('Ваше имя успешно добавлено!')
                if val == 10:  # проверка, выбрал ли пользователь большой режим
                    if flag == 0:  # режим 5x5
                        cur2.execute(f"""INSERT INTO users(username, time, level)
                        VALUES('{self.lineEdit.text()}', {clock}, '5x5')""")  # заносим инфу в БД: имя, время, режим
                        curpass.execute(f"""INSERT INTO users(username, password)
                        VALUES('{self.lineEdit.text()}', '{self.password}')""")  # заносим инфу в БД: ник, пароль
                        self.errorz.setText('Ваше имя успешно добавлено!')
                    elif flag == 1:  # режим 9х9
                        cur2.execute(f"""INSERT INTO users(username, time, level)
                        VALUES('{self.lineEdit.text()}', {clock}, '9x9')""")  # заносим инфу в БД: имя, время, режим
                        curpass.execute(f"""INSERT INTO users(username, password)
                        VALUES('{self.lineEdit.text()}', '{self.password}')""")  # заносим инфу в БД: ник, пароль
                        self.errorz.setText('Ваше имя успешно добавлено!')
                    elif flag == 2:  # режим 10х10
                        cur2.execute(f"""INSERT INTO users(username, time, level)
                        VALUES('{self.lineEdit.text()}', {clock}, '10x10')""")  # заносим инфу в БД: имя, время, режим
                        curpass.execute(f"""INSERT INTO users(username, password)
                        VALUES('{self.lineEdit.text()}', '{self.password}')""")  # заносим инфу в БД: ник, пароль
                        self.errorz.setText('Ваше имя успешно добавлено!')
                else:  # если пользователь выбрал большой режим
                    cur2.execute(f"""INSERT INTO users(username, time, level)
                    VALUES('{self.lineEdit.text()}', {clock}, '{str(val)}x{str(val)}')""")
                    curpass.execute(f"""INSERT INTO users(username, password)
                    VALUES('{self.lineEdit.text()}', '{self.password}')""")  # заносим инфу в БД: ник, пароль
                    self.errorz.setText('Ваше имя успешно добавлено!')
        con2.commit()  # сохраняем инфу в БД
        conpass.commit()
        self.champion = cur2.execute(f"""SELECT username FROM users
                WHERE level = '{self.lvl}' ORDER BY time""").fetchone()
        # выводим юзера с минимальным временем
        self.label_4.setText(str(*self.champion))
        self.label_4.setFont(QFont("Times", 10, QFont.Bold))  # меняем шрифт
        # если игрок стал чемпионом, инфа меняется в реальном времени

    def NewUser(self):
        self.password = str(QInputDialog.getText(self, 'Новый пользователь', 'Придумайте пароль')[0])

    def UppUser(self):
        self.password = str(QInputDialog.getText(self, 'Обновление данных', 'Введите пароль')[0])


class FAQInfo(QWidget):  # кнопка FAQ на экране выбора режима. Читает из файла. Краткое описание игры
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('FAQ.ui', self)
        self.setWindowTitle('FAQ')
        with open('FAQ.txt', 'r', encoding='utf8') as FAQfile:  # читаем из файла на русском
            for i in FAQfile.readlines():
                self.label.setText(self.label.text() + i)
        self.label.sizeHint()


class Modes(QWidget):  # выбор режима
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global val
        val = 10
        uic.loadUi('выбор режима.ui', self)
        self.setWindowTitle('Выбор режима')
        self.startt.clicked.connect(self.start)  # начало игры
        self.FAQ.clicked.connect(self.defFAQ)  # открывает новую форму FAQ с описанием игры
        self.horizontalSlider.setSingleStep(1)  # шаг ползунка - 1
        self.horizontalSlider.setMinimum(10)  # минимальное значение ползунка - 10
        self.horizontalSlider.setMaximum(18)  # максимальное значение ползунка - 18: больше не влезет по y
        self.horizontalSlider.valueChanged[int].connect(self.changeValue)  # коннект ползунка

    def changeValue(self, value):  # выводим на лейбл значение ползунка
        global val
        self.label.setText(str(value))
        val = value
        self.sizeHint()

    def start(self):
        global a  # создание формы игры. Без глобал сразу сворачивается
        global flag  # передача размеров: 3 режима и большой размер
        global val  # передача больших размеров: ползунок
        if val != 10:  # большой размер
            flag = -1
            a = Sapper(val)
            a.show()  # выводим форму игры
            ex1.hide()  # скрываем форму выбора режима
        elif self.x5.isChecked():  # проверка QRadioButton на выбор одного из 3х основных режимов
            flag = 0  # 5x5
            a = Sapper(5)
            a.show()
            ex1.hide()
        elif self.x9.isChecked():
            flag = 1  # 9x9
            a = Sapper(9)
            a.show()
            ex1.hide()
        elif self.x10.isChecked():
            flag = 2  # 10x10
            a = Sapper(10)
            a.show()
            ex1.hide()

    def defFAQ(self):
        global b  # новая форма, сворачивается без глобала
        b = FAQInfo()
        b.show()


class MyButton(QPushButton):  # для создания флажка при клике ПКМ пришлось переопределить класс кнопки.
    # За основу был взят код с https://ru.stackoverflow.com/questions/748835
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icondesk = []
        for _ in range(leng):
            self.icondesk.append([0] * leng)  # для просмотра, есть ли флажок в клетке. 1 - есть, 0 - нет

    def mousePressEvent(self, event):
        button = event.button()
        if button == Qt.RightButton:
            xx = self.objectName().index('x')
            if self.icondesk[int(self.objectName()[1:xx])][int(self.objectName()[xx + 1:])] == 1:
                # если флажок уже стоит и пришел ещё один клик ПКМ, то снимаем флаг нулевой картинкой
                self.setIcon(QIcon())
                self.icondesk[int(self.objectName()[1:xx])][int(self.objectName()[xx + 1:])] = 0
            else:
                self.icondesk[int(self.objectName()[1:xx])][int(self.objectName()[xx + 1:])] = 1  # ставим флажок
                self.setIcon(QIcon('флажок.png'))
                self.setIconSize(QSize(50, 50))
        return QPushButton.mousePressEvent(self, event)  # возвращаем кнопку с готовым ПКМом


class Sapper(QWidget):
    def __init__(self, length=5):  # пришлось сделать значение по умолчанию, чтобы подавать размеры
        super().__init__()
        global leng
        leng = length  # для всех классов
        self.timeer = QLabel(self)  # лейбл для вывода времени
        self.clocks = 0  # счётчик времени
        self.setWindowTitle('Сапёр')
        self.lenght = length  # размеры поля в формате length/length
        self.clearcell = self.lenght ** 2 - self.lenght ** 2 // 7  # кол-во пустых клеток = размеры ** 2 - кол-во бомб
        self.nazad = QPushButton(self)  # кнопка, позволяющая вернуться к выбору режима
        self.nazad.setText('Назад')
        self.nazad.sizeHint()
        self.nazad.clicked.connect(self.returne)
        self.nazad.move(50, 15)
        self.restarting = QPushButton(self)  # кнопка рестарта
        self.restarting.setText('RESTART')
        self.restarting.sizeHint()
        self.restarting.clicked.connect(self.restart)
        self.label = QLabel(self)  # лейбл для подсчета пустых клеток
        self.move(0, 0)
        self.start_x = 20  # 20 + 50 (размер одной клетки сапёра), 70 - начальная координата по x т,к в цикле сразу + 50
        self.start_y = 0  # 0 + 50 (размер одной клетки сапёра), 50 - начальная координата по x т,к в цикле сразу + 50
        self.cnt = 0  # кол-во бомб рядом с клеткой, по которой кликнули
        self.bombs = 0  # для спавна бомб
        self.coord_x = 0  # координата кликнутой клетки в списке, внутри вложенного
        self.coord_y = 0  # координата кликнутой клетки в списке, номер вложенного списка
        self.backdesk = []  # невидимая доска для проверки бомба (1) или пусто (0)
        self.frontdesk = []  # пока что не используется
        for _ in range(self.lenght):  # просто умножением не получилось из-за него вся строка была в минах
            self.backdesk.append([0] * self.lenght)
        for _ in range(length):
            self.frontdesk.append([0] * self.lenght)
        # for t in self.backdesk: - глянуть массив с бомбами
        #     print(t) - глянуть
        for i in range(len(self.backdesk)):  # спавним кнопки
            self.start_y += 50
            self.start_x = 20
            for j in range(len(self.backdesk)):
                self.start_x += 50
                self.a = MyButton(self)  # определили клик ПКМ
                self.a.setObjectName('n' + str(j) + 'x' + str(i))  # создаем имя в формате n0x0, n0x1 и тд
                # print(self.a.objectName())
                self.a.move(self.start_x, self.start_y)
                self.a.resize(50, 50)
                self.a.clicked.connect(self.click)
        self.label.move(70, self.start_y + 50)
        self.restarting.move(self.start_x + 50, self.start_y + 50)
        self.label.setText(f'Осталось открыть клеток: {str(self.clearcell)}')
        self.timeer.move(150, 20)
        self.timeer.resize(100, 20)
        self.deftimer()  # начинаем считать время
        self.sizeHint()

    def click(self):
        xx = self.sender().objectName().index('x')
        self.coord_x = int(self.sender().objectName()[1:xx])  # номер внутри вложенного списка
        self.coord_y = int(self.sender().objectName()[xx + 1:])  # номер вложенного списка
        # помогает различать записи по типу 110 (11 0 or 1 10)
        if self.clearcell == self.lenght ** 2 - self.lenght ** 2 // 7:  # условие соблюдается только при первом клике
            # позволяет безопасно кликнуть в первый раз. Генерация бомб идет после клика
            while self.bombs != self.lenght ** 2 // 7:  # плотность бомб - каждая 7я
                chx = randrange(leng)
                chy = randrange(leng)
                if self.backdesk[chy][chx] == 0 and not(chx == self.coord_x and chy == self.coord_y):
                    self.backdesk[chy][chx] = 1
                    self.bombs += 1
            for i in self.backdesk:  # - посмотреть на массив, свериться со значениями кнопок
                print(i)
            self.xod()
        else:
            self.xod()

    def xod(self):
        global c  # форма поражения / победы
        global winlose  # 0 - поражение, 1 - победа
        self.cnt = 0  # кол-во бомб рядом с кликнутой кнопкой
        # for i in self.backdesk:  # - посмотреть на массив, свериться со значениями кнопок
        #     print(i)
        # print(self.coord_x, self.coord_y)  # - проверка координат на правильность
        if self.backdesk[self.coord_y][self.coord_x] == 1:  # если бомба, то вешаем картинку бомбы
            self.sender().setIcon(QIcon('Бомбочка.png'))
            self.sender().setIconSize(QSize(50, 50))  # под размер кнопки
            self.cnt = -99  # чтобы время перестало считать
            self.sender().setStyleSheet('QPushButton {background-color: black;}')
            # красим кнопку. Инфу взял отсюда: https://ru.stackoverflow.com/questions/1061002
            self.setEnabled(False)  # блокируем всё поле
            winlose = 0
            c = Lose()
            c.show()
            # a.hide()
        # далее 100 строк, которые считают кол-во бомб рядом
        # сначала думал просто прогонять все 8 клеток и отлавливать ошибку IndexError, но из-за того, что
        # существует координата -1 и это не ошибка, приходится опять писать много условий, что делает идею бессмысленной
        elif self.coord_y == 0:  # далее 100 строк, которые считают кол-во бомб рядом
            if self.coord_x == 0:
                if self.backdesk[self.coord_y + 1][self.coord_x + 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y + 1][self.coord_x] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y][self.coord_x + 1] == 1:
                    self.cnt += 1
            elif self.coord_x == self.lenght - 1:
                if self.backdesk[self.coord_y + 1][self.coord_x - 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y + 1][self.coord_x] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y][self.coord_x - 1] == 1:
                    self.cnt += 1
            else:
                if self.backdesk[self.coord_y + 1][self.coord_x + 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y + 1][self.coord_x] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y][self.coord_x + 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y + 1][self.coord_x - 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y][self.coord_x - 1] == 1:
                    self.cnt += 1
        elif self.coord_y == self.lenght - 1:
            if self.coord_x == 0:
                if self.backdesk[self.coord_y - 1][self.coord_x + 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y - 1][self.coord_x] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y][self.coord_x + 1] == 1:
                    self.cnt += 1
            elif self.coord_x == self.lenght - 1:
                if self.backdesk[self.coord_y - 1][self.coord_x - 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y - 1][self.coord_x] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y][self.coord_x - 1] == 1:
                    self.cnt += 1
            else:
                if self.backdesk[self.coord_y - 1][self.coord_x + 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y - 1][self.coord_x] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y][self.coord_x + 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y - 1][self.coord_x - 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y][self.coord_x - 1] == 1:
                    self.cnt += 1
        else:
            if self.coord_x == 0:
                if self.backdesk[self.coord_y + 1][self.coord_x] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y - 1][self.coord_x] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y + 1][self.coord_x + 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y - 1][self.coord_x + 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y][self.coord_x + 1] == 1:
                    self.cnt += 1
            elif self.coord_x == self.lenght - 1:
                if self.backdesk[self.coord_y + 1][self.coord_x] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y - 1][self.coord_x] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y + 1][self.coord_x - 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y - 1][self.coord_x - 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y][self.coord_x - 1] == 1:
                    self.cnt += 1
            else:
                if self.backdesk[self.coord_y + 1][self.coord_x] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y - 1][self.coord_x] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y + 1][self.coord_x - 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y - 1][self.coord_x - 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y][self.coord_x - 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y + 1][self.coord_x + 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y - 1][self.coord_x + 1] == 1:
                    self.cnt += 1
                if self.backdesk[self.coord_y][self.coord_x + 1] == 1:
                    self.cnt += 1
        if self.cnt > 0:  # красим кнопку в красный и выводим кол-во бомб рядом
            self.sender().setText(str(self.cnt))
            self.sender().setStyleSheet('QPushButton {background-color: red; color: black;}')
            self.sender().setIcon(QIcon())
        elif self.cnt == 0:  # бомб рядом нет - красим в зеленый
            self.sender().setStyleSheet('QPushButton {background-color: green;}')
            self.sender().setIcon(QIcon())
        self.clearcell -= 1  # пустых клеток становится на 1 меньше с каждым кликом не по бомбе
        if self.clearcell == 0:  # победа, если все нормальные кнопки открыты
            self.cnt = -99  # перестаем считать время
            self.setEnabled(False)
            winlose = 1
            c = Lose()
            c.show()
            a.hide()
        self.sender().setEnabled(False)  # блокируем открытую кнопку
        self.label.setText(f'Осталось открыть клеток: {str(self.clearcell)}')

    def returne(self):  # возвращает к выбору режима
        ex1.show()
        a.hide()

    def restart(self):  # начать заново в том же режиме
        global a
        global flag
        global val
        if flag == 0:
            a.hide()
            a = Sapper(5)
            a.show()
        elif flag == 1:
            a.hide()
            a = Sapper(9)
            a.show()
        elif flag == 2:
            a.hide()
            a = Sapper(10)
            a.show()
        elif flag == -1:
            a.hide()
            a = Sapper(val)
            a.show()

    def deftimer(self):  # счетчик времени
        global clock
        if self.cnt != -99:  # считаем до победы \ поражения
            self.timeer.setText('Время: ' + str(self.clocks))
            self.clocks += 1
            t = Timer(1, self.deftimer)  # спустя 1 сек снова вызываем функцию
            t.start()
            clock = self.clocks


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = Modes()
    ex1.show()
    sys.exit(app.exec())
