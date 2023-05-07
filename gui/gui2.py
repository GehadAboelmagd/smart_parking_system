import tkinter as tk
import ocr_cv


def pay_page():

    tk.Label( text="Time:  4 hours ",font=('Arial',15,'bold'),bg='AntiqueWhite1',fg='purple').place(x=260,y=120)
    x=tk.Label(text="price:          6 $",font=('Arial',15,'bold'),bg='AntiqueWhite1',fg='purple').place(x=260,y=149)
    b=tk.Button(window,
               text="pay",
                font=('Arial',15,'bold'),
                bg='royal blue',
                fg='white',
                 width=5,
                height=1)
    b.pack(pady=180)

def get_car_page():
  root.destroy()
  newWindow=tk.Tk()
  newWindow.title("Hello car")
  newWindow.configure(bg='#000F35')
  newWindow.geometry(f"{screen_w}x{screen_h}")

  def face():
      newWindow.destroy()

      '''OCR'''
      ocr_cv.testing_mode = False

      #id = ocr_cv.ocr_main()
      id=('54302518496307',True)

      if (id[1]):
         # pay
         pass
      else:
          get_car_page()
      ##############



  tk.Label(newWindow,
       text="Get it by",font=('Arial',15,'bold'),bg='AntiqueWhite1',fg='purple').place(x=30,y=150)

  btn1=tk.Button(newWindow,
              text="ID Card",
                font='Arial',
                bg='RoyalBlue3',
                fg='white',
                command=face)
  btn1.place(x=200,y=150)


  btn2=tk.Button(newWindow,
                text="password",
                font='Arial',
                 bg='RoyalBlue3',
                 fg='white')
  btn2.place(x=290,y=150)

  def cancel():
        newWindow.destroy()
        root()

  btn3=tk.Button(newWindow,
                text="Cancel",
                font='Arial',
                bg='purple',
                fg='white',
                command=cancel)
  btn3.place(x=240,y=220)

def root():
    global window
    global screen_w
    global screen_h
    window = tk.Tk()
    window.title("Hello car")

    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    # Set the dimensions of the root
    window.configure(bg='#000F35')
    window.geometry(f"{screen_w}x{screen_h}")

    btn = tk.Button(window,
              text="Get the car",
              font=('Arial',15,'bold'),
              bg='violet red',
              fg='white',
              command=get_car_page)
    btn.pack(pady=150)

    window.mainloop()

if __name__ == '__main__':
    root()