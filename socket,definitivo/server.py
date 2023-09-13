import socket
import threading

host  = '127.0.0.1' #local host
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

comandos_lista = ['/cadastrar', '/emails']
clients = []
nicknames = []
emails = ['lucassgs58@gmail.com']
senhas = []


def comandos():
    while True:
        comando = input('ADMIN > ')
        if comando == '/cadastrar':


            email_novo = input('email: ')
            senha_nova = input('senha: ')
            emails.append(email_novo)
            senhas.append(senha_nova)
            #numero = emails.index(email)
        elif comando == '/emails':
            print()
            for email in emails:
                print(email)
        elif comando == '/comandos':
            print()
            for comando_lista in comandos_lista:
                print(comando_lista)



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
            #email = emails[index]
            broadcast(f'{nickname} deixou o chat' .encode('utf-8'))
            nicknames.remove(nickname)
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f"conectado com {str(address)} ")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
      
        client.send('EMAIL'.encode('utf-8'))
        email = client.recv(1024).decode('utf-8')
 
        if email in emails:
            password_index = emails.index(email)
            print(password_index)
            senha = client.recv(1024).decode('utf-8')
            nicknames.append(nickname)
            clients.append(client)
            print('sucesso')
            print(senha)
            #if senha == senhas(password_index):

                #nicknames.append(nickname)
                #clients.append(client)
                #print('sucesso')
            #else:
                #client.send('PASS'.encode('utf-8'))
                #client.close()
                #continue                

        else:
            client.send('NOT'.encode('utf-8'))
            client.close()
            continue

        
        print(f'nickname do cliente é {nickname}')
        broadcast(f'{nickname} entrou no chat!!!'.encode('utf-8'))
        client.send('conectado ao servidor'.encode('utf-8'))


        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

admin_thread = threading.Thread(target=comandos)
admin_thread.start()        

        

print('server está escutando')
recieve()
