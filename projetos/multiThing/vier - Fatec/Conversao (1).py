import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class JanelaConverso(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Converso")
        #self.geometry('400x300')

        # Crie a janela.
        MainFrame = ttk.Frame(self)
        MainFrame.grid(column=0, row=0, sticky=(N, E, S, W))
        MainFrame.columnconfigure(1, weight=2)
        MainFrame.columnconfigure(2, weight=3)
        MainFrame.columnconfigure(3, weight=2)
        MainFrame.columnconfigure(4, weight=1)
        MainFrame.rowconfigure(1, weight=3)




        self.exibe=StringVar()
        #################### Entrada do Display  ###############################
        Entra=  ttk.Entry(MainFrame, width=48, textvariable=self.exibe)
        Entra.grid(column=2,row=1,sticky= (NSEW), padx=20, pady=10)
        
        self.fim = StringVar()
        

        #################### Saida do Label  ###############################
        Saida = ttk.Label(MainFrame, textvariable= self.fim)
        Saida.grid(column=2, row=5, columnspan=1, rowspan=1, sticky=(N,W,E),padx=65, pady=5)

        #################### INFORMATIVO ENTRADA ###############################
        texte = ttk.Label(MainFrame, text= "Escolha o Tipo de Entrada")
        texte.grid(column=1, row=1,sticky=(W),padx=5, pady=10)

        #################### INFORMATIVO SAIDA ###############################
        texts = ttk.Label(MainFrame, text= "Escolha o Tipo de Saida")
        texts.grid(column=3, row=1,sticky=(E),padx=5, pady=10)
        #name.delete(0,'end')          # delete between two indices, 0-based
        #name.insert(0, 'your name')

        self.base = StringVar()
        self.baseFim = StringVar()

         # bin+ario
        Binario = ttk.Radiobutton(MainFrame, text='Binario', variable=self.base, value='2')
        Binario.grid(column=1,row=2,sticky= (NSEW),padx=15)
        Binario2 = ttk.Radiobutton(MainFrame, text='Binario', variable=self.baseFim, value='2')
        Binario2.grid(column=3,row=2,sticky= (NSEW),padx=15)
        
        # ternaria
        Ternaria = ttk.Radiobutton(MainFrame, text='Ternaria', variable=self.base, value='3')
        Ternaria.grid(column=1,row=3,sticky= (NSEW),padx=15)
        Ternaria2 = ttk.Radiobutton(MainFrame, text='Ternaria', variable=self.baseFim, value='3')
        Ternaria2.grid(column=3,row=3,sticky= (NSEW),padx=15)

        # octadecimal
        Octadecimal = ttk.Radiobutton(MainFrame, text='Octadecimal', variable=self.base, value='8')
        Octadecimal.grid(column=1,row=4,sticky= (NSEW),padx=15)
        Octadecimal2 = ttk.Radiobutton(MainFrame, text='Octadecimal', variable=self.baseFim, value='8')
        Octadecimal2.grid(column=3,row=4,sticky= (NSEW),padx=15)

        # decimal
        Decimal = ttk.Radiobutton(MainFrame, text='Decimal', variable=self.base, value='10')
        Decimal.grid(column=1,row=5,sticky= (NSEW),padx=15)
        Decimal2 = ttk.Radiobutton(MainFrame, text='Decimal', variable=self.baseFim, value='10')
        Decimal2.grid(column=3,row=5,sticky= (NSEW),padx=15)

        # hexadecimal
        Hexadecimal = ttk.Radiobutton(MainFrame, text='Hexadecimal', variable=self.base, value='16')
        Hexadecimal.grid(column=1,row=6,sticky= (NSEW),padx=15)
        Hexadecimal2 = ttk.Radiobutton(MainFrame, text='Hexadecimal', variable=self.baseFim, value='16')
        Hexadecimal2.grid(column=3,row=6,sticky= (NSEW),padx=15)
        
        
        
        
        botaoSair = ttk.Button(MainFrame, text="Sair !", command=exit)
        botaoSair.grid(column=4,row=5, sticky=(SW),padx=8)


        botaoGo = ttk.Button(MainFrame, text="Converter", command= self.potencia)
        botaoGo.grid(column=4,row=3, sticky=(SW),padx=8)

    def potencia(self):
        decimalConvertido = 0
        numerico = []
        Letra  = {"A" : 10 , "B" :11 ,"C": 12,"D":13,"E": 14 ,"F":15}
        #self.exibe.get()
        test = '010101111100110010110001011'
        separado = (list(test))    
        base = 2
        totalChar = len(separado)
        expoente = 0
        x = 0
    
        while x < totalChar:

            if separado[x] in Letra:
                numerico.append(Letra [separado[x]])       
            else:
                numerico.append(int(separado [x]))         
            x = x + 1          
        
        Indice = totalChar - 1
    
        while Indice >= 0:
            decimalConvertido = numerico[Indice]*(base**expoente) + decimalConvertido	        
            expoente = expoente + 1
            Indice = Indice - 1

        self.im = str(decimalConvertido)
        fim = self.dividir()
        
        self.fim.set(fim)

    
    def dividir(self):

        dividido = []   
        letra = {10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}
        
        #if self.fim == "":
            #valor = self.fim.get()
        #else:
        valor = int(self.im) #self.exibe.get()

        while valor != 0:
            resto = valor % 16 #self.baseFim 
            valor  =  valor // 16 #self.baseFim

            if resto < 10:                     
                dividido.append(str(resto))
            else:	
                dividido.append (letra.get(resto))                       

        dividido.reverse()

        resu = ''.join(dividido)
        
        #self.fim.set(dividido)
        return resu

    def logica(self):
        
        
        saida = self.baseFim.get()
        entrada = self.base.get()
        
        try:
            if (entrada == '' or saida == ''): 
                raise messagebox.ERROR ( "ATENÇÃO", "Escolha uma Opção!!!!!")   
        except  BaseException:
            pass

        if (entrada != "10"):
            fim = JanelaConverso.potencia
            print(fim)
        elif (saida != "10"):
            fim = JanelaConverso.dividir
            
        #if saida:
        
        return fim