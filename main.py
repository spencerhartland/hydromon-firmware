from picozero import RGBLED
from ssd1306 import SSD1306_I2C
from rgb1602 import RGB1602
from machine import Pin, I2C
from imu import MPU6050
from Preferences import PreferencesDecoder
import PreferenceKeys
import sys
from time import sleep
import framebuf
from WaterMonitor import WaterMonitor
import _thread
import Input
from Battery import Battery
from server import Server

DEBUG = True

# I2C BUSES
# Bus 0: OLED and MPU6050
i2c0 = I2C(0, sda = Pin(16), scl = Pin(17), freq = 400000)
# Bus 1: LCD
i2c1 = I2C(1, sda = Pin(14), scl = Pin(15), freq = 400000)

# Hardware initialization
led = RGBLED(11, 12, 13)
oled = SSD1306_I2C(128, 32, i2c0)
mpu6050 = MPU6050(i2c0)
lcd = RGB1602(2, 16, i2c1)

# Preferences
decoder = PreferencesDecoder("preferences.json")

# Fill-level monitoring
monitor = WaterMonitor()

# Battery SoC monitoring
battery = Battery()

# Semaphore lock for multithreading
sLock = _thread.allocate_lock()

def displayBatterySOC():
    batterySOC = battery.percentage()
    if DEBUG:
        print(f"{batterySOC}")
    
    lcd.setCursor(0, 1)
    
    if batterySOC <= 10.0:
        lcd.printout("charge now")
    else:
        lcd.printout(f"{batterySOC}")

def standbyWake():
    """
    Turns on LCD, LED, and OLED. LCD displays the set standby message and color, the
    LED is set to its standby color, and the OLED displays the current estimated fill level
    at full brightness. Standby is any time that the drink reminder alert is not active.
    """
    # LCD standby message
    lcdStandbyMessage = decoder.getPreferenceValue(PreferenceKeys.LCD_STANDBY_MESSAGE)
    lcdStandbyColor = decoder.getPreferenceValue(PreferenceKeys.LCD_STANDBY_COLOR)
    lcd.setRGB(lcdStandbyColor[0], lcdStandbyColor[1], lcdStandbyColor[2])
    lcd.clear()
    lcd.printout(lcdStandbyMessage)
    # LCD status line
    displayBatterySOC()
    # LED
    ledStandbyColor = decoder.getPreferenceValue(PreferenceKeys.LED_STANDBY_COLOR)
    led.color = ledStandbyColor
    # OLED
    oledMaxBrightness = decoder.getPreferenceValue(PreferenceKeys.OLED_MAX_BRIGHTNESS)
    oled.contrast(oledMaxBrightness)
    
def lowPowerMode():
    """
    Greatly reduces power consumption of the entire system by turning off the LCD's
    backlight, turning off the LED, and dimming the OLED before turning it off.
    """
    lcd.setRGB(0, 0, 0)
    led.color = (0, 0, 0)
    oled.contrast(10)
    
def displayWaterDropIcon():
    directory = "assets"
    filename = "water-drop_0.pbm"
    path = directory + "/" + filename
    with open(path, 'rb') as image:
            image.readline() # Magic number
            image.readline() # Creator comment
            image.readline() # Dimensions
            data = bytearray(image.read())
            fbuf = framebuf.FrameBuffer(data, 128, 32, framebuf.MONO_HLSB)
            oled.blit(fbuf, 0, 0)
            oled.show()
            sleep(1.0)
    
def displayWaterDropAnimation():
    directory = "assets"
    filenamePrefix = "water-drop_"
    bitmapSuffix = "pbm"
    for i in range(0, 51, 1):
        filename = directory + "/" + filenamePrefix + str(i) + "." + bitmapSuffix
        with open(filename, 'rb') as image:
            image.readline() # Magic number
            image.readline() # Creator comment
            image.readline() # Dimensions
            data = bytearray(image.read())
            fbuf = framebuf.FrameBuffer(data, 128, 32, framebuf.MONO_HLSB)
            oled.blit(fbuf, 0, 0)
            oled.show()
            sleep(0.015)
    
def drinkReminderAlert(alertTimeout):
    # LCD
    lcdAlertMessage = decoder.getPreferenceValue(PreferenceKeys.LCD_ALERT_MESSAGE)
    lcdAlertColor = decoder.getPreferenceValue(PreferenceKeys.LCD_ALERT_COLOR)
    lcd.setRGB(lcdAlertColor[0], lcdAlertColor[1], lcdAlertColor[2])
    lcd.clear()
    lcd.printout(lcdAlertMessage)
    # LED
    ledAlertColor = decoder.getPreferenceValue(PreferenceKeys.LED_ALERT_COLOR)
    led.color = ledAlertColor
    # OLED
    oledMaxBrightness = decoder.getPreferenceValue(PreferenceKeys.OLED_MAX_BRIGHTNESS)
    oled.contrast(oledMaxBrightness)
    oled.fill(0)
    oled.show()
    alertCount = 0
    while alertCount <= alertTimeout:
        displayWaterDropAnimation()
        alertCount += 1
    
