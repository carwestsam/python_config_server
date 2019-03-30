import unittest
import asyncio

import ujson as ujson
from starlette.testclient import TestClient

from main import app

class TestLoadConfiguration(unittest.TestCase):
    def test_case(self):
        client = TestClient(app)
        data = ujson.loads(client.request('GET', '/config/config.json').content)
        self.assertEqual(data['foo'], 'bar')
