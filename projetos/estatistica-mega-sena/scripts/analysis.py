import pandas as pd

# Substitua 'zwei.csv' pelo nome do arquivo que você deseja analisar
nome_do_arquivo = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/zwei.csv'
nome_do_arquivo = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/zwei-minus.csv'
nome_do_arquivo = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/drie.csv'
nome_do_arquivo = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/vier.csv'
nome_do_arquivo = '/home/lola/VScode/Python/projetos/estatistica-mega-sena/csv/fünf.csv'

try:
    # Carrega o arquivo CSV para um DataFrame
    df = pd.read_csv(nome_do_arquivo)

    print(f"--- Análise Exploratória do Arquivo: {nome_do_arquivo} ---")

    # 1. Visualizar as 5 primeiras linhas do arquivo
    print("\n--- 5 Primeiras Linhas ---")
    print(df.head())

    # 2. Obter informações gerais sobre as colunas (tipos de dados, valores não nulos)
    print("\n--- Informações Gerais do DataFrame ---")
    df.info()

    # 3. Gerar estatísticas descritivas básicas para as colunas numéricas
    print("\n--- Estatísticas Descritivas ---")
    print(df.describe())

except FileNotFoundError:
    print(f"\nErro: O arquivo '{nome_do_arquivo}' não foi encontrado.")
except Exception as e:
    print(f"\nOcorreu um erro: {e}")