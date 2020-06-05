import sys
import psycopg2
from gui import *
from database import *

class AppGui(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.con = None
        self.countUsers = 0
        self.countTarifs = 0
        self.cur = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.createdbButton.clicked.connect(self.createDB)
        self.ui.deletedbButton.clicked.connect(self.deleteDB)
        self.ui.deleteTablesButton.clicked.connect(self.cleanAllTables)
        self.ui.userButtonFind.clicked.connect(self.selectUsers)
        self.ui.userButtonInsert.clicked.connect(self.insertUser)
        self.ui.userButtonDelete.clicked.connect(self.deleteFromUser)
        self.ui.userButtonClean.clicked.connect(self.cleanUsertable)
        self.ui.tarifButtonFind.clicked.connect(self.selectTarif)
        self.ui.tarifButtonInsert.clicked.connect(self.insertTarif)
        self.ui.tarifButtonDelete.clicked.connect(self.deleteFromTarif)
        self.ui.tarifButtonClean.clicked.connect(self.cleanTariftable)
        self.ui.tableWidgetUser.setHorizontalHeaderLabels(["Номер", "ФИО", "Адрес", "id Тариф"])
        self.ui.tableWidgetTarif.setHorizontalHeaderLabels(["id тарифа", "Название тарифа", "Стоимость", "Кол. клиентов"])



    def updateTableUser(self, rows = None):
        i=0
        if rows == "" or rows is None:
            self.cur.callproc("selectAllUsers")
            rows = self.cur.fetchall()

        for r in rows:
            self.ui.tableWidgetUser.setItem(i, 0, QtWidgets.QTableWidgetItem(str(r[0])))
            self.ui.tableWidgetUser.setItem(i, 1, QtWidgets.QTableWidgetItem(str(r[1])))
            self.ui.tableWidgetUser.setItem(i, 2, QtWidgets.QTableWidgetItem(str(r[2])))
            self.ui.tableWidgetUser.setItem(i, 3, QtWidgets.QTableWidgetItem(str(r[3])))
            i=i+1
        if(len(rows)<self.countUsers):
            for j in range(len(rows),self.countUsers):
                self.ui.tableWidgetUser.takeItem(j, 0)
                self.ui.tableWidgetUser.takeItem(j, 1)
                self.ui.tableWidgetUser.takeItem(j, 2)
                self.ui.tableWidgetUser.takeItem(j, 3)
        self.countUsers = len(rows)

    def updateTableTarif(self, rows = None):
        i = 0
        if rows == "" or rows is None:
            self.cur.callproc("selectAllTarifs")
            rows = self.cur.fetchall()

        for r in rows:
            self.ui.tableWidgetTarif.setItem(i, 0, QtWidgets.QTableWidgetItem(str(r[0])))
            self.ui.tableWidgetTarif.setItem(i, 1, QtWidgets.QTableWidgetItem(str(r[1])))
            self.ui.tableWidgetTarif.setItem(i, 2, QtWidgets.QTableWidgetItem(str(r[2])))
            self.ui.tableWidgetTarif.setItem(i, 3, QtWidgets.QTableWidgetItem(str(r[3])))
            i = i + 1
        if (len(rows) < self.countTarifs):
            for j in range(len(rows), self.countTarifs):
                self.ui.tableWidgetTarif.takeItem(j, 0)
                self.ui.tableWidgetTarif.takeItem(j, 1)
                self.ui.tableWidgetTarif.takeItem(j, 2)
                self.ui.tableWidgetTarif.takeItem(j, 3)
        self.countTarifs = len(rows)


    def createDB(self):
        self.ui.deletedbButton.setEnabled(True)
        self.ui.deleteTablesButton.setEnabled(True)
        self.ui.userButtonFind.setEnabled(True)
        self.ui.userButtonInsert.setEnabled(True)
        self.ui.userButtonDelete.setEnabled(True)
        self.ui.userButtonClean.setEnabled(True)
        self.ui.tarifButtonFind.setEnabled(True)
        self.ui.tarifButtonInsert.setEnabled(True)
        self.ui.tarifButtonDelete.setEnabled(True)
        self.ui.tarifButtonClean.setEnabled(True)
        con = psycopg2.connect(
            database='postgres', user='postgres',
            host='localhost', password='root')
        con.autocommit = True
        cur = con.cursor()
        cur.execute(open("sqlcreate.sql", "r").read())
        cur.callproc('createDB')
        cur.close()
        con.close()
        self.con = psycopg2.connect(
            dbname='lababase', user='newuser',
            host='localhost', password='123')
        self.con.autocommit = True
        self.cur = self.con.cursor()
        self.cur.execute(open("sqlFunc.sql", "r").read())
        self.updateTableTarif()
        self.updateTableUser()

    def deleteDB(self):
        self.ui.deletedbButton.setEnabled(False)
        self.ui.deleteTablesButton.setEnabled(False)
        self.ui.userButtonFind.setEnabled(False)
        self.ui.userButtonInsert.setEnabled(False)
        self.ui.userButtonDelete.setEnabled(False)
        self.ui.userButtonClean.setEnabled(False)
        self.ui.tarifButtonFind.setEnabled(False)
        self.ui.tarifButtonInsert.setEnabled(False)
        self.ui.tarifButtonDelete.setEnabled(False)
        self.ui.tarifButtonClean.setEnabled(False)
        self.cleanAllTables()
        self.cur.close()
        self.con.close()
        con = psycopg2.connect(
            database='postgres', user='postgres',
            host='localhost', password='root')
        con.autocommit = True
        cur = con.cursor()
        cur.callproc('dropDB')
        cur.close()
        con.close()


    def createTables(self):
        self.cur.callproc("createTables")

    def insertUser(self):
        phone = self.ui.phoneLineEdit.text()
        username = self.ui.usernameLineEdit.text()
        address = self.ui.addressLineEdit.text()
        idtarif = self.ui.tarifLineEdit.text()
        if (phone != "" and username != "" and address != "" and idtarif != ""):
            self.cur.callproc("insertUser", [phone, username, address, idtarif])
            self.updateTableUser()
            self.updateTableTarif()

    def insertTarif(self):
        id = self.ui.tarifidLineEdit.text()
        tarif = self.ui.tarifnameLineEdit.text()
        price = self.ui.tarifpriceLineEdit.text()
        if (id != "" and tarif != "" and price != ""):
            self.cur.callproc("insertTarif", [id, tarif, price])
            self.updateTableTarif()

    def selectUsers(self):
        username = self.ui.usernameLineEdit.text()
        if username == "":
            self.cur.callproc("selectAllUsers")
        else:
            self.cur.callproc("selectUsers", [str(username)])
        rows = self.cur.fetchall()
        self.updateTableUser(rows)

    def selectTarif(self):
        tarif = self.ui.tarifnameLineEdit.text()
        if tarif == "":
            self.cur.callproc("selectAllTarifs")
        else:
            self.cur.callproc("selectTarifs", [str(tarif)])
        rows = self.cur.fetchall()
        self.updateTableTarif(rows)

    def deleteFromUser(self):
        username = self.ui.usernameLineEdit.text()
        self.cur.callproc("deleteFromUsertable", [username])
        self.updateTableUser()

    def deleteFromTarif(self):
        tarif = self.ui.tarifnameLineEdit.text()
        self.cur.callproc("deleteFromTariftable", [tarif])
        self.updateTableTarif()

    def cleanUsertable(self):
        self.cur.callproc("cleanUsertable")
        self.updateTableUser()

    def cleanTariftable(self):
        self.cur.callproc("cleanTariftable")
        self.updateTableTarif()

    def cleanAllTables(self):
        self.cleanUsertable()
        self.cleanTariftable()
        self.updateTableTarif()

    def setIndex(self):
        self.cur.callproc("setIndex")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = AppGui()
    myapp.show()
    sys.exit(app.exec_())