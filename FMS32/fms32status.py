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

            
class FMS32Pro:

    def __init__(self, ip='127.0.0.1', port=9300):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        self.connected = False
        self.api = ConnectAPI()
        
    def connect(self):
        self.socket.connect((self.ip, self.port))
        self.connected = True
    
    def disconnect(self):
        self.socket.close()
        
    def read(self):
        while True:
            try:
                data = self.socket.recv(100)
                if data:
                    self.parse(data)
            except KeyboardInterrupt:
                self.disconnect()
                return
            except socket.timeout:
                pass
                
    def parse(self, data):
        data = data.decode("utf-8")
        if data.startswith("FMSTlg"):
            data = data.strip().split()
            if len(data) != 15:
                return
            self.api.set_status(data[1], data[6])


if __name__ == "__main__":
    fms = FMS32Pro()
    fms.connect()
    fms.read()
