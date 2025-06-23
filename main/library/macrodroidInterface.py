import os
import requests
import json
from main.core.config import settings


class MacrodroidBase:

    def __init__(self, macrodroid_url: str) -> None:
        self.macrodroid_url = macrodroid_url

    def send(self,  mobile_number: str, message: str) -> dict:
        url = f"{self.macrodroid_url}?mobilenumber={mobile_number}&message={message}"
        r = requests.get(url=url)
        print("url ", url)
        print("r ", r)
        # Print status code
        print("Status Code:", r.status_code)

        # Print response body as text
        print("Response Text:", r.text)

        # Print response body as JSON (if applicable)
        try:
            print("Response JSON:", r.json())
        except ValueError:
            print("Response is not JSON.")
        if r.ok:
            print(f"{r.text}")
        else:
            print(f"ERROR {r.text}")

        return r.text

class MacrodroidInterface():

    def __init__(self):
        self.macrodroid_url = settings.MACRODROID_URL
        self.client = MacrodroidBase(self.macrodroid_url)

macrodroid_interface = MacrodroidInterface()
