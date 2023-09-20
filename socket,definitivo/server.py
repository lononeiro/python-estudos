import socket
import threading
import hashlib

host  = '127.0.0.1' #local host
port = 666

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

nome_administrador = 'administrador'

#listas e dicionarios:
usuarios_dicionario = {}
comandos_lista = ['/cadastrar', '/emails', '/clientes', '/mensagem, /emails_cadastrados']

clients = []
nicknames = []

emails = ['lucassgs58@gmail.com', 'bimbimbambam@gmail.com', '123' ]
emails_cadastrados = []
senhas = ['123lucas', '123', '123']


#funções:
def comandos():
    while True:
        comando = input('ADMIN > ')
        if comando == '/cadastrar':

            email_novo = input('email: ')
            senha_nova = input('senha: ')
            emails.append(email_novo)

            md5 = hashlib.md5()
            md5.update(senha_nova.encode('utf-8'))
            senha_encriptografada = md5.hexdigest()
            senhas.append(senha_encriptografada)

            print(senhas)   
            add_dicionario(email_novo, senha_nova)

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
                print()
            print()

        elif comando == '/mensagem':
            print()
            escrita_administrador = input('administrador: ')
            escrita_administrador = str(escrita_administrador)
            mensagem_administrador = f'{nome_administrador}: {escrita_administrador}'
            mensagem_administrador = mensagem_administrador.encode('utf-8')
            broadcast(mensagem_administrador)

        elif comando == '/emails_cadastrados':
             for email_cadastrado in emails_cadastrados:
                  print(email_cadastrado)
        




def add_dicionario(email, senha):
    for email, senha in zip(emails, senhas):
        usuarios_dicionario[email] = senha

add_dicionario(emails, senhas)

#função para cadastrar email e senha nova
def cadastrar(email_novo, senha_nova):
            email_novo = input('email: ')
            senha_nova = input('senha: ')
            emails.append(email_novo)
            senhas.append(senha_nova)
            add_dicionario(email_novo, senha_nova)

#função para mandar a mensagem para todos os clientes
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

#função para receber e interpretar mensagens
print()
def receba():
    while True:
        client, address = server.accept()
        print(f"conectado com {str(address)} ")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nickname = str(nickname)

        client.send('EMAIL'.encode('utf-8'))
        email = client.recv(1024).decode('utf-8')
        email = str(email)

        #verifica se o email recebido ja está logado
        if email in emails_cadastrados:
            client.send('CADASTRADO'.encode('utf-8'))
        else:
            client.send('SENHA'.encode('utf-8'))
            senha = client.recv(1024)
            md5 = hashlib.md5()
            md5.update(senha)
            senha_encriptografada = md5.hexdigest()


        #verifica se o email digitado existe dentro da lista de emails
        if email in emails:
                    
                    #verifica se a senha digitada está correta
                    senha_correspondente = usuarios_dicionario[email]
                    if senha_encriptografada == senha_correspondente:
                        
                        nicknames.append(nickname)
                        clients.append(client)
                        emails_cadastrados.append(email)
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

        #thread para rodar a função de lidar com as mensagens dentro da função de receber
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

#thread para o servidor sempre poder dar comando
admin_thread = threading.Thread(target=comandos)
admin_thread.start()        

print('server está escutando')
print('/comandos para ver os comandos.')
receba()
