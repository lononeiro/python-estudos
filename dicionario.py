email = {}

m = 1

while m == 1:   

    
    print('digite seu nome para criar email: ')
    nome = str(input())
    emails = nome.lower() + '@gmail.com'
    email[nome] = emails
    print('digite 1 para continuar criando emails')
    m = int(input())

for item in email.values():
    print(item)
    