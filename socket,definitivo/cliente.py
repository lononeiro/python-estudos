import socket
import threading

nickname = input("escolha um nome: ") #define nickname como o nome escolhido

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET: define o endereço ipv4, SOCK_STREAM: define o tipo de socket como TCP
client.connect(('127.0.0.1', 55555)) #define o endereço IP

def recieve(): #função para fazer o esquema de receber mensagem
    while True:
        try:
            message = client.recv(1024).decode('utf-8') #recebe uma mensagem mandada pelo servidor
            if message == 'NICK': #caso a mensagem recebida pelo servidor for nick ele envia o nickname
                client.send(nickname.encode('utf-8')) #envia o nickname 
            else:
                print(message) #se nao receber nada diferente ele printa a mensagem recebida pelo servidor
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
