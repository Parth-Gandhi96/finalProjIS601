import unittest
import app


class HomeViewTest(unittest.TestCase):
    temp_app = None

    @classmethod
    def setUpClass(cls):
        cls.temp_app = app()

    def setUp(self):
        try:
            data = cls.temp_app.fetchAvgProfitGenreWise()
            if data is None:
                print("Data is NONE")
            else:
                print("Data is not NONE")
        except:
            print("Cannot call the function for fetchAvgProfitGenreWise!")


if __name__ == "__main__":
    unittest.main()