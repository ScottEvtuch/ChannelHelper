
import csv

from channelhelper import(
    Channel,
    ChannelList,
    Frequency,
    FMConfig,
    DStarConfig,
)


class KenwoodTHD74Channel(Channel):
    """
    A memory channel for the Kenwood TH-D74 RT Systems software
    """
    def __init__(
        self,
        names,
        configs,
        downlink_freq,
        uplink_freq,
        group="",
        comment="",
    ):
        super(KenwoodTHD74Channel, self).__init__(
            names,
            configs,
            downlink_freq,
            uplink_freq,
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


class KenwoodTHD74ChannelList(ChannelList):
    """
    A list of Channels for a THD74 radio
    """

    COMPATIBLE_CONFIGS = (
        FMConfig,
        DStarConfig,
    )
    CHANNEL_CLASS = KenwoodTHD74Channel

