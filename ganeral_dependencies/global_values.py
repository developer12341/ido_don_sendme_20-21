
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


