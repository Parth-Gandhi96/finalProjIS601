import unittest
import webapp2
import app


class HomeViewTest(unittest.TestCase):

    def test_test(self):
        assert app.test() == "Works!"


if __name__ == "__main__":
    unittest.main()