import socket
import threading
import sys 


#TODO: Implement a client that connects to your server to chat with other clients here

# Use sys.stdout.flush() after print statemtents

if __name__ == "__main__":
	try:
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Client socket created succesfully")
	except socket.error as err:
		print("Client socket creation failed. Error: %s" %(err))


	#ip = socket.gethostbyname(socket.gethostname())
	HOST = "127.0.0.1"
	PORT = 1309

	clientSocket.connect((HOST, PORT))
	print(f"Succesfully connected to server with address: {HOST}")

	msg = clientSocket.recv(1024).decode()
	print(f"Message from server: {msg}")

	while True:
		fwd = input("Type something: ")
		clientSocket.send(fwd.encode())

		if fwd == "Stop":
			print("Disconnecting from server...")
			break

		print(f"Echoed message is: {clientSocket.recv(1024).decode()}")

	clientSocket.close()
	print("Succesfully disconnected")