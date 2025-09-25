from tkinter import *
from tkinter import ttk
import tkinter as tk


#def exibe (*args):
    #<<ComboboxSelect>>
 #   conversao()
    #test.raiz
    

class principal(tk.Tk):
    def __init__(self):
        super().__init__()

        listaBox = StringVar()
        self.title("MULThings")   

        QuadroPrincipal = ttk.Frame(self, padding= "3 3 12 12")
        QuadroPrincipal.grid(column=5,row=5,sticky=(N, W, E, S))
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)


        botao= ttk.Button(self, text="Pronto",command= print("exibe"))
        botao.grid(column= 3, row= 5, sticky= (SW))

        TextInicial = ttk.Label(self,text="Escolha uma das opção").grid(column=3,row=1,sticky=N)

        lista = ttk.Combobox(self, textvariable= listaBox, state= 'readonly')
        lista.grid(column=3, row=2, sticky=(N,E,S,W))
        lista ['values'] = ("-- Escolha --","Conversor", "Matematica Disgreta", "Reconhecedor de fala", "Calculadora Eletronica")
        listaBox = lista.get()

        lista.current(0)


        def chama():
            calculadora()












        botaoSair= ttk.Button(self, text="Sair!",command=exit)
        botaoSair.grid(column=5,row=5)



if __name__ == '__main__':
    app = principal()
    app.mainloop()