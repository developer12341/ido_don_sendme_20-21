import socket
from ganeral_dependencies import RSA_crypt
from server_dependencies import client_thread, sql_manager

IP, PORT = "127.0.0.1", 12345

#setting up the server
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((IP,PORT))
server.listen(10)

#setting up needed varubles and objects
server_e, server_d, server_N = RSA_crypt.generateKeys(32)
public_key = f"{server_e} {server_N} "
data_base = sql_manager.User_Db("userdata")

#{address: username, ...}
addr_name = {}
#{address: chatId, ...}
addr_chatId = {}
#{chatId: [address,address...], ...}
chatId_addr = {}

while True:

    client, addr = server.accept()
    try:
        client.send(public_key.encode("ascii"))

        encrypted_msg = client.recv(2048)

        msg = RSA_crypt.decrypt(encrypted_msg, server_d,server_N).split()
        client_e, client_d, client_N = map(lambda string: int(string),msg)

        thread = client_thread.request_heandler(client,addr,client_e,client_d,client_N,data_base,addr_name,addr_chatId,chatId_addr)

        thread.start()
    except:
        pass