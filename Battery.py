from machine import ADC, Pin
import time

class Battery:
    # Icons for battery percentage display
    EMPTY_ICON = bytearray([0x0E, 0x1B, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1F])
    
    # System input voltage
    _VSYS = ADC(29)
    # Indicates whether or not USB power is connected
    _CHARGING = Pin(24, Pin.IN)
    # Used to convert raw ADC value to voltage
    _CONVERSION_FACTOR = 3 * 3.3 / 65535
    
    # Reference voltages
    _FULL_BATTERY = 4.2
    _EMPTY_BATTERY = 2.8
    
    def percentage(self):
        """
        Reads the system input voltage and calculates the battery's state of charge from that value.
        
        Returns:
        percentage (float) -- The battery's state of charge as a percentage.
        """
        # convert the raw ADC read into a voltage, and then a percentage
        voltage = self._VSYS.read_u16() * self._CONVERSION_FACTOR
        percentage = 100 * ((voltage - self._EMPTY_BATTERY) / (self._FULL_BATTERY - self._EMPTY_BATTERY))
        if percentage > 100:
            percentage = 100.0
            
        return percentage