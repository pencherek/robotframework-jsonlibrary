# -*- coding: utf-8 -*-

__author__ = 'Traitanit Huangsri'
__email__ = 'traitanit.hua@ascendcorp.com'

from JSONLibrary import JSONLibrary
import unittest
import os


class JSONLibraryTest(unittest.TestCase):
    test = JSONLibrary()
    json = None

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.json = self.test.load_json_from_file(os.path.join(dir_path, 'json', 'example.json'))

    def test_add_dict_element_to_json(self):
        json_path = '$..address'
        data_to_add = {'latitude': '13.1234', 'longitude': '130.1234'}
        json_object = self.test.add_object_to_json(self.json, json_path, data_to_add)
        self.assertDictContainsSubset(data_to_add, json_object['address'])

    def test_add_new_object_to_root(self):
        json_path = '$.country'
        data_to_add = 'Thailand'
        json_object = self.test.add_object_to_json(self.json, json_path, data_to_add)
        self.assertEqual(json_object['country'], 'Thailand')

    def test_add_list_element_to_json(self):
        json_path = '$..favoriteColor'
        data_to_add = 'green'
        json_object = self.test.add_object_to_json(self.json, json_path, data_to_add)
        self.assertIn(data_to_add, json_object['favoriteColor'])

    def test_get_value_from_json_path(self):
        json_path = '$..number'
        values = self.test.get_value_from_json(self.json, json_path)
        expected_result = ['0123-4567-8888', '0123-4567-8910', '0123-4567-8999']
        self.assertListEqual(values, expected_result)

    def test_get_none_from_json_path(self):
        json_path = '$..occupation'
        values = self.test.get_value_from_json(self.json, json_path)
        self.assertIsNone(*values)

    def test_get_empty_list_from_json_path(self):
        json_path = '$..siblings'
        values = self.test.get_value_from_json(self.json, json_path)
        expected_result = []
        self.assertListEqual(*values, expected_result)

    def test_get_value_from_json_path_not_found(self):
        json_path = '$..notfound'
        self.assertRaises(AssertionError, self.test.get_value_from_json, self.json, json_path, fail_on_empty=True)

        # backward-compatilibity, fail_on_empty is False by default
        values = self.test.get_value_from_json(self.json, json_path)
        expected_result = []
        self.assertListEqual(values, expected_result)

    def test_has_value_from_json_path_passed(self):
        json_path = '$..isMarried'
        self.test.should_have_value_in_json(self.json, json_path)

    def test_has_value_from_json_path_failed(self):
        json_path = '$..hasSiblings'
        self.assertRaises(AssertionError, self.test.should_have_value_in_json, self.json, json_path)

    def test_has_no_value_from_json_path_passed(self):
        json_path = '$..hasSiblings'
        self.test.should_not_have_value_in_json(self.json, json_path)

    def test_has_no_value_from_json_path_failed(self):
        json_path = '$..isMarried'
        self.assertRaises(AssertionError, self.test.should_not_have_value_in_json, self.json, json_path)

    def test_update_value_to_json(self):
        json_path = '$..address.streetAddress'
        value_to_update = 'Ratchadapisek Road'
        json_object = self.test.update_value_to_json(self.json, json_path, value_to_update)
        self.assertEqual(value_to_update, json_object['address']['streetAddress'])

    def test_update_value_to_json_as_index(self):
        json_path = '$..phoneNumbers[0].type'
        value_to_update = 'mobile'
        json_object = self.test.update_value_to_json(self.json, json_path, value_to_update)
        self.assertEqual(value_to_update, json_object['phoneNumbers'][0]['type'])

    def test_delete_object_from_json(self):
        json_path = '$..isMarried'
        json_object = self.test.delete_object_from_json(self.json, json_path)
        self.assertFalse('isMarried' in json_object)

    def test_delete_array_elements_from_json(self):
        json_path = '$..phoneNumbers[0]'
        json_object = self.test.delete_object_from_json(self.json, json_path)
        self.assertFalse(any(pn['type']=='iPhone' for pn in json_object['phoneNumbers']))

    def test_delete_all_array_elements_from_json(self):
        json_path = '$..phoneNumbers[*]'
        json_object = self.test.delete_object_from_json(self.json, json_path)
        expected_result = []
        self.assertListEqual(expected_result, json_object['phoneNumbers'])

    def test_invalid_syntax_doesnt_crash(self):
        json_path = '$.bankAccounts[?(@.amount>=100)].bank'
        values = self.test.get_value_from_json(self.json, json_path)
        expected_result = ['WesternUnion', 'HSBC']
        self.assertListEqual(values, expected_result)
        
        json_path = "$.bankAccounts[?(@.amount=>100)].bank"
        self.assertRaises(AssertionError, self.test.get_value_from_json, self.json, json_path)

    def test_convert_json_to_string(self):
        json_str = self.test.convert_json_to_string(self.json)
        self.assertTrue(isinstance(json_str, str))

    def test_convert_string_to_json(self):
        json_obj = self.test.convert_string_to_json('{"firstName": "John"}')
        self.assertTrue("firstName" in json_obj)

    def test_dump_json_to_file(self):
        if os.name == 'nt':
            tmp_path = os.getenv('TMP', 'c:\\Temp\\')
        else:
            tmp_path = os.getenv('TMP', '/tmp/')
        file_path = '%ssample.json' % (tmp_path)
        json_file = self.test.dump_json_to_file(file_path, self.json)
        self.assertTrue(os.path.exists(json_file))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()