import operator
cpfs = []
votos_urna = {}
urna = {22 : 'bolsolnaro', 13 : 'lula', 51 : 'artur do val', 89 : 'lucas', 84 : 'abobora', 67 : 'mateus', 75 : 'iago', 85 : 'vera'}

def validar_cpf(cpf):   
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    if resto < 2:
        digito_verificador1 = 0
    else:
        digito_verificador1 = 11 - resto

    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    if resto < 2:
        digito_verificador2 = 0
    else:
        digito_verificador2 = 11 - resto

    # Verifica se os dígitos verificadores estão corretos
    if int(cpf[9]) == digito_verificador1 and int(cpf[10]) == digito_verificador2:
        return True
    else:
        return False

for key, value in urna.items():
            print(key, "->", value)

for key in urna.keys():
       votos_urna[key] = 0
p = 1

while p == 1:
    print()
    cpf = (input('digite seu cpf: '))
    if validar_cpf(cpf): 
        if cpf in cpfs:
             print('esse cpf ja votou!!')
             continue
        else:
            cpfs.append(cpf)    

            print('digite o nuúmero de seu candidato:')
            
            numero_candidato = int(input())
            
            if numero_candidato in urna:
                print(f'você votou no {urna[numero_candidato]} com sucesso!!')
                
                votos_urna[numero_candidato] = votos_urna[numero_candidato] + 1
                print()
            else:
                print('esse candidato não existe!!')
                continue
            
            r = (input("digite continue para continuar votando: "))
            if r != 'continue':
                p = 0
    else:
        print('cpf invalido')
        continue

print('o resultado da votação foi: ')
print()

for value, key in votos_urna.items():
            print(urna[value], "->", key, " votos")


m = max(votos_urna.values())
x = next(k for k, v in votos_urna.items() if v == m)

x = urna[x]


print()
print(f'o {x} foi o vencedor com {votos_urna[numero_candidato]} votos')        