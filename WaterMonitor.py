from Preferences import PreferencesDecoder
import PreferenceKeys

# Preferences
decoder = PreferencesDecoder("preferences.json")

class WaterMonitor:
    def __init__(self):
        self._sipSize = decoder.getPreferenceValue(PreferenceKeys.SIP_SIZE)
        self._maxFillLevel = 521 # 521 ml is the capacity of the hydroflask
        self._estimatedFillLevel = self._maxFillLevel
        
    def decreaseFillLevel(self):
        if (self._estimatedFillLevel - self._sipSize) >= 0:
            self._estimatedFillLevel -= self._sipSize
        else:
            self._estimatedFillLevel = 0
        
    def resetFillLevel(self):
        self._estimatedFillLevel = self._maxFillLevel
        
    def getFillLevel(self):
        return self._estimatedFillLevel / self._maxFillLevel