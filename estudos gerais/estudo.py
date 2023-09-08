import operator
votos_urna = {}
urna = {22 : 'bolsolnaro', 13 : 'lula', 51 : 'artur do val', 89 : 'lucas', 84 : 'abobora', 67 : 'mateus', 75 : 'iago'}

for key, value in urna.items():
            print(key, "->", value)

for key in urna.keys():
       votos_urna[key] = 0
p = 1
while p == 1:

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


print('o resultado da votação foi: ')
print()

for value, key in votos_urna.items():
            print(urna[value], "->", key, " votos")


m = max(votos_urna.values())
x = next(k for k, v in votos_urna.items() if v == m)
print()
print(f'o {x} foi o vencedor com {votos_urna[numero_candidato]} votos')        