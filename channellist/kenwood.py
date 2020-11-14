
import csv

from channellist import(
    Frequency,
    FMConfig,
    DStarConfig,
)


class KenwoodTHD74Channel(Frequency):
    """
    A memory channel for the Kenwood TH-D74 RT Systems software
    """
    def __init__(
        self,
        names,
        downlink_freq,
        uplink_freq,
        configs,
        group="",
        comment="",
    ):
        super(KenwoodTHD74Channel, self).__init__(
            names,
            downlink_freq,
            uplink_freq,
            configs,
            group,
            comment,
        )
        if len(self.configs) != 1:
            print("THD74 cannot have channels with more than one mode")
        elif isinstance(self.configs[0],FMConfig):
            self.mode = 'FM'
        elif isinstance(self.configs[0],DStarConfig):
            self.mode = 'DStar'
        else:
            print("THD74 only supports FM and DStar")


class KenwoodTHD74ChannelList(object):
    """
    Stores a list of THD74 Channels
    """
    def __init__(self):
        self.channels = {}

    def convert_repeaters(
        self,
        repeaters,
        i=1,
    ):
        if not isinstance(repeaters,list):
            repeaters = [repeaters]

        for repeater in repeaters:
            configs = []
            for config in repeater.configs:
                if isinstance(config,(FMConfig,DStarConfig)):
                    configs.append(config)
            for config in configs:
                self.channels[i] = KenwoodTHD74Channel(
                    names=repeater.names,
                    downlink_freq=repeater.downlink_freq,
                    uplink_freq=repeater.uplink_freq,
                    configs=[config],
                )
            i += 1

