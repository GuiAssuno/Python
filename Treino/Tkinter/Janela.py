from tkinter import *
from tkinter import ttk

# Funcao Calculate
def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

#configura a janela principal do aplicativo, dando a ela o título "Pés para Metros".
janela = Tk()
janela.title("Tentativa de App")                                                    

#Criando um widget de quadro, que conterá o conteúdo da interface de usuário.
frame = ttk.Frame(janela, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky=(N, W, E, S))
janela.columnconfigure(0, weight=1)
janela.rowconfigure(0, weight=1)

#variavel pes
feet = StringVar()
#caixa de entrada
feet_entry = ttk.Entry(frame, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky= (W, E))

#variavel metros
meters = StringVar()

#exibe o resultado da conversao
ttk.Label(frame, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

#botao calcular
ttk.Button (frame, text= "Calcular", command=calculate).grid(column=3,row=3, sticky=(W))

# frases
ttk.Label(frame, text="Pes").grid(column=3,row=1, sticky=(W))
ttk.Label(frame, text="Metros").grid(column=3, row=2, sticky=(W))
ttk.Label(frame, text="Equivale a").grid(column=1, row=2, sticky=(E))


#percorre todos os widgets contidos em nosso quadro e da um pouco de espaço ao redor de cada um 
for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)


#coloca o foco no nosso widget de entrada. Assim, o cursor começará naquele campo.
feet_entry.focus()

#se o usuário apertar Return (Enter no Windows), ele ira chamar a funcao calculate
janela.bind("<Return>", calculate)                                                                                         

janela.mainloop()