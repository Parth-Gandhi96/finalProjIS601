import unittest
import app
import requests

class HomeViewTest(unittest.TestCase):

    def test_avgProfitGenreWiseJSON(self):
        try:
            data = requests.get('http://0.0.0.0:5000/avgProfitGenreWiseJSON')
            print(data)
            if data is None:
                print("avgProfitGenreWiseJSON Data is NONE")
            else:
                print("avgProfitGenreWiseJSON Data is not NONE")
        except:
            print("Cannot call the function for avgProfitGenreWiseJSON!")

    def test_tempPass_always(self):
        pass


if __name__ == "__main__":
    unittest.main()