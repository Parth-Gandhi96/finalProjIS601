import unittest
from app import app

from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

import mysql.connector

class HomeViewTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            app.app,app.mysql = app.createRunAppTest()
            try: app.run(host='0.0.0.0')
            except: print("app run failed on 0.0.0.0")
            try: app.mysql.init_app(app)
            except: print("mysql init failed")
        except Exception as e:
            print("Error while creating the app and running it")
            print(e)

        try:
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="finalProjData"
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM userTable")
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
        except:
            print("some error while fetching data using mysql connector!")

    def test_avgProfitGenreWiseJSON(self):
        try:
            data = app.avgProfitGenreWiseJSON()
            print(data)
            if data is None:
                print("avgProfitGenreWiseJSON Data is NONE")
            else:
                print("avgProfitGenreWiseJSON Data is not NONE")
        except Exception as e:
            print("Cannot call the function for avgProfitGenreWiseJSON!")
            print(e)

    def test_tempPass_always(self):
        pass


if __name__ == "__main__":
    unittest.main()