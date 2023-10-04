import sys
from django.conf import settings
import requests

# https://api.flutterwave.com/v3/transactions/:id/verify

class FlutterWave:
    FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY
    base_url = 'https://api.flutterwave.com/v3/'
    

    def verify_payment(self, ref, *args, **kwargs):
        # path = f'/transactions/:{id}/verify'
        path = f'/transactions/verify_by_reference'

        headers = {
            "Authorization": f"Bearer {f'{self.FLUTTERWAVE_SECRET_KEY}'}",
            "Content-Type": 'application/json',
        }
        url = self.base_url + path
        response = requests.get(url, headers=headers, params={'tx_ref': ref})

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        response_data = response.json()
        return response_data['status'], response_data['message']

