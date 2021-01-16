import tkinter as tk
from client_dependencies import start_window,register,login

def main(server,keys):

    def close():
        root.destroy()

    root = tk.Tk()
    root.minsize(500,500)
    root.maxsize(1500,1500)
    root.title("sendme")
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)
    root.protocol("WM_DELETE_WINDOW",close)

    start_frame = tk.Frame(root)
    login_frame = tk.Frame(root)
    register_frame = tk.Frame(root)
    chat_picker_frame = tk.Frame(root)
    chat_frame= tk.Frame(root)

    for frame in (start_frame, login_frame, register_frame, chat_picker_frame, chat_frame):
        frame.grid(row=0, column=0, sticky='news')

    start_window.Create_Frame(start_frame,register_frame,login_frame)
    register.Create_Frame(register_frame,login_frame,chat_picker_frame)
    login.Create_Frame(login_frame,register_frame,chat_picker_frame,server,(keys[0],keys[2]),(keys[1],keys[2]))

    login_frame.tkraise()
    root.mainloop() 