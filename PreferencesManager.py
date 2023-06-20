import json
from UUIDs import UUIDs

class PreferencesManager:
    PREFS_FILENAME = "preferences.json"
    
    def __init__(self):
        self.fetch()
    
    def getAll(self):
        return self._preferencesData.items()
    
    def getValue(self, prefKey):
        for key, value in self._preferencesData.items():
            if key == prefKey:
                if (prefKey == UUIDs.PREF_LCD_STANDBY_COLOR or
                    prefKey == UUIDs.PREF_LCD_ALERT_COLOR or
                    prefKey == UUIDs.PREF_LED_STANDBY_COLOR or
                    prefKey == UUIDs.PREF_LED_ALERT_COLOR):
                    return self._hexToRGB(value)
                elif (prefKey == UUIDs.PREF_STANDBY_TIMEOUT or
                    prefKey == UUIDs.PREF_ALERT_TIMEOUT or
                    prefKey == UUIDs.PREF_ALERT_DELAY or
                    prefKey == UUIDs.PREF_OLED_MAX_BRIGHTNESS or
                    prefKey == UUIDs.PREF_SIP_SIZE):
                    return int(value)
                else:
                    return value
                
        raise InvalidPreferenceKeyError(f"Could not find key {prefKey} in preferences.")
    
    def setValue(self, prefKey, newValue):
        for key, value in self._preferencesData.items():
            if key == prefKey:
                # Modify the value and save to preferences.json
                self._preferencesData[key] = newValue
                with open(self.PREFS_FILENAME, "w") as preferences:
                    json.dump(self._preferencesData, preferences)
                return
                
        raise InvalidPreferenceKeyError(f"Could not find key {requestedKey} in preferences.")
    
    def fetch(self):
        with open(self.PREFS_FILENAME, "r") as preferences:
            data = preferences.read()
            self._preferencesData = json.loads(data)
            
    def _hexToRGB(self, color):
        if len(color) != 6:
            raise ValueError("Invalid hexadecimal color string")
        try:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            return [r, g, b]
        except ValueError:
            print("Invalid hexadecimal color string")
    
    class InvalidPreferenceKeyError(Exception):
        pass
            
                    
                    
