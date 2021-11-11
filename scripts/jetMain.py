import spidev
import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import numpy as np

directionPin = 27
enablePin = 22
stepPin = 17

k_move = 100 #посчитать и всатавить коэффициент м/такт, связующий сдвиг и step()
d = 1 #d - диаметр сопла в м
motorSteps = d * k_move / 100 

measure = []

spi = spidev.SpiDev()

def initSpiAdc():
    spi.open(0, 0)
    spi.max_speed_hz = 1600000
    print ("SPI for ADC has been initialized")


def deinitSpiAdc():
    spi.close()
    print ("SPI cleanup finished")


def getAdc():
    adcResponse = spi.xfer2([0, 0])
    adc = ((adcResponse[0] & 0x1F) << 8 | adcResponse[1]) >> 1
    return(adc)


def initStepMotorGpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([directionPin, enablePin, stepPin], GPIO.OUT)
    print ("GPIO for step motor have been initialized")


def deinitStepMotorGpio():
    GPIO.output([directionPin, enablePin, stepPin], 0)
    GPIO.cleanup()
    print ("GPIO cleanup finished")


def step():
    GPIO.output(stepPin, 0)
    time.sleep(0.005)
    GPIO.output(stepPin, 1)
    time.sleep(0.005)
    

def stepForward(n):
    GPIO.output(directionPin, 1)
    GPIO.output(enablePin, 1)

    for i in range(n):
        step()

    GPIO.output(enablePin, 0)


def stepBackward(n):
    GPIO.output(directionPin, 0)
    GPIO.output(enablePin, 1)

    for i in range(n):
        step()

    GPIO.output(enablePin, 0)


def saveMeasures(measure):
    filename = ('{} mm.txt'.format(n))

    with open(filename, "w") as outfile:
        outfile.write('- Jet Lab\n\n')
        outfile.write('- Experiment date = {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        outfile.write('- Number of samples in measure = {}\n'.format(100))
        outfile.write('- Number of motor steps between measures = {}\n'.format(motorSteps))
        outfile.write('- Measures count = {}\n\n'.format(100))

        
        outfile.write('- adc12bit\n')
        np.savetxt(outfile, np.array(measure).T, fmt='%d')

def move():

    steps = 0    
    while True:
        n = input('Введите 0 (h - справка) > ')

        if n == 'h':
            print('\nСправка:')
            print('     0 - запуск')

        elif n == '0':
            for i in range (100):
                measure.append(getAdc()) 
                stepForward(motorSteps)        
            saveMeasures(measure)
            stepBackward(motorSteps * 100)

        else:
            print('Попробуйте снова/n')


def calibration():
    for i in range (500):
        measure.append(getAdc())
    filename = ('00 Pa.txt'.format(n)) #изменить на max Pa во второй раз

    with open(filename, "w") as outfile:
        outfile.write('- Jet Lab\n\n')
        outfile.write('- Experiment date = {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        outfile.write('- Number of samples in measure = {}\n'.format(1))
        outfile.write('- Number of motor steps between measures = {}\n'.format(motorSteps))
        outfile.write('- Measures count = {}\n\n'.format(500))

        
        outfile.write('- adc12bit\n')
        np.savetxt(outfile, np.array(measure).T, fmt='%d')


def init():
    initSpiAdc() 
    initStepMotorGpio()

def deinit():
    deinitSpiAdc()
    deinitStepMotorGpio()
    
try:
    init()
    calibration() # отключить после калибровки
#    move() #включить после калибровки
finally:
    deinit()
