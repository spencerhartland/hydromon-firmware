from aioble import aioble
import bluetooth

class ServicesManager:
    def __init__(self, services):
        """
        Creates an instance of `ServicesManager` which can be used to manage the
        specified services.
        
        Arguments:
            services (dict) - A dictionary using the format specified below that contains
                the services and characteristics you wish to manage.
                
                ```
                services = {
                    serviceUUID_1: {
                        characteristicUUID_1: (value, read, write),
                        ...
                        characteristicUUID_X: (value, read, write)
                    },
                    ...
                    serviceUUID_2: {
                        characteristicUUID_1: (value, read, write),
                        ...
                        characteristicUUID_X: (value, read, write)
                    }
                }
                ```
                
        Returns:
            ServiceManager - An instance of type `ServiceManager` which can be used to
                initialize and manager `aioble.Service` and `aioble.Characteristic` objects.
        """
        self._services = services

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

if __name__ == "__main__":
    import HydromonServices as Services
    manager = ServicesManager(Services.dictionary)
    devInfoService = manager.createService(Services.UUIDs.DEV_INFO_SERVICE)
    print(devInfoService)
    
    