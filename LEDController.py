import time
from machine import Pin,PWM 

class LED:
    # RGB LED Pins
    _RED = Pin(1)
    _GREEN = Pin(2)
    _BLUE = Pin(3)
    
    def __init__(self):
        # Remember the last selected color for on/off
        self._previousColor = (0, 0, 0)
        
    # PUBLIC METHODS
        
    # Set the color of the LED
    def setColor(self, red, green, blue):
        # Check input
        for color in [red, green, blue]:
            if color > 255 or color < 0:
                print("RGB color values must be in the range 0 to 255 incusive.")
                return
            
        # Remember this color
        self._previousColor = (red, green, blue)
        
        # Convert RGB values to duty cycles
        dutyRed = int(red * (65535/255))
        dutyGreen = int(green * (65535/255))
        dutyBlue = int(blue * (65535/255))
        
        # Set duty cycles
        self._pwmRed.duty_u16(dutyRed)
        self._pwmGreen.duty_u16(dutyGreen)
        self._pwmBlue.duty_u16(dutyBlue)
        
    # Turn LED on
    # MUST be called after initialization and before any other commands
    # Should be used to turn the LED back on after using `turnOff`
    def turnOn(self):
        self._initPWM()
        self.setColor(self._previousColor[0], self._previousColor[1], self._previousColor[2])
    
    # Turn LED off
    # This method deinitializes the PWM output on the LED pins.
    # Should always be called before program end, like when catching a `KeyboardInterrupt`.
    def turnOff(self):
        self._deinitPWM()
        
    # PRIVATE METHODS
    
    def _initPWM(self):
        self._pwmRed = PWM(self._RED, freq=1000)
        self._pwmGreen = PWM(self._GREEN, freq=1000)
        self._pwmBlue = PWM(self._BLUE, freq=1000)
        
    def _deinitPWM(self):
        self._pwmRed.deinit()
        self._pwmGreen.deinit()
        self._pwmBlue.deinit()