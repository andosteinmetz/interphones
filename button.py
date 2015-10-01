import RPi.GPIO as GPIO
import time

#set the button pin
buttonPin = 17

#configure GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#LED class definition
class LED:
    diodeStates = [GPIO.LOW, GPIO.HIGH]

    def __init__(self, pinNumber, initialState):
        self.pin = pinNumber
        self.state = initialState
        GPIO.setup(pinNumber, GPIO.OUT)

    def toggle(self):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0
        GPIO.output(self.pin, self.diodeStates[self.state])

    def blinkOnce(self):
        GPIO.output(self.pin, self.diodeStates[1])
        time.sleep(0.05)
        GPIO.output(self.pin, self.diodeStates[0])

#TODO -  create a button class. may be portable to the actual project

class momentarySwitch:

    def __init__(self, pinNumber, triggerLow):
        self.pin = pinNumber
        self.triggerLow = triggerLow
        
        if self.triggerLow:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.pressed = GPIO.FALLING
            self.released = GPIO.RISING
            
        else:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.pressed = GPIO.RISING
            self.released= GPIO.FALLING

    def listen(self):
        GPIO.wait_for_edge(self.pin, self.pressed)
        print 'button pressed'
        time.sleep(0.05)

        GPIO.wait_for_edge(buttonPin, self.released)
        print 'button released'
        time.sleep(0.05)
            

#LED instance
firstLED = LED(22, 0)

#Hall Effect receiver switch
receiverSwitch = momentarySwitch(buttonPin, False)
button = momentarySwitch(23, True)

#start the program
raw_input('Press Enter when ready...')

print 'Waiting for falling edge on port 17'

while True:
    try:
        receiverSwitch.listen()
        # Problems watching multiple buttons
        #button.listen()

    except KeyboardInterrupt:
        GPIO.output(ledPin, GPIO.LOW)
        GPIO.cleanup()

GPIO.output(ledPin, GPIO.LOW)
GPIO.cleanup()
