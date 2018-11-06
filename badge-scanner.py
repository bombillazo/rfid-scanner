# External library imports
import RPi.GPIO as GPIO
import array, threading, time, requests, sys, re
from signal import pause

# Pin definitions
D0 = 26 # BCM pin 26 (BOARD pin 37, GR)
D1 = 19 # BCM pin 19 (BOARD pin 35, WH)
BZ = 21 # BCM pin 21 (BOARD pin 40, YE)
GR = 20 # BCM pin 20 (BOARD pin 38, OR)
RD = 16 # BCM pin 16 (BOARD pin 36, BR)

# Pin Setup
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(D0, GPIO.IN) # Data 0 pin set as input
GPIO.setup(D1, GPIO.IN) # Data 1 pin set as input
GPIO.setup(BZ, GPIO.OUT) # Buzzer pin set as output
GPIO.setup(GR, GPIO.OUT) # Green LED pin set as output
GPIO.setup(RD, GPIO.OUT) # Red LED set as output

# Constants
TIMER_COUNT = 0.25

# Variable initializations
bits = []
userid = 0
readStarted = False
url = ""

# Reading functions
def checkReadStatus():
    global timer, readStarted
    if(readStarted):
        timer.cancel()
        timer = threading.Timer(TIMER_COUNT,readComplete)
        timer.start()
    else:
        readStarted = True
        timer.start()

def readD0(D0):
    global readStarted
    bits.append(0)
    checkReadStatus()

def readD1(D1):
    global readStarted
    bits.append(1)
    checkReadStatus()

def readComplete():
    global bits, userid
    if(len(bits) == 37):
        GPIO.output(GR, GPIO.LOW)
        bitsTotal = ''.join(str(b) for b in bits)
        bitsID = bitsTotal[12:-1]
        print('Card read succesfully. User card number = ' + str(int(bitsID,2)))
        userid = int(bitsID,2)
        h = {'Content-Type': 'application/json',}
        d = '{"cardId": "' + str(userid)  + '"}'
        try:
            r = requests.post(url, headers=h, data=d)
            if(r.status_code == 200):
                print('Data sucessfully sent to server.')
                ok()
            else:
                print('Error returned by server, please check server logs for more info.')
                error()
        except:
            print('Error sending data to server, please check network configuration.')
            error()
    else:
        print('Error reading or decoding data, please swipe card again.')
        error()
    bits = []
    readStarted = False

# Status functions
def error():
    for i in range(3):
        GPIO.output(BZ, GPIO.LOW)
        GPIO.output(GR, GPIO.LOW)
        GPIO.output(RD, GPIO.LOW)
        time.sleep(.35)
        GPIO.output(BZ, GPIO.HIGH)
        GPIO.output(GR, GPIO.HIGH)
        GPIO.output(RD, GPIO.HIGH)
        time.sleep(0.05)

def ok():
    GPIO.output(GR, GPIO.LOW)
    for i in range(2):
        beep(0.35,0.25)
    time.sleep(2)
    GPIO.output(GR, GPIO.HIGH)

# Helper functions
def beep(s_on, s_off):
    GPIO.output(BZ, GPIO.LOW)
    time.sleep(s_on)
    GPIO.output(BZ, GPIO.HIGH)
    time.sleep(s_off)

# Main

try:
    
    timer = threading.Timer(TIMER_COUNT, readComplete)
    GPIO.add_event_detect(D0, GPIO.FALLING, callback=readD0)
    GPIO.add_event_detect(D1, GPIO.FALLING, callback=readD1)

    GPIO.output(BZ, GPIO.HIGH)
    GPIO.output(GR, GPIO.HIGH)
    GPIO.output(RD, GPIO.HIGH)
    
    if(len(sys.argv) != 2):
        print('Please pass the app URL as an argument when running this file.')
        GPIO.cleanup()
        sys.exit()
    url = sys.argv[1]()
        sys.exit()
    
    print('**** RFID CARD SCANNER ***\nPress Ctrl+C to end.\nReady to scan...')
    pause()
    GPIO.cleanup()
    
except KeyboardInterrupt:
    GPIO.cleanup()
    print('\nProgram End.')
