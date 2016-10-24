from django.test import TestCase
from sms import views
from django.test.client import RequestFactory
import unittest
from twilio.rest import TwilioRestClient
import os
import datetime
import time

# Create your tests here.


class SmsTestCase(TestCase):
    rf = RequestFactory()
    testNumber = os.environ.get("TEST_PHONE_NUMBER")

    def testStartSuccess(self):
        request = self.rf.post("/buy/", {"phone": self.testNumber, "text": "This is a successful test"})
        response = views.start(request)
        self.assertEqual(response.status_code, 402)

    def testStartFail(self):
        request = self.rf.post("/buy/", {"phone": "122122", "text": "This is a successful test"})
        response = views.start(request)
        self.assertEqual(response.status_code, 500)

    def testNumberConvertNone(self):
        result = views.convert_to_e164(None)
        self.assertIsNone(result)

    def testNumberConvertE16(self):
        result = views.convert_to_e164("+12345678900")
        self.assertEqual(result, "+12345678900")

    def testNumberConvertUS(self):
        result = views.convert_to_e164("2345678900")
        self.assertEqual(result, "+12345678900")

    @unittest.mock.patch('two1.bitserv.django.decorator.Payment.contains_payment', return_value=True)
    def testBuySuccess(self, *args):
        request = self.rf.post("/buy/", {"phone": self.testNumber, "text": "This is a successful test"})
        client = TwilioRestClient(account=os.environ.get('TWILIO_ACCOUNT'),
                                  token=os.environ.get('TWILIO_AUTH_TOKEN'))
        available_numbers = client.phone_numbers.list()
        if len(available_numbers) < 1:
            self.fail('No numbers in twilio')
        startTime = datetime.datetime.now()
        response = views.buy(request, self.testNumber, "Test Successful", available_numbers)
        self.assertEqual(response.status_code, 200)
