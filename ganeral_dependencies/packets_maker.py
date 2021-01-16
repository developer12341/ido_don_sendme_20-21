import uuid, math, time
import concurrent.futures

#setting some constents
LOGIN = b'\x01'
REGISTER = b'\x02'
SEND_MSG = b'\x03'
SEND_FILE = b'\x04'
SEND_IMG = b'\x05'
SERVER_KEYS = b'\x06'
CREATE_CHAT = b'\x07'
CONN_CHAT = b'\x08'
GET_USERS = b'\x09'
CLOSE_CONN = b'\x0a'
LEAVE_CHAT = b'\x0b'
REG_LOGIN_SUC = b'\x0c'
REG_LOGIN_FAIL = b'\x0d'
GET_GROUP_KEYS = b'\x0e'
FORGOT_MY_PASSWORD = b'\x0f'
AUTHENTICAT_EMAIL = b'\x10'
USERNAME_TAKEN = b'\x11'
EMAIL_TAKEN = b'\x12'


#flags - to chack packet validitys and to let the reciver know for sure what this packet is
CONTENT_PACKET = b'\x00'
FILE_NAME_PACKET = b'\x01'
R_L_FAIL = b'\x02'
R_L_SUC = b'\x03'
A_EMAIL_PACKET = b'\x04'

HEADER_SIZE = 16 # bytes
PACKET_SIZE = 1024  #bytes
CONTENT_SIZE = PACKET_SIZE - HEADER_SIZE
IMG_SIZE_FAC = 0.5 # 0 < IMG_SIZE_FAC < 1


PASSWORD_MIN_LEN = 10
PASSWORD_MAX_LEN = 100
USERNAME_MIN_LEN = 5
USERNAME_MAX_LEN = 30



class Packet_Maker:
    """
        request - 
            LOGIN 
            REGISTER 
            SEND_MSG 
            SEND_FILE 
            SEND_IMG
        content, file_name  - only bytes, if it is string then convert 
        using .encode("ascii")
        file_name must have the file type(.jpeg, .pdf...)
        file_path must be a string
    """

    def __init__(self, request, public_key, content = None, file_path = None, file_name = None):
        """
            prepering the packets and the header
        """
        self.e,self.N = public_key
        self.amount_name_p = 0

        if request == SEND_FILE:
            #edge case - sending file without a name or a type
            if not file_name:
                raise Exception("you must have a file name and type to send a file!")
            

            #encrypt the file name and file itself
            self.file_name = self.encrypt(file_name)
            self.content = self.encrypt(content)

            self.amount_name_p += math.ceil(len(self.file_name)/CONTENT_SIZE)


        elif request == SEND_IMG:
            #displaying a suggestion
            if content:
                print("you don't need to enter content when sending an image")
            
            import PIL
            from PIL import Image
            import io

            #commpressing a file
            img = Image.open(file_path)
            new_size = map(lambda x: int(IMG_SIZE_FAC*x), img.size)
            img = img.resize(new_size, PIL.Image.ANTIALIAS)
            buffer= io.BytesIO()
            file_format = file_name.split(b'.')[-1].decode("ascii")
            img.save(buffer, format=file_format)

            #encrypt the content of the image and the file name
            self.content = buffer.getvalue()
            self.content = self.encrypt(self.content)
            self.file_name = self.encrypt(file_name)

            self.amount_name_p += math.ceil(len(self.file_name)/CONTENT_SIZE)
        elif request == REG_LOGIN_FAIL:
            self.general_packets = self.create_fail_packet()
            return
        elif request == USERNAME_TAKEN:
            self.general_packets = self.create_fail_packet()
            return
        elif request == REG_LOGIN_SUC:
            self.general_packets = self.create_success_packet()
            return
        elif request == AUTHENTICAT_EMAIL:
            self.general_packets = self.create_authenticate_email_packet()
            return
        elif request == SEND_MSG or request == LOGIN or request == REGISTER:
            #encrypt the content of the massage
            self.content = self.encrypt(content)
        
            

        packet_id = uuid.uuid4().bytes[:8]

        self.amount_content_p = math.ceil(len(self.content)/CONTENT_SIZE)
        self.amount_of_packets = self.amount_content_p + self.amount_name_p

        #edge case - there are too many packets
        if self.amount_of_packets > 16777216:
            raise Exception(f"the content is too big :( \namount of packets = {self.amount_of_packets}")
        
        #this part is in every packet so im making it hear
        self.header = request + packet_id 
        self.header += self.amount_of_packets.to_bytes(3,"big")
        if not self.amount_name_p:
            self.name_packets = map(self.create_name_packets, range(self.amount_name_p))
        self.content_packets = map(self.create_content_packet,range(self.amount_name_p,self.amount_content_p))

    def encrypt(self,msg):
        """
            encrypt every massege with the following formula
            (msg)^e % N = c 
        """
        cipher = map(lambda num: pow(num, self.e, self.N).__str__(), msg)
        cipher = ' '.join(cipher).encode("ascii")
        return cipher

    def create_fail_packet(self):
        packet_id = uuid.uuid4().bytes[:8]
        header = REG_LOGIN_FAIL + packet_id 
        header += bytes([0,0,1])
        header += bytes([0,0,0])
        header += R_L_FAIL #flag - this is a "fail to register or log in" packet
        return header + bytes(CONTENT_SIZE-len(header))
    
    def create_authenticate_email_packet(self):
        packet_id = uuid.uuid4().bytes[:8]
        header = AUTHENTICAT_EMAIL + packet_id 
        header += bytes([0,0,1])
        header += bytes([0,0,0])
        header += A_EMAIL_PACKET #flag - this is a "fail to register or log in" packet
        return header + bytes(CONTENT_SIZE-len(header))

    def create_success_packet(self):
        packet_id = uuid.uuid4().bytes[:8]
        header = REG_LOGIN_SUC + packet_id 
        header += bytes([0,0,1])
        header += bytes([0,0,0])
        header += R_L_SUC #flag - this is a "succsuss to register or log in" packet
        return header + bytes(CONTENT_SIZE-len(header))

    def create_name_packets(self,packet_number):
        packet = self.header
        packet += packet_number.to_bytes(3,"big") # packet number
        packet += FILE_NAME_PACKETP #flag - this is a file_name packet

        if len(self.file_name) > CONTENT_SIZE:
            packet += self.file_name[:CONTENT_SIZE]
            self.file_name = self.file_name[CONTENT_SIZE:]
        else:
            packet += self.file_name[:CONTENT_SIZE]

    def create_content_packet(self,packet_number):
        """
        this function is prepering a packet. it takes the content of a file or
        a message, the relevent information and is packing it in a convinent package.

        a packet is made of a header and a content
        {header}
            <request> <request id> <amount of packets> <packet number> <flag - is it a file path?>
        {header}
        <encrypted content>
        """

        packet = self.header + packet_number.to_bytes(3,"big") # packet number
        packet += CONTENT_PACKET #flag - this is a content packet
        packet += self.content[packet_number*CONTENT_SIZE:(packet_number + 1)*CONTENT_SIZE]
        packet += bytes(PACKET_SIZE - len(packet))

        return packet

def main():
    pass

if __name__ == "__main__":
    main()