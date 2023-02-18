import socket
import threading
import sys 


#TODO: Implement a client that connects to your server to chat with other clients here

# Use sys.stdout.flush() after print statemtents

def msg_input(clientSocket):
	while True:
		msg = clientSocket.recv(1024).decode()
		print(f"From server: {msg}")
		if msg == "Stop":
			break

def msg_output(clientSocket):
	while True:
		msg = input("")
		clientSocket.send(msg.encode())
		
		if msg == "Stop":
			break
	

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

	#set up two threads: 1) receives messages 2) sends messages
	output_thread = threading.Thread(target=msg_output, args=(clientSocket,))
	input_thread = threading.Thread(target=msg_input, args=(clientSocket,))
	
	output_thread.start()
	input_thread.start()
	
	output_thread.join()
	input_thread.join()

	clientSocket.close()
	print("Disconnected")

		
