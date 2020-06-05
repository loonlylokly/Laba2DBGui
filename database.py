import psycopg2

class db():

    def __init__(self):
        con = psycopg2.connect(
            dbname='lababase', user='newuser',
            host='localhost', password='123')
        con.autocommit = True
        self.cur = con.cursor()
        self.cur.execute(open("sqlFunc.sql", "r").read())

    def createTables(self):
        self.cur.callproc("createTables")

    def insertUser(self, phone, username, address, idtarif):
        self.cur.callproc("insertUser", [phone, username, address, idtarif])

    def insertTarif(self, id, tarif, price):
        self.cur.callproc("insertTarif", [id, tarif, price])

    def selectUsers(self, username):
        self.cur.callproc("selectUsers", [username])

    def selectTarif(self, tarif):
        self.cur.callproc("selectTarif", [tarif])

    def deletFromUser(self, username):
        self.cur.callproc("deleteFromUsertable", [username])

    def deletFromTarif(self, tarif):
        self.cur.callproc("deleteFromTariftable", [tarif])

    def cleanUsertable(self):
        self.cur.callproc("cleanUsertable")

    def cleanTariftable(self):
        self.cur.callproc("cleanTariftable")

    def cleanAllTables(self):
        self.cur.callproc("cleanAllTables")

    def setIndex(self):
        self.cur.callproc("setIndex")