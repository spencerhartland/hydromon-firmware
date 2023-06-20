from aioble import aioble
import bluetooth
from UUIDs import UUIDs
from PreferencesManager import PreferencesManager
        
class ServicesManager:
    MFC_NAME = "Spencer Hartland"
    MODEL_NUM = "M00000001"
    FIRMWARE_REV = "1.0.0"
    SOFTWARE_REV = "1.0.0"
    
    def __init__(self, preferencesManager):
        self._prefs = preferencesManager.getAll()
        self._services = {
            # { service: {characteristic, characteristic, ...} }
            # Device Information Service
            UUIDs.DEV_INFO_SERVICE: {
                # {UUID: (vaue, read, write), ...}
                # Manufacturer's Name String
                UUIDs.DIS_MFC_NAME: (self.MFC_NAME, True, False),
                # Model Number String
                UUIDs.DIS_MODEL_NUM: (self.MODEL_NUM, True, False),
                # Firmware Revision String
                UUIDs.DIS_FIRMWARE_REV: (self.FIRMWARE_REV, True, False),
                # Software Revision String
                UUIDs.DIS_SOFTWARE_REV: (self.SOFTWARE_REV, True, False)
            }
        }
        # Preferences Service
        self._services[UUIDs.PREFERENCES_SERVICE] = {}
        for uuid, value in self._prefs:
            self._services[UUIDs.PREFERENCES_SERVICE][uuid] = (value, True, True)

    # Returns (Service, [Characteristic, Characteristic, ...])
    def createService(self, uuid):
        result = ()
        
        if uuid in self._services:
            service = aioble.Service(bluetooth.UUID(uuid))
            
            chars = []
            for key, char in self._services[uuid].items():
                value = char[0]
                read = char[1]
                write = char[2]
                characteristic = aioble.Characteristic(service, bluetooth.UUID(key), read=read, write=write, capture=write)
                characteristic.write(value.encode('utf-8'))
                chars.append(characteristic)
            
            result = (service, chars)
            
        return result
    
    