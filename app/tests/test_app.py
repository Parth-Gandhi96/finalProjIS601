import unittest
from app import app

from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

import mysql.connector

class HomeViewTest(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        try:
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="finalProjData"
            )
            myCursor = mydb.cursor()
        except:
            print("Some error while fetching data using mysql connector!")

    def test_avgProfitGenreWiseJSON(self):
        try:
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="finalProjData"
            )
            myCursor = mydb.cursor()
        except:
            print("Some error while fetching data using mysql connector!")

        try:
            app.cursor = myCursor
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