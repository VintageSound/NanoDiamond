import pyvisa

from Data.microwaveConfiguration import microwaveConfiguration
from Data.measurementType import measurementType 

# Python interface for Rohde & Schwarz smr20.
class microwaveInterfaceSMR20():
    _instance = None

    # This is to make sure there is only one instance if the interface, so that no one will use 
    # the same connection \ socket \ series twice
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(microwaveInterfaceSMR20, cls).__new__(cls)
            cls._instance.initialize()

        return cls._instance

    def initialize(self, resource_name = "GPIB0::3::INSTR"):
        self.resource_name = resource_name
        self.rm = pyvisa.ResourceManager()
        self.resource = None

    def connect(self):
        try:
            self.resource = self.rm.open_resource(self.resource_name)
            print("Connected to SMR20.")
        except Exception as e:
            print(f"Failed to connect to SMR20: {e}")

    def disconnect(self):
        if self.resource is not None:
            self.resource.close()
            self.resource = None
            print("Disconnected from SMR20.")

    def getIsConnected(self):
        connected = False
        try:
            # Try to write an empty string to the resource
            self.resource.write('')
            connected = True
        except:
            pass
        return connected

    def turnOnMicrowave(self):
        if not self.getIsConnected():
            raise ConnectionError("SNR20 is disconnected")
        
        self._write("OUTP:STAT ON")

    def turnOffMicrowave(self):
        if not self.getIsConnected():
            raise ConnectionError("SNR20 is disconnected")
        
        self._write("OUTP:STAT OFF")

    # TODO: Test
    def checkIfMicrowaveIsOn(self):
        # Query the status of the microwave
        response = self._query("OUTP:STAT?")
        
        # Check the response
        if response.strip() == '1':
            return True
        else:
            return False

    def sendODMRSweepCommand(self, config : microwaveConfiguration):
        self._set_freq_mode_sweep()
        self._set_power(config.power)
        self._set_trigger_mode(config.trigMode)
        #self._set_sweep_mode(2)
        self._set_sweep_parameters(config.startFreq, config.stopFreq, config.stepSize, config.stepTime)
        self._set_sweep_spacing("LINear")
        self._start_sweep()

    def sendRabiCommand(self, config : microwaveConfiguration):
        self._set_freq_mode_fix()
        self._set_power(config.power)
        self._set_trigger_mode(config.trigMode)
        self._set_frequency(config.centerFreq)

    def _query(self, command):
        # Send a query command to the instrument and return the response.
        return self.resource.query(command)

    def _write(self, command):
        # Send a write command to the instrument.
        return self.resource.write(command)

    def _identify(self):
        # Get the instrument's identification string.
        return self._query("*IDN?")

    def _set_frequency(self, frequency):
        # Set the frequency in MHz.
        self._write("FREQ:CW %d E6" % frequency)

    def _set_power(self, power):
        # Set the power in dB.
        self._write("POW %d" % power)

    def _set_sweep_parameters(self, start_frequency, stop_frequency, step_size, dwell_time):
        # Set the sweep parameters. Frequencies in MHz
        self._write("FREQ:STAR %d E6" % start_frequency)
        self._write("FREQ:STOP %d E6" % stop_frequency)
        self._write("SWE:STEP %f E6" % step_size)
        self._write("SWE:DWEL %f ms" % dwell_time)

    def _start_sweep(self):
        # Start the sweep.
        self._write("TRIG:SWE:IMM")

    def _set_trigger_mode(self, mode):
        # Set the trigger mode.
        if mode == 0:
            self._write("TRIG:SWE:SOUR AUTO")
        elif mode == 1:
            self._write("TRIG:SWE:SOUR SING")
        elif mode == 2:
            self._write("TRIG:SWE:SOUR EXT")

        else:
            raise ValueError("Invalid trigger mode: %s" % mode)

    def _set_sweep_mode(self, mode):
        # Set the sweep mode.
        if mode == 0:
            self._write("SWEEP:MODE AUTO")
        elif mode == 1:
            # MANual
            self._write("SWEEP:MODE MAN")
        elif mode == 2:
            self._write("SWEEP:MODE STEP")
        else:
            raise ValueError("Invalid sweep mode: %s" % mode)

    def _set_sweep_spacing(self, spacing):
        # Set the sweep mode. LINear, LOGarithmic, RAMP
        self._write("SWE:SPAC %s" % spacing)

    def _set_freq_mode_sweep(self):
        self._write("FREQ:MODE SWE")
        
    def _set_freq_mode_fix(self):
        self._write("FREQ:MODE FIX")
        
    def _get_state(self):
        # get the power state (on or off)
        return self._query("OUTP:STAT?").strip()

    def _software_trig(self):
        # Send a software trigger to the smr 20
        self._write("TRIG:SWE:IMM")


