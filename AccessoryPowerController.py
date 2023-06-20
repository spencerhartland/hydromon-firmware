from machine import Pin
from time import sleep
import sys

_VEXT_CTRL_PIN = 36

# Controls 3.3V output to accessory components (OLED, LCD)
# Enables reduced power consumption when accessories are not in use
class AccessoryPower:
    _vextCtrl = Pin(_VEXT_CTRL_PIN, Pin.OUT)
    
    @staticmethod
    def enable():
        AccessoryPower._vextCtrl.value(0)
        
    @staticmethod
    def disable():
        AccessoryPower._vextCtrl.value(1)
    
