import unittest
import app
import os


class HomeViewTest(unittest.TestCase):

    # def test_test(self):
    #     assert app.test() == "Works!"

    def test_env_var(self):
        assert str(os.environ.get('SENDER_EMAIL_ADDRESS'))=="parth96g@gmail.com"

    def test_fetchMovieCollectionLast5Years(self):
        assert app.fetchMovieCollectionLast5Years() is not None


if __name__ == "__main__":
    unittest.main()