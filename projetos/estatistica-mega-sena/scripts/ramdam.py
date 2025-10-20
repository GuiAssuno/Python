import random
import os

pasta = 'Python/projetos/estatistica-mega-sena/arquivos'
arquivo = 'apostas.txt'

caminho = os.path.join(pasta, arquivo)

'''
NUMEROS = tuple(range(1,61)) 

escolha = 0
dezenas = []

while True:
    numero = random.choice(NUMEROS)
    if numero not in dezenas:
        dezenas.append(if (numero <= 9 ) '0' + str(numero))

    if len(dezenas) == 6:
        break

dezenas = sorted(dezenas)
resultado = ''
'''

NUMEROS = tuple(range(1, 61))
dezenas = []
resultado =''
encontrado = False

while True:
    numero = random.choice(NUMEROS)

    if numero not in dezenas:
        if numero <= 9:
            formatada = '0' + str(numero)
        else:  
            formatada = str(numero)
        dezenas.append(formatada)

    if len(dezenas) == 6:
        break
    
dezenas = sorted(dezenas)

for dezena in dezenas:
    resultado += dezena + ' - '
print(resultado[:-3])
resultado = resultado[:-3]

try:
    with open(caminho, 'r', encoding='utf-8') as arq:
        for linha in arq:
            if resultado in linha.strip():
                encontrado = True
                break

except FileNotFoundError:
    print("Arquivo não encontrado.")


if not encontrado:
    with open(caminho, 'a', encoding='utf-8') as arq:
        arq.write(resultado + '\n')

