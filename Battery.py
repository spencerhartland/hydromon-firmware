from machine import ADC, Pin
import time

class Battery:   
    # System input voltage
    _ADC1_CH0 = ADC(Pin(1))
    _ADC_RES = 4096
    
    # Reference voltages
    _VSYS = 3.3
    _FULL_BATTERY = 4.2
    _EMPTY_BATTERY = 2.8
    
    def voltage(self):
        # convert the raw ADC reading into volts
        raw = self._ADC1_CH0.read()
        voltage = (raw * self._VSYS) / self._ADC_RES
        return voltage
        
    
    def percentage(self):
        """
        Reads the system input voltage and calculates the battery's state of charge from that value.
        
        Returns:
        percentage (float) -- The battery's state of charge as a percentage.
        """
        voltage = self.voltage()
        percentage = 100 * ((voltage - self._EMPTY_BATTERY) / (self._FULL_BATTERY - self._EMPTY_BATTERY))
        if percentage > 100:
            percentage = 100.0
        elif percentage < 0:
            percentage = 0.0
            
        return percentage