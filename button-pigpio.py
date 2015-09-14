#import RPi.GPIO as GPIO
import pigpio
import time

#set the button pin
buttonPin = 17
ledPin = 22

#configure GPIO
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#create + configure pigpio instance
pig = pigpio.pi()
pig.set_pull_up_down(buttonPin, pigpio.PUD_UP)


#LED class definition
class LED:
    diodeStates = [0, 1]

    def __init__(self, pinNumber, initialState):
        self.pin = pinNumber
        self.state = initialState
        pig.set_mode(pinNumber, pigpio.OUTPUT)

    def toggle(self):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0
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
        pig.wait_for_edge(buttonPin, pigpio.FALLING_EDGE)
        print 'button pressed'
        firstLED.blinkOnce()
        firstLED.toggle()
        time.sleep(0.05)

        pig.wait_for_edge(buttonPin, pigpio.RISING_EDGE)
        print 'button released'
        time.sleep(0.05)

    except KeyboardInterrupt:
        firstLED.turnOff();
        pig.stop()

firstLED.turnOff()
pig.stop()
