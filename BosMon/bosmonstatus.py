#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import socket
import requests
import json
from datetime import datetime as dt

class ConnectAPI:

    def __init__(self):
        token = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'apitoken'),'r').read().strip()
        self.headers = {
            'authorization': f'bearer {token}',
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        self.body = None
        self.url = None

    def set_status(self, radio, status, position=None):
        self.url = f"https://connectapi.feuersoftware.com/interfaces/public/vehicle/{radio}/status"
        self.body = {
            'status': status
        }
        self._send()


    def _send(self):
        r = requests.post(self.url, data=json.dumps(self.body), headers=self.headers)
        if r.status_code != 200:
            print(f"Fehler beim senden des Alarms {r.status_code}, \"{r.text}\"")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Fehler, Falsche Anzahl an Argumenten!")
    api = ConnectAPI()
    api.set_status(sys.argv[1], sys.argv[2])
    
