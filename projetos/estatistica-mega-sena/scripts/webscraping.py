import requests
from bs4 import BeautifulSoup
import pandas as pd

def coletar_dados_site(url, tag_alvo, classe_alvo):
    """
    Função genérica para fazer web scraping em um site.
    
    :param url: A URL completa do site que você quer analisar.
    :param tag_alvo: A tag HTML onde o dado está (ex: 'h2', 'a', 'div').
    :param classe_alvo: A classe CSS do elemento para filtrar (ex: 'post-title').
    :return: Uma lista com os textos dos elementos encontrados.
    """
    print(f"Iniciando a coleta de dados da URL: {url}")
    
    # Lista para armazenar os dados coletados
    dados_coletados = []

    try:
        # 1. FAZER A REQUISIÇÃO PARA O SITE
        # O cabeçalho 'User-Agent' ajuda a simular um navegador real, evitando bloqueios.
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        
        # Verifica se a requisição foi bem-sucedida (código 200)
        response.raise_for_status() 
        print("Página baixada com sucesso!")

        # 2. ANALISAR O CONTEÚDO HTML
        site = BeautifulSoup(response.text, 'lxml')
        print("HTML analisado. Procurando pelos dados...")

        # 3. LOCALIZAR OS DADOS
        # Encontra TODOS os elementos que correspondem à tag e classe fornecidas.
        elementos_encontrados = site.find_all(tag_alvo, class_=classe_alvo)
        
        if not elementos_encontrados:
            print(f"Atenção: Nenhum elemento encontrado com a tag '{tag_alvo}' e classe '{classe_alvo}'. Verifique o site.")
            return []

        # 4. EXTRAIR A INFORMAÇÃO
        for elemento in elementos_encontrados:
            # .text extrai apenas o texto de dentro da tag
            texto = elemento.text.strip() # .strip() remove espaços em branco extras
            dados_coletados.append(texto)
            
        print(f"{len(dados_coletados)} itens encontrados e extraídos.")
        return dados_coletados

    except requests.exceptions.RequestException as e:
        print(f"Erro ao tentar acessar a página: {e}")
        return []
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return []


# --- COMO USAR A FUNÇÃO ---

# Defina os parâmetros para o site que você quer coletar (Exemplo: G1)
url_alvo = 'https://g1.globo.com/'
# Com base na nossa inspeção, a tag é 'a' e a classe é 'feed-post-link'
tag = 'a'
classe = 'feed-post-link'

# Chama a função
titulos_g1 = coletar_dados_site(url_alvo, tag, classe)
print(titulos_g1)
# Se a coleta funcionou, vamos salvar os dados em um CSV usando pandas
if titulos_g1:
    # Cria um DataFrame do pandas
    df = pd.DataFrame(titulos_g1, columns=['Manchetes'])
    print(df.describe())
    # Salva em um arquivo CSV
    df.to_csv('manchetes_g1.csv', index=False, encoding='utf-8')
    
    print("\n--- Primeiras 5 manchetes coletadas: ---")
    print(df.head())
    print("\nDados salvos com sucesso no arquivo 'manchetes_g1.csv'!")