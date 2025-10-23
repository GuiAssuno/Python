import random
import os
import pathlib
import re

class gerador_de_dezenas:
    def __init__(self):
        self.NUMEROS = tuple(range(1, 61))
        self.resultado =''
        self.encontrado = False

    def gerador(self):
        dezenas = []

        while True:
            numero = random.choice(self.NUMEROS)

            if numero not in dezenas:
                dezenas.append(str(numero).zfill(2))

            if len(dezenas) == 6:
                break
            
        dezenas = sorted(dezenas)
        self.resultado = ' - '.join(dezenas)

        return self.resultado

    def salvar (self, conteudo, pasta = None, arquivo = 'apostas.txt'):

        caminho_abs_arquivo = pathlib.Path(__file__).resolve()
        pasta = caminho_abs_arquivo.parent.parent
        caminho = pasta / 'arquivos' / arquivo
        caminho_sorteios =  pasta / 'arquivos' / 'scrape.txt'

        padrao = r'\d{2} - \d{2} - \d{2} - \d{2} - \d{2} - \d{2}'
        try:
            if re.search (padrao, conteudo):
                try:
                    
                    print(caminho)
                except:
                    return 0

                try:
                    # VERIFICA SE É REPETIDO
                    with open(caminho, 'r', encoding='utf-8') as arq:
                        for linha in arq:
                            if conteudo in linha.strip():
                                self.encontrado = True
                                break
                    
                    # VERIFICA SE EXISTE
                    with open (caminho_sorteios, 'r', encoding='utf-8') as sorteios:
                        for sorteio_realizado in sorteios:
                            if conteudo == sorteio_realizado[-17]:
                                return "ja foi sorteado"

                except:
                    print ("ERRO NA LEITURA DO ARQUIVO")


                if not self.encontrado:
                    try:

                        with open(caminho, 'a', encoding='utf-8') as arq:     
                                arq.write(f"|    {conteudo}    |                          |                       |                     |\n")
                            
                    except Exception as e:
                        return f"Não foi possivel gravar no arquivo - {e}"
            
        
        except TypeError as e:
            print (f"Erro: {e}")            
            
            try:
                with open (caminho_sorteios, 'w', encoding='utf-8') as sorteios:
                    for linha in conteudo:
                        sorteios.write(f"{linha}\n")

            except Exception as e:
                return f"não funciou {e}"            

if __name__ == '__main__':
    
    resultado = gerador_de_dezenas()
    print(resultado.salvar(resultado.gerador()))