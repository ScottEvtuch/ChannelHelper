
from channelhelper import(
    Frequency,
    FMConfig,
    DStarConfig,
    YSFConfig,
    DMRConfig,
)

class Channel(Frequency):
    """
    A memory channel for a radio
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
        super(Channel, self).__init__(
            names,
            configs,
            downlink_freq,
            uplink_freq,
        )
        self.group = group
        self.comment = comment


class ChannelList(object):
    """
    A list of channels for a radio
    """

    COMPATIBLE_CONFIGS = (
        FMConfig,
        DStarConfig,
        YSFConfig,
        DMRConfig,
    )
    CHANNEL_CLASS = Channel

    def __init__(self):
        self.channels = {}
        self.groups = ()

    def add_channels(
        self,
        channel_list,
    ):
        if not isinstance(channel_list,ChannelList):
            raise ValueError("add_channels requires a ChannelList object")

        for key, input_channel in channel_list.channels.items():
            self.channels[key] = self.CHANNEL_CLASS(
                names=input_channel.names,
                configs=input_channel.configs,
                downlink_freq=input_channel.downlink_freq,
                uplink_freq=input_channel.uplink_freq,
                comment=input_channel.comment,
            )

    def add_frequencies(
        self,
        frequencies,
        i=1,
    ):
        if not isinstance(frequencies,list):
            frequencies = [frequencies]

        for frequency in frequencies:
            configs = []
            for config in frequency.configs:
                if isinstance(config,self.COMPATIBLE_CONFIGS):
                    configs.append(config)
            for config in configs:
                self.channels[i] = self.CHANNEL_CLASS(
                    names=frequency.names,
                    configs=[config],
                    downlink_freq=frequency.downlink_freq,
                    uplink_freq=frequency.uplink_freq,
                    comment=frequency.comment,
                )
            i += 1

    def add_repeaters(
        self,
        repeaters,
        i=1,
    ):
        self.add_frequencies(repeaters, i)
