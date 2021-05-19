import unittest
from app import app

import mysql.connector

from flask import request, Response

class helper:
    @staticmethod
    def getMySqlCursor():
        myCursor = None
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
        return myCursor

class AppTest(unittest.TestCase):

    def test_avgProfitGenreWiseJSON(self):

        try:
            app.testHelper()
            res = app.avgProfitGenreWiseJSON()
            print(res.response)
            if res is None:
                print("avgProfitGenreWiseJSON Data is NONE")
            else:
                self.assertEqual(res.status_code, 200)
                print("Successfully checked for avgProfitGenreWiseJSON: 200 OK!")
        except Exception as e:
            print("Cannot call the function for avgProfitGenreWiseJSON!")
            print(e)

    def test_tempPass_always(self):
        pass


if __name__ == "__main__":
    unittest.main()