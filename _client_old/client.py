import socket, threading, tkinter, time
import login,register ,start_window,chat_picker,chat,crypto,data_structures,workers


class varubeles:
    cur_window = "pick_log_reg"
    chat_pin = ""
    username = ""
def main():
    start_event = threading.Event()

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("127.0.0.1",12345))

    e, d, N = crypto.generateKeys(32)
    
    server_e, server_N = client.recv(1024).decode("ascii").split()
    server_e = int(server_e); server_N = int(server_N)
    client.send(crypto.encrypt((str(e) + " " + str(d) + " " + str(N)),server_e,server_N).encode("ascii"))

    recv_obj = workers.recv_manager(client,start_event,d,N)
    send_obj = workers.send_manager(client,start_event,e,N)

    recv_obj.start()
    send_obj.start()

    varubeles.recv_obj = recv_obj
    varubeles.send_obj = send_obj
    varubeles.close_protocol = False
    varubeles.start_event = start_event

    start_event.set()
    start_event.wait()
    while not varubeles.close_protocol:

        if varubeles.cur_window == "pick_log_reg":
            start_window.main(varubeles)
        
        elif varubeles.cur_window == "login":
            login.main(varubeles)
        
        elif varubeles.cur_window == "register":
            register.main(varubeles)

        elif varubeles.cur_window == "chat_picker":
            chat_picker.main(varubeles)

        elif varubeles.cur_window == "chat":
            chat.main(varubeles)
        else:
            varubeles.close_protocol = True



    send_obj.insert("close_protocol")
    msg = recv_obj.get_item()
    while msg != "close_protocol":
        msg = recv_obj.get_item()
        
        
    send_obj.insert("ok_bye")

    msg = recv_obj.get_item()
    if msg != "ok_bye":
        raise Exception("the server never sent 'ok_bye'")

    send_obj.join()
    recv_obj.join()

main()