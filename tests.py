import os
import unittest
import sms
from unittest import mock
import dotenv
import json

# Create your tests here.


class SmsTestCase(unittest.TestCase):
    testNumber = os.environ.get("TEST_PHONE_NUMBER")

    def setUp(self):
        self.app = sms.app.test_client()

    def testStartSuccess(self):
        response = self.post("/buy", {"phone": self.testNumber,
                                      "text": "This is a successful test"})
        self.assertEqual(response.status_code, 402)

    def testStartFail(self):
        response = self.post("/buy", {"phone": "122122",
                                      "text": "This is a successful test"})
        error = {"error": "number provided was invalid"}
        self.assertEqual(response.data.decode("UTF-8"), json.dumps(error))

    @mock.patch('two1.bitserv.flask.decorator.Payment.contains_payment',
                return_value=True)
    def testBuySuccess(self, *args):
        response = self.post("/buy", {"phone": self.testNumber,
                                      "text": "This is a successful test"})
        self.assertEqual(response.status_code, 200)

    def post(self, url, data):
        return self.app.post(url,
                             data=json.dumps(data),
                             content_type='application/json')

if __name__ == '__main__':
    dotenv_file = ".env"
    if os.path.isfile(dotenv_file):
        dotenv.load_dotenv(dotenv_file)
    unittest.main()
