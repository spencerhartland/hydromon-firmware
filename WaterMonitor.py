import json

class WaterMonitor:
    _FILENAME = "fillLevel.json"
    
    def __init__(self, sipSize):
        self._sipSize = sipSize
        self._maxFillLevel = 521 # 521 ml is the capacity of the hydroflask
        levelFromMemory = self._retrieveFillLevel()
        if levelFromMemory == None:
            self._estimatedFillLevel = self._maxFillLevel
            self._saveFillLevel()
        else:
            self._estimatedFillLevel = levelFromMemory
        
    def decreaseFillLevel(self):
        if (self._estimatedFillLevel - self._sipSize) >= 0:
            self._estimatedFillLevel -= self._sipSize
        else:
            self._estimatedFillLevel = 0
        self._saveFillLevel()
        
    def resetFillLevel(self):
        self._estimatedFillLevel = self._maxFillLevel
        self._saveFillLevel()
        
    def getFillLevel(self):
        return self._estimatedFillLevel / self._maxFillLevel
    
    def _saveFillLevel(self):
        data = {'estimatedFillLevel': self._estimatedFillLevel}
        try:
            with open(self._FILENAME, 'w') as file:
                json.dump(data, file)
        except Exception as e:
            print("An error occurred while saving the data:", str(e))
            
    def _retrieveFillLevel(self):
        try:
            with open(self._FILENAME, 'r') as file:
                data = json.load(file)
            return data.get('estimatedFillLevel', None)
        except Exception as e:
            print("An error occurred while reading the data:", str(e))
            return None