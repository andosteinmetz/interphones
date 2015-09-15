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
        self.setup()
        
    def setup(self):
        #set columns as low output
        for i in range(len(self.cols)):
            pig.set_mode(self.cols[i], pigpio.OUTPUT)
            pig.write(self.cols[i], 0)

        #set rows as input with pull up resistor
        for j in range(len(self.rows)):
            pig.set_mode(self.rows[j], pigpio.INPUT)
            pig.set_pull_up_down(self.rows[j], pigpio.PUD_UP)

    def getKey(self):
        self.setup()
        keyInput = []
        rowVal = -1
        for i in range(len(self.rows)):
            tmpRead = pigpio.read(self.rows[i])
            if tmpRead == 0:
                rowVal = i

        # if rowVal is greater than the row count - 1 or less than zero, exit
        if rowVal < 0 or rowVal > len(self.cols) -1:
            self.exit()
            return

        #convert columns to input
        for j in range(len(self.cols)):
            col = self.cols[j]
            pig.setmode(col, pigpio.INPUT)
            pig.set_pull_up_down(col, pigpio.PUD_DOWN)

        #Switch the i-th row found from scan to output
        pigpio.set_mode(self.rows[rowVal], pigpio.OUTPUT)
        pigpio.write(self.rows[rowVal], 1)

        # Scan colums for still-pushed key
        colVal = -1
        for j in range(len(self.cols)):
            tmpRead = pig.read(self.cols[j])
            if tmpRead == 1:
                colVal = j

        if colVal < 0 or colVal > self.cols - 1:
            self.exit()
            return

        keyInput.append(rowVal)
        keyInput.append(colVal)

    def exit(self):
        for i in range(len(self.rows)):
            pig.set_mode(self.row[i], pigpio.INPUT)
            pig.set_pull_up_down(self.row[i], pigpio.PUD_UP)
        for j in range(len(self.cols)):
            pig.set_mode(self.cols[j], pigpio.INPUT, pigpio.PUD_UP)
            

        return input
                       
