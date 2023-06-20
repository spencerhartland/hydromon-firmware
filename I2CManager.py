from machine import SoftI2C, Pin
import time
import ssd1306
import rgb1602
import imu
from micropython import const
import sys

# Device Information OLED
# 128x64, built-in

_DEV_INFO_OLED_WIDTH = const(128)
_DEV_INFO_OLED_HEIGHT = const(64)

_DEV_INFO_OLED_RST = const(21)
_DEV_INFO_OLED_SDA = const(17)
_DEV_INFO_OLED_SCL = const(18)

_DEV_INFO_OLED_RST_PIN = Pin(_DEV_INFO_OLED_RST, Pin.OUT, Pin.PULL_UP)
_DEV_INFO_OLED_SDA_PIN = Pin(_DEV_INFO_OLED_SDA, Pin.OUT, Pin.PULL_UP)
_DEV_INFO_OLED_SCL_PIN = Pin(_DEV_INFO_OLED_SCL, Pin.OUT, Pin.PULL_UP)

# Fill Level OLED
# 128x32

_FILL_LEVEL_OLED_WIDTH = const(128)
_FILL_LEVEL_OLED_HEIGHT = const(32)

_FILL_LEVEL_OLED_SDA = const(5)
_FILL_LEVEL_OLED_SCL = const(4)

_FILL_LEVEL_OLED_SDA_PIN = Pin(_FILL_LEVEL_OLED_SDA, Pin.OUT, Pin.PULL_UP)
_FILL_LEVEL_OLED_SCL_PIN = Pin(_FILL_LEVEL_OLED_SCL, Pin.OUT, Pin.PULL_UP)

# LCD
# 16x2

_LCD_ROW = const(16)
_LCD_COL = const(2)

_LCD_SDA = const(6)
_LCD_SCL = const(7)

_LCD_SDA_PIN = Pin(_LCD_SDA, Pin.OUT, Pin.PULL_UP)
_LCD_SCL_PIN = Pin(_LCD_SCL, Pin.OUT, Pin.PULL_UP)

# Inertial Measurement Unit (IMU)
# MPU6050

_IMU_SDA = const(46)
_IMU_SCL = const(45)

_IMU_SDA_PIN = Pin(_IMU_SDA, Pin.OUT, Pin.PULL_UP)
_IMU_SCL_PIN = Pin(_IMU_SCL, Pin.OUT, Pin.PULL_UP)

# Manages I2C communication with connected components.
class I2CManager:
    def __init__(self):
        # Init sequence for built-in OLED
        _DEV_INFO_OLED_RST_PIN.value(1)
        time.sleep_ms(20)
        _DEV_INFO_OLED_RST_PIN.value(0)
        time.sleep_ms(20)
        _DEV_INFO_OLED_RST_PIN.value(1)
        time.sleep_ms(20)
        
        # Init devices
        # Device Info OLED
        self._bus0 = SoftI2C(sda=_DEV_INFO_OLED_SDA_PIN, scl=_DEV_INFO_OLED_SCL_PIN)
        self.deviceInfoOLED = ssd1306.SSD1306_I2C(_DEV_INFO_OLED_WIDTH, _DEV_INFO_OLED_HEIGHT, self._bus0)
        self.deviceInfoOLED.poweroff()
        
        # Fill Level OLED
        self._bus1 = SoftI2C(sda=_FILL_LEVEL_OLED_SDA_PIN, scl=_FILL_LEVEL_OLED_SCL_PIN)
        self.fillLevelOLED = ssd1306.SSD1306_I2C(_FILL_LEVEL_OLED_WIDTH, _FILL_LEVEL_OLED_HEIGHT, self._bus1)
        self.fillLevelOLED.poweroff()
        
        # LCD
        self._bus3 = SoftI2C(sda=_LCD_SDA_PIN, scl=_LCD_SCL_PIN)
        self.LCD = rgb1602.RGB1602(_LCD_ROW, _LCD_COL, self._bus3)
        
        # IMU
        self._bus4 = SoftI2C(sda=_IMU_SDA_PIN, scl=_IMU_SCL_PIN)
        self.imu = imu.MPU6050(self._bus4)