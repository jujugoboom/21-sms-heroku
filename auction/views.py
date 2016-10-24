import threading
from two1.bitserv.django import payment
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
import ast

# Create your views here.
lock = threading.Lock()
startprice = 2000
increment = 100
currentwinner = []


@api_view(['POST'])
def start(request):
    winner = iscurrentwinner(request)
    if str(winner) == "error":
        data = {"error":
                "you must provide your payout address in the request data"}
        json_data = json.dumps(data)
        return HttpResponse(json_data, status=500)
    if winner:
        data = {"error": "you are already the highest bidder"}
        json_data = json.dumps(data)
        return HttpResponse(json_data, status=500)
    with lock:
        return buy(request, request.data)


def get_current_price(request):
    if len(currentwinner) < 1:
        return startprice
    return currentwinner[1] + increment


@api_view(['POST'])
@payment.required(get_current_price)
def buy(request, requestdata):
    buyer_info = ast.literal_eval(request.META.get("HTTP_BITCOIN_TRANSFER"))
    address = str(requestdata['address'])
    amount = int(buyer_info["amount"])
    if len(currentwinner) < 1:
        currentwinner.insert(0, address)
        currentwinner.insert(1, amount)
    else:
        currentwinner[0] = address
        currentwinner[1] = amount
    data = {"bid":
            "you bid {} and currently have the highest bid".format(amount)}
    json_data = json.dumps(data)
    return HttpResponse(json_data, status=200)


@api_view(['GET'])
def getcurrentprice(request):
    price = startprice
    if len(currentwinner) > 0:
        price = currentwinner[1] + increment
    data = {"price": price}
    json_data = json.dumps(data)
    return HttpResponse(json_data, status=200)


def iscurrentwinner(request):
    if len(request.data) < 1:
        return "error"
    if len(currentwinner) < 1:
        return False
    return request.data["address"] == currentwinner[0]
