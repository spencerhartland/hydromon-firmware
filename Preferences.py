import json
import PreferenceKeys

def _decodeColor(color):
        red = 0
        blue = 0
        green = 0
        
        for rgb, value in color.items():
            if rgb == "red":
                red = value
            elif rgb == "green":
                green = value
            elif rgb == "blue":
                blue = value
                
        return (red, green, blue)

class PreferencesDecoder:
    def __init__(self, filename):
        self._filename = filename
        with open(filename, "r") as preferences:
            # Get the JSON data and parse it into a dict
            data = preferences.read()
            self._preferencesData = json.loads(data)
                    
    def getPreferenceValue(self, requestedKey):
        for prefKey, value in self._preferencesData.items():
            if prefKey == requestedKey:
                if type(value) is dict:
                    # The preference contains an object describing a color
                    return _decodeColor(value)
                else:
                    return value
                
        return (0, 0, 0)
    
    def fetchPreferences(self):
        with open(self._filename, "r") as preferences:
            data = preferences.read()
            self._preferencesData = json.loads(data)
            
                    
                    
