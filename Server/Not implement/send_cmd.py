import socket

chaine = "shell whoami"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.2", 1111))

try:
	s.send(chaine.encode())
	s.close
	print("ok")
except:
	print("ko")
