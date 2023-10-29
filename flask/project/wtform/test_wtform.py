import unittest

from flask import json

from .app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index_get(self):
        resp = self.app.get('/')

        assert resp.status_code == 200

    def test_index_post_400(self):
        resp = self.app.post('/')

        assert resp.status_code == 400
        assert b'<div class="error">Number a required</div>' in resp.data
        assert b'<div class="error">Number b required</div>' in resp.data
        assert b'<div class="error">Not a valid choice</div>' in resp.data

    def test_index_post(self):
        resp = self.app.post('/', data={'a': 1, 'b': 2, 'op': '+'})

        assert resp.status_code == 200
        assert b'<div class="field"><input value="3.0"></div>' in resp.data

    def test_ajax_post_400(self):
        resp = self.app.post('/ajax')
        assert resp.status_code == 400

        json_ = json.dumps(json.loads(resp.data), sort_keys=True, indent=2)
        assert json_ == '''{
  "errors": {
    "a": [
      "Number a required"
    ],
    "b": [
      "Number b required"
    ],
    "op": [
      "Not a valid choice",
      "Operator must on of '+. -, *, /'"
    ]
  }
}'''

    def test_ajax_post(self):
        resp = self.app.post('/ajax',
                             headers={'Content-Type': 'application/json'},
                             data=json.dumps({'a': 1, 'b': 2, 'op': '+'}))
        assert resp.status_code == 200

        json_ = json.loads(resp.data)
        assert json_['ans'] == 3.0
