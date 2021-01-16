import socket, threading,time,os,pickle,random,sys
import data_structures, workers, crypto
from cryptography.fernet import Fernet

key = Fernet("cpRKk-zl8Db0ohBEb4wKgOxGNpWWAsVFMM3NSumzkqA=".encode())
                
def init_client(client,addr):
    client.send((str(global_variables.e) + " " + str(global_variables.N)).encode("ascii"))

    client_e, client_d, client_N = crypto.decrypt(client.recv(2048),global_variables.d, global_variables.N).split()

    recv_obj = workers.recv_manager(client,int(client_d),int(client_N))
    send_obj = workers.send_manager(client,int(client_e),int(client_N))
    threading._start_new_thread(client_thread,(client,addr,send_obj,recv_obj))
    return send_obj

def client_thread(client,addr,send_obj,recv_obj):

    recv_obj.start()
    send_obj.start()
    class Client_variables:
        username = ""
        chat_pin = ""
    
    while True:
        msg = recv_obj.get_item()
        if msg == "close_protocol":
            brodcast(f"{Client_variables.username} has left this chat",Client_variables.chat_pin)
            break

        elif msg == "login":
            Client_variables.username = recv_obj.get_item()
            password = recv_obj.get_item()
            userdata = get_user_data()

            if Client_variables.username in userdata and userdata[Client_variables.username] == password:
                if not Client_variables.username in global_variables.active_users:
                    send_obj.insert("good to go")
                    global_variables.active_users[Client_variables.username] = addr
                else:
                    send_obj.insert("this account is connected elsewhere")

            else:
                send_obj.insert("the username or the password is incorract")

        elif msg == "register":
            Client_variables.username = recv_obj.get_item()
            password = recv_obj.get_item()
            year = recv_obj.get_item()
            month = recv_obj.get_item()
            day = recv_obj.get_item()
            data = get_user_data()
            if not Client_variables.username in data:
                write_to_user_data(Client_variables.username,password,year,month,day)
                send_obj.insert("good to go")
                global_variables.active_users[Client_variables.username] = addr
            else:
                send_obj.insert("this username is taken, please pick a diffrent one")

        elif msg == "msg":
            msg = recv_obj.get_item()
            brodcast(msg,Client_variables.chat_pin)
        
        elif msg == "create new chat":
            Client_variables.chat_pin = create_new_chat(addr,Client_variables.username)
            send_obj.insert(Client_variables.chat_pin)
            brodcast("{} created this chat group".format(Client_variables.username),Client_variables.chat_pin)
            log_server(Client_variables.username + "created chat: " + Client_variables.chat_pin)

        elif msg == "join chat":
            Client_variables.chat_pin = recv_obj.get_item()
            msg = join_chat(Client_variables.chat_pin,addr)
            send_obj.insert(msg)
            if msg == "good to go":
                lines = get_log_chat(Client_variables.chat_pin)
                for line in lines:
                    send_obj.insert(line)
                log_server(f"{Client_variables.username} has joined chat {Client_variables.chat_pin}")
                brodcast("{} has joined this chat".format(Client_variables.username),Client_variables.chat_pin)

        elif msg == "leave chat":
            del global_variables.chats[Client_variables.chat_pin][addr]
            if global_variables.chats[Client_variables.chat_pin] == {}:
                del global_variables.chats[Client_variables.chat_pin]
            Client_variables.chat_pin = ""

        elif msg == "start send file":
            brodcast("start send file",Client_variables.chat_pin)
            brodcast(recv_obj.get_item(),Client_variables.chat_pin)
            brodcast(recv_obj.get_item(),Client_variables.chat_pin)
            brodcast(Client_variables.username,Client_variables.chat_pin)



    send_obj.insert("close_protocol")

    recv_obj.get_item()

    send_obj.insert("ok_bye")
    
    recv_obj.join()
    send_obj.join()
    log_server(f"{addr} left server")
    client.close()
    remove_client(addr,Client_variables.chat_pin,Client_variables.username)




