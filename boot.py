from Input import *
from PreferencesManager import PreferencesManager
from WaterMonitor import WaterMonitor
from ServicesManager import *
import time
import sys
import uasyncio as asyncio
from BluetoothManager import BluetoothManager
from Hydromon import Hydromon

# Debug Flag
_DEBUG = False

if __name__ == "__main__":
    # Get user preferences from memore
    preferences = PreferencesManager()
        
    # Enable bluetooth connections
    bt = BluetoothManager(preferences)
    
    # Init fill-level monitoring
    sipSize = preferences.getValue(UUIDs.PREF_SIP_SIZE)
    waterMonitor = WaterMonitor(sipSize)
    
    # Input monitoring
    inputManager = InputManager()
    
    # Hardware control
    hydromon = Hydromon(preferences, waterMonitor)
    
    def buttonPressAction():
        waterMonitor.decreaseFillLevel()
        hydromon.displayFillLevel(True)
        time.sleep(1.5)
        hydromon.shutOffAccessoryComponents()
        
    def buttonHoldAction():
        waterMonitor.resetFillLevel()
        hydromon.displayFillLevel(True)
        time.sleep(1.5)
        hydromon.shutOffAccessoryComponents()

    async def loopForever():
        # Startup sequence
        hydromon.startup()
        
        timeSincePreviousAlert = 0
        
        if _DEBUG:
            _debugCounter = 0
        
        while True:
            try:
                alertTimeout = preferences.getValue(UUIDs.PREF_ALERT_TIMEOUT)
                alertDelay = preferences.getValue(UUIDs.PREF_ALERT_DELAY)
                if timeSincePreviousAlert >= alertDelay:
                    # Time to drink
                    hydromon.drinkReminderAlert(alertTimeout)
                    timeSincePreviousAlert = 0
                    hydromon.displayFillLevel()
                    hydromon.shutOffAccessoryComponents()
                    
                standbyTimeout = preferences.getValue(UUIDs.PREF_STANDBY_TIMEOUT)
                standbyCount = 0
                # Acceleration along the z-axis
                # ~1.0 indicates no acceleration (1g is the accel of gravity)
                # < 0.95 indicates the device is being picked up
                # > 1.05 indicates the device is being put down
                zAccel = hydromon.getZAcceleration()
                print(f"z-accel: {zAccel}")
                if zAccel < 0.98:
                    # Hydromon is being picked up
                    hydromon.standbyWake()
                    while standbyCount <= standbyTimeout:
                        await asyncio.sleep(1.0)
                        standbyCount += 1
                    hydromon.shutOffAccessoryComponents()
                
                timeSincePreviousAlert += (standbyCount + 1)
                await asyncio.sleep(1.0)
                
                if _DEBUG:
                    # Ends loop after specified numnber of debug iterations
                    _debugCounter += 1
                    if _debugCounter > 120:
                        print("DEBUG TIME LIMIT EXCEEDED")
                        break
                    
                inputManager.parseInputs(onPress=buttonPressAction, onHold=buttonHoldAction)
                
                # Check for updates to preferences
                preferences.fetch()
                
            except Exception as e:
                print(f"{type(e).__name__}: {str(e)}")
                sys.exit()
                
    async def main():
        await asyncio.gather(loopForever(), bt.monitorForBLEConnections(), inputManager.monitorForInput())
                

    asyncio.run(main())