from unittest import TestCase, mock
from drone_kubernetes_apply.drone_kubernetes_apply_runner import *
import os
import requests_mock


test_files_location = os.getenv("TEST_FILES_LOCATION", "test_files")


class BaseTests(TestCase):

    def test_create_output_file(self):
        create_output_file("it_writes!", "/tmp/test_output")
        f = open("/tmp/test_output", "r")
        reply = f.read()
        f.close()
        self.assertEqual(reply, "it_writes!")

    def test_file_reader_read_file(self):
        reply = read_file(test_files_location + "/test_read_file")
        self.assertEqual(reply, "it_reads!")

    def test_file_reader_read_file_raise_error_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_file(test_files_location + "/non_existing_file")

    def test_read_all_envvars_to_dict_force_uppercase_false(self):
        test_envvars = {"TEST_ENV": "123", "test_env_lowercase": "456"}
        with mock.patch.dict(os.environ, test_envvars):
            reply = read_all_envvars_to_dict()
            self.assertEqual(type(reply), dict)
            self.assertEqual(reply["TEST_ENV"], "123")
            self.assertEqual(reply["test_env_lowercase"], "456")

    def test_populate_template_string_works_simple(self):
        test_template_values_dict = {"test": "test that works"}
        expected_reply = "this is a test that works"
        reply = populate_template_string("this is a $test", test_template_values_dict)
        self.assertEqual(reply, expected_reply)

    def test_populate_template_string_works_complex(self):
        test_template_values_dict = {"test1": "test that", "test2": "works"}
        expected_reply = "this is a $Complex$123 test that works"
        reply = populate_template_string("this is a $Complex$123 $test1 $test2", test_template_values_dict)
        self.assertEqual(reply, expected_reply)

    def test_populate_template_string_no_template_values(self):
        test_template_values_dict = None
        expected_reply = "this is a $test"
        reply = populate_template_string("this is a $test", test_template_values_dict)
        self.assertEqual(reply, expected_reply)

    def test_populate_template_string_no_template_values_no_template_placement(self):
        test_template_values_dict = None
        expected_reply = "this is a test"
        reply = populate_template_string("this is a test", test_template_values_dict)
        self.assertEqual(reply, expected_reply)

    # TODO update test to make sure it creates the modified file
    def test_main_init(self):
        test_envvars = {"PLUGIN_METRONOME_JOB_FILE": test_files_location + "/metronome.json"}
        with mock.patch.dict(os.environ, test_envvars):
            with requests_mock.Mocker() as request_mocker:
                request_mocker.head('http://metronome.mesos:9000/v1/jobs/prod.example.app', status_code=200)
                request_mocker.put('http://metronome.mesos:9000/v0/scheduled-jobs/prod.example.app', status_code=200,
                                   text='{"test_json_key": "test_json_value"}')
                init()