def displayFillLevel(animated=False):
    # Get fill level
    level = monitor.getFillLevel()
    # Calculate the number of lines to show
    lines = int(128 * level)
    # Clear the display
    oled.fill(0)
    # Display fill level
    for line in range(0, (lines - 1), 1):
        oled.vline(line, 0, 32, 1)
        if animated:
            oled.show()
            sleep(0.0015)
    if not animated:
        oled.show()
        
"""
        
def monitorForInput(queue):
    \"""
    Runs a loop on a background thread that monitors for input (button presses).
    Quick tap: user drank water, short press (3 secs): user filled bottle,
    long press (7 secs): enter editing mode.
    \"""
    button = Pin(10, Pin.IN, Pin.PULL_UP)
    sLock.acquire()
    while True:
        try:
            if not button.value() == True:
                sleep(1.0)
                if not button.value() == True:
                    # If the button is still pressed after 1 sec of waiting, check for short press.
                    sleep(1.0)
                    if not button.value() == True:
                        # Officially a short press, check that the user has let go after 3 sec.
                        sleep(2.0)
                        if not button.value() == True:
                            # Still holding... check for a long press
                            sleep(2.0)
                            if not button.value() == True:
                                # Long press
                                queue.addInput(Input.LONG_PRESS)
                        else:
                            # Short press
                            queue.addInput(Input.SHORT_PRESS)
                else:
                    # Quick tap
                    queue.addInput(Input.QUICK_TAP)
        except KeyboardInterrupt:
            sys.exit(0)
    sLock.release()
    
"""

# Main loop
if __name__ == "__main__":    
    # Set everything up according to user preferences, show that everything is working upon startup
    standbyWake()
    # Show Fill Level with animation
    displayFillLevel(animated = True)
    
    # Wait, enter low power mode, then enter the main loop
    sleep(3.0)
    lowPowerMode()
    
    # Begin monitoring for input
    inputQueue = Input.Queue()
    _thread.start_new_thread(monitorForInput, (inputQueue, ))
    
    timeSincePreviousAlert = 0
    if DEBUG:
        DEBUG_counter = 0
    while True:
        try:
            alertTimeout = decoder.getPreferenceValue(PreferenceKeys.ALERT_TIMEOUT)
            alertDelay = decoder.getPreferenceValue(PreferenceKeys.ALERT_DELAY)
            if timeSincePreviousAlert >= alertDelay:
                # Time to drink
                drinkReminderAlert(alertTimeout)
                timeSincePreviousAlert = alertTimeout
                displayFillLevel()
                lowPowerMode()
            
            standbyTimeout = decoder.getPreferenceValue(PreferenceKeys.STANDBY_TIMEOUT)
            standbyCount = 0
            # Acceleration along the z-axis
            # ~1.0 indicates no acceleration (1g is the accel of gravity)
            # < 0.95 indicates the device is being picked up
            # > 1.05 indicates the device is being put down
            # THESE VALUES COULD BE TOO SENSITIVE, ADJUST AFTER TESTING
            zAccel = mpu6050.accel.xyz[2]
            
            if DEBUG:
                print(f"Z-Axis Acceleration: {zAccel}")
                
            if zAccel < 0.95:
                # The device is being picked up
                standbyWake()
                while standbyCount <= standbyTimeout:
                    sleep(1.0)
                    standbyCount += 1
                lowPowerMode()
            
            timeSincePreviousAlert += (standbyCount + 1)
            sleep(1.0)
            
            if DEBUG:
                # DEBUG ONLY
                DEBUG_counter += 1
                if DEBUG_counter > 120:
                    print("DEBUG TIME LIMIT EXCEEDED")
                    break
                
            # Check for inputs
            for i in range(inputQueue.length()):
                userInput = inputQueue.getInput(i)
                if userInput == Input.QUICK_TAP:
                    # Quick tap: user drank water
                    monitor.decreaseFillLevel()
                    displayWaterDropIcon()
                    timeSincePreviousAlert += 1
                elif userInput == Input.SHORT_PRESS:
                    # Short press: user refilled the bottle
                    monitor.resetFillLevel()
                    displayWaterDropAnimation()
                    displayFillLevel(True)
                    timeSincePreviousAlert += 1.0
                elif userInput == Input.LONG_PRESS:
                    # Long press: enter editing mode
                    server = Server()
                    server.listenForRequests()
                    server.shutdown()
            inputQueue.reset()
            
            # Update fill level without animation
            displayFillLevel()
            
            # Check if there have been updates to user preferences
            decoder.fetchPreferences()
        except KeyboardInterrupt:
            sys.exit(0)
 