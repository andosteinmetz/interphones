#import RPi.GPIO as GPIO
import pigpio
import time

#set the button pin
buttonPin = 17
ledPin = 22

#create + configure pigpio instance
pig = pigpio.pi()

#initialize timestamp
time_stamp = time.time()

#LED class definition
class LED:
    diodeStates = [0, 1]

    def __init__(self, pinNumber, initialState):
        self.pin = pinNumber
        self.state = initialState
        pig.set_mode(pinNumber, pigpio.OUTPUT)

    def toggle(self):
        #if self.state == 0:
        #    self.state = 1
        #else:
        #    self.state = 0
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

class momentarySwitch:
    #
    #bouncetime is in fractions of a second ie 0.2 is 200ms
    #triggerLow is a boolean value indicating whether the switch is active on low or high voltage
    #callback functions should take at least 3 args - gpio, level and tick
    #
    def __init__(self, pinNumber, triggerLow, callback=None, release_callback=None, bouncetime=0.3):
        self.pin = pinNumber
        self.triggerLow = triggerLow
        self.pud = pigpio.PUD_UP if triggerLow else pigpio.PUD_DOWN
        self.pressed = pigpio.FALLING_EDGE if triggerLow else pigpio.RISING_EDGE
        self.released = pigpio.RISING_EDGE if triggerLow else pigpio.FALLING_EDGE
        self.callback = debounce(bouncetime, callback)
        self.release_callback = debounce(bouncetime, release_callback)
        
        pig.set_mode(self.pin, pigpio.INPUT)
        pig.set_pull_up_down(self.pin, self.pud)

    def listen(self):
        if self.callback:
            self.listening_for_press = pig.callback(self.pin, self.pressed, self.callback)
        if self.release_callback:
            self.listening_for_release = pig.callback(self.pin, self.released, self.release_callback)

    def unlisten(self):
        self.listening_for_press.cancel()
        self.listening_for_release.cancel()

def receiverPickedUp(gpio, level, tick):
    print 'The receiver has been picked up'
    button.listen()

def receiverHungUp(gpio, level, tick):
    print 'The receiver has been hung up'
    button.unlisten()

def buttonPressed(gpio, level, tick):
    print(gpio, level, tick)

def debounce(bouncetime, func, *args):
    def debounced(*args):
        global time_stamp
        time_now = time.time()
        if (time_now - time_stamp) >= bouncetime:
            func( *args )
        time_stamp = time_now
    return debounced

receiverSwitch = momentarySwitch(17, False, receiverPickedUp, receiverHungUp, 0)
button = momentarySwitch(23, True, buttonPressed, 0.3)


#LED instance
firstLED = LED(22, 0)        

#start the program
raw_input('Press Enter when ready...')

print 'Waiting for input'

receiverSwitch.listen()

while True:
    try:
        time.sleep(0.01)

    except KeyboardInterrupt:
        firstLED.turnOff()
        pig.stop()

firstLED.turnOff()
pig.stop()
