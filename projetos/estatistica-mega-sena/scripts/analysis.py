import pandas as pd

ascendente = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/ascendente.csv'
descendente = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/descendente.csv'
dia_concurso = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/dia_concurso.csv'
dois_grupos = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/dois_grupos.csv'
trinca_mais_sai = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/drie.csv'
fibonacci = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/fibonacci.csv'
frequencia_dezena = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/frequencia_dezena.csv'
quina_mais_sai = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/fünf.csv'
mair_tempo_sem_sair = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/mair_tempo_sem_sair.csv'
mdc = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/mdc.csv'
mmc = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/mmc.csv'
multiplicacao_total = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/multiplicacao_total.csv'
numero_do_consurso = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/numero_do_consurso.csv'
numero_primos = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/numero_primos.csv'
ordem_crescente = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/ordem_crescente.csv.csv'
ordem_saida = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/ordem_saida.csv'
par_impar = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/par_impar.csv'
quadrante = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/quadrante.csv'
soma_total = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/soma_total.csv'
subtracao_total = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/subtracao_total.csv'
tamanho_intervalo_entre_dezenas = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/tamanho_intervalo_entre_dezenas.csv'
tempo_atual_sem_sair = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/tempo_atual_sem_sair.csv'
total_de_possibilidades = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/total_de_possibilidades.csv'
tres_grupos = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/tres_grupos.csv'
quatra_mais_sai = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/vier.csv'
dupla_menos_sai = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/zwei-minus.csv'
dupla_mais_sai = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/zwei.csv'

try:
    
    # Carrega o arquivo CSV para um DataFrame
    df = pd.read_csv(dupla_mais_sai)

    print(f"--- Análise Exploratória do Arquivo: {dupla_mais_sai} ---")

    # 1. Visualizar as 5 primeiras linhas do arquivo
    print("\n--- 5 Primeiras Linhas ---")
    print(df.head())

    # 2. Obter informações gerais sobre as colunas (tipos de dados, valores não nulos)
    print("\n--- Informações Gerais do DataFrame ---")
    df.info()

    # 3. Gerar estatísticas descritivas básicas para as colunas numéricas
    print("\n--- Estatísticas Descritivas ---")
    print(f'{df.describe()}')

except FileNotFoundError:
    print(f"\nErro: O arquivo '{dupla_mais_sai}' não foi encontrado.")
except Exception as e:
    print(f"\nOcorreu um erro: {e}")