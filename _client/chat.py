import tkinter,threading,ctypes,time,data_structures,os,ntpath,datetime

from tkinter.filedialog import askopenfilename
from tkinter.ttk import Progressbar

def path_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

class msg_loop(threading.Thread):
    def __init__(self,recv_obj,username,queue):
        self.recv_obj = recv_obj
        self.queue = queue
        self.users = [username]
        self.running = True
        self.img_send_stop = False
        self.set_back_entry = threading.Event()
        threading.Thread.__init__(self)
    
    def run(self):
        msg = self.recv_obj.get_item()
        while self.running:
            if msg.find(" has joined this chat") != -1:
                if not msg.replace(" has joined this chat","") in self.users:
                    self.users.append(msg.replace(" has joined this chat",""))
            
            elif msg.find(" created this chat group") != -1:
                if not msg.replace(" created this chat group","") in self.users:
                    self.users.append(msg.replace(" created this chat group",""))

            elif msg.find(" has left this chat") != -1:
                name = msg.replace(" has left this chat","")
                for i in range(len(self.users)):
                    if self.users[i] == name:
                        del self.users[i]
                        break
            
            if msg == "start send file":
                self.img_send_stop = True
                f = open(".//files//" + str(datetime.datetime.now().strftime("%d-%m-%y--%H-%M")) + self.recv_obj.get_item(),"wb")
                f.write(bytes.fromhex(self.recv_obj.get_item()))
                self.queue.insert(f"{self.recv_obj.get_item()} sent a file")
                self.queue.insert(f"the file was saved in {os.getcwd()}\\files")
                self.img_send_stop = False
                self.set_back_entry.set()
            else:
                self.queue.insert(msg)
            msg = self.recv_obj.get_item()


    def join(self):
        self.running = False
        self.recv_obj.get_out_of_wait()
        threading.Thread.join(self)


def main(self):
    def close():
        if not loop.img_send_stop:
            loop.join()
            self.close_protocol = True
            window.destroy()
        else:
            ctypes.windll.user32.MessageBoxW(0, "you cant close the application\nwhile you apload a file", "sorry :(", 0)
            

    def on_send():
        if chat_entry.get() and not loop.img_send_stop:
            self.send_obj.insert("msg")
            self.send_obj.insert(f"<{self.username}>:{chat_entry.get()}")
            chat_entry.delete(0, 'end')

    def on_enter(event):
        if chat_entry.get() and not loop.img_send_stop:
            self.send_obj.insert("msg")
            self.send_obj.insert(f"<{self.username}>:{chat_entry.get()}")
            chat_entry.delete(0, 'end')
        
    def group_info():
        info = "chat_pin: {}\n\nusers in the chat\n\n".format(self.chat_pin)
        for name in loop.users:
            info += name + "\n"
        ctypes.windll.user32.MessageBoxW(0, info, "group info", 0)

    def leave_group():
        if not loop.img_send_stop:
            self.send_obj.insert("leave chat")
            self.cur_window = "chat_picker"
            loop.join()
            time.sleep(0.1)
            window.after_cancel(self.cur_after)
            window.destroy()
    
    def listen_queue():
        if loop.img_send_stop:
            progress["value"] = (progress["value"] % 100 ) + 20
        if loop.set_back_entry.is_set():
            progress.grid_forget()
            chat_entry.grid(row=1,column=0,sticky="NWES")
            loop.img_send_stop = False
            loop.set_back_entry.clear()        
        if thread_queue.not_empty.is_set():
            list_box.insert(tkinter.END,thread_queue.remove())        
        if not self.close_protocol and self.cur_window == "chat":
            self.cur_after = window.after(100,listen_queue)

    def on_send_file():
        if not loop.img_send_stop:
            filepath = askopenfilename()
            if filepath:
                chat_entry.grid_forget()
                progress.grid(row=1,column=0,sticky="NWES")
                loop.img_send_stop = True
                f = open(filepath,"rb")
                self.send_obj.insert("start send file")
                self.send_obj.insert(path_name(filepath))
                self.send_obj.insert(f.read().hex())
                f.close()
            
            

            
    window =  tkinter.Tk()
    window.title("sendme - chat pin: {}".format(self.chat_pin))
    window.geometry("400x400")
    window.protocol('WM_DELETE_WINDOW',close)

    menubar = tkinter.Menu(window)
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="grope info", command=group_info)
    filemenu.add_separator()
    filemenu.add_command(label="leave grope", command=leave_group)
    menubar.add_cascade(label="options", menu=filemenu)


    window.config(menu=menubar)
    window.grid_rowconfigure(0,weight=1)
    window.grid_columnconfigure(0,weight=9999)
    window.grid_columnconfigure(1,weight=1)
    window.grid_columnconfigure(2,weight=1)

    scrollbar = tkinter.Scrollbar(window)
    scrollbar.grid(row=0,column=3,sticky="NSWE",padx=(0,0))
    
    list_box = tkinter.Listbox(window,yscrollcommand = scrollbar.set)
    list_box.grid(row=0,column=0,columnspan=3,sticky="NWES")

    scrollbar.config(command = list_box.yview)


    chat_entry = tkinter.Entry(window,font="arial 14")
    chat_entry.grid(row=1,column=0,sticky="NWES")
    chat_entry.bind("<Return>",on_enter)

    tkinter.Button(window,text="+",font="arial 14",command=on_send_file).grid(row=1,column=1,sticky="NWES")

    
    tkinter.Button(window,text="send",font="arial 14",command=on_send).grid(row=1,column=2,columnspan=2,sticky="NWES")

    thread_queue = data_structures.queue()

    progress = Progressbar(window, orient = tkinter.HORIZONTAL,length = 100, mode = 'indeterminate') 
    loop = msg_loop(self.recv_obj,self.username,thread_queue)
    loop.start()
    window.after(100,listen_queue)
    window.mainloop()
