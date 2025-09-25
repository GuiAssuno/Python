import googlemaps
from datetime import datetime

# Substitua 'SUA_CHAVE_DA_API' pela sua chave da API
gmaps = googlemaps.Client(key='SUA_CHAVE_DA_API')

# Geocodificação de um endereço
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
print(geocode_result)

# Direções entre dois pontos
directions_result = gmaps.directions('Sydney Town Hall', 'Parramatta, NSW', mode='transit', departure_time=datetime.now())
print(directions_result)


import tkinter as tk
from tkinter import ttk
from tkinterweb import HtmlFrame
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='SUA_CHAVE_DA_API')

def show_map():
    map_url = gmaps.static_map(size='800x600', center='Sydney Town Hall', zoom=15)
    map_frame.set_url(map_url)

root = tk.Tk()
root.title("Google Maps em Python")
map_frame = HtmlFrame(root)
map_frame.pack(fill=tk.BOTH, expand=True)
show_map()
root.mainloop()



import requests
from bs4 import BeautifulSoup

# URL do site que você quer obter informações
url = 'https://exemplo.com'

# Fazendo a requisição HTTP para o site
response = requests.get(url)

# Parsing do conteúdo HTML do site
soup = BeautifulSoup(response.content, 'html.parser')

# Encontrar e extrair informações
for info in soup.find_all('tag_da_informacao', class_='classe_da_informacao'):
    print(info.text)












import cx_Oracle

# Configurações da conexão
dsn_tns = cx_Oracle.makedsn('host', 'port', service_name='service_name')

# Conectar ao banco de dados
connection = cx_Oracle.connect(user='usuario', password='senha', dsn=dsn_tns)

# Criar um cursor
cursor = connection.cursor()

# Executar uma consulta SQL
cursor.execute('SELECT * FROM tabela')

# Iterar pelos resultados
for row in cursor:
    print(row)

# Fechar o cursor e a conexão
cursor.close()
connection.close()


Substitua 'host', 'port', 'service_name', 'usuario', 'senha' e 'tabela' pelas suas próprias configurações e credenciais do banco de dados.


