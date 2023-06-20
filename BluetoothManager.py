import uasyncio as asyncio
from aioble import aioble
import bluetooth
from micropython import const
from ServicesManager import *
import sys

# Device Name
_DEVICE_NAME = "hydromon"

# Advertising Interval
# These values and timings come from Apple's Accessory Design Guidelines
_ADV_INT_PRIMARY_uS = const(20000) # Use for 30 secs at least (20ms)
_ADV_INT_SECONDARY_uS = const(1022500) # If not found in 30 secs, use this to conserve battery (1022.5ms)

# Advertising timeout
_ADV_INT_PRIMARY_TIMEOUT_MS = const(30000) # 30 seconds

class BluetoothManager:
    def __init__(self, preferences):
        self._preferences = preferences
        
    async def monitorForBLEConnections(self):
        serviceManager = ServicesManager(self._preferences)
        devInfoService = serviceManager.createService(UUIDs.DEV_INFO_SERVICE)
        prefsService = serviceManager.createService(UUIDs.PREFERENCES_SERVICE)
        
        # Register services
        aioble.register_services(devInfoService[0], prefsService[0],)
        
        # Monitor
        while True:
            try:
                print("Awaiting a connection...")
                connection = await self._connection()
                print("Connected to", connection.device)
                
                # Create a task for each characteristic
                tasks = await self._writes(prefsService[1], self._prefDataHandler)
                
                # Await disconnect from central
                await self._disconnect(connection, tasks)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{type(e).__name__}: {str(e)}")
        
    def _prefDataHandler(self, uuid, data):
        prefValue = data.decode('utf-8')
        for key, value in self._preferences.getAll():
            if bluetooth.UUID(key) == uuid:
                self._preferences.setValue(key, prefValue)
                print(f"Saved {uuid}: {prefValue}")
    
    async def _connection(self):
        # Use primary advertising interval for 30 seconds
        try:
            # Connect to central
            connection = await aioble.advertise(
                interval_us=_ADV_INT_PRIMARY_uS,
                name=_DEVICE_NAME,
                services=[UUIDs.DEV_INFO_SERVICE,],
                timeout_ms=_ADV_INT_PRIMARY_TIMEOUT_MS
            )
            return connection
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            print(f"{type(e).__name__}: {str(e)}")
        
        # After 30 secs, use secondary interval
        while True:
            try:
                # Connect to central
                connection = await aioble.advertise(
                    interval_us=_ADV_INT_SECONDARY_uS,
                    name=_DEVICE_NAME,
                    services=[UUIDs.DEV_INFO_SERVICE,],
                )
                return connection
            except asyncio.TimeoutError:
               continue 
            except Exception as e:
                print(f"{type(e).__name__}: {str(e)}")
                
    async def _disconnect(self, connection, tasks):
        # Wait for disconnection and cancel all tasks when it happens
        while True:
            try:
                await connection.disconnected()
            except Exception as e:
                print(f"{type(e).__name__}: {str(e)}")
                continue
            
            for task in tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    print("Task was cancelled")
            break
                
    async def _writes(self, characteristics, dataHandler):
        """
        Waits for remote writes to the specified characterisitc. Passes written data
        to the provided `dataHandler` method.
        
        Arguments:
            characteristics (list of aioble.Characteristic) - The characteristics to be monitored
                for remote writes.
            dataHandler (function) - A function that takes bytes data as an argument.
        """
        tasks = []
        for characteristic in characteristics:
            tasks.append(asyncio.create_task(self._monitorWrites(characteristic, dataHandler)))

        return tasks

    async def _monitorWrites(self, characteristic, dataHandler):
        while True:
            try:
                data = await characteristic.written()
                dataHandler(characteristic.uuid, data[1])
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"{type(e).__name__}: {str(e)}")
                break