
from channelhelper import(
    Frequency,
    FMConfig,
)

class Channel(Frequency):
    """
    A memory channel for a radio
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
        super(Channel, self).__init__(
            names,
            downlink_freq,
            uplink_freq,
            configs,
        )
        self.group = group
        self.comment = comment


class ChannelList(object):
    """
    A list of channels for a radio
    """

    COMPATIBLE_CONFIGS = (
        FMConfig,
    )
    CHANNEL_CLASS = Channel

    def __init__(self):
        self.channels = {}
        self.groups = ()

    def add_repeaters(
        self,
        repeaters,
        i=1,
    ):
        if not isinstance(repeaters,list):
            repeaters = [repeaters]

        for repeater in repeaters:
            configs = []
            for config in repeater.configs:
                if isinstance(config,self.COMPATIBLE_CONFIGS):
                    configs.append(config)
            for config in configs:
                self.channels[i] = self.CHANNEL_CLASS(
                    names=repeater.names,
                    downlink_freq=repeater.downlink_freq,
                    uplink_freq=repeater.uplink_freq,
                    configs=[config],
                )
            i += 1

