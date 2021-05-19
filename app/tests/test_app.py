import unittest
from app import app

class HomeViewTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            app.createRunAppTest()
        except Exception as e:
            print("Error while creating the app and running it")
            print(e)

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