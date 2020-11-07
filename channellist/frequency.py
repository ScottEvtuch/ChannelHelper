

class Frequency(object):
    """
    An entry that describes a set of configurations that will allow radio communication
    """

    def __init__(
        self,
        names,
        downlink_freq,
        uplink_freq,
        fm_config=None,
        dstar_config=None,
        ysf_config=None,
        dmr_config=None,
        comment="",
    ):
        self.names = sorted(names, key=len, reverse=True)
        self.comment = comment
        self.downlink_freq = downlink_freq
        self.uplink_freq = uplink_freq
        self.fm_config = fm_config
        self.dstar_config = dstar_config
        self.ysf_config = ysf_config
        self.dmr_config = dmr_config

    def name(self, max_length=32):
        for name in self.names:
            if len(name) < max_length:
                return name


class Repeater(Frequency):
    """
    An entry that describes configuration for a specific stationary repeater
    """

    def __init__(
        self,
        names,
        downlink_freq,
        uplink_freq,
        fm_config=None,
        dstar_config=None,
        ysf_config=None,
        dmr_config=None,
        comment="",
        callsign="",
        position={},
        municipality="",
        county="",
        state="",
        country="",
    ):
        super(Repeater, self).__init__(
            names,
            downlink_freq,
            uplink_freq,
            fm_config,
            dstar_config,
            ysf_config,
            dmr_config
        )
        self.callsign = callsign
        self.position = position
        self.municipality = municipality
        self.county = county
        self.state = state
        self.country = country
        self._build_repeater_names()


    def _build_repeater_names(self):
        if '' != self.callsign:
            self.names.append(self.callsign)
        if '' != self.municipality:
            self.names.append("{} {}".format(self.callsign,self.municipality))
            self.names.append("{} {}, {}".format(self.callsign,self.municipality,self.state))
        elif '' != self.county:
            self.names.append("{} {}".format(self.callsign,self.county))
            self.names.append("{} {}, {}".format(self.callsign,self.county,self.state))


class FMConfig(object):
    """
    Configuration parameters for communicating via frequency-modulated voice
    """

    def __init__(
        self,
        ctcss_input=None,
        ctcss_output=None,
        dcs_input=None,
        dcs_output=None,
        dcs_polarity=None,
    ):
        self.ctcss_input = ctcss_input
        self.ctcss_output = ctcss_output

        self.dcs_input = dcs_input
        self.dcs_output = dcs_output
        self.dcs_polarity = dcs_polarity


class DStarConfig(object):
    """
    Configuration parameters for communicating via D-Star
    """

    def __init__(
        self,
        urcall="CQCQCQ",
        rpt1="",
        rpt2="",
        code_number=None,
    ):
        self.urcall = urcall
        self.rpt1 = rpt1
        self.rpt2 = rpt2
        self.code_number = code_number


class YSFConfig(object):
    """
    Configuration parameters for communicating via Yaesu System Fusion
    """

    def __init__(
        self,
        dg_input=None,
        dg_output=None,
    ):
        self.dg_input = dg_input
        self.dg_output = dg_output


class DMRConfig(object):
    """
    Configuration parameters for communicating via DMR
    """

    def __init__(
        self,
        color_code=1,
    ):
        self.color_code = color_code

