import _thread
from machine import Pin

QUICK_TAP = "quick-tap"
SHORT_PRESS = "short-press"
LONG_PRESS = "long-press"

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

class InputHandler:
    def __init__(self):
        # Begin monitoring for input
        self._inputQueue = Input.Queue()
        _thread.start_new_thread(self.monitorForInput, (self.inputQueue, ))
        
    def monitorForInput(self):
        """
        Runs a loop on a background thread that monitors for input (button presses).
        Quick tap: user drank water, short press (3 secs): user filled bottle,
        long press (7 secs): enter editing mode.
        """
        button = Pin(10, Pin.IN, Pin.PULL_UP)
        sLock.acquire()
        while True:
            try:
                if not button.value() == True:
                    sleep(1.0)
                    if not button.value() == True:
                        # If the button is still pressed after 1 sec of waiting, check for short press.
                        sleep(1.0)
                        if not button.value() == True:
                            # Officially a short press, check that the user has let go after 3 sec.
                            sleep(2.0)
                            if not button.value() == True:
                                # Still holding... check for a long press
                                sleep(2.0)
                                if not button.value() == True:
                                    # Long press
                                    self._inputQueue.addInput(LONG_PRESS)
                            else:
                                # Short press
                                self._inputQueue.addInput(SHORT_PRESS)
                    else:
                        # Quick tap
                        self._inputQueue.addInput(QUICK_TAP)
            except KeyboardInterrupt:
                sys.exit(0)
        sLock.release()
    
    def parseInputs(self):
        # Check for inputs
        for i in range(self._inputQueue.length()):
            userInput = self._inputQueue.getInput(i)
            if userInput == QUICK_TAP:
                # Quick tap: user drank water
                monitor.decreaseFillLevel()
                displayWaterDropIcon()
                timeSincePreviousAlert += 1
            elif userInput == SHORT_PRESS:
                # Short press: user refilled the bottle
                monitor.resetFillLevel()
                displayWaterDropAnimation()
                displayFillLevel(True)
                timeSincePreviousAlert += 1.0
            elif userInput == LONG_PRESS:
                # Long press: enter editing mode
                server = Server()
                server.listenForRequests()
                server.shutdown()
        inputQueue.reset()


        """
        TODO: Fix `parseInputs` by adding parameters that take functions as input and call them for each
        input type. Implement input handling using `InputHandler` in `main.py` and `server.py`.
        """