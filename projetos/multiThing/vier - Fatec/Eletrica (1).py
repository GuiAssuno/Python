import tkinter as tk
from tkinter import *
from tkinter import ttk


class JanelaEletrica(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Eletrica")
        self.geometry('200x250')

        # Crie os elementos da janela filha aqui...
        MainFrame = ttk.Frame(self)
        MainFrame.grid(column=0, row=0, sticky=(N, E, S, W))

        botao = ttk.Button(MainFrame, text="Sair !", command=exit)
        botao.grid(column=1,row=3, sticky=(SW))
    