def brodcast(msg,chat_pin):
    if(chat_pin != "" and chat_pin in global_variables.chats):
        log_chat(msg,chat_pin)
        chat = global_variables.chats[chat_pin]
        for send_obj in chat.values():
            send_obj.insert(msg)

def remove_client(addr,chat_pin,username):
    #thread dict part
    del global_variables.users[addr]
    if chat_pin != "":
        #chat part
        del global_variables.chats[chat_pin][addr]
        if global_variables.chats[chat_pin] == {}:
            del global_variables.chats[chat_pin]
    #active users part
    if username in global_variables.active_users:
        del global_variables.active_users[username]

def join_chat(chat_pin,addr):
    if chat_pin in global_variables.chats:
        global_variables.chats[chat_pin][addr] = global_variables.users[addr]
        return "good to go"
    else:
        listdir =  os.listdir(os.getcwd() + "\\chat_logs")
        for filename in listdir:
            if filename == ("chat_log" + chat_pin + ".txt"):
                global_variables.chats[chat_pin] = {addr:global_variables.users[addr]}
                return "good to go"
        return "there is no " + str(chat_pin) + " chat room"

def create_new_chat(addr,username):
    pin = random.randint(100,1000)
    while pin in global_variables.chats and os.path.exists(os.getcwd() + "\\chat_logs\\chat_log" + pin + ".txt"):
        pin = random.randint(100,1000)
    global_variables.chats[str(pin)] = {addr:global_variables.users[addr]}
    return str(pin)

def main():

    server = socket.socket()
    server.bind(("0.0.0.0",12345))
    server.listen()
    
    #{addr:client_thread...}
    global_variables.users = {}

    #{username:addr....}
    global_variables.active_users = {}

    #{chat_pin:{addr:client_thread...}}
    global_variables.chats = {}

    global_variables.e,global_variables.d,global_variables.N = crypto.generateKeys(32)
    while True:
        client, addr = server.accept()
        log_server("{} connected to server".format(addr))
        send_obj = init_client(client,addr)
        global_variables.users[addr] = send_obj

def log_server(msg):
    with open(".\\log.txt","a") as userfile:
        userfile.write(key.encrypt(msg.encode()).decode() + "\n")
    
def log_chat(msg,chat_pin):
    with open(".\\chat_logs\\chat_log" + chat_pin + ".txt","a") as userfile:
        userfile.write(key.encrypt(msg.encode()).decode() + "\n")

def get_log_chat(chat_pin):
    with open(".\\chat_logs\\chat_log" + chat_pin + ".txt","r") as userfile:
        return [key.decrypt(line.encode()).decode() for line in userfile.readlines()]
    
def write_to_user_data(username,password,year,month,day):
    userfile = open(os.getcwd()  + "\\userdata.pickle","rb")
    data = pickle.load(userfile)
    userfile.close()
    data[key.encrypt(username.encode())] = key.encrypt(password.encode())
    userfile = open(os.getcwd()  + "\\userdata.pickle","wb")
    pickle.dump(data,userfile)
    userfile.close()
    userfile = open(os.getcwd()  + "\\userdata_expanded.pickle","rb")
    data = pickle.load(userfile)
    userfile.close()
    data[key.encrypt(username.encode())] = [key.encrypt(password.encode()),key.encrypt(year.encode()),key.encrypt(month.encode()),key.encrypt(day.encode())]
    userfile = open(os.getcwd()  + "\\userdata_expanded.pickle","wb")
    pickle.dump(data,userfile)
    userfile.close()

def get_user_data():
    with open(os.getcwd()  + "\\userdata.pickle","rb") as userfile:
        new_dic = {}
        for k,v in pickle.load(userfile).items():
            new_dic[key.decrypt(k).decode()] = key.decrypt(v).decode()
        return new_dic

class global_variables:
    pass

main()