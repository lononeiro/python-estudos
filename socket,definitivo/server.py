import socket
import threading

host  = '127.0.0.1' #local host
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(f'{nickname} deixou o chat' .encode('utf-8'))
            nicknames.remove(nickname)
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f"conectado com {str(address)} ")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        

        nicknames.append(nickname)
        clients.append(client)

        print(f'nickname do cliente é {nickname}')
        broadcast(f'{nickname} entrou no chat!!!'.encode('utf-8'))
        client.send('conectado ao servidor'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('server está escutando')
recieve()