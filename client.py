import socket
import threading
import sys 


#TODO: Implement a client that connects to your server to chat with other clients here

# Use sys.stdout.flush() after print statemtents

def msg_input(clientSocket):
	while True:
		new_msg = clientSocket.recv(1024).decode()
		if not new_msg:
			break
		print(f"{new_msg}")
		sys.stdout.flush()

def msg_output(clientSocket):
	while True:
		msg = input("")
		clientSocket.send(msg.encode())
		if msg == ":Exit":
			break

if __name__ == "__main__":
	# read and parse command line arguments
	if (len(sys.argv) != 10):
		print("Cannot start client with given parameters")
		sys.exit()
	else:
		if (sys.argv[1] != "-join"):
			print("First argument should be \"join\"!")
			sys.exit()
		elif (sys.argv[2] != "-host"):
			print("Second argumet should be \"host\"!")
		elif (sys.argv[4] != "-port"):
			print("Fourth argumet should be \"port\"!")
			sys.exit()
		elif (sys.argv[6] != "-username"):
			print("Sixth argumet should be \"username\"!")
			sys.exit()
		elif (sys.argv[8] != "-passcode"):
			print("Eight argumet should be \"passcode\"!")
			sys.exit()

		HOST = sys.argv[3]
		PORT = int(sys.argv[5])
		USERNAME = sys.argv[7]
		PASSWORD = sys.argv[9]

	# initialize client TCP socket
	try:
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#print("Client socket created succesfully")
	except socket.error as err:
		print("Client socket creation failed. Error: %s" %(err))
		sys.stdout.flush()

	# attemp connection to server
	try:
		clientSocket.connect((HOST, PORT))
	except socket.error as err:
		print(f"Couldn't establich connection with host: {HOST}")
		sys.stdout.flush()
	
	# send credentials for login
	clientSocket.send(PASSWORD.encode())
	if (clientSocket.recv(1024).decode() == "Allowed"):
		print(f"Connected to {HOST} on port {PORT}")
		sys.stdout.flush()
		clientSocket.send(USERNAME.encode())
	else:
		print("Invalid credentials. Try again.")
		clientSocket.close()
		sys.exit()

	#set up two threads: 1) receives messages 2) sends messages
	output_thread = threading.Thread(target=msg_output, args=(clientSocket,))
	input_thread = threading.Thread(target=msg_input, args=(clientSocket,))
	
	output_thread.start()
	input_thread.start()
	
	output_thread.join()
	input_thread.join()

	clientSocket.close()

		
