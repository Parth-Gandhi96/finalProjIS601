import unittest
import app


class HomeViewTest(unittest.TestCase):
    temp_app = None

    @classmethod
    def setUpClass(cls):
        cls.temp_app = app()

    def setUp(self):
        pass


if __name__ == "__main__":
    unittest.main()