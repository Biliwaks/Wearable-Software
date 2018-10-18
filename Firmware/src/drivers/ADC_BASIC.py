# -*- coding: utf-8 -*-
"""
Driver file for the BASIC ADC. Read the value from a analog pin for integrating into
the SoftWEAR package.
"""
#import Adafruit_GPIO.AdafruitBBIOAdapter as AdafruitBBIOAdapter # Main peripheral class. Implements GPIO read out
import Adafruit_BBIO.ADC as ADC

# Adapter for BBGW
# GPIO = AdafruitBBIOAdapter()

# Timeout device
TIMEOUT_TICKS = 10
TIMEOUT_ENABLED = True
TIMEOUT_THRESHOLD = 0.005

class ADCBasic:
    """Driver for BASIC ADC."""

    # Name of the device
    _name = 'ADC_BASIC'

    # Direction of the driver (in/out)
    _dir = 'in'

    # Dimension of the driver (0-#)
    _dim = 1

    # Dimension map of the driver (0-#)
    _dimMap = ['Voltage']

    # Pin
    _pin = None

    # Muxed pin
    _muxedPin = None

    # Zero counter
    _zeroCounter = 0

    # Settings of the driver
    _settings = {
        'modes': ['Auto Detection', 'Manual Detection']
    }

    # Mode
    _mode = None




    def __init__(self, pin, muxedPin = None):
        """Device supports a pin."""
        self._pin = pin                                         # Set pin
        self._muxedPin = muxedPin                               # Set muxed pin
        self._zeroCounter = 0                                   # Set zero counter to 0
        self._mode = self._settings['modes'][0]                 # Set default mode
        ADC.setup()                                             # Enable ADC readings


    def getDeviceConnected(self):
        """Return True if the device is connected, false otherwise."""
        if not TIMEOUT_ENABLED:                                 # Check if flag to deconnect inactive devices is set
            return True

        # BUG: Due to a bug in the ADC driver, read the values 2 times to get the most recent
        ADC.read(self._pin)

        if self._mode == 'Auto Detection':                      # Got for >0 detection
            currentValueZero = ADC.read(self._pin) < TIMEOUT_THRESHOLD # Check if current value is different to zero
            pastValuesZero = self._zeroCounter < TIMEOUT_TICKS  # Check if past values are constant zero

            return not (currentValueZero and pastValuesZero)    # Return False to deconnect device
        elif self._mode == 'Manual Detection':                  # Connected anyway
            return True

    def configureDevice(self):
        """Once the device is connected, it must be configured."""
        return                                                  # No need to setup ADC individually

    def getValues(self):
        """Get values for the basic input."""
        # BUG: Due to a bug in the ADC driver, read the values 2 times to get the most recent
        ADC.read(self._pin)
        v = ADC.read(self._pin)
        if self._mode == 'Auto Detection':                      # Go for detection
            if v < TIMEOUT_THRESHOLD:                           # Count how many times the values is zero
                self._zeroCounter += 1                          # Increase zero counter
            else:
                self._zeroCounter = 0                           # Reset zero counter
        elif self._mode == 'Manual Detection':                  # Keep device anyway
            self._zeroCounter = 0                               # Reset zero counter
        return [v]                                              # Read the value


    def getDevice(self):
        """Return device name."""
        return self._name
    def getName(self):
        """Return device name."""
        if self._muxedPin == None:
            return '{}@ADC[{}]'.format(self._name, self._pin)
        else:
            return '{}@ADC[{}:{}]'.format(self._name, self._pin, self._muxedPin)
    def getDir(self):
        """Return device direction."""
        return self._dir
    def getDim(self):
        """Return device dimension."""
        return self._dim
    def getDimMap(self):
        """Return device dimension map."""
        return self._dimMap[:]
    def getPin(self):
        """Return device pin."""
        return self._pin
    def getMuxedPin(self):
        """Return device muxed pin."""
        return self._muxedPin
    def getAbout(self):
        """Return device settings."""
        return {'dimMap': self._dimMap[:]}
    def getSettings(self):
        """Return device settings."""
        return self._settings
    def getMode(self):
        """Return device mode."""
        return self._mode

    def setMode(self, mode):
        """Set device mode."""
        if (mode in self._settings['modes']):
            self._mode = mode
        else:
            raise ValueError('mode {} is not allowed'.format(mode))