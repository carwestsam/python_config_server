import unittest
import os
import ujson as ujson
from starlette.testclient import TestClient

conf_path = os.environ['CONFIG_URI'] = 'file://' + os.getcwd() + '/test_configs/sample_config/'


class TestLoadConfiguration(unittest.TestCase):
    def test_initial_config_path(self):
        from main import app
        client = TestClient(app)
        data = ujson.loads(client.request('GET', '/config/config.json').content)
        self.assertEqual(data['version'], '20190329')

    def test_should_load_from_config_file_and_create_service_route(self):
        from main import app
        client = TestClient(app)
        response = client.request('GET', '/config/account-service/20190329/development')
        self.assertEqual(response.status_code, 200)
        data = ujson.loads(response.content)
        self.assertEqual(data['config']['name'], 'account_service_app')
        response = client.request('GET', '/config/account-service/20181002/development')
        self.assertEqual(response.status_code, 200)

    def test_should_have_latest_protocal_for_every_service(self):
        from main import app
        client = TestClient(app)
        response = client.request('GET', '/config/account-service/latest/development')
        self.assertEqual(response.status_code, 200)
        data = ujson.loads(response.content)
        self.assertEqual(data['version'], '20190329')
        self.assertEqual(data['config']['name'], 'account_service_app')
