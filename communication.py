"""
                          Coder : ENG.Mahmoud | Eng.Gehad
                          Version : v2.0B
                          version Date :  19 / 5 / 2023
                          Code Type : python 
                          Title : Smart Parking System
                          Interpreter : cPython  v3.11.0 [Compiler : MSC v.1933 AMD64]
"""
import serial
import time
import tkinter as tk
import serial.tools.list_ports

com = None
def com_page(error=0):
    page = tk.Tk()
    page.geometry(f"400x150+500+200")
    page.title("Controller Com page")
    page.iconbitmap('icon_1.ico')

    if(error==1):
        tk.Label(page, text='Wrong com', font=('Arial', 10),fg='red').place(x=5, y=5)

    l_e = tk.Label(page,text='Enter  Com Port',font=('Arial', 14, 'bold'))
    l_e.place(x=130,y=20)

    entry = tk.Entry(page,)
    entry.place(x=110,y=60,height=25,width=200)


    global com
    com = None
    def get_val():
        global com
        com = entry.get()
        page.destroy()

    b = tk.Button(page,text="Enter",
                      font=('Arial', 14, 'bold'),
                      bg='#04B400',
                      fg='white',
                      borderwidth=0,command=get_val)
    b.place(x=180,y=100)

    page.mainloop()


ports = list(serial.tools.list_ports.comports())

for port in ports:
    if "Arduino" in port.description:
        com = port.device

while(1):
    try:
        ser = serial.Serial(com, 9600)
        break
    except:
        com_page(1)
        if(com==None): break

if(com==None): exit()

def prepare_for_parknig(park_n):
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



def park(park_n):
    time.sleep(3)
    data_sent = '2' + chr(park_n)
    ser.write(data_sent.encode('Ascii'))
    ser.flush()
    while True:
        if (ser.in_waiting):
            data_received = str(ser.read(1), 'UTF-8')
            if (data_received == 'D'): break


def getcar(park_n):
    time.sleep(3)
    data_sent= '3'+ chr(park_n)
    ser.write(data_sent.encode('Ascii'))
    ser.flush()
    while True :
        if(ser.in_waiting):
            data_received = str(ser.read(1),'UTF-8')
            if(data_received=='D'): break
