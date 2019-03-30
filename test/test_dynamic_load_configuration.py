import shutil
import ujson
import unittest
import os
from os.path import isdir

from starlette.testclient import TestClient

conf_path = 'file://' + os.path.dirname(
    os.path.realpath(__file__)) + '/test_configs/dynamic_config'
# print('config_path', conf_path)


class TestDynamicLoadConfiguration(unittest.TestCase):
    def setUp(self):
        os.environ['CONFIG_URI'] = conf_path

    def test_should_return_not_found_when_config_not_exist(self):
        transfer_conf_path = conf_path.replace('file://', '') + '/transfer-service'
        if isdir(transfer_conf_path):
            shutil.rmtree(transfer_conf_path)

        from main import app
        client = TestClient(app)
        resp = client.request('GET', '/config/transfer-service/20190329/production')
        self.assertEqual(resp.status_code, 200)
        data = ujson.loads(resp.content)
        self.assertTrue('error' in data)

        os.mkdir(transfer_conf_path)
        os.mkdir(transfer_conf_path + '/20190329')
        with open(transfer_conf_path + '/20190329/production.json', 'wb') as infile:
            infile.write('{"name":"transfer_service"}'.encode('utf-8'))

        resp = client.request('GET', '/config/transfer-service/20190329/production')
        self.assertEqual(resp.status_code, 200)
        data = ujson.loads(resp.content)
        self.assertFalse('error' in data)

        if isdir(transfer_conf_path):
            shutil.rmtree(transfer_conf_path)
