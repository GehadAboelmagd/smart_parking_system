import serial
import time

def prepare_for_parknig(park_n):
    ser=serial.Serial('COM7',9600)
    # open serial communication port
    # the COM number differs from one device to another
    time.sleep(3)
    # time_delay to ensure the serial port is ready for communication
    data_sent= '1' + chr(park_n)
    ser.write(data_sent.encode('Ascii'))
    ser.flush()  #wait to ensure data is sent
    while True:
        if(ser.in_waiting):  # wait until data is available on cpu serial port
            data_received=str(ser.read(1),'UTF-8')
            # the serial.read is capable of reading up to 100 bytes
            if(data_received=='D'): break
    ser.close()


def park(park_n):
    ser = serial.Serial('COM7', 9600)
    time.sleep(3)
    data_sent = '2' + chr(park_n)
    ser.write(data_sent.encode('Ascii'))
    ser.flush()
    while True:
        if (ser.in_waiting):
            data_received = str(ser.read(1), 'UTF-8')
            if (data_received == 'D'): break
    ser.close()


def getcar(park_n):
    ser = serial.Serial('COM7', 9600)
    time.sleep(3)
    data_sent= '3'+ chr(park_n)
    ser.write(data_sent.encode('Ascii'))
    ser.flush()
    while True :
        if(ser.in_waiting):
            data_received = str(ser.read(1),'UTF-8')
            if(data_received=='D'): break
    ser.close()