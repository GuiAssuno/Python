import ctypes
import random
import streamlit as slit
import pandas as pd
import pathlib
import time

# --- 1. Carregar a biblioteca C ---
try:
    lib = ctypes.CDLL('/home/lola/VScode/C/Estrutura_de_Dados/trabalho_ed/library/libc.so')
except OSError as e:
    print(f"Erro ao carregar a biblioteca C: {e}")
    print("Você compilou o quick_sort.c para libc.so?")
    exit()

# --- 2. Definir a função ---
lib.inicia_quick_sort.restype = ctypes.c_double  # O retorno é um double
lib.inicia_quick_sort.argtypes = [
    ctypes.POINTER(ctypes.c_int), # ponteiro para o vetor de int
    ctypes.c_int,                 # int n
    ctypes.c_int                  # int op
]

# --- 3. Função "wrapper" do Python ---
def executar_c(tamanho, op_metodo, usar_fixo=False):
    
    if usar_fixo:
        # Use os elementos fixos
        dados = [3, 7, 9, 2, 9, 6, 4, 1, 0, 8, 5]
        # Garante que o tamanho seja o correto
        if tamanho > len(dados):
            dados.extend([0] * (tamanho - len(dados))) # Preenche com 0
        dados = dados[:tamanho] # Corta se for menor
    else:
        # Gerar elementos aleatórios (Python é mais rápido nisso)
        dados = [random.randint(0, 10000) for _ in range(tamanho)]

    # Converte a lista Python em um array C
    ArrayC = ctypes.c_int * tamanho
    vetor_c = ArrayC(*dados) # O '*' "desempacota" a lista

    # --- 4. Chamar a função C! ---
    print(f"Executando C: tam={tamanho}, op={op_metodo}")
    
    # Python chama C aqui. O C executa na velocidade máxima.
    tempo_segundos = lib.inicia_quick_sort(vetor_c, tamanho, op_metodo)
    
    tempo_ms = tempo_segundos * 1000.0
    print(f"C retornou: {tempo_ms:.4f} ms")
    
    return tempo_ms



# --- Gerenciamento de Estado (para guardar os dados do gráfico) ---
if 'resultados' not in slit.session_state:
    slit.session_state.resultados = pd.DataFrame(columns=['Tamanho (milhares)', 'Tempo (ms)', 'Metodo'])

# --- Interface Gráfica (Side Bar) ---
slit.sidebar.title("Configurações do Teste")


mapa_algoritmo = {
    "Lomuto": "1",
    "Hoare": "2",
    "3-Vias": "3"
}

mapa_metodos = {
    "Último":"1",
    "Primeiro":"2",
    "Mediana de 3":"3",
    "Meio":"4",
    "Aleatório":"5"
}

algoritmo = slit.sidebar.selectbox("Algoritmo de Partição",  ("Lomuto","Hoare","3-Vias"), index=0)
op_algoritimo = mapa_algoritmo[algoritmo]

metodo = slit.sidebar.selectbox("Método de Escolha do Pivô", ("Último",
    "Primeiro",
    "Mediana de 3",
    "Meio",
    "Aleatório"), index=0)
op_pivot = mapa_metodos[metodo]


# Slider para o tamanho
tam = slit.sidebar.slider("Tamanho do Vetor", 
                        min_value=1000, 
                        max_value=100000, 
                        value=1000, 
                        step=1000)

# Escolha de dados
tipo_dados = slit.sidebar.radio("Tipo de Dados", ["Aleatórios", "Vetor Fixo"])
usar_fixo = (tipo_dados == "Vetor Fixo")

# Botão de Executar
if slit.sidebar.button("Executar Teste"):
    # Chamar nossa função "wrapper" que chama o C
    op_code = int(op_algoritimo + op_pivot)

    with slit.spinner(f"Executando {algoritmo} com pivô {metodo} de {tam} elementos..."):
        tempo_ms = executar_c(tamanho=tam, op_metodo=op_code, usar_fixo=usar_fixo)
    
    # Adicionar dados ao nosso DataFrame
    nova_linha = pd.DataFrame({
        'Tamanho': [100000],
        'Tempo': [tempo_ms],
        'Metodo': [algoritmo]
    })
    slit.session_state.resultados = pd.concat([slit.session_state.resultados, nova_linha], ignore_index=True)

# Botão de Limpar
if slit.sidebar.button("Limpar Dados do Gráfico"):
    slit.session_state.resultados = pd.DataFrame(columns=['Tamanho', 'Tempo (ms)', 'Metodo'])


# ------------------------------------------ Área Principal (Gráfico e Dados) ---------------------------------------
slit.title("Analise de Algoritmos e de Pivot" \
" QuickSort")

slit.header("Gráfico de Desempenho")

if not slit.session_state.resultados.empty:
    # O Streamlit cria um gráfico de linhas automaticamente!
    slit.line_chart(
        slit.session_state.resultados,
        x='Tamanho',
        y='Tempo (ms)',
        x_label= 'Tamanho',
        y_label='Tempo (ms)',
        color='Metodo' # Uma linha para cada método!
    )
    
    slit.header("Dados Coletados")
    slit.dataframe(slit.session_state.resultados)
else:
    slit.info("Clique em 'Executar Teste' na barra lateral para começar.")