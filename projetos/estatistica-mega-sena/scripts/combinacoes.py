import pathlib

def gerador_com_for(NUMEROS):

    caminho_abs_arquivo = pathlib.Path(__file__).resolve()
    pasta = caminho_abs_arquivo.parent.parent
    caminho = pasta / 'arquivos' / 'combinacoes.txt'

    try:
        with open(caminho, 'w', encoding='utf-8') as arq:
            arq.write("")
    except Exception as e:
        return f"Não foi possivel limpar o arquivo - {e}"

    contador_combinacoes = 0

    for primeiro in range(1, NUMEROS - 4):
        for segundo in range(primeiro + 1, NUMEROS - 3):
            for terceiro in range(segundo + 1, NUMEROS - 2):
                for quarto in range(terceiro + 1, NUMEROS - 1):
                    for quinto in range(quarto + 1, NUMEROS):
                        for sexto in range(quinto + 1, NUMEROS):

                            dezenas = [primeiro, segundo, terceiro, quarto, quinto, sexto]
                            contador_combinacoes += 1

                            try:
                                with open(caminho, 'a', encoding='utf-8') as arq:
                                    linha_formatada = ", ".join([str(d).zfill(2) for d in dezenas])
                                    arq.write(f"{linha_formatada}\n")
                                    
                            except Exception as e:
                                return f"Não foi possivel gravar no arquivo - {e}"

    print(f"Total de combinações geradas: {contador_combinacoes}")
    return 


if __name__ == '__main__':

    gerador_com_for(61)
