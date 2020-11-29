
import requests
import csv
import hashlib
import json

from channelhelper.frequency import (
    Repeater,
    FMConfig,
    DStarConfig,
    YSFConfig,
    DMRConfig,
)


class RBPuller(object):
    """
    Pulls repeater information from Repeaterbook
    """

    NEAR_URL = 'https://www.repeaterbook.com/repeaters/downloads/RT/app_direct2.php'
    STATE_URL = 'https://www.repeaterbook.com/api/export.php'


    def __init__(self):
        self.near_repeaters = {}
        self.near_repeater_states = set()
        self.state_repeaters = {}


    def get_near_repeaters(self):
        repeaters = []
        for repeater_hash, near_repeater in self.near_repeaters.items():
            repeater_data = {}
            repeater_data.update(near_repeater)
            repeater_data.update(self.state_repeaters[repeater_hash])

            repeaters.append(self._get_repeater_object(repeater_data))

        return repeaters


    def load_near_repeaters(self, location, range):
        near_params = {
            'lat': location['lat'],
            'long': location['long'],
            'band[]': [
                14,
                22,
                44,
            ],
            'radius': range,
            'Dunit': 'm',
        }
        api_result = requests.get(url=self.NEAR_URL,params=near_params)

        csv_content = api_result.text.splitlines()
        if csv_content[1] == "There were no repeaters found.":
            return

        csv_reader = csv.DictReader(csv_content, delimiter='|', quotechar='"')
        for repeater in csv_reader:
            repeater_hash = self._get_repeater_hash(
                callsign = repeater['Name'],
                uplink_freq = repeater['Transmit Frequency'],
                downlink_freq = repeater['Receive Frequency'],
                state = repeater['State'],
            )
            self.near_repeaters[repeater_hash] = repeater
            self.near_repeater_states.add(repeater['State'])

        self.load_state_repeaters(self.near_repeater_states)


    def load_state_repeaters(self, states=[]):
        state_params = {
            'country': 'United States',
            'state': '',
        }
        for state in states:
            state_params['state'] = state
            api_result = requests.get(url=self.STATE_URL,params=state_params)

            json_data = json.loads(api_result.text.replace('\t',''))

            for repeater in json_data['results'][:-1]:
                repeater_hash = self._get_repeater_hash(
                    callsign = repeater['Callsign'],
                    uplink_freq = repeater['Input Freq'],
                    downlink_freq = repeater['Frequency'],
                    state = repeater['State'],
                )
                self.state_repeaters[repeater_hash] = repeater


    def _get_repeater_object(self, repeater_data):
        if 'Lat' in repeater_data:
            position = {
                'lat': repeater_data['Lat'],
                'long': repeater_data['Long'],
            }
        else:
            position = None

        configs = []

        if repeater_data['FM Analog'] == "Yes":
            fmconfig = FMConfig()
            if repeater_data['PL'] not in ["","CSQ"]:
                if repeater_data['PL'][0] == "D":
                    fmconfig.dcs_output = int(repeater_data['PL'][1:])
                else:
                    fmconfig.ctcss_output = float(repeater_data['PL'])
            if repeater_data['TSQ'] not in ["","CSQ"]:
                if repeater_data['TSQ'][0] == "D":
                    fmconfig.dcs_input = int(repeater_data['TSQ'][1:])
                else:
                    fmconfig.ctcss_input = float(repeater_data['TSQ'])
            configs.append(fmconfig)

        repeater = Repeater(
            names=[],
            configs=configs,
            downlink_freq=repeater_data['Frequency'],
            uplink_freq=repeater_data['Input Freq'],
            comment=repeater_data['Landmark'],
            callsign=repeater_data['Callsign'],
            position=position,
            municipality=repeater_data['Nearest City'],
            county=repeater_data['County'],
            state=repeater_data['State'],
            country=repeater_data['Country'],
        )

        return repeater


    def _get_repeater_hash(self, callsign, uplink_freq, downlink_freq, state):
        md5 = hashlib.md5()
        md5.update(callsign.encode())
        md5.update(uplink_freq.encode())
        md5.update(downlink_freq.encode())
        md5.update(state.encode())
        return md5.hexdigest()
