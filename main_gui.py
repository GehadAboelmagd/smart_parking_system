"""
                          Coder : ENG.Mahmoud | Eng.Hager
                          Version : v2.0B
                          version Date :  19 / 5 / 2023
                          Code Type : python 
                          Title : Smart Parking System
                          Interpreter : cPython  v3.11.0 [Compiler : MSC v.1933 AMD64]
"""
import os , sys
import tkinter as tk
from tkinter import messagebox
import random
import ocr_cv
import parking_db as db
import communication as arduino



def message(window,text,type):

    '''
    type:
        0 => error
        1 => message
    '''

    color = '#72fb6f'
    if(type == 0):
        color = '#ffb0b0'

    l_m = tk.Label(window, text=text, font=('Arial',12, 'bold'), bg=color, fg='#2a0000', borderwidth=20)
    l_m.place(x=50, y=50)

    window.update()
    window.after(3000,l_m.destroy)
def park_wait_page():

    global l_8
    global done_b

    # define page
    global p_page_2
    p_page_2 = tk.Tk()
    p_page_2.configure(bg='#000F35')
    p_page_2.geometry(f"{screen_w}x{screen_h}+0+0")
    p_page_2.title("parking Page.2")

    global error_type
    global text_error
    if (error_type == 1):
        message(p_page_2,text_error,0)
        error_type = 0
        text_error = ''

    elif (error_type==2):
        message(p_page_2,text_error,1)
        error_type = 0
        text_error = ''

    #################################


    # wait word
    l_3 = tk.Label(p_page_2, text='WAIT', font=('Arial', 150, 'bold'), bg='#000F35', fg='#FAFF00', borderwidth=0)
    l_3.place(x=(screen_w / 2)-240, y=(screen_h / 2)-150)


    def done():
        l_8.destroy()
        done_b.destroy()

        l_9 = tk.Label(p_page_2, text='WAIT', font=('Arial', 150, 'bold'), bg='#000F35', fg='#FAFF00', borderwidth=0)
        l_9.place(x=(screen_w / 2) - 240, y=(screen_h / 2) - 150)

        def park():
            '''arduino code'''
            try:
                arduino.park(user_info['park_cell']+1)
            except:
                p_page_2.destroy()
                global error_type
                global text_error

                error_type = 1
                text_error = 'Error in arduino'
                root_page()
                return 0

            #########################
            l_9.destroy()
            l_4 = tk.Label(p_page_2, text='DONE', font=('Arial', 150, 'bold'), bg='#000F35', fg='#04B400', borderwidth=0)
            l_4.place(x=(screen_w / 2) - 240, y=(screen_h / 2) - 150)

            def destroy_l():
                p_page_2.destroy();root_page()

            p_page_2.after(5000, destroy_l)

        p_page_2.after(100, park)

    def park_now():
        '''arduino code'''

        try:
            arduino.prepare_for_parknig(user_info['park_cell']+1)
        except:
            p_page_2.destroy()
            global error_type
            global text_error

            error_type = 1
            text_error = 'Error in arduino'
            root_page()
            return 0

        #########################
        l_3.destroy()

        global l_8
        global done_b

        l_8 = tk.Label(p_page_2, text='Park car now', font=('Arial', 50, 'bold'), bg='#000F35', fg='#FAFF00',borderwidth=0)
        l_8.place(x=(screen_w / 2) - 200, y=(screen_h / 4))

        done_b = tk.Button(p_page_2, text='Done', font=('Arial', 16, 'bold'), bg='#04B400', fg='white',borderwidth=0)
        done_b.configure(command=done)
        done_b.place(x=(screen_w / 2) - 70, y=(screen_h / 2) + 50,width=screen_w/9,height=screen_h/15)

    # will change to 10 after add arduino
    p_page_2.after(1000,park_now)

    p_page_2.mainloop()
