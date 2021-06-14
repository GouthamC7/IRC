import threading
import socket

host = '127.0.0.1' #localhost
port = 55555
rooms = {}
users = {}
users_room = {}
instructions = '\nList of commands:\n' \
               '-------------------------------------------------\n' \
               '<list> to list all the rooms\n' \
               '<quit> to quit\n' \
               '<help> to list all the commands\n' \
               '<leave> to leave the room \n' \
               '[<join> roomname] to join or create the room\n' \
               '[<switch> roomname] to switch room\n' \
               '[<personal> name message] to send personal message'

#starting the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

class User:
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.currentRoom = ''


class Room:
    def __init__(self, name):
        self.members = []
        self.nicknames = []
        self.name = name

def welcome_message(self):
        msg = self.name + " welcomes: "

def broadcast(message, roomname):
    for client in rooms[roomname].members:
        msg = '['+roomname+'] '+message
        client.send(msg.encode('ascii'))

def list_all_rooms(nickname):
    name = users[nickname]
    print(len(rooms))
    if len(rooms) == 0:
        name.send('No rooms are available to join'.encode('ascii'))
    else:
        reply = "List of available rooms: \n"
        for room in rooms:
            print(rooms[room].name)
            reply += '\n-----------\n' + rooms[room].name + '\n------------\n'
            print(rooms[room].nicknames)

            #if nickname not in rooms[room].nicknames:
            for member in rooms[room].nicknames:
                reply += member + '\n'
        name.send(f'{reply}'.encode('ascii'))

def join_room(nickname, room_name):
    name = users[nickname]
    user = users_room[nickname]
    if room_name not in rooms:
        room = Room(room_name)
        rooms[room_name] = room
        room.members.append(name)
        room.nicknames.append(nickname)

        user.currentRoom = room_name
        user.rooms.append(room)
        name.send(f'{room_name} created'.encode('ascii'))
    else:
        room = rooms[room_name]
        if room_name in user.rooms:
            name.send('You are already in the room'.encode('ascii'))
        else:
            room.members.append(name)
            room.nicknames.append(nickname)
            user.currentRoom = room_name
            user.rooms.append(room)
            broadcast(f'{nickname} joined the room', room_name)
            #name.send('Joined room'.encode('ascii'))

def switch_room(nickname, roomname):
    user = users_room[nickname]
    name = users[nickname]
    room = rooms[roomname]
    if roomname == user.currentRoom:
        name.send('You are already in the room'.encode('ascii'))
    elif room not in user.rooms:
        name.send('Switch not available, You are not part of the room'.encode('ascii'))
    else:
        user.currentRoom = roomname
        name.send(f'Switched to {roomname}'.encode('ascii'))

def leave_room(nickname):
    user = users_room[nickname]
    name = users[nickname]
    if user.currentRoom == '':
        name.send('You are not part of any room'.encode('ascii'))
    else:
        roomname = user.currentRoom
        room = rooms[roomname]
        user.currentRoom = ''
        user.rooms.remove(room)
        rooms[roomname].members.remove(name)
        rooms[roomname].nicknames.remove(nickname)
        broadcast(f'{nickname} left the room', roomname)
        name.send('You left the room'.encode('ascii'))

def personalMessage(message):
    args = message.split(" ")
    user = args[2]
    sender = users[args[0]]
    if user not in users:
        sender.send('User not found'.encode('ascii'))
    else:
        reciever = users[user]
        msg = ' '.join(args[3:])
        reciever.send(f'[personal message] {args[0]}: {msg}'.encode('ascii'))
        sender.send(f'[personal message] {args[0]}: {msg}'.encode('ascii'))

def remove_client(nickname):
    nicknames.remove(nickname)
    client = users[nickname]
    user = users_room[nickname]
    user.currentRoom = ''
    for room in user.rooms:
        print(room.name)
        room.members.remove(client)
        print(room.members)
        room.nicknames.remove(nickname)
        print(room.nicknames)
        broadcast(f'{nickname} left the room', room.name)

def handle(client):
    nick=''
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            args = message.split(" ")
            name = users[args[0]]
            nick = args[0]
            if '<help>' in message:
                name.send(instructions.encode('ascii'))
            elif '<list>' in message:
                list_all_rooms(args[0])
            elif '<join>' in message:
                join_room(args[0], ' '.join(args[2:]))
            elif '<leave>' in message:
                leave_room(args[0])
            elif '<switch>' in message:
                switch_room(args[0], args[2])
            elif '<personal>' in message:
                personalMessage(message)
            elif '<quit>' in message:
                remove_client(args[0])
                name.send('QUIT'.encode('ascii'))
                name.close()
            else:
                if users_room[args[0]].currentRoom == '':
                    name.send('You are not part of any room'.encode('ascii'))
                else:
                    msg = ' '.join(args[1:])
                    broadcast(f'{args[0]}: {msg}',users_room[args[0]].currentRoom)

            #broadcast(message)
        except Exception as e:
            print("exception occured ", e)
            index = clients.index(client)
            clients.remove(client)
            client.close()
            '''nickname = nicknames[index]
            print(f'{nickname} left')
            user = users_room[nickname]'''
            '''if user.currentRoom != '':
                roomname = user.currentRoom
                user.currentRoom = ''
                #user.rooms.remove(roomname)
                rooms[roomname].members.remove(name)
                rooms[roomname].nicknames.remove(nickname)
                broadcast(f'{nickname} left the room', roomname)'''
            print(f'nick name is =============== {nick}')
            if nick in nicknames:
                remove_client(nick)
            if nick in nicknames:
                nicknames.remove(nick)

            #broadcast(f'{nickname} left the room'.encode('ascii'))

            break

def recieve():
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}')
        print(client)
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        user = User(nickname)
        users_room[nickname] = user
        users[nickname] = client
        print(f'Nickname of the client is {nickname}')
        #broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))
        client.send(instructions.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is up and listening...')
recieve()







