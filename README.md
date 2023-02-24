# CS3251 Programming Assignment 1
Private repository for version control and cloud access to my CS 3251 Programming Assingment 1.

## server.py
Simulates a chatroom by accepting incoming clients, verifying their credentials, and welcoming them into the chatroom

## client.py
Simulates a user for the chatroom

# Arguments required to initialize server and client
## server.py
python server.py -start -port {enter any port number} -passcode {enter any passcode}

## client.py
python client.py -join -host 127.0.0.1 -port {same port number as server.py} -username {any username} -passcode {same passcode as server.py}
