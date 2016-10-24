from django.test import TestCase
from sms import views
from django.test.client import RequestFactory

# Create your tests here.
class SmsTestCase(TestCase):
    rf = RequestFactory()
    def testStartSuccess():
        request = rf.post("/buy/", "{\"phone\": \"410-349-7954\", \"text\": \"This is a successful test\"}")
        self.assertEqual(request.status_code, 402)
