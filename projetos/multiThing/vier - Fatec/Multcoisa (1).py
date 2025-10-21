import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from calculadora import JanelaCalcula
from Conversao import JanelaConverso
from Recogination import JanelaRecogination
from Eletrica import JanelaEletrica


class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Janela Principal")
        self.geometry('400x300')
        #self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)

        
        Mainframe = ttk.Frame(self)
        Mainframe.grid(column=0,row=0,sticky=(N, E, S, W))
        self.listaOption = StringVar()
        # Crie os elementos da janela principal aqui...
        # Por exemplo, um botão para abrir a janela filha:
        botao = ttk.Button(Mainframe, text="Pronto", command= self.verifica)
        botao.grid(column= 3,row= 2, sticky=(SE))
        
       
        
        botao = ttk.Button(Mainframe, text="Sair !", command=exit)
        botao.grid(column=4,row=4, sticky=(SW))

        texto= ttk.Label(Mainframe, text="Escolha uma opção")
        texto.grid(column=2,row=1,sticky= (N,S))

        
        lista=  ttk.Combobox(Mainframe, textvariable=self.listaOption, state='readonly')
        lista.grid(column=2,row=2,sticky= (N,S), padx=5, pady=5)
        
        lista['values'] = ("Escolha uma opção", "Conversor", "Mat. Disgreta", "Reconhecedor de voz", "Eletronica") 
        lista.set("Escolha uma opção")
        #lista.bind('<<ComboboxSelected>>')


        for child in Mainframe.winfo_children(): 
            child.grid_configure(padx=15, pady=15)
        
        #lista.bind('<<ComboboxSelected>>', listaOption)

    def verifica(self):

        compara = self.listaOption.get()
        if(compara == "Conversor"):
            JanelaConverso()
        
        elif(compara == "Mat. Disgreta"):
            JanelaCalcula()

        elif(compara == "Reconhecedor de voz"):
            JanelaRecogination()
        
        elif(compara == "Eletronica"):
            JanelaEletrica()
        elif(compara == "Escolha uma opção"):
            messagebox.showinfo("Tente Novamente","Escolha uma Opção!!!!!")

        
  

       
    #def abrir_janela_filha(self):
        # Crie uma instância da janela filha e a exiba
     #   JanelaCalcula()








if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()