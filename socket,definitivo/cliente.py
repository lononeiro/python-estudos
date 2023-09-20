import socket
import threading

print('-' *10, 'login', '-'*10)
email = (input('digite seu email: '))
senha = (input('digite sua senha: '))
nickname = input("escolha um nome: ")
print('-'*27)

loop = 1
while loop == 1:
    if nickname != 'administrador':
        loop = 2
    else:
        print('nome inválido escolha outro.')
        nickname = input('escolha seu nome: ')


email = str(email)
senha = str(senha)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 666))

stop_thread = False

def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))

            elif message == 'EMAIL':
                client.send(email.encode('utf-8'))
            
            elif message == 'CADASTRADO':
                print('esse email já está cadastrado')
                client.close()
                stop_thread = True
                
            elif message == 'SENHA':
                client.send(senha.encode('utf-8'))

            elif message == 'NOT':
                print('email inválido, não foi possivel conectar.')

                client.close()
                stop_thread = True
                
            elif message == 'PASS':
                print('senha errada, desconectando...')
                client.close()
                stop_thread = True
                

            else:
                print(message)

        except:
            print('um erro aconteceu')
            client.close()  
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_threat = threading.Thread(target=write)
write_threat.start()
