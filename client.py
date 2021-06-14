import threading
import socket
import sys

nickname = input("Enter your name: ")
threads = []
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == 'QUIT':
                print("Have a great day")
                sys.exit(2)
            else:
                print(message)
        except Exception as e:
            print('Server is down, Please try again later')
            client.close()
            sys.exit(2)

def write():
    while True:
        message = '{} {}'.format(nickname, input(''))
        try:
            client.send(message.encode('ascii'))
        except:
            sys.exit(0)

receive_thread = threading.Thread(target=receive)
receive_thread.start()
threads.append(receive_thread)
write_thread = threading.Thread(target=write)
write_thread.start()
threads.append(write_thread)