#bibliotecas utilizadas
import socket
import threading
import hashlib


host  = '127.0.0.1' #local host
port = 666

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
#nome do adm
nome_administrador = 'administrador'

#listas e dicionarios:
comandos_lista = ['/cadastrar', '/emails', '/clientes', '/mensagem, /emails_cadastrados']

clients = []
nicknames = []
emails = [] #lista nova
senhas = [] #lista nova
emails_cadastrados = [] #lista nova
    

#coletar os emails da lista nos emails (novo)
with open('usuarios_SOCKET.txt', 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()  
            partes = linha.split(':')
            if len(partes) == 2:
                arquivo_email, arquivo_senha = partes
                emails.append(arquivo_email)
                senhas.append(arquivo_senha)


#funções novas
#função para cadastrar email e senha nova no arquivo txt(novo)
def cadastrar_usuario(email, senha):
    with open('usuarios_SOCKET.txt', 'a') as arquivo:
        arquivo.write(f'{email}:{senha}\n')



#função para os comandos (novo)
def comandos():
    while True:
        comando = input('ADMIN > ')
        if comando == '/cadastrar': #comando para cadastrar clientes novos no banco de dados(txt)
            parar = 1
            email_novo = input('email: ')
            
            if email_novo in emails:
                while parar == 1:
                    print("email digitado ja está cadastrado, digite outro")
                    email_novo = input('email: ')
                    if email_novo in emails:
                        continue
                    else:
                        parar = 2
            senha_nova = input('senha: ')
            md5 = hashlib.md5() # encriptografar a senha com o md5
            md5.update(senha_nova.encode('utf-8'))
            senha_encriptografada = md5.hexdigest()
            cadastrar_usuario(email_novo, senha_encriptografada)
            emails.append(email_novo)
            senhas.append(senha_encriptografada)

        elif comando == '/emails': #comando para mostrar os emails
            print()
            for email in emails:
                print(email)
        
        elif comando == '/clientes': #comando para mostrar os clientes cadastrados
            for nomes in nicknames:
                print(f'> {nomes}')
        
        elif comando == '/comandos': #ver todos os comandos
            print()
            for comando_lista in comandos_lista:
                print(comando_lista)
                print()
            print()

        elif comando == '/mensagem': #mandar mensagem para os clientes
            print()
            escrita_administrador = input('administrador: ')
            escrita_administrador = str(escrita_administrador)
            mensagem_administrador = f'{nome_administrador}: {escrita_administrador}'
            mensagem_administrador = mensagem_administrador.encode('utf-8')
            broadcast(mensagem_administrador)

        elif comando == '/emails_cadastrados': #verificar os emails cadastrados
             for email_cadastrado in emails_cadastrados:
                  print(email_cadastrado)
        


#função para mandar a mensagem para todos os clientes (original)
def broadcast(message):
    for client in clients:
        client.send(message)

#função para, caso consiga, fazer o broadcast da mensagem recebida (original)
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

#função para receber e interpretar mensagens (original)
print()
def receba():
    while True:
        client, address = server.accept()
        print(f"conectando com {str(address)} ")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nickname = str(nickname)

        client.send('EMAIL'.encode('utf-8'))
        email = client.recv(1024).decode('utf-8')
        email = str(email)

        #verifica se o email recebido ja está logado (novo)
        if email in emails_cadastrados:
            client.send('CADASTRADO'.encode('utf-8'))
            continue
        else:
            client.send('SENHA'.encode('utf-8')) #se o email nao estiver cadastrado recebe a senha (novo)
            senha = client.recv(1024)
            md5 = hashlib.md5()
            md5.update(senha) #encriptografa a senha recebida (novo)
            senha_encriptografada = md5.hexdigest() 


        #verifica se o email digitado existe dentro da lista de emails (novo)
        if email in emails:
                posicao_da_lista = emails.index(email)
                print(posicao_da_lista)
                #verifica se a senha digitada está correta (novo
                print(senhas)
                if senha_encriptografada == senhas[posicao_da_lista]:
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

        #thread para rodar a função de lidar com as mensagens dentro da função de receber (antigo)
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

#thread para o servidor sempre poder dar comando (novo)
admin_thread = threading.Thread(target=comandos)
admin_thread.start()        

print('server está escutando')
print('/comandos para ver os comandos.')
receba()
