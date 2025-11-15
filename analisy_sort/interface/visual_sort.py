import matplotlib.pyplot as plt
import time
import random

# Função para inicializar e atualizar o gráfico
def desenha_vetor(vetorzinho, pivot_index=-1, ponteiro_esq=-1, ponteiro_dir=-1, cor_destaque=None):
 
    if cor_destaque is None:
        cor_destaque = []

    plt.clf() 

    # NÃO ESQUECER Q X (índices) | Y (valores)
    # depois trocar para ver se fica melhor
    x = list(range(len(vetorzinho)))
    y = vetorzinho

    cor_das_bolinha = ['black'] * len(vetorzinho)
    tamanho_das_bolinha = [10] * len(vetorzinho)

    # cor para mostrar o pivot
    if pivot_index != -1:
        cor_das_bolinha[pivot_index] = 'red'
        tamanho_das_bolinha[pivot_index] = 60

    # cor dos selecionados  
    if ponteiro_esq != -1:
        cor_das_bolinha[ponteiro_esq] = 'green'
        tamanho_das_bolinha[ponteiro_esq] = 60
    if ponteiro_dir != -1:
        cor_das_bolinha[ponteiro_dir] = 'orange'
        tamanho_das_bolinha[ponteiro_dir] = 60

    # cor final 
    for auxiliar in cor_destaque:
        if auxiliar != pivot_index and auxiliar != ponteiro_esq and auxiliar != ponteiro_dir:
            cor_das_bolinha[auxiliar] = 'purple'
            tamanho_das_bolinha[auxiliar] = 60


    plt.scatter(x, y, c=cor_das_bolinha, s=tamanho_das_bolinha) #gera grafico kk

    
    plt.title("Quicksort_animado_kk")
    plt.xlabel("indice_vetor")
    plt.ylabel("valor")
    plt.xlim(-1, len(vetorzinho))
    plt.ylim(0, max(vetorzinho) + 1)
    plt.grid(True)


    plt.pause(0.1) 


def partition(vetorzinho, menor, maior):
    pivot = vetorzinho[maior]
    auxiliar = menor - 1

    #desenha o primeiro vector
    desenha_vetor(vetorzinho, pivot_index=maior, ponteiro_esq=menor, ponteiro_dir=maior-1)

    for ponteiro in range(menor, maior):
        
        desenha_vetor(vetorzinho, pivot_index=maior, ponteiro_esq=auxiliar+1, ponteiro_dir=ponteiro)

        if vetorzinho[ponteiro] <= pivot:
            auxiliar = auxiliar + 1
            
            vetorzinho[auxiliar], vetorzinho[ponteiro] = vetorzinho[ponteiro], vetorzinho[auxiliar]
            
            desenha_vetor(vetorzinho, pivot_index=maior, ponteiro_esq=auxiliar, ponteiro_dir=ponteiro, cor_destaque=[auxiliar, ponteiro])

    # troca-troca vetorzinho[auxiliar + 1] e vetorzinho[maior]
    vetorzinho[auxiliar + 1], vetorzinho[maior] = vetorzinho[maior], vetorzinho[auxiliar + 1]
    
    # troca final do pivô
    desenha_vetor(vetorzinho, pivot_index=auxiliar + 1, cor_destaque=[auxiliar + 1, maior])

    return auxiliar + 1

#  ==========  O Quick Sort  ==========
def quick_sort(vetorzinho, menor, maior):
    if menor < maior:
        partido = partition(vetorzinho, menor, maior)

        quick_sort(vetorzinho, menor, partido - 1)
        quick_sort(vetorzinho, partido + 1, maior)

#  ==========  ------------  ========== 


def visualiza_sort(vetorzinho):
    plt.ion()

    tamanho = len(vetorzinho) - 1
    
    desenha_vetor(vetorzinho) # funcao q desenha o graficuzinho

    quick_sort(vetorzinho, 0, tamanho)

    # mostra ordenado
    desenha_vetor(vetorzinho, cor_destaque=list(range(tamanho)))
    
    plt.title("cabo_é_o_fim_brow")
    plt.ioff() 
    plt.show() 


if __name__ == "__main__": 

    #lembrar que função 
    # ramdom.sample((range (1,100))intervalo onde ele busca esses numeros, (10)elementos) 
    # retorna sem repetição
    data = random.sample(range(1, 100), 50)# cria_o array
    
    
    print(f"Array Inicial: {data}")

    visualiza_sort(data)
    print(f"Array Final: {data}")