def park_page_1():
    #define page
    global p_page_1
    p_page_1 = tk.Tk()
    p_page_1.configure(bg='#000F35')
    p_page_1.geometry(f"{screen_w}x{screen_h}+0+0")
    p_page_1.title("parking Page.1")

    global error_type
    global text_error
    if (error_type == 1):
        message(p_page_1,text_error,0)
        error_type = 0
        text_error = ''

    elif (error_type==2):
        message(p_page_1,text_error,1)
        error_type = 0
        text_error = ''

    #################################

    # show password
    l_1 = tk.Label(p_page_1,text='Please save this password',font=('Arial',12),bg='#000F35',fg='#FF4141', borderwidth=0)
    l_1.place(x=(screen_w/2)-90,y=(screen_h/4)-100)


    password = str(random.randint(1000,9999))

    user_info['password']= password
    l_2 = tk.Label(p_page_1,text=f'{password}',font=('Arial',90,'bold'),bg='#000F35',fg='#FAFF00', borderwidth=0)
    l_2.place(x=(screen_w / 2)-125, y=(screen_h / 4))
    #####################

    def b_park_2():
        p_page_1.destroy()
        '''add user_info to DB'''

        user_info['park_cell']=int(db.db_cmd(0,user_info['id'],password)[0])

        global  error_type
        global  text_error
        if(user_info['park_cell']==-1):
            error_type = 1
            text_error = f'User id {user_info["id"]} , NOT found or Already in Parking .'
            root_page()
            return 0

        #########################
        park_wait_page()


    # define continue parking button
    park_2 = tk.Button(p_page_1, text='Park Now',font=('Arial',16,'bold'),bg='#04B400',fg='white', borderwidth=0)
    park_2.configure(command=b_park_2)
    park_2.place(x=(screen_w/2)-70,y=(screen_h/2)+50,width=screen_w/9,height=screen_h/15)
    ###################################

    def b_cancel():
        p_page_1.destroy()
        global error_type
        global text_error

        error_type = 1
        text_error = f'Order is canceled'
        root_page()

    # define cancel button
    cancel = tk.Button(p_page_1, text='Cancel',font=('Arial',16,'bold'),bg='#D40101',fg='white', borderwidth=0)
    cancel.configure(command=b_cancel)
    cancel.place(x=(screen_w/2)-70,y=(screen_h/4)*3-50,width=screen_w/9,height=screen_h/15)
    ###################################

    p_page_1.mainloop()
def park_button():

    if(db.db_cmd(2)) :
        message(root,'Parking is full',0)
        return 0

    root.destroy()
    ocr_cv.testing_mode = False
    id = ocr_cv.ocr_main()
    #id=('11111111111111',True)
    user_info['id']=id[0]

    global error_type
    global text_error

    if(id[1]):
        error_type = 2
        text_error = f'Your id is {id[0]}'
        park_page_1()
    else:
        error_type = 1
        text_error = 'Not found id , Try again'
        root_page()
def get_wait_page():

    global l_g_8

    # define page
    global g_page_2
    g_page_2 = tk.Tk()
    g_page_2.configure(bg='#000F35')
    g_page_2.geometry(f"{screen_w}x{screen_h}+0+0")
    g_page_2.title("GET Page.2")

    global error_type
    global text_error
    if (error_type == 1):
        message(g_page_2,text_error,0)
        error_type = 0
        text_error = ''

    elif (error_type==2):
        message(g_page_2,text_error,1)
        error_type = 0
        text_error = ''
    #################################


    # wait word
    l_3 = tk.Label(g_page_2, text='WAIT', font=('Arial', 150, 'bold'), bg='#000F35', fg='#FAFF00', borderwidth=0)
    l_3.place(x=(screen_w / 2)-240, y=(screen_h / 2)-150)


    def done():
        '''arduino code'''
        arduino.getcar(int(get_info[0])+1)
        #########################
        l_3.destroy()
        l_4 = tk.Label(g_page_2, text='DONE', font=('Arial', 150, 'bold'), bg='#000F35', fg='#04B400', borderwidth=0)
        l_4.place(x=(screen_w / 2) - 240, y=(screen_h / 2) - 150)

        def destroy_l():
            g_page_2.destroy();root_page()

        g_page_2.after(5000, destroy_l)


    # will change to 10 after add arduino
    g_page_2.after(100,done)

    g_page_2.mainloop()
