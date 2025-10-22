import random
import os

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

    def salvar (self, pasta = None, arquivo = 'apostas.txt'):
        
        if (pasta == None):
            try:
                import pathlib

                caminho_abs_arquivo = pathlib.Path(__file__).resolve()
                pasta = caminho_abs_arquivo.parent.parent
                caminho = pasta / 'arquivos' / arquivo
                print(caminho)
            except:
                return 0
        else:
            caminho = os.path.join(pasta, arquivo)

        try:
            with open(caminho, 'r', encoding='utf-8') as arq:
                for linha in arq:
                    if self.resultado in linha.strip():
                        self.encontrado = True
                        break

        except FileNotFoundError:
            return "Arquivo não encontrado."

        if not self.encontrado:
            
            try:
                with open(caminho, 'a', encoding='utf-8') as arq:
                    arq.write(f"|    {self.resultado}    |                          |                       |                     |\n")
            
            except Exception as e:
                return f"Não foi possivel gravar no arquivo - {e}"


if __name__ == '__main__':
    
    resultado = gerador_de_dezenas()
    print(resultado.gerador())
    print(resultado.salvar())