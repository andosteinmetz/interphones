import pigpio
import time
pig = pigpio.pi()

#LED class definition
class LED:
    diodeStates = [0, 1]

    def __init__(self, pinNumber, initialState):
        self.pin = pinNumber
        self.state = initialState
        pig.set_mode(pinNumber, pigpio.OUTPUT)

    def toggle(self):
        self.state = not self.state
        pig.write(self.pin, self.diodeStates[self.state])

    def blinkOnce(self):
        pig.write(self.pin, 0)
        time.sleep(0.05)
        pig.write(self.pin, self.diodeStates[1])
        time.sleep(0.05)
        pig.write(self.pin, self.diodeStates[0])

    def turnOff(self):
        self.state = 0;
        pig.write(self.pin, self.diodeStates[0])
