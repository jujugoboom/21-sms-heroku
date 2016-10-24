from django.test import TestCase
from sms import views
from django.test.client import RequestFactory

# Create your tests here.


class SmsTestCase(TestCase):
    rf = RequestFactory()
    #wallet = settings.WALLET
    #requests = BitTransferRequests(wallet)

    def testStartSuccess(self):
        request = self.rf.post("/buy/", {"phone": "410-349-7954", "text": "This is a successful test"})
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

    '''def testBuy(self):
        request = self.rf.post("/buy/", {"phone": "410-349-7954", "text": "This is a successful test"})
        response = views.buy(request, "+14103497954", "Test Successful")
        print(response._headers)
        for header in response._headers:
            response._headers[header] = response._headers[header][1]
        response.headers = response._headers
        response.url = "http://testserver/payments/channel"
        headers = self.requests.make_402_payment(response=response, max_price=10000)
        newrequest = self.rf.post("/buy/", {"phone": "410-349-7954", "text": "This is a successful test"})
        for key in headers:
            newrequest.META[key] = headers[key]
        print(newrequest.META)
        newresponse = views.buy(newrequest, "+14103497954", "Test Successful")
        print(newresponse.status_code)'''