def pay_page():
    global pay_p
    pay_p = tk.Tk()
    pay_p.title("pay")
    pay_p.configure(bg='#000F35')
    pay_p.geometry(f"{screen_w}x{screen_h}")

    global error_type
    global text_error
    if (error_type == 1):
        message(pay_p,text_error,0)
        error_type = 0
        text_error = ''

    elif (error_type==2):
        message(pay_p,text_error,1)
        error_type = 0
        text_error = ''

    def pay_b_func():
        pay_p.destroy()
        get_wait_page()

    tk.Label(pay_p,text=f"Time: {get_info[3]}  hours ",font=('Arial',20,'bold'),bg='#000F35',fg='white').place(x=(screen_w / 2)-100, y=(screen_h / 4)+100)
    tk.Label(pay_p,text=f"Cost:  {get_info[2]}  $",font=('Arial',20,'bold'),bg='#000F35',fg='white').place(x=(screen_w / 2)-100, y=(screen_h /4)+200 )
    pay_b=tk.Button(pay_p,
               text="pay",
                font=('Arial', 16, 'bold'),
                bg='#04B400',
                fg='white',
                borderwidth=0,
                command=pay_b_func)
    pay_b.place(x=(screen_w / 2) - 70, y=(screen_h / 4) * 3 - 50,width=screen_w/9,height=screen_h/15)

    pay_p.mainloop()
def password_page():
    password_p = tk.Tk()
    password_p.title("get car")
    password_p.configure(bg='#000F35')
    password_p.geometry(f"{screen_w}x{screen_h}")

    global error_type
    global text_error
    if (error_type == 1):
        message(password_p,text_error,0)
        error_type = 0
        text_error = ''

    elif (error_type==2):
        message(password_p,text_error,1)
        error_type = 0
        text_error = ''

    def validate_numeric_input(value):
        if value.isdigit():
            return True
        elif value == "":
            return True
        else:
            return False

    validate_command = password_p.register(validate_numeric_input)


    tk.Label(password_p, text='ID', font=('Arial', 18, 'bold'), bg='#000F35', fg='#BBC2FE').place(
        x=(screen_w / 2)-10, y=200)

    entry_id = tk.Entry(password_p,font=('Arial', 14, 'bold'), validate="key", validatecommand=(validate_command, "%P"))
    entry_id.place(x=(screen_w / 2)-150, y=240,width=300,height=30)


    tk.Label(password_p, text='PASSWORD', font=('Arial', 18, 'bold'), bg='#000F35', fg='#BBC2FE').place(
        x=(screen_w / 2) -70, y=300)

    entry_password = tk.Entry(password_p, font=('Arial', 14, 'bold'), validate="key",validatecommand=(validate_command, "%P"))
    entry_password.place(x=(screen_w / 2) - 150, y=340, width=300, height=30)

    def enter_b_func():
        id_user = entry_id.get()
        password = entry_password.get()

        if(id_user == "" or password == ""):
            messagebox.showwarning("Warning", "EMPTY INPUT")
            return 0

        global get_info

        get_info = db.db_cmd(1,id_user,password)
        #get_info = (2, True, 50, 5)

        if (get_info[0] == -1):
            messagebox.showwarning("Warning", "Not exist user")
            return 0
        password_p.destroy()
        pay_page()


    enter_b = tk.Button(password_p,
                      text="Enter",
                      font=('Arial', 16, 'bold'),
                      bg='#04B400',
                      fg='white',
                      borderwidth=0,
                      command=enter_b_func)
    enter_b.place(x=(screen_w / 2) - 70, y=(screen_h / 4) * 3 - 150,width=screen_w/9,height=screen_h/15)

    def cancel():
           password_p.destroy()
           get_car_page()

    btn3=tk.Button(password_p,
                   text="Cancel",
                   font = ('Arial', 16, 'bold'),
                   bg = '#D40101',
                   fg = 'white',
                   borderwidth = 0,
                   command=cancel)
    btn3.place(x=(screen_w/2)-70,y=(screen_h/4)*3-50,width=screen_w/9,height=screen_h/15)

    password_p.mainloop()
