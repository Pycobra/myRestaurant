import sys
from django.conf import settings
import requests

# https://api.flutterwave.com/v3/transactions/:id/verify

class FlutterWave:
    FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY
    base_url = 'https://api.flutterwave.com/v3/'
    

    def verify_payment(self, id, *args, **kwargs):
        path = f'/transactions/:{id}/verify'

        headers = {
            "Authorization": f"Bearer {f'{FLUTTERWAVE_SECRET_KEY}'}",
            "Content-Type": 'application/json',
        }
        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        response_data = response.json()
        return response_data['status'], response_data['message']


# const Flutterwave = require('flutterwave-node-v3');
# const flw = new Flutterwave("public key", "secret key");
# const payload = {"id": "288200108"};
# const response = await flw.Transaction.verify(payload)

# {
#   "status": "success",
#   "message": "Transaction fetched successfully",
#   "data": {
#     "id": 288200108,
#     "tx_ref": "LiveCardTest",
#     "flw_ref": "YemiDesola/FLW275407301",
#     "device_fingerprint": "N/A",
#     "amount": 100,
#     "currency": "NGN",
#     "charged_amount": 100,
#     "app_fee": 1.4,
#     "merchant_fee": 0,
#     "processor_response": "Approved by Financial Institution",
#     "auth_model": "PIN",
#     "ip": "::ffff:10.5.179.3",
#     "narration": "CARD Transaction ",
#     "status": "successful",
#     "payment_type": "card",
#     "created_at": "2020-07-15T14:31:16.000Z",
#     "account_id": 17321,
#     "card": {
#       "first_6digits": "232343",
#       "last_4digits": "4567",
#       "issuer": "FIRST CITY MONUMENT BANK PLC",
#       "country": "NIGERIA NG",
#       "type": "VERVE",
#       "token": "flw-t1nf-4676a40c7ddf5f12scr432aa12d471973-k3n",
#       "expiry": "02/23"
#     },
#     "meta": null,
#     "amount_settled": 98.6,
#     "customer": {
#       "id": 216519823,
#       "name": "Yemi Desola",
#       "phone_number": "N/A",
#       "email": "user@gmail.com",
#       "created_at": "2020-07-15T14:31:15.000Z"
#     }
#   }
# }


from six import text_type
import secrets


import uuid
import re
import timeit

from decimal import Decimal
import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync