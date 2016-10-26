from twilio.rest import TwilioRestClient
from two1.bitserv.flask import Payment
from flask import Flask
from flask import request
import dotenv
import os
import json
import yaml
from twilio.rest.exceptions import TwilioRestException
from twilio.rest.lookups import TwilioLookupsClient
from two1.wallet import Two1Wallet

dotenv_file = ".env"
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

client = TwilioRestClient(account=os.environ.get('TWILIO_ACCOUNT'),
                          token=os.environ.get('TWILIO_AUTH_TOKEN'))

validationclient = TwilioLookupsClient(account=os.environ.get('TWILIO_ACCOUNT'),
                                       token=os.environ.get('TWILIO_AUTH_TOKEN'))

app = Flask(__name__)

TWO1_WALLET_MNEMONIC = os.environ.get("TWO1_WALLET_MNEMONIC")
TWO1_USERNAME = os.environ.get("TWO1_USERNAME")
wallet = Two1Wallet.import_from_mnemonic(mnemonic=TWO1_WALLET_MNEMONIC)

payment = Payment(app, wallet, username=TWO1_USERNAME)


@app.route('/buy', methods=["POST"])
def start():
    to = ""
    post_data = request.get_json()
    if(post_data is None):
        return "You need to provide post data", 500
    try:
        response = validationclient.phone_numbers.get(post_data['phone'])
        to = response.phone_number
    except TwilioRestException as e:
        data = {"error": "number provided was invalid"}
        json_data = json.dumps(data)
        return json_data, 500
    message = post_data['text']
    available_numbers = client.phone_numbers.list()
    if len(available_numbers) < 1:
        return "This endpoint is down right now. Please try again later", 500
    return buy(to, message, available_numbers)


@payment.required(2500)
def buy(to, message, available_numbers):
    from_number = available_numbers[0].phone_number
    client.messages.create(from_=from_number,
                           to=to,
                           body=message)
    data = {"to": to, "from": from_number, "message": message}
    json_data = json.dumps(data)
    return json_data


@app.route("/manifest", methods=["GET"])
def manifest():
    with open('manifest.yaml', 'r') as f:
        manifest = yaml.load(f)
    return json.dumps(manifest)

if __name__ == '__main__':
    app.run()
