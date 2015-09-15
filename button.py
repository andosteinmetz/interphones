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

#LED instance
firstLED = LED(22, 0)        

#start the program
print 'Make sure a button is connected so that when pressed'
print 'it will connect GPIO port 17 to GND'
raw_input('Press Enter when ready...')

print 'Waiting for falling edge on port 17'

while True:
    try:
        GPIO.wait_for_edge(buttonPin, GPIO.FALLING)
        print 'button pressed'
        #firstLED.blinkOnce()
        firstLED.toggle()
        time.sleep(0.05)

        GPIO.wait_for_edge(buttonPin, GPIO.RISING)
        print 'button released'
        time.sleep(0.05)

    except KeyboardInterrupt:
        GPIO.output(ledPin, GPIO.LOW)
        GPIO.cleanup()

GPIO.output(ledPin, GPIO.LOW)
GPIO.cleanup()
