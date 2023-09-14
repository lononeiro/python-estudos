import socket
import threading

host  = '127.0.0.1' #local host
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

comandos_lista = ['/cadastrar', '/emails', '/clientes']
clients = []
nicknames = []
usuarios_dicionario = {}
emails = ['lucassgs58@gmail.com', 'bimbimbambam@gmail.com', '123' ]
senhas = ['123lucas', '123', '123']


def add_dicionario(email, senha):
    for email, senha in zip(emails, senhas):
        usuarios_dicionario[email] = senha

add_dicionario(emails, senhas)



def comandos():
    while True:
        comando = input('ADMIN > ')
        if comando == '/cadastrar':


            email_novo = input('email: ')
            senha_nova = input('senha: ')
            emails.append(email_novo)
            senhas.append(senha_nova)
            add_dicionario(email_novo, senha_nova)
            print(usuarios_dicionario)

        elif comando == '/emails':
            print()
            for email in emails:
                print(email)
        
        elif comando == '/clientes':
            for nomes in nicknames:
                print(f'> {nomes}')
        
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
            broadcast(f'{nickname} deixou o chat' .encode('utf-8'))
            nicknames.remove(nickname)
            break


def recieve():
    while True:
        client, address = server.accept()
        print(f"conectado com {str(address)} ")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nickname = str(nickname)

        client.send('EMAIL'.encode('utf-8'))
        email = client.recv(1024).decode('utf-8')
        email = str(email)

        client.send('SENHA'.encode('utf-8'))
        senha = client.recv(1024).decode('utf-8')
        senha = str(senha)
 


        if email in emails:
                    
                    
                    senha_correspondente = usuarios_dicionario[email]
                    if senha == senha_correspondente:
                        
                        nicknames.append(nickname)
                        clients.append(client)
                    else:
                        client.send('PASS'.encode('utf-8'))
                        client.close()
                        continue                

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
print('/comandos para ver os comandos.')
recieve()
