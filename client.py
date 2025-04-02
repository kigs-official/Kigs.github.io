import socket

HOST = "localhost"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Enter username: ")
password = input("Enter password: ")
client.send(f"{username}:{password}".encode())

response = client.recv(1024).decode()
if response == "OK":
    print("Login successful! You can start chatting.")
else:
    print("Login failed!")
    client.close()
    exit()

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            print(message)
        except:
            break

import threading
threading.Thread(target=receive_messages, daemon=True).start()

while True:
    msg = input()
    client.send(msg.encode())
