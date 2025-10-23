import requests
from bs4 import BeautifulSoup
import pandas as pd
import gerador_de_numeros as gn
import re
import pathlib
salvar = gn.gerador_de_dezenas()


# Solução simples e direta
def separar_registros(dados, format):
    '''função para filtrar formatação especifica do codigo'''
    # filtra apenas o conteudo chave     
    partes = re.findall(format, dados)
    
    return partes



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
        padrao = r"\d{4} - \d{2}/\d{2}/\d{4} -  \d{2}(?: \d{2}){5}"
        
        for elemento in elementos_encontrados:
            # .text extrai apenas o texto de dentro da tag
            resultado = separar_registros(elemento.text, padrao)
        print(f"{len(resultado)} itens encontrados e extraídos.")
        return resultado

    except requests.exceptions.RequestException as e:
        print(f"Erro ao tentar acessar a página: {e}")
        return []
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return []


#============================  M A I N ====================================

url_alvo = 'https://asloterias.com.br/lista-de-resultados-da-mega-sena'
tag = 'div'            
classe = 'col-md-8'   #quesquisando no google MDTDab

dados_brutos = coletar_dados_site(url_alvo, tag, classe)
print(len(dados_brutos))

caminho_sorteios = (pathlib.Path(__file__).resolve().parent.parent) / 'arquivos' / 'scrape.txt'
atualizar = True

with open(caminho_sorteios, 'r') as c:
    numeros_de_linhas = len(c.readlines())
    if len(dados_brutos) <= numeros_de_linhas:
        atualizar = False

    if not numeros_de_linhas: 
        salvar.salvar(dados_brutos,arquivo="scrape.txt")

    if atualizar:
        print(salvar.salvar(dados_brutos,arquivo="scrape.txt"))
