import unittest
import os
import json
from vscodenv import extensions_json

class TestExtensionsJson(unittest.TestCase):

    def setUp(self):
        self.not_exist_json_path = "not_exist_extensions.json"
        self.json_path = "extensions.json"
        self.json_key = "required"
        self.json_values = ['extension-1', 'extension-2']
        json_content = '{"recommendations":["extension-0"], "%s":["%s", "%s"]}' % (self.json_key, self.json_values[0], self.json_values[1])
        with open(self.json_path, "w") as json_file:
            json_file.write(json_content)

        self.malformed_json_path = "malformed_extensions.json"
        malformed_json_content = '{"%s:"%s", "%s"]}' % (self.json_key, self.json_values[0], self.json_values[1])
        with open(self.malformed_json_path, "w") as json_file:
            json_file.write(malformed_json_content)

    def test_parse_json_should_return_values(self):
        ret = extensions_json._parse_json(self.json_path, self.json_key)
        self.assertCountEqual(ret, self.json_values)

    def test_parse_json_should_return_empty_if_malformed(self):
        ret = extensions_json._parse_json(self.malformed_json_path, self.json_key)
        self.assertEqual(ret, [])

    def test_parse_json_should_return_empty_if_file_not_exists(self):
        json_path = "path_does_not_exist"
        key = "required"
        ret = extensions_json._parse_json(json_path, key)
        self.assertEqual(ret, [])

    def test_parse_json_should_return_empty_if_key_not_exists(self):
        key = "key_not_exist"
        ret = extensions_json._parse_json(self.json_path, key)
        self.assertEqual(ret, [])

    def test_extend_list_json_should_extend_json_values(self):
        values = ['extension-1', 'extension-3', 'extension-4']
        result = self.json_values[:]
        for value in values:
            if value not in result:
                result.append(value)

        extensions_json._extend_list_json(self.json_path, self.json_key, values)

        with open(self.json_path) as file_json:
            data = json.load(file_json)
            json_values = data[self.json_key]

        self.assertCountEqual(json_values, result)

    def test_extend_list_json_should_create_new_file_if_not_exists(self):
        values = ['extension-1', 'extension-3', 'extension-4']
        extensions_json._extend_list_json(self.not_exist_json_path, self.json_key, values)

        with open(self.not_exist_json_path) as file_json:
            data = json.load(file_json)
            json_values = data[self.json_key]

        self.assertCountEqual(json_values, values)

    def tearDown(self):
        try:
            os.remove(self.json_path)
            os.remove(self.malformed_json_path)
            os.remove(self.not_exist_json_path)
        except IOError:
            pass

if __name__ == '__main__':
    unittest.main()