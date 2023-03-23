import serial

ser = serial.Serial('COM7',9600)
def getcar(park_n):
    c= '2'+ chr(park_n);
    ser.write(c.encode())
    ser.flush()
    while True :
        if(ser.in_waiting):
            d = str(ser.read(1),'UTF-8')
            if(d=='D'): break

    print('done')

# test function
while True :
    c = int(input('Enter number of parking : '))
    getcar(c)
