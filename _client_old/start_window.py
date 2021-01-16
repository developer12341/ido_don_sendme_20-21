import tkinter,threading

def main(self):
    def close():
        self.close_protocol = True
        threading._start_new_thread(window.destroy,tuple())

    def register_function():
        self.cur_window = "register"
        window.destroy()
    
    def login_function():
        self.cur_window = "login"
        window.destroy()
    
    window = tkinter.Tk()
    window.geometry("400x400")
    window.title("sendme")
    window.protocol("WM_DELETE_WINDOW",close)

    lable1 = tkinter.Label(window, text="Welcome to sendme!",font="arial 20 bold")
    lable1.grid(row=0,column=0,columnspan=2,sticky="NWE",pady=20)

    window.columnconfigure(0,weight=1)
    window.columnconfigure(1,weight=1)
    window.rowconfigure(1,weight=1)

    register_frame = tkinter.Frame(window)
    register_frame.grid(row=1,column=0,sticky="WESN",padx=20,pady=20)
    
    register_frame.rowconfigure(0,weight=1)
    register_frame.rowconfigure(2,weight=1)
    register_frame.columnconfigure(0,weight=1)

    register_text = tkinter.Label(register_frame,text="new to sendme?",font="20")
    register_text.grid(row=0,column=0,sticky="WESN")
    tkinter.Button(register_frame,text= "register",font=20,command=register_function).grid(row=1,column=0,sticky="SN")


    login_frame = tkinter.Frame(window)
    login_frame.grid(row=1,column=1,sticky="WESN",padx=20,pady=20)
    
    
    login_frame.rowconfigure(0,weight=1)
    login_frame.rowconfigure(2,weight=1)
    login_frame.columnconfigure(0,weight=1)

    login_text = tkinter.Label(login_frame,text="have an existing user?",font="20")
    login_text.grid(row=0,column=0,sticky="WESN")
    tkinter.Button(login_frame,text= "log in",font=20,command=login_function).grid(row=1,column=0,sticky="SN")

    window.mainloop()