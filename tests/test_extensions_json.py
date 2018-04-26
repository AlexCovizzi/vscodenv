import unittest
from .. import extensions_json

class TestExtensionsJson(unittest.TestCase):

    def setUp(self):
        pass

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()