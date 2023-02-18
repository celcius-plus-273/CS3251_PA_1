import socket
import threading
import sys


#TODO: Implement all code for your server here

# Use sys.stdout.flush() after print statemtents

if __name__ == "__main__":
	try:
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Server socket created succesfully")
		sys.stdout.flush()
	except socket.error as err:
		print("Server socket creation failed. Error: %s" %(err))
		sys.stdout.flush()

	PORT = 1309

	try:
		serverSocket.bind(("", PORT))
		print("Server socket was succesfully binded to port {}".format(PORT))
		sys.stdout.flush()
	except socket.error as err:
		print(f"Server socket binding to port {PORT} failed")
		sys.stdout.flush()

	serverSocket.listen(3)
	print("Server is listening...")

	serverIP = socket.gethostbyname(socket.gethostname())
	num = 1

	while(True):
		client, addr = serverSocket.accept()

		print(f"Client: {num} has succesfully connected")
		
		client.send(f"You're client {num}".encode())
		#num += 1

		while True:
			msg = client.recv(1024).decode()
			if msg == "Stop":
				break
			client.send(msg.encode())
		

		client.close()
		print(f"Client {num} has been disconnected")
