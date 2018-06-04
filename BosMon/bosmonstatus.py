#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import re
import socketserver
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




class BosMonTCPHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        data = self.request.recv(1024).strip().decode("utf-8")
        print(data)
        address = re.search("<address>(?P<address>.*)<\/address>", data)
        if address:
            address = address.groupdict().get("address", None)
        type = re.search("<type>(?P<type>.*)<\/type>", data)
        if type:
            type = type.groupdict().get("type", None)
        timestamp = re.search("<timestamp>(?P<timestamp>.*)<\/timestamp>", data)
        if timestamp:
            timestamp = timestamp.groupdict().get("timestamp", None)
        flags = re.search("<flags>(?P<flags>.*)<\/flags>", data)
        if flags:
            flags = flags.groupdict().get("flags", None)
        status = re.search("<status>(?P<status>.*)<\/status>", data)
        if status:
            status = status.groupdict().get("status", None)
        direction = re.search("<direction>(?P<direction>.*)<\/direction>", data)
        if direction:
            direction = direction.groupdict().get("direction", None)
        shortdescription = re.search("<shortdescription>(?P<shortdescription>.*)<\/shortdescription>", data)
        if shortdescription:
            shortdescription = shortdescription.groupdict().get("shortdescription", None)
        longdescription = re.search("<longdescription>(?P<longdescription>.*)<\/longdescription>", data)
        if longdescription:
            longdescription = longdescription.groupdict().get("longdescription", None)
        api = ConnectAPI()
        api.set_status(address, status)
        
        

if __name__ == "__main__":
    server = socketserver.TCPServer(("127.0.0.1", 5555), BosMonTCPHandler)
    server.serve_forever()
