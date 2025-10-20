import pandas as pd

# 1. Defina o caminho do arquivo e o novo resultado que você quer adicionar
caminho_do_arquivo = 'zwei.csv'

# Crie um dicionário com os novos dados.
# IMPORTANTE: As chaves do dicionário DEVEM ser exatamente iguais aos nomes das colunas no CSV.
# Para 'zwei.csv', as colunas são: P1, P2, frequencia, atual, ultimo, maior, media
novo_resultado = {
    'P1': 1,
    'P2': 9,
    'frequencia': 15,
    'atual': 0,
    'ultimo': 2830,
    'maior': 300,
    'media': 95.5
}

try:
    # 2. Carregue o arquivo CSV existente para um DataFrame
    # O 'try...except' lida com o caso de o arquivo ainda não existir.
    try:
        df = pd.read_csv(caminho_do_arquivo)
    except FileNotFoundError:
        print(f"Arquivo '{caminho_do_arquivo}' não encontrado. Um novo arquivo será criado.")
        # Se o arquivo não existe, cria um DataFrame vazio com as colunas corretas
        df = pd.DataFrame(columns=novo_resultado.keys())

    # 3. Converta o novo resultado (dicionário) em um DataFrame de uma linha
    novo_df = pd.DataFrame([novo_resultado])

    # 4. Concatene (junte) o DataFrame original com o novo DataFrame
    # ignore_index=True é importante para resetar o índice da nova linha
    df_atualizado = pd.concat([df, novo_df], ignore_index=True)
    
    # Opcional: Visualizar as últimas linhas para confirmar a adição
    print("--- Últimas 5 linhas do arquivo (após adicionar o novo resultado) ---")
    print(df_atualizado.tail())

    # 5. Salve o DataFrame atualizado de volta para o arquivo CSV
    # index=False é ESSENCIAL para não salvar o índice do DataFrame como uma nova coluna
    df_atualizado.to_csv(caminho_do_arquivo, index=False)
    
    print(f"\nDados adicionados com sucesso ao arquivo '{caminho_do_arquivo}'!")

except Exception as e:
    print(f"Ocorreu um erro: {e}")

import pandas as pd

caminho_do_arquivo = 'zwei.csv'

# Carregue o arquivo
df = pd.read_csv(caminho_do_arquivo)

# Suponha que você quer editar a linha onde P1 é 10 e P2 é 33
# E você quer mudar o valor da coluna 'frequencia' para 41

# .loc é usado para localizar linhas e colunas por nome/condição
# A condição localiza a linha exata
condicao = (df['P1'] == 10) & (df['P2'] == 33)

# O segundo argumento de .loc é a coluna que você quer alterar
df.loc[condicao, 'frequencia'] = 41

# Salve as alterações de volta no arquivo
df.to_csv(caminho_do_arquivo, index=False)

print("Linha modificada com sucesso!")