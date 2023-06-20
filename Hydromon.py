from AccessoryPowerController import AccessoryPower
from Input import *
from I2CManager import I2CManager
from PreferencesManager import PreferencesManager
from WaterMonitor import WaterMonitor
from ServicesManager import *
from LEDController import LED
import time
import sys
import uasyncio as asyncio
from BluetoothManager import BluetoothManager
from Battery import Battery

# Debug Flag
_DEBUG = True

# Constants
_STARTUP_LCD_MESSAGE = "Hello, Spencer!" # TODO: Add to prefs for customizable startup message
_HYDROMON_TEXT = "HYDROMON"

_STARTUP_WAIT = 5

# Assets
_ICON_BATTERY_0 = "assets/battery-0.pbm"
_ICON_BATTERY_25 = "assets/battery-25.pbm"
_ICON_BATTERY_50 = "assets/battery-50.pbm"
_ICON_BATTERY_75 = "assets/battery-75.pbm"
_ICON_BATTERY_100 = "assets/battery-100.pbm"
_ICON_WATER_DROP = "assets/water-drop.pbm"

class Hydromon:
    def __init__(self, preferences, waterMonitor):
        AccessoryPower.enable()
        # Init hardware
        self._i2c = I2CManager()
        # Init preferences
        self._preferences = preferences
        # Init water level monitoring
        self._water = waterMonitor
        # Battery SOC Monitoring
        self._battery = Battery()
        # LED
        self._led = LED()
        AccessoryPower.disable()
        
    def startup(self):
        AccessoryPower.enable()
        # Demonstrate functionality of hardware
        # Device Info Display
        self._i2c.deviceInfoOLED.poweron()
        self._i2c.deviceInfoOLED.fill(0) # Clear screen
        self._i2c.deviceInfoOLED.text(_HYDROMON_TEXT, 32, 20)
        self._i2c.deviceInfoOLED.show()
        # LCD
        lcdStandbyColor = self._preferences.getValue(UUIDs.PREF_LCD_STANDBY_COLOR)
        self._i2c.LCD.setRGB(lcdStandbyColor[0], lcdStandbyColor[1], lcdStandbyColor[2])
        self._i2c.LCD.printout(_STARTUP_LCD_MESSAGE)
        # Fill level display
        self.displayFillLevel(True)
        # LED
        ledStandbyColor = self._preferences.getValue(UUIDs.PREF_LED_STANDBY_COLOR)
        self._led.turnOn()
        self._led.setColor(ledStandbyColor[0], ledStandbyColor[1], ledStandbyColor[2])
        # Wait a moment, 
        time.sleep(_STARTUP_WAIT)
        # Power off components to save power
        self.shutOffAccessoryComponents()
        
    def shutOffAccessoryComponents(self):
        self._led.turnOff()
        self._i2c.deviceInfoOLED.poweroff()
        self._i2c.fillLevelOLED.poweroff()
        self._i2c.LCD.setRGB(0, 0, 0)
        self._i2c.LCD.clear()
        AccessoryPower.disable()
        
    def standbyWake(self):
        AccessoryPower.enable()
        # LCD
        lcdStandbyMessage = self._preferences.getValue(UUIDs.PREF_LCD_STANDBY_MESSAGE)
        lcdStandbyColor = self._preferences.getValue(UUIDs.PREF_LCD_STANDBY_COLOR)
        self._i2c.LCD.clear()
        self._i2c.LCD.setRGB(lcdStandbyColor[0], lcdStandbyColor[1], lcdStandbyColor[2])
        self._i2c.LCD.printout(lcdStandbyMessage)
        # LED
        ledStandbyColor = self._preferences.getValue(UUIDs.PREF_LED_STANDBY_COLOR)
        self._led.turnOn()
        self._led.setColor(ledStandbyColor[0], ledStandbyColor[1], ledStandbyColor[2])
        # Device info dispay
        self.displayDeviceInfo()
        # Fill level display
        self.displayFillLevel()
        
    def displayDeviceInfo(self):
        AccessoryPower.enable()
        # Get battery level
        level = self._battery.percentage()
        # Turn on display
        self._i2c.deviceInfoOLED.poweron()
        # Display battery info
        if level <= 10:
            batteryImageFile = self._ICON_BATTERY_EMPTY
        elif level <= 25:
            batteryImageFile = self._ICON_BATTERY_25
        elif level <= 50:
            batteryImageFile = self._ICON_BATTERY_50
        elif level <= 75:
            batteryImageFile = self._ICON_BATTERY_75
        elif level <= 100:
            batteryImageFile = self._ICON_BATTERY_100
        batteryFbuf = self._makeFramebuffer(128, 64, batteryImageFile)
        self._i2c.deviceInfoOLED.blit(batteryFbuf, -5, -10)
        self._i2c.deviceInfoOLED.show()
        # Display drink reminder notification
        waterDropImageFile = self._ICON_WATER_DROP
        waterDropFbuf = self._makeFramebuffer(24, 64, waterDropImageFile)
        self._i2c.deviceInfoOLED.blit(waterDropFbuf, 104, -10)
        self._i2c.deviceInfoOLED.show()
    
    def displayFillLevel(self, animated=False):
        AccessoryPower.enable()
        self._i2c.fillLevelOLED.poweron()
        # Get fill level
        level = self._water.getFillLevel()
        # Calculate the number of lines to show
        lines = int(128 * level)
        # Clear the display
        self._i2c.fillLevelOLED.fill(0)
        # Display fill level
        for line in range(0, (lines - 1), 1):
            self._i2c.fillLevelOLED.vline(line, 10, 12, 1)
            if animated:
                self._i2c.fillLevelOLED.show()
                time.sleep(0.0015)
        if not animated:
            self._i2c.fillLevelOLED.show()
            
    def drinkReminderAlert(self, alertTimeout):
        AccessoryPower.enable()
        # LCD
        lcdAlertMessage = self._preferences.getValue(UUIDs.PREF_LCD_ALERT_MESSAGE)
        lcdAlertColor  = self._preferences.getValue(UUIDs.PREF_LCD_ALERT_COLOR)
        self._i2c.LCD.clear()
        self._i2c.LCD.setRGB(lcdAlertColor[0], lcdAlertColor[1], lcdAlertColor[2])
        self._i2c.LCD.printout(lcdAlertMessage)
        # LED
        ledAlertColor = self._preferences.getValue(UUIDs.PREF_LED_ALERT_COLOR)
        self._led.turnOn()
        self._led.setColor(ledAlertColor[0], ledAlertColor[1], ledAlertColor[2])
        # Device info display
        # TODO: Add more to drink reminder
        timeout = 0
        while timeout <= alertTimeout:
            time.sleep(1.0)
            timeout += 1
        self._i2c.LCD.clear()
        self._i2c.LCD.setRGB(0, 0 ,0)
        self._led.turnOff()
            
    def getZAcceleration(self):
        return self._i2c.imu.accel.xyz[2]
    
    def _makeFramebuffer(self, width, height, filename):
        with open(filename, 'rb') as image:
            image.readline() # Magic number
            image.readline() # Creator comment
            image.readline() # Dimensions
            data = bytearray(image.read())
            fbuf = framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)