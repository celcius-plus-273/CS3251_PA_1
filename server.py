import socket
import threading
import sys
import datetime

#TODO: Implement all code for your server here

# Use sys.stdout.flush() after print statemtents

def find_username(msg):
	n = 0
	while ( n < len(msg) and (msg[n] != ":")):
		n += 1
	return msg[0 : n]

def chatroom_conection_input(all_clients, client, buffer, chat_lock, client_lock):
	while True:
		msg = client.recv(1024).decode()
		username = all_clients[client]
		if msg == ":Exit":
			# delete cient from client dictionary
			client_lock.acquire()
			all_clients.pop(client)
			client_lock.release()

			# send a message informming others that client has left
			chat_lock.acquire()
			buffer.append(f"{username} left the chatroom")
			chat_lock.release()

			# close connection with client
			client.close()
			break
		elif msg == ":)":
			chat_lock.acquire()
			buffer.append(f"{username}: [Feeling Happy]")
			chat_lock.release()
		elif msg == ":(":
			chat_lock.acquire()
			buffer.append(f"{username}: [Feeling Sad]")
			chat_lock.release()
		elif msg == ":mytime":
			mydatetime = (datetime.datetime.now()).strftime("%c")
			chat_lock.acquire()
			buffer.append(f"{username}: {mydatetime}")
			chat_lock.release()
		elif msg == "+1hr":
			mydatetime = datetime.datetime.now()
			myhour = mydatetime.hour
			myday = mydatetime.day
			if (myhour != 23):
				mydatetime = mydatetime.replace(hour=(myhour+1))				
			else:
				mydatetime = mydatetime.replace(day=myday+1, hour=00)
			chat_lock.acquire()
			mydatetime = mydatetime.strftime("%c")				
			buffer.append(f"{username}: {mydatetime}")
			chat_lock.release()
		else:
			chat_lock.acquire()
			buffer.append(f"{username}: {msg}")
			chat_lock.release()
				
def chatroom_output(all_clients, buffer, lock):
	while True:
		while len(buffer) != 0:
			lock.acquire()
			msg = buffer[0]
			msg_username = find_username(msg)
			print(msg)
			sys.stdout.flush()
			for client in all_clients:
				if (all_clients[client] == msg_username):
					continue
				client.send(msg.encode())
			buffer.pop(0)
			lock.release()


if __name__ == "__main__":
	# read and parse command line arguments
	if (len(sys.argv) != 6):
		print("Can't initialize server with given parameters")
		sys.exit()
	else:
		if (sys.argv[1] != "-start"):
			print("First argument should be \"start\"!")
			sys.exit()
		elif (sys.argv[2] != "-port"):
			print("Second argumet should be \"port\"!")
			sys.exit()
		elif (sys.argv[4] != "-passcode"):
			print("Third argumet should be \"passcode\"!")
			sys.exit()

		PORT = int(sys.argv[3])
		PASSWORD = sys.argv[5]

	# initialize a server TCP socket
	try:
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#print("Server socket created succesfully")
		#sys.stdout.flush()
	except socket.error as err:
		print("Server socket creation failed. Error: %s" %(err))
		sys.stdout.flush()

	# bind the server socket to port 127.0.0.1 (loopback) and given port from cml argument
	try:
		serverSocket.bind(("127.0.0.1", PORT))
		#print("Server socket was succesfully binded to port {}".format(PORT))
		#sys.stdout.flush()
	except socket.error as err:
		print("Server socket binding to port {} failed".format(PORT))
		sys.stdout.flush()

	# initialize chatlog for chatroom
	chat_lock = threading.Lock()
	chat_buffer = []

	# intialize client dictionary
	clients_lock = threading.Lock()
	all_clients = {}

	# start listening for clients
	serverSocket.listen(3)

	# initialize and start the chatroom output thread
	server_output_thread = threading.Thread(target=chatroom_output, args=(all_clients, chat_buffer, chat_lock,))
	server_output_thread.start()

	num_clients = 0
	while(True):
		client, addr = serverSocket.accept()
		num_clients += 1
		if (client.recv(1024).decode() == PASSWORD):
			# send authorization to client
			client.send("Allowed".encode())

			# receive username from client
			USERNAME = client.recv(1024).decode()

			# send a welcome message to all other clients and server
			print(f"{USERNAME} joined the chatroom")
			sys.stdout.flush()
			for other_client in all_clients:
				other_client.send(f"{USERNAME} joined the chatroom".encode())

			# appends client to array of clients
			clients_lock.acquire()
			all_clients[client] = USERNAME
			clients_lock.release()

			client_thread = threading.Thread(target=chatroom_conection_input, args=(all_clients, client, chat_buffer, chat_lock, clients_lock, ))
			client_thread.start()

		else:
			client.send("Not Allowed".encode())
			print("Client not allowed")
			client.close()
	

	serverSocket.close()
		



