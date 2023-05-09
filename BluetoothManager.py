import uasyncio as asyncio
from aioble import aioble
import bluetooth
from micropython import const
from ServicesManager import ServicesManager
import HydromonServices as Services
import sys

# Device Name
_DEVICE_NAME = "hydromon"

# Advertising Interval
# These values and timings come from Apple's Accessory Design Guidelines
_ADV_INT_PRIMARY_uS = const(20000) # Use for 30 secs at least (20ms)
_ADV_INT_SECONDARY_uS = const(1022500) # If not found in 30 secs, use this to conserve battery (1022.5ms)

class BluetoothManager:
    async def connection(self):
        while True:
            try:
                # Connect to central
                connection = await aioble.advertise(
                    interval_us=_ADV_INT_PRIMARY_uS,
                    name=_DEVICE_NAME,
                    services=[Services.UUIDs.DEV_INFO_SERVICE,],
                )
                return connection
            except asyncio.TimeoutError:
                print("Advertising timeout")
            except asyncio.CancelledError:
                print("Advertising cancelled")
                
    async def writes(self, characteristic, dataHandler):
        """
        Waits for remote writes to the specified characterisitc. Passes written data
        to the provided `dataHandler` method.
        
        Arguments:
            characteristic (aioble.Characteristic) - The characteristic to be monitored
                for remote writes.
            dataHandler (function) - A function that takes bytes data as an argument.
        """
        try:
            data = await characteristic.written()
            dataHandler(data[1])
        except:
            print("Unknown exception: stopped waiting for writes.")

if __name__ == "__main__":
    manager = ServicesManager(Services.dictionary)
    devInfoService = manager.createService(Services.UUIDs.DEV_INFO_SERVICE)
    prefsService = manager.createService(Services.UUIDs.PREFERENCES_SERVICE)

    # Register services
    aioble.register_services(devInfoService[0], prefsService[0],)
    
    def prefDataHandler(data):
        prefValue = data.decode('utf-8')
        print("Value: ", prefValue)
        
    async def main():
        bt = BluetoothManager()
        while True:
            try:
                print("Awaiting a connection...")
                connection = await bt.connection()
                print("Connected to", connection.device)
                print("Waiting for writes to ", prefsService[1][0].uuid)
                await bt.writes(prefsService[1][0], prefDataHandler)
                print("Awaiting disconnection from central...")
                await connection.disconnected()
                print("Disconnected")
            except KeyboardInterrupt:
                sys.exit()
    
    asyncio.run(main())