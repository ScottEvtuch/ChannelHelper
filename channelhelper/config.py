
import json

from channelhelper import (
    Frequency,
    FMConfig,
    ChannelList,
)


class JSONConfig(object):
    """
    Pulls configuration from a JSON file
    """

    def __init__(
        self,
        path
    ):
        self.path = path
        self.channels = ChannelList()

        self._load_file()

    def _load_file(self):
        with open(self.path, 'rb') as json_file:
            self.json_data = json.load(json_file)
        self._load_channels()

    def _load_channels(self):
        for channel in self.json_data['channels']:
            channel_number = channel['number']
            input_config = channel['config']
            if input_config['type'] == 'FM':
                config = FMConfig(
                    ctcss_input=input_config.get('ctcss_input'),
                    ctcss_output=input_config.get('ctcss_output'),
                    dcs_input=input_config.get('dcs_input'),
                    dcs_output=input_config.get('dcs_output'),
                    dcs_polarity=input_config.get('dcs_polarity'),
                )
            frequency = Frequency(
                names=channel['names'],
                configs=[config],
                downlink_freq=channel['downlink_freq'],
                uplink_freq=channel.get('uplink_freq'),
            )
            self.channels.add_frequencies(frequency, channel_number)

