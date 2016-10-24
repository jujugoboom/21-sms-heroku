from twilio.rest import TwilioRestClient
from two1.bitserv.django import payment
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import os
import phonenumbers
import json
import yaml
from two1sms import settings
from twilio.rest.exceptions import TwilioRestException
from twilio.rest.lookups import TwilioLookupsClient

# Create your views here.

client = TwilioRestClient(account=os.environ.get('TWILIO_ACCOUNT'),
                          token=os.environ.get('TWILIO_AUTH_TOKEN'))

validationclient = TwilioLookupsClient(account=os.environ.get('TWILIO_ACCOUNT'),
                                       token=os.environ.get('TWILIO_AUTH_TOKEN'))


@api_view(['POST'])
def start(request):
    to = ""
    try:
        response = validationclient.phone_numbers.get(request.data['phone'])
        to = response.phone_number
    except TwilioRestException as e:
        data = {"error": "number provided was invalid"}
        json_data = json.dumps(data)
        return HttpResponse(json_data, status=500)
    message = message = request.data['text']
    available_numbers = client.phone_numbers.list()
    if len(available_numbers) < 1:
        return HttpResponse("This endpoint is down right now. Please try again later", status=500)
    return buy(request, to, message, available_numbers)


@api_view(['POST'])
@payment.required(2500)
def buy(request, to, message, available_numbers):
    from_number = available_numbers[0].phone_number
    client.messages.create(from_=from_number,
                           to=to,
                           body=message)
    data = {"to": to, "from": from_number, "message": message}
    json_data = json.dumps(data)
    return HttpResponse(json_data, status=200)


def convert_to_e164(raw_phone):
    if not raw_phone:
        return

    if raw_phone[0] == '+':
        # Phone number may already be in E.164 format.
        parse_type = None
    else:
        # If no country code information present, assume it's a US number
        parse_type = "US"

    phone_representation = phonenumbers.parse(raw_phone, parse_type)
    return phonenumbers.format_number(phone_representation,
                                      phonenumbers.PhoneNumberFormat.E164)


@api_view(['GET'])
def manifest(request):
    with open(settings.BASE_DIR + "/two1sms/manifest.yaml", 'r') as infile:
        return JsonResponse(yaml.load(infile), status=200)
