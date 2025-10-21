import tkinter as tk
from tkinter import *
from tkinter import ttk
from funcal import caluladora


class JanelaCalcula(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.geometry('400x300')
        #self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)
        
        MainFrame = ttk.Frame(self)
        MainFrame.grid(column=0, row=0, sticky=(N, E, S, W))
        
        ####################### ----- DISPLAY CALCULADORA ----- #######################
        
        exibe=StringVar()
        display=  ttk.Entry(MainFrame, width=32, textvariable=exibe)
        display.grid(column=3,row=1,sticky= (NSEW), padx=5, pady=5)

        ############################### -- Operadores  -- ######################################

        botaoADD = ttk.Button(MainFrame, text=" + ", command= caluladora(2))
        botaoADD.grid(column=4, row=1, sticky= (N, S), padx=5, pady=5)
        
        botaoSUB = ttk.Button(MainFrame, text=" - ", command= caluladora(1))
        botaoSUB.grid(column=4, row=2, sticky= (N, S), padx=5, pady=5)
        
        botaoMULT = ttk.Button(MainFrame, text=" X ", command= caluladora(4))
        botaoMULT.grid(column=4, row=3, sticky= (N, S), padx=5, pady=5)
        
        botaoDIV = ttk.Button(MainFrame, text=" / ", command= caluladora(3))
        botaoDIV.grid(column=4, row=4, sticky= (N, S), padx=5, pady=5)

        botaoEQU = ttk.Button(MainFrame, text=" = ", command= caluladora())
        botaoEQU.grid(column=5, row=4, sticky= (N, S), padx=5, pady=5)

        botaoSair = ttk.Button(MainFrame, text="Sair",command= self.destroy)
        botaoSair.grid(column=5, row=1, sticky= (SW), padx=5, pady=5)

        
        ################################ T E C L A D O ################################
        

        botaoUM = ttk.Button(MainFrame, text="1", command=exibe('1'))
        botaoUM.grid(column=1, row=2, sticky= (NSEW), padx=5, pady=5)
        
       # botaoDOIS = ttk.Button(MainFrame, text="2", command=exibe='2')
        #botaoDOIS.grid(column=2, row=2, sticky= (NSEW), padx=5, pady=5)
        
        #botaoTRES = ttk.Button(MainFrame, text="3", command= exibe='3')
        #botaoTRES.grid(column=3, row=2, sticky= (NSEW), padx=5, pady=5)
        
        #botaoQUATRO = ttk.Button(MainFrame, text="4", command=exibe='4')
        #botaoQUATRO.grid(column=1, row=3, sticky= (NSEW), padx=5, pady=5)

        #botaoCINCO = ttk.Button(MainFrame, text="5", command=exibe='5')
        #botaoCINCO.grid(column=2, row=3, sticky= (NSEW), padx=5, pady=5)

        #botaoSEIS = ttk.Button(MainFrame, text="6", command=exibe='6')
        #botaoSEIS.grid(column=3, row=3, sticky= (NSEW), padx=5, pady=5)
        
        botaoSETE = ttk.Button(MainFrame, text="7", command= exibe('7'))
        botaoSETE.grid(column=1, row=4, sticky= (NSEW), padx=5, pady=5)
        
        #botaoOITO = ttk.Button(MainFrame, text="8", command=exibe='8')
        #botaoOITO.grid(column=2, row=4, sticky= (NSEW), padx=5, pady=5)
        
        #botaoNOVE = ttk.Button(MainFrame, text="9", command=exibe='9')
        #botaoNOVE.grid(column=3, row=4, sticky= (NSEW), padx=5, pady=5)
        
        #botaoZERO = ttk.Button(MainFrame, text="0", command=exibe='0')
        #botaoZERO.grid(column=2, row=5, sticky= (NSEW), padx=5, pady=5)

        #botaoPONTO = ttk.Button(MainFrame, text="-/+", command=exibe='.')
        #botaoPONTO.grid(column=1, row=5, sticky= (NSEW), padx=5, pady=5)

        #botaoTROCA = ttk.Button(MainFrame, text=".", command= exibe='-')
        #botaoTROCA.grid(column=3, row=5, sticky= (NSEW), padx=5, pady=5)
    

    def print(self,numero):
      self.exibe = numero
    
    def opera(opc):
        caluladora.operador(opc)
    
        if opc == 0 :
            sinal = 'sinais'
        return sinal


    #def equa ():
    #    exibe = resultado()