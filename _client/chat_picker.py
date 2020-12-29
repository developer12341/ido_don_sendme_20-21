import tkinter,threading

    
def main(self):
    def close():
        self.close_protocol = True
        threading._start_new_thread(window.destroy,tuple())

    def join_chat():
        self.send_obj.insert("join chat")
        self.send_obj.insert(pin_entry.get())
        msg = self.recv_obj.get_item()
        if(msg == "good to go"):
            self.chat_pin = pin_entry.get()
            self.cur_window = "chat"
            window.destroy()
        else:
            tkinter.Label(window,text=msg,fg="red").grid(row=4,column=0,columnspan=2,sticky="WENS")


    def open_new_chat():
        self.send_obj.insert("create new chat")
        self.chat_pin = self.recv_obj.get_item()
        self.cur_window = "chat"
        window.destroy()
        

    window = tkinter.Tk()
    window.geometry("400x400")
    window.title("sendme")
    window.protocol('WM_DELETE_WINDOW',close)
    tkinter.Label(window,text=f"hello {self.username}!",font="arial 23").grid(row=0,column=0,columnspan=2,sticky="NWE",pady=20)

    window.grid_columnconfigure(0,weight=1)
    window.grid_columnconfigure(1,weight=1)
    window.grid_rowconfigure(1,weight=1)
    window.grid_rowconfigure(3,weight=3)
    window.grid_rowconfigure(5,weight=1)

    tkinter.Label(window,text="want to join a group chat?\nenter pin code",font=15).grid(row=1,column=0,sticky="S")

    pin_entry = tkinter.Entry(window,font=15)
    pin_entry.grid(row=2,column=0,pady=20)

    tkinter.Button(window,text="join chat",font=15,command= join_chat).grid(row=3,column=0,sticky="N")


    tkinter.Label(window,text="start a new chat!",font=15).grid(row=1,column=1,sticky="S")
    tkinter.Button(window,text="start new chat",font=15,command=open_new_chat).grid(row=2,column=1,sticky="N",pady=20)

    window.mainloop()