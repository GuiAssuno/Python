import tkinter as tk
from tkinter import *
from tkinter import ttk


class JanelaCalcula(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")

        # janela filha 
        MainFrame = ttk.Frame(self)
        MainFrame.grid(column=0, row=0, sticky=(N, E, S, W))


        exibe=StringVar()
        display=  ttk.Entry(MainFrame, width=32, textvariable=exibe)
        display.grid(column=3,row=1,sticky= (NSEW), padx=5, pady=5)
        #name.delete(0,'end')          # delete between two indices, 0-based
        #name.insert(0, 'your name')

        botaoADD = ttk.Button(MainFrame, text="+", command=soma(exibe))
        botaoADD.grid(column=4, row=1, sticky= (N, S), padx=5, pady=5)
        
        botaoSUB = ttk.Button(MainFrame, text="-", command=div(exibe))
        botaoSUB.grid(column=4, row=2, sticky= (N, S), padx=5, pady=5)
        
        botaoMULT = ttk.Button(MainFrame, text="X", command=mult(exibe))
        botaoMULT.grid(column=4, row=3, sticky= (N, S), padx=5, pady=5)
        
        botaoDIV = ttk.Button(MainFrame, text="%", command=div(exibe))
        botaoDIV.grid(column=4, row=4, sticky= (N, S), padx=5, pady=5)

        botaoEQU = ttk.Button(MainFrame, text="=", command=div(exibe))
        botaoEQU.grid(column=5, row=4, sticky= (N, S), padx=5, pady=5)

        botaoSair = ttk.Button(MainFrame, text="Sair",command=self.destroy)
        botaoSair.grid(column=5, row=1, sticky= (SW), padx=5, pady=5)

        
        # T E C L A D O #########################################################################
        

        botaoUM = ttk.Button(MainFrame, text="1", command= (exibe = "1"))
        botaoUM.grid(column=1, row=2, sticky= (NSEW), padx=5, pady=5)
        
        botaoDOIS = ttk.Button(MainFrame, text="2", command=div(exibe))
        botaoDOIS.grid(column=2, row=2, sticky= (NSEW), padx=5, pady=5)
        
        botaoTRES = ttk.Button(MainFrame, text="3", command=mult(exibe))
        botaoTRES.grid(column=3, row=2, sticky= (NSEW), padx=5, pady=5)
        
        botaoQUATRO = ttk.Button(MainFrame, text="4", command=div(exibe))
        botaoQUATRO.grid(column=1, row=3, sticky= (NSEW), padx=5, pady=5)

        botaoCINCO = ttk.Button(MainFrame, text="5", command=div(exibe))
        botaoCINCO.grid(column=2, row=3, sticky= (NSEW), padx=5, pady=5)

        botaoSEIS = ttk.Button(MainFrame, text="6", command=div(exibe))
        botaoSEIS.grid(column=3, row=3, sticky= (NSEW), padx=5, pady=5)
        
        botaoSETE = ttk.Button(MainFrame, text="7", command=soma(exibe))
        botaoSETE.grid(column=1, row=4, sticky= (NSEW), padx=5, pady=5)
        
        botaoOITO = ttk.Button(MainFrame, text="8", command=div(exibe))
        botaoOITO.grid(column=2, row=4, sticky= (NSEW), padx=5, pady=5)
        
        botaoNOVE = ttk.Button(MainFrame, text="9", command=mult(exibe))
        botaoNOVE.grid(column=3, row=4, sticky= (NSEW), padx=5, pady=5)
        
        botaoZERO = ttk.Button(MainFrame, text="0", command=div(exibe))
        botaoZERO.grid(column=2, row=5, sticky= (NSEW), padx=5, pady=5)

        botaoPONTO = ttk.Button(MainFrame, text="-/+", command=div(exibe))
        botaoPONTO.grid(column=1, row=5, sticky= (NSEW), padx=5, pady=5)

        botaoTROCA = ttk.Button(MainFrame, text=".", command=div(exibe))
        botaoTROCA.grid(column=3, row=5, sticky= (NSEW), padx=5, pady=5)



        
       
        
def soma(valor):
    valor
    return print (valor)

def sub(valor):
    valor
    return print (valor)

def mult(valor):
    valor
    return print (valor)

def div(valor):
    valor
    return print (valor)




if __name__ == "__main__":
    app = JanelaCalcula()
    app.mainloop()


