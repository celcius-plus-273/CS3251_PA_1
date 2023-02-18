import socket
import threading
import sys
import time


#TODO: Implement all code for your server here

# Use sys.stdout.flush() after print statemtents

def repeat_msg(client):
	while True:
		client.send("Are you receving?".encode())
		time.sleep(7)

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

	num = 1

	while(True):
		client, addr = serverSocket.accept()

		print(f"Client: {num} has succesfully connected")
		
		client.send(f"You're client {num}".encode())
		#num += 1
		repeat_thread = threading.Thread(target=repeat_msg, args=(client,))
		repeat_thread.start()


		while True:
			msg = client.recv(1024).decode()
			client.send(msg.encode())
			print(f"Echoed message: {msg}")
			if msg == "Stop":
				break
		
		
		repeat_thread.join()
		client.close()
		print(f"Client {num} has been disconnected")
