#a place i will put all of my cross client - server code

import threading,data_structures,time

keysize = 32
class recv_manager(threading.Thread,data_structures.queue):

    def __init__(self,client,d,N):
        self.running = True
        self.client = client
        self.d = d
        self.N = N
        self.continue_recv = threading.Event()
        threading.Thread.__init__(self)
        data_structures.queue.__init__(self)
        
    def get_item(self):
        #a function thet return the newest massage
        if(self.not_empty.is_set()):
            return self.remove()
        
        self.continue_recv.set()
        self.continue_recv.clear()
        self.wait_for_item()
        return self.remove()

    def decrypt(self, cipher):
        msg = ""
        parts = cipher.split()

        for part in parts:
            if part:
                c = int(part)
                msg += chr(pow(c,self.d, self.N))
        return msg

    def run(self):
        self.continue_recv.wait()
        self.raw_msg = ""
        while self.running:
            self.raw_msg += self.client.recv(4096).decode("ascii")
            while self.raw_msg[-1] != "-":
                self.raw_msg += self.client.recv(4096).decode("ascii")
                
            massages = self.raw_msg.split("-")
            for i in range(len(massages)-1):
                self.insert(self.decrypt(massages[i]))
            self.raw_msg = massages[len(massages)-1]
            self.continue_recv.wait()
    
    def join(self):
        #a method for killing the threads
        self.running = False
        self.continue_recv.set()
        threading.Thread.join(self)



class send_manager(threading.Thread,data_structures.queue):
    def __init__(self,client,e,N):
        self.client = client
        self.N = N
        self.e = e
        self.running = True
        threading.Thread.__init__(self)
        data_structures.queue.__init__(self)
        
    
    def encrypt(self,msg):
        cipher = ""

        for c in msg:
            m = ord(c)
            cipher += str(pow(m, self.e, self.N)) + " "

        return cipher
    
    def run(self):
        self.wait_for_item()
        while self.running:
            self.client.send((self.encrypt(self.remove()) + '-').encode("ascii"))
            self.wait_for_item()

    
    def join(self):
        while self.not_empty.is_set():
            time.sleep(0.07)
        self.running = False
        self.not_empty.set()
        threading.Thread.join(self)
