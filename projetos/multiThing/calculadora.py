from tkinter import *
from tkinter import ttk
import tkinter as tk
import Python.projetos.multiThing.janela as janela

class calculadora(tk.toplevel):
    def __init__(self, principal):
        super().__init__(principal)
        
        self.title("Calculadora")
        frameCalcula = ttk.Frame(self,padding= '3 3 12 12')
        frameCalcula.grid(column=0, row=0, sticky=(N, E, S, W))
        

        