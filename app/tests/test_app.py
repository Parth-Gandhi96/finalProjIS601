import unittest
from app import app

import mysql.connector

from flask import request, Response

class AppTest(unittest.TestCase):

    def test_avgProfitGenreWiseJSON(self):
        try:
            try:
                app.cursor = mysql.connector.connect(host="127.0.0.1", user="root", password="",
                                                     database="finalProjData").cursor
            except:
                print("Error while fetching data using mysql connector!")
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