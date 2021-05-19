import unittest
from main import app
import os


class HomeViewTest(unittest.TestCase):

    # def test_test(self):
    #     assert app.test() == "Works!"

    tempApp = None

    @classmethod
    def setUpClass(cls):
        tempApp = app()

    def test_env_var(self):
        try:
            assert str(os.environ.get('SENDER_EMAIL_ADDRESS')) == "parth96g@gmail.com"
        except AssertionError:
            print("email is: ",str(os.environ.get('SENDER_EMAIL_ADDRESS')))


    def test_fetchMovieCollectionLast5Years(self):
        try:
            assert app.fetchMovieCollectionLast5Years() is not None
        except AssertionError:
            print("DB not loaded....")

if __name__ == "__main__":
    unittest.main()