import tkinter as tk
import ocr_cv
import random
import communication


def park_wait_page():
    # define page
    global p_page_2
    p_page_2 = tk.Tk()
    p_page_2.configure(bg='#000F35')
    p_page_2.geometry(f"{screen_w}x{screen_h}+0+0")
    p_page_2.title("parking Page.2")
    #################################


    # wait word
    l_3 = tk.Label(p_page_2, text='WAIT', font=('Arial', 150, 'bold'), bg='#000F35', fg='#FAFF00', borderwidth=0)
    l_3.place(x=(screen_w / 2)-240, y=(screen_h / 2)-150)


    def done():
        '''arduino code'''

        #########################
        l_3.destroy()
        l_4 = tk.Label(p_page_2, text='DONE', font=('Arial', 150, 'bold'), bg='#000F35', fg='#04B400', borderwidth=0)
        l_4.place(x=(screen_w / 2) - 240, y=(screen_h / 2) - 150)

        def destroy():  p_page_2.destroy();root_page()
        p_page_2.after(5000,destroy)


    # will change to 10 after add arduino
    p_page_2.after(5000,done)

    p_page_2.mainloop()
def park_page_1():
    #define page
    global p_page_1
    p_page_1 = tk.Tk()
    p_page_1.configure(bg='#000F35')
    p_page_1.geometry(f"{screen_w}x{screen_h}+0+0")
    p_page_1.title("parking Page.1")
    #################################

    # show password
    l_1 = tk.Label(p_page_1,text='Please save this password',font=('Arial',12),bg='#000F35',fg='#FF4141', borderwidth=0)
    l_1.place(x=(screen_w/2)-90,y=(screen_h/4)-100)

    '''check generated password not in DB'''
    ################
    password = random.randint(1000,9999)
    user_info['password']=password
    l_2 = tk.Label(p_page_1,text=f'{password}',font=('Arial',90,'bold'),bg='#000F35',fg='#FAFF00', borderwidth=0)
    l_2.place(x=(screen_w / 2)-125, y=(screen_h / 4))
    #####################

    def b_park_2():
        p_page_1.destroy()
        '''add user_info to DB'''
        #########################
        park_wait_page()


    # define continue parking button
    park_2 = tk.Button(p_page_1, text='Park Now',font=('Arial',14,'bold'),bg='#04B400',fg='white', borderwidth=0)
    park_2.configure(command=b_park_2)
    park_2.place(x=(screen_w/2)-70,y=(screen_h/2)+50,width=140,height=40)
    ###################################

    def b_cancel(): p_page_1.destroy();root_page()

    # define cancel button
    cancel = tk.Button(p_page_1, text='Cancel',font=('Arial',14,'bold'),bg='#D40101',fg='white', borderwidth=0)
    cancel.configure(command=b_cancel)
    cancel.place(x=(screen_w/2)-70,y=(screen_h/4)*3-50,width=140,height=40)
    ###################################

    p_page_1.mainloop()

def park_button():
    root.destroy()
    ocr_cv.testing_mode = False
    ocr_cv.max_rec_frametime_min_fps = [-1, 1000]
    ocr_cv.min_rec_frametime_max_fps = [10000, -1]
    id = ocr_cv.ocr_main()
    # id = (0,True) -> test

    user_info['id']=id[0]

    if(id[1]):
        park_page_1()
    else:
        root_page()

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

    #define parking button
    b_park = tk.Button(root, text='Park',font=('Arial',14,'bold'),bg='#04B400',fg='white', borderwidth=0)
    b_park.configure(command=park_button)
    b_park.place(x=(screen_w/2)-70,y=(screen_h/2)-50,width=140,height=40)
    ###################################

    #define getcar button
    b_get = tk.Button(root, text='GetCar',font=('Arial',14,'bold'),bg='#D40101',fg='white', borderwidth=0)
    #b_get.configure(command=)
    b_get.place(x=(screen_w/2)-70,y=(screen_h/4)*3-50,width=140,height=40)
    ###################################


    root.mainloop()

if __name__ == "__main__":

    user_info ={'id':None,'password':None,'park_cell':None}
    root_page()
