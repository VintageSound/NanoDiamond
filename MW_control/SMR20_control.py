import pyvisa


class RSMR20:
    """Python interface for Rohde & Schwarz smr20."""

    def __init__(self, resource_name):
        self.resource = pyvisa.ResourceManager().open_resource(resource_name)

    def default_values(self):
        """set the device to fix frequency mode, center freq at 2.87GHz, power at 0 dBm and external trigger"""
        self.set_freq_mode(0)
        self.set_frequency(2870)
        self.set_power(0)
        self.set_trigger_mode(2)

    def query(self, command):
        """Send a query command to the instrument and return the response."""
        return self.resource.query(command)

    def write(self, command):
        """Send a write command to the instrument."""
        return self.resource.write(command)

    def identify(self):
        """Get the instrument's identification string."""
        return self.query("*IDN?")

    def set_frequency(self, frequency):
        """Set the frequency in MHz."""
        self.write("FREQ:CW %d E6" % frequency)

    def set_power(self, power):
        """Set the power in dB."""
        self.write("POW %d" % power)

    def set_sweep_parameters(self, start_frequency, stop_frequency, step_size, dwell_time):
        """Set the sweep parameters. Frequencies in MHz"""
        self.write("FREQ:STAR %d E6" % start_frequency)
        self.write("FREQ:STOP %d E6" % stop_frequency)
        self.write("SWE:STEP %d E6" % step_size)
        self.write("SWE:DWEL %d ms" % dwell_time)

    def start_sweep(self):
        """Start the sweep."""
        self.write("TRIG:SWE:IMM")

    # def set_trigger_mode(self, mode):
    #     """Set the trigger mode. AUTO, SINGle or EXT"""
    #     self.write("TRIG:SWE:SOUR %s" % mode)

    def set_trigger_mode(self, mode):
        """Set the trigger mode."""
        if mode == 0:
            self.write("TRIG:SWE:SOUR AUTO")
        elif mode == 1:
            self.write("TRIG:SWE:SOUR SING")
        elif mode == 2:
            self.write("TRIG:SWE:SOUR EXT")
        else:
            raise ValueError("Invalid trigger mode: %s" % mode)

    def set_sweep_mode(self, mode):
        """Set the sweep mode. AUTO, MANual, STEP"""
        self.write("SWE:MODE %s" % mode)

    def set_sweep_mode(self, mode):
        """Set the sweep mode."""
        if mode == 0:
            self.write("SWEEP:MODE AUTO")
        elif mode == 1:
            self.write("SWEEP:MODE MAN")
        elif mode == 2:
            self.write("SWEEP:MODE STEP")
        else:
            raise ValueError("Invalid sweep mode: %s" % mode)

    def set_sweep_spacing(self, spacing):
        """Set the sweep mode. LINear, LOGarithmic, RAMP"""
        self.write("SWE:SPAC %s" % spacing)

    def on(self):
        """Turn the instrument on."""
        self.write("OUTP:STAT ON")

    def off(self):
        """Turn the instrument off."""
        self.write("OUTP:STAT OFF")

    def set_freq_mode(self, mode):
        """Set the frequency mode."""
        if mode == 0:
            self.write("FREQ:MODE FIX")
        elif mode == 1:
            self.write("FREQ:MODE SWE")
        else:
            raise ValueError("Invalid frequency mode: %s" % mode)

    def get_state(self):
        "get the power state (on or off)"
        return self.query("OUTP:STAT?").strip()

    def software_trig(self):
        """"Send a software trigger to the smr 20"""
        self.write("TRIG:SWE:IMM")

if __name__ == "__main__":
    smr20 = RSMR20("GPIB0::3::INSTR")
    print(smr20.query("*IDN?"))
    # smr20.default_values()
    # smr20.on()
    # smr20.set_frequency(500)
    # smr20.on()
    # smr20.set_sweep_parameters(75, 500, 1, 100)
    # smr20.start_sweep()



