import unittest
import app
import requests

class HomeViewTest(unittest.TestCase):

    def test_avgProfitGenreWiseJSON(self):
        try:
            data = requests.get('http://localhost:5000/avgProfitGenreWiseJSON')
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