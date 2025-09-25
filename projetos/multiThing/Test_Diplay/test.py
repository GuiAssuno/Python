import tkinter as tk
from tkinter import *
from tkinter import ttk
import funcal as F

class JanelaCalcula(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.geometry('320x200')

        MainFrame = ttk.Frame(self)
        MainFrame.grid(column=0, row=0, sticky=(N, E, S, W))
        MainFrame.columnconfigure(1,weight=3)

        ####################### ----- DISPLAY CALCULADORA ----- #######################        
        
        self.display=  Text(MainFrame, width=32,height=2,wrap='none',
                       relief='solid')
        self.display.grid(column=1,row=1, columnspan=3, sticky= (NSEW), padx=5, pady=5)

        ################################ T E C L A D O ################################

        botaoUM = ttk.Button(MainFrame, text= "1", command= lambda: self.digito ('1'))
        botaoUM.grid(column=1, row=2, sticky= (NSEW), padx=5, pady=5)

        botaoU = ttk.Button(MainFrame, text= "=", command= self.calculo)
        botaoU.grid(column=2, row=2, sticky= (NSEW), padx=5, pady=5)

    def digito(self,numero):                # função para exibir numero do botão
        self.display.delete('1.0', '2.end')
        self.display.insert('1.0', "3+4+3-5/98*46735^4787(45-23)")   # no display Text
        print(numero)

    def calculo(self):
        tela = self.display.get('1.0', '1.end')
        self.display.delete('1.0', '2.end')
        prin = F.separaChar(tela)
        self.display.insert('1.0', prin)

if __name__ == "__main__":
    app = JanelaCalcula()
    app.mainloop()