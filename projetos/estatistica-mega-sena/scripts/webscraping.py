import requests
from bs4 import BeautifulSoup
import pandas as pd
import gerador_de_numeros as gn
import re

salvar = gn.gerador_de_dezenas()

# Sua string de dados
dados = "2735 - 11/06/2024 - 05 33 46 47 53 592731 - 01/06/2024 - 04 12 32 45 49 58"

# Solução simples e direta
def separar_registros(dados):
    # Adiciona espaço entre registros quando um termina com 2 dígitos e outro começa com número
    print(dados)
    padrao = r"\d{4} - \d{2}/\d{2}/\d{4} -  \d{2}(?: \d{2}){5}"

    texto = re.findall(padrao, dados)
    #texto = re.findall(r"\d{4} - \d{2}/\d{2}/\d{4} - \d{2}(?: \d{2}){5}", dados)
    print(texto)
    # Divide por espaços múltiplos e filtra
    partes = texto
    print(partes)
    registros = []
    
    # Reconstrói os registros (cada registro tem 11 partes: N, -, DD, /, MM, /, AAAA, -, NN, NN, NN, NN, NN, NN)
    i = 0
    print (len(partes))
    while i < len(partes):
        if partes[i].isdigit() and i + 12 < len(partes):
            registro = f"{partes[i]} - {partes[i+1]} {partes[i+2]} {partes[i+3]} {partes[i+4]} {partes[i+5]} - {partes[i+6]} {partes[i+7]} {partes[i+8]} {partes[i+9]} {partes[i+10]} {partes[i+11]}"
            registros.append(registro)
            i += 12
        else:
            i += 1
    print (registro)
    return registros



def coletar_dados_site(url, tag_alvo, classe_alvo):
    """
    Função genérica para fazer web scraping em um site.
    
    :url: A URL completa do site que você quer analisar.
    :tag_alvo: A tag HTML onde o dado está (ex: 'h2', 'a', 'div').
    :classe_alvo: A classe CSS do elemento para filtrar (ex: 'post-title').
    :return: Uma lista com os textos dos elementos encontrados.
    """
    print(f"Iniciando a coleta de dados da URL: {url}")
    
    # Lista para armazenar os dados coletados
    dados_coletados = []

    try:

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
            resultado = separar_registros(texto)
            print(len(resultado))
            dados_coletados.append(resultado)
            
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
url_alvo = 'https://asloterias.com.br/lista-de-resultados-da-mega-sena'
# Com base na nossa inspeção, a tag é 'a' e a classe é 'feed-post-link'
tag = 'div'            
classe = 'col-md-8'   #quesquisando no google MDTDab

# Chama a função
titulos_g1 = coletar_dados_site(url_alvo, tag, classe)
print(len(titulos_g1))
# Se a coleta funcionou, vamos salvar os dados em um CSV usando pandas
if titulos_g1:
    # Cria um DataFrame do pandas
    #df = pd.DataFrame(titulos_g1, columns=['Manchetes'])
    #print(df.describe())
    # Salva em um arquivo CSV
    #df.to_csv('manchetes_g1.csv')
    print(salvar.salvar(titulos_g1,arquivo="scrape.txt"))
    
    
    
 #   print("\n--- Primeiras 5 manchetes coletadas: ---")
  #  print(df.head())
   # print("\nDados salvos com sucesso no arquivo 'manchetes_g1.csv'!")