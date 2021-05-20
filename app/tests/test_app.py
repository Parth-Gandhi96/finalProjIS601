import unittest
from app import app

import mysql.connector

from flask import request, Response

class AppTest(unittest.TestCase):

    def test_avgProfitGenreWiseJSON(self):
        try:
            db = mysql.connector.connect(host="127.0.0.1", user="root", password="",
                                                 database="finalProjData")
            app.cursor = db.cursor()
            res = app.avgProfitGenreWiseJSON()
            # print(res.response)
            if res is None:
                print("avgProfitGenreWiseJSON Data is NONE")
            else:
                self.assertEqual(res.status_code, 200)
                print("Passed Successfully avgProfitGenreWiseJSON: [res:200 OK]!")
        except Exception as e:
            print("Test Case failed: avgProfitGenreWiseJSON!")
            print(e)

    def test_top10Profited(self):
        try:
            db = mysql.connector.connect(host="127.0.0.1", user="root", password="",
                                                 database="finalProjData")
            app.cursor = db.cursor()
            res = app.top10ProfitedJSON()
            # print(res.response)
            if res is None:
                print("top10ProfitedJSON Data is NONE")
            else:
                self.assertEqual(res.status_code, 200)
                print("Passed Successfully top10ProfitedJSON: [res:200 OK]!")
        except Exception as e:
            print("Test Case failed: top10ProfitedJSON!")
            print(e)

    def test_avgProfitImdbWiseJSON(self):
        try:
            db = mysql.connector.connect(host="127.0.0.1", user="root", password="",
                                                 database="finalProjData")
            app.cursor = db.cursor()
            res = app.avgProfitImdbWiseJSON()
            # print(res.response)
            if res is None:
                print("avgProfitImdbWiseJSON Data is NONE")
            else:
                self.assertEqual(res.status_code, 200)
                print("Passed Successfully avgProfitImdbWiseJSON: [res:200 OK]!")
        except Exception as e:
            print("Test Case failed: avgProfitImdbWiseJSON!")
            print(e)

    def test_last5yearChartsJSON(self):
        try:
            db = mysql.connector.connect(host="127.0.0.1", user="root", password="",
                                                 database="finalProjData")
            app.cursor = db.cursor()
            res = app.last5yearChartsJSON()
            # print(res.response)
            if res is None:
                print("last5yearChartsJSON Data is NONE")
            else:
                self.assertEqual(res.status_code, 200)
                print("Passed Successfully last5yearChartsJSON: [res:200 OK]!")
        except Exception as e:
            print("Test Case failed: last5yearChartsJSON!")
            print(e)


if __name__ == "__main__":
    unittest.main()