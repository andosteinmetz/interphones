# python utility for decoding matrix keypad data
# using pigpio https://github.com/joan2937/pigpio

############################
# TO DO - redesign this to respond to interrupts (falling edge on row)
# then maybe I only have to check cols on incoming row input?
############################

import pigpio
import time

pig = pigpio.pi()

class Keypad:
    colCount = 0
    rowCount = 0

    cols = []
    rows = []

    #columnPins and rowPins are arrays of integers representing the input pins numbers.
    def __init__(self, columnPins, rowPins):
        self.cols = columnPins
        self.rows = rowPins
        self.colCount = len(columnPins)
        self.rowCount = len(rowPins)
        self.setup()
        
    def setup(self):
        #set columns as low output
        for i in range(self.colCount):
            pig.set_mode(self.cols[i], pigpio.OUTPUT)
            pig.write(self.cols[i], 0)

        #set rows as input with pull up resistor
        for j in range(self.rowCount):
            pig.set_mode(self.rows[j], pigpio.INPUT)
            pig.set_pull_up_down(self.rows[j], pigpio.PUD_UP)

    def getKey(self):
        # returns an array with the row and column values in that order
        self.setup()
        keyInput = []
        rowVal = -1
        for i in range(self.rowCount):
            tmpRead = pig.read(self.rows[i])
            if tmpRead == 0:
                rowVal = i

        # if rowVal is greater than the row count - 1 or less than zero, exit
        if rowVal < 0 or rowVal > self.colCount -1:
            self.exit()
            return

        keyInput.append(rowVal)

        #convert columns to input
        for j in range(self.colCount):
            col = self.cols[j]
            pig.set_mode(col, pigpio.INPUT)
            pig.set_pull_up_down(col, pigpio.PUD_DOWN)

        #Switch the i-th row found from scan to output
        pig.set_mode(self.rows[rowVal], pigpio.OUTPUT)
        pig.write(self.rows[rowVal], 1)

        # Scan colums for still-pushed key
        colVal = -1
        for j in range(self.colCount):
            tmpRead = pig.read(self.cols[j])
            if tmpRead == 1:
                colVal = j

        if colVal < 0 or colVal > self.colCount - 1:
            self.exit()
            return

        # return column and row numbers
        keyInput.append(colVal)
        keyVal = (keyInput[0] * self.colCount) + keyInput[1]
        self.exit()
        return keyVal 

    def exit(self):
        for i in range(self.rowCount):
            pig.set_mode(self.rows[i], pigpio.INPUT)
            pig.set_pull_up_down(self.rows[i], pigpio.PUD_UP)
        for j in range(self.colCount):
            pig.set_mode(self.cols[j], pigpio.INPUT)
            pig.set_pull_up_down(self.cols[j], pigpio.PUD_UP)
                       
if __name__ == '__main__':
    #configure GPIO
    myCols = [6,13,19,26]
    myRows = [21,20,16,12]

    #create an instance
    kp = Keypad(myCols, myRows)

    #Loop while waiting for a keypress
    try:
        myInput = None
        while myInput == None:
            myInput = kp.getKey()

        #print the result
        print myInput
        pig.stop()

    except KeyboardInterrupt:
        pig.stop()
