import unittest
import os
import ujson as ujson
from starlette.testclient import TestClient


class TestLoadConfiguration(unittest.TestCase):
    def test_initial_config_path(self):
        conf_path = os.environ['CONFIG_URI'] = 'file://' + os.getcwd() + '/../sample_config/'
        print(conf_path)
        from main import app
        client = TestClient(app)
        data = ujson.loads(client.request('GET', '/config/config.json').content)
        self.assertEqual(data['version'], '20190329')