def get_car_page():
  global get_car

  get_car=tk.Tk()
  get_car.title("get car")
  get_car.configure(bg='#000F35')
  get_car.geometry(f"{screen_w}x{screen_h}")

  global error_type
  global text_error
  if (error_type == 1):
      message(get_car, text_error, 0)
      error_type = 0
      text_error = ''

  elif (error_type == 2):
      message(get_car, text_error, 1)
      error_type = 0
      text_error = ''

  def ocr_b():
      get_car.destroy()

      '''OCR'''
      ocr_cv.testing_mode = False

      global ocr_info
      global get_info
      ocr_info = ocr_cv.ocr_main()
      #ocr_info=('11111111111111',True)

      if (ocr_info[1]):

          get_info = db.db_cmd(1,ocr_info[0])
          #get_info = (2, True, 50, 5)

          global error_type
          global text_error

          if (get_info[0] == -1):
              error_type = 1
              text_error = f'Not found id : {ocr_info[0]},Use password'
              get_car_page()
              return 0

          error_type = 2
          text_error = f'id : {ocr_info[0]}'
          pay_page()
      else:
          error_type = 1
          text_error = f'Not found id : {ocr_info[0]},Use password'
          get_car_page()
      ##############

  def password_b():
      get_car.destroy()
      password_page()

  tk.Label(get_car,
       text="Get it by",font=('Arial',30,'bold'),bg='#000F35',fg='#FF0000').place(x=(screen_w/8),y=(screen_h/2)-100)

  btn1=tk.Button(get_car,
                text="ID Card",
                font=('Arial', 16, 'bold'),
                bg='#04B400',
                fg='white', borderwidth=0,
                command=ocr_b)
  btn1.place(x=(screen_w/3),y=(screen_h/2)-90,width=screen_w/9,height=screen_h/15)


  btn2=tk.Button(get_car,
                text="password",
                font=('Arial', 16, 'bold'),
                bg='#04B400',
                fg='white', borderwidth=0,
                command=password_b)
  btn2.place(x=(screen_w/3)*2-120,y=(screen_h/2)-90,width=screen_w/9,height=screen_h/15)


  def cancel():
        get_car.destroy()
        root_page()

  btn3=tk.Button(get_car,
                text="Cancel",
                font = ('Arial', 16, 'bold'),
                bg = '#D40101',
                fg = 'white',
                borderwidth = 0,
                command=cancel)
  btn3.place(x=(screen_w/2)-70,y=(screen_h/4)*3-50,width=screen_w/9,height=screen_h/15)

  get_car.mainloop()
def root_page():
    global root
    root = tk.Tk()

    # Get the screen geometry
    global screen_w
    global screen_h
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # Set the dimensions of the root
    root.configure(bg='#000F35')
    root.geometry(f"{screen_w}x{screen_h}+0+0")

    root.title("Home Page")

    global error_type
    global text_error
    if (error_type==1):
        message(root,text_error,0)
        error_type = 0
        text_error=''

    elif (error_type==2):
        message(root,text_error,1)
        error_type = 0
        text_error=''


    #define parking button
    b_park = tk.Button(root, text='Park',font=('Arial',16,'bold'),bg='#04B400',fg='white', borderwidth=0)
    b_park.configure(command=park_button)
    b_park.place(x=(screen_w/2)-70,y=(screen_h/2)-50,width=screen_w/9,height=screen_h/15)
    ###################################

    def get_car_button(): root.destroy();get_car_page()
    #define getcar button
    b_get = tk.Button(root, text='GetCar',font=('Arial',16,'bold'),bg='#D40101',fg='white', borderwidth=0)
    b_get.configure(command=get_car_button)
    b_get.place(x=(screen_w/2)-70,y=(screen_h/4)*3-50,width=screen_w/9,height=screen_h/15)
    ###################################


    root.mainloop()



if __name__ == "__main__":

    error_type = 0 # 0=> no error , 1=> error , 2=> message
    text_error = ''

    user_info ={'id':None,'password':None,'park_cell':None}
    root_page()
