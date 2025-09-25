from googlesearch import search
import requests
from bs4 import BeautifulSoup

def google_search(query, num_results = 5):
    results = []
    for result in search(query,num_results, lang="pt"):
        results.append(result)
    return result

if __name__ == "__main__":
    while True:
        pergunta=input("O que voce quer saber? (Digite 'sair' para encerrar): ")
        if pergunta.lower()=="sair":
            print("Encerrando o programa")
            break
        print ("Buscando no Google...\n")
        resultados = google_search(pergunta)

        print("Aqui estão alguns resultados:")
        i = str
        
        for resultado in resultados:
            i = str(i) + str(resultado)
        
        print(f"{i}")

        url = resultados
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for info in soup.find_all():
            print(info)

