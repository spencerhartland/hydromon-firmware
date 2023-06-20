import uasyncio as asyncio
from machine import Pin
import utime

_INPUT_PRESS = "press"
_INPUT_HOLD = "hold"
_WATER_DROP_BUTTON_PIN_NUMBER = 42

class Queue:
    def __init__(self):
        self._queue = {}
        self._queueMaxLength = 10
        
    def addInput(self, value):
        inputNumber = len(self._queue)
        if inputNumber < self._queueMaxLength:
            self._queue[str(inputNumber)] = value
        else:
            for i in range((self._queueMaxLength - 1), 1, -1):
                self._queue[str(i)] = self._queue[str(i -1)]
                self._queue["0"] = value
                
    def reset(self):
        self._queue = {}
        
    def getInput(self, number):
        if number >= self._queueMaxLength:
            print("Index for queue out of bounds.")
        else:
            return self._queue[str(number)]
        
    def length(self):
        return len(self._queue)
        
    def __str__(self):
        descStr = "["
        queueLength = len(self._queue)
        for i in range(queueLength):
            descStr += (str(i) + ": " + self._queue[str(i)])
            if i <= (queueLength - 2):
                descStr += ", "
            else:
                descStr += "]"
        return descStr

class InputManager:
    def __init__(self):
        # Begin monitoring for input
        self._inputQueue = Queue()
        self._button = AsyncButton(self._inputQueue)
        
    async def monitorForInput(self):
        """
        Runs a loop on a background thread that monitors for input (button presses).
        Quick tap: user drank water, short press (3 secs): user filled bottle,
        long press (7 secs): enter editing mode.
        """
        while True:
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
            
    def parseInputs(self, onPress, onHold):
        for i in range(self._inputQueue.length()):
            userInput = self._inputQueue.getInput(i)
            if userInput == _INPUT_PRESS:
                onPress()
            elif userInput == _INPUT_HOLD:
                onHold()
                
        self._inputQueue.reset()
        
class AsyncButton:
    def __init__(self, queue):
        self._button = Pin(_WATER_DROP_BUTTON_PIN_NUMBER, Pin.IN, Pin.PULL_UP)
        self._callback = self.inputCallback
        self._button.irq(self.irqHandler, Pin.IRQ_FALLING)
        self._inputQueue = queue
        
    def inputCallback(self):
        initialTime = utime.ticks_ms()
        while self._button.value() == 0:
            pass
        pressTime = utime.ticks_diff(utime.ticks_ms(), initialTime)
        
        # `pressTime` less than 50ms indicates bouncing
        if pressTime > 50 and pressTime < 1000:
            self._inputQueue.addInput(_INPUT_PRESS)
        elif pressTime > 1000:
            self._inputQueue.addInput(_INPUT_HOLD)
        
        # Wait added to 'debounce' the button
        utime.sleep_ms(10)
        
    def irqHandler(self, pin):
        if self._callback:
            self._callback()

# Example of how to use
"""
async def main():
    waterDropButton = InputManager()
    try:
        asyncio.create_task(waterDropButton.monitorForInput())
        while True:
            waterDropButton.parseInputs()
            asyncio.sleep(3)
    except Exception as e:
        print(f"{type(e).__name__}: {str(e)}")
        import sys
        sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
"""
    