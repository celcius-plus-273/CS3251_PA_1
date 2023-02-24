import socket
import threading
import sys 
import datetime

#TODO: Implement all code for your server here

# Use sys.stdout.flush() after print statemtents

# function that sends a message to other clients in the server and also prints the mesage
# to the server
def send_message(username, message, clientList, clientLock):
	# print message on server
	print(message)
	sys.stdout.flush()

	# locks the client list while a message is being sent
	clientLock.acquire()

	# iterate through each client
	for clientSocket in clientList:
		# skip sending to sender
		if (clientList[clientSocket] == username):
			continue

		# sends the messagae to current client on the list
		clientSocket.send(message.encode())
	
	# unlocks the client list
	clientLock.release()

# thread target function that initalizes a user in the chatroom
def chatroom_user(clientSocket, username, clientList, clientLock):
	while True:
		recv_msg = clientSocket.recv(1024).decode()
		if recv_msg == ":Exit":
			# delete cient from client list
			clientLock.acquire()
			clientList.pop(clientSocket)
			clientLock.release()

			# send a message informming others that client has left
			message = f'{username} left the chatroom'
			send_message(username, message, clientList, clientLock)

			# close connection with client
			clientSocket.close()

			# end thread
			break

		elif recv_msg == ":)":
			# parse the :) input
			message = f"{username}: [feeling happy]"
			send_message(username, message, clientList, clientLock)
		
		elif recv_msg == ":(":
			# parse the :( input
			message = f"{username}: [feeling sad]"
			send_message(username, message, clientList, clientLock)

		elif recv_msg == ":mytime":
			# parse mytime input
			mydatetime = (datetime.datetime.now()).strftime("%c")
			message = f"{username}: {mydatetime}"
			send_message(username, message, clientList, clientLock)

		elif recv_msg == ":+1hr":
			# parse +1hr input
			mydatetime = datetime.datetime.now()
			myhour = mydatetime.hour
			myday = mydatetime.day
			if (myhour != 23):
				mydatetime = mydatetime.replace(hour=(myhour+1))				
			else:
				mydatetime = mydatetime.replace(day=myday+1, hour=00)
			mydatetime = mydatetime.strftime("%c")		

			message = f"{username}: {mydatetime}"
			send_message(username, message, clientList, clientLock)

		else:
			# sends original message
			message = f'{username}: {recv_msg}'
			send_message(username, message, clientList, clientLock)


if __name__ == "__main__":
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

	try:
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as err:
		print("Socket creation failed")

	try:
		serverSocket.bind(('', PORT))
	except socket.error as err:
		print("Socket binding failed")

	
	serverSocket.listen(3)
	print(f"Server started on port {PORT}. Accepting connections")
	sys.stdout.flush()

	# list of all clients
	clientList = {}
	# lock for list of clients
	clientLock = threading.Lock()

	while True:
		clientSocket, clientAddress = serverSocket.accept()
		passcode = clientSocket.recv(1024).decode()
		
		if passcode != PASSWORD:
			clientSocket.send("INCORRECT".encode())
			clientSocket.close()
			continue

		# send ack message
		clientSocket.send("CONNECTED".encode())

		# receive username from client
		username = clientSocket.recv(1024).decode()

		# send welcome message to server and other clients
		welcome_message = f'{username} joined the chatroom'
		send_message(username, welcome_message, clientList, clientLock)

		# add new client to list
		clientLock.acquire()
		clientList[clientSocket] = username
		clientLock.release()

		# Initialize chatroom thread for new client
		client_thread = threading.Thread(target=chatroom_user, args=(clientSocket, username, clientList, clientLock, ))
		client_thread.start()

	serverSocket.close()
