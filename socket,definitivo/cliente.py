#bibliotecas
import socket
import threading

#tela inicial de cadastro con função 
print('-' *10, 'login', '-'*10)
email = (input('digite seu email: '))
senha = (input('digite sua senha: '))
nickname = input("escolha um nome: ") 
print('-'*27)

#esquema para nao poder escolher o nome de administrador (novo)
loop = 1
while loop == 1:
    if nickname != 'administrador':
        loop = 2
    else:
        print('nome inválido escolha outro.')
        nickname = input('escolha seu nome: ')

#transforma o email e senha em string (novo)
email = str(email)
senha = str(senha)

#define as configuraçõe de rede (antigo)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 666))

stop_thread = False

#configuração para receber e interpretar mensagens recebidas pelo servidor
def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK': 
                client.send(nickname.encode('utf-8')) #envia o nome (angito)

            elif message == 'EMAIL': 
                client.send(email.encode('utf-8')) #envia o email (novo)
            
            elif message == 'CADASTRADO': #se receber essa mensagem é porque o email ja está cadastrado (novo)
                print('esse email já está cadastrado')
                client.close()
                stop_thread = True
                
            elif message == 'SENHA':
                client.send(senha.encode('utf-8')) #envia senha (novo)

            elif message == 'NOT': #recebe se o email for inválido (novo)
                print('email inválido, não foi possivel conectar.')
                
                client.close()
                stop_thread = True
                
            elif message == 'PASS': #recebe se a senha estiver errada (novo)
                print('senha errada, desconectando...')
                client.close()
                stop_thread = True
                

            else:
                print(message) #printa a mensagem (antigo)

        except:
            print('um erro aconteceu')
            client.close()  
            break
#função para escrever mensagens e mandar elas pro servidor (antigo)
def write():
    while True:
        message = f'{nickname}: {input()}'
        client.send(message.encode('utf-8'))

#faz com que as threads se iniciem (antigo)
recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_threat = threading.Thread(target=write)
write_threat.start()
