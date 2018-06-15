#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import requests
import re
import time
import serial
import json
from datetime import datetime as dt
import coloredlogs, logging

logger = logging.getLogger("ConnectAPI")
logger.propagate = False
coloredlogs.install(level='INFO', fmt='%(asctime)s %(levelname)s [%(name)s] %(message)s', logger=logger)

class ConnectAPI:

    def __init__(self, ric=None, dump=False):
        if not ric or  not os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'token_{}'.format(ric))):
            logger.warning("Unbekannte RIC {}, Fehler beim laden des Tokens".format(ric))
            return
        token = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'token_{}'.format(ric)),'r').read().strip()
        self.headers = {
                'authorization': 'bearer {}'.format(token),
                'accept': 'application/json',
                'content-type': 'application/json',
                }
        self.body = None
        self.url = None
        self.dump = dump

    def einsatz(self, start, keyword, address=None, position=None, facts=None, ric=None, properties=None):
        self.url = "https://connectapi.feuersoftware.com/interfaces/public/operation"
        self.body = {
                'start': start,
                'keyword': keyword
                }
        if address:
            self.body['address'] = address
        if position:
            self.body['position'] =  {'latitude':position[0], 'longitude': position[1]}
        if facts:
            self.body['facts'] = facts
        if ric:
            self.body['ric'] = ric
        if properties:
            self.body['properties'] = properties
        self._send()


    def fahrzeugstatus(self, radio, status, position=None):
        self.url = "https://connectapi.feuersoftware.com/interfaces/public/vehicle/{}/status".format(radio)
        self.body = {
                'status': status
                }
        if position:
            self.body['position'] = {'latitude':position[0], 'longitude': position[1]}
        self._send()


    def _send(self):
        if not self.dump:
            r = requests.post(self.url, data=json.dumps(self.body), headers=self.headers)
            if r.status_code != 200:
                logger.warning("Fehler beim senden des Alarms {r.status_code}, \"{}\"".format(r.text))
            else:
                logger.info("Alarm erfolgreich gesendet!")
        if self.dump:
            print(self.url)
            print(self.headers)
            print(self.body)

def main():
    try:
        # Connect to DME
        s = serial.Serial('/dev/ttyS0', 9600)
        message = []
        while 1:
            for c in s.read():
                message.append(c)
                # Read Bytes of incomming message until \n (0x0A, 10)
                if c == 10:
                    data = bytearray(message).decode().strip()
                    message = []
                    # Filter Values out of the incoming message
                    alarm = re.search(
                            r"(?P<zeit>[^\s]*)\s"
                            "(?P<datum>[^\/]*)\/"
                            "(?P<ric>[^\/]*)\/"
                            "(?P<stichwort>[^\/]*)\/"
                            "(?P<gemeinde>[^\/]*)\/"
                            "(?P<ortsteil>[^\/]*)\/"
                            "(?P<ortslage>[^\/]*)\/"
                            "(?P<strasse>[^\/]*)\/"
                            "(?P<nummer>[^\/]*)\/"
                            "(?P<infos>[^\/]*)\/"
                            "(?P<objekt>[^\/]*)\/"
                            "(?P<sachverhalt>.*)\/#K01;"
                            "N(?P<latmin>\d{2})(?P<latsec>[^E]*)E(?P<lonmin>\d{2})(?P<lonsec>[^\/]*)\/"
                            "(?P<alarmzeit>\d{2}:\d{2})"
                            , data)
                    # If Regex Filter was not successfull due to invalid message format for example, print error and continue to wait for next message
                    if not alarm:
                        logger.warning("Unbekannte Daten erhalten \"{}\"".format(data))
                        continue
                    # Set up API which loads Token according to the passed RIC
                    api = ConnectAPI(alarm.group("ric"))
                    # If the API Setup fails due to non existing Token for the passed RIC, exit
                    if not api:
                        return
                    # Pass alarm values to API and trigger Connect Alarm
                    api.einsatz(
                            alarm.group("zeit"),
                            alarm.group("stichwort"),
                            '{} {}, {}-{}'.format(
                                alarm.group("strasse"), 
                                alarm.group("nummer"), 
                                alarm.group("gemeinde"), 
                                alarm.group("ortsteil")
                            ),
                            (float("{}.{}".format(alarm.group('latmin'), alarm.group('latsec'))), 
                             float("{}.{}".format(alarm.group('lonmin'), alarm.group('lonsec')))
                            ),
                            alarm.group("sachverhalt"),
                            alarm.group("ric"),
                            [{"key":"Infos", "value": alarm.group("infos")},
                                {"key":"Ortslage", "value": alarm.group("ortslage")},
                                {"key":"Objekt", "value": alarm.group("objekt")}
                                ]
                            )

    except (KeyoardInterrupt, SystemExit):
        logger.info("Exit")
    except Exception as e:
        logger.error("Error: {}".format(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
