import tkinter as tk
from tkinter import *
from tkinter import ttk


class JanelaRecogination(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Recogination")
        self.geometry('800x600')

        # Crie os elementos da janela filha aqui...
        MainFrame = ttk.Frame(self)
        MainFrame.grid(column=0, row=0, sticky=(N, E, S, W))
        
        
        botao = ttk.Button(MainFrame, text="Sair !", command=exit)
        botao.grid(column=7,row=4, rowspan=1, sticky=(SW),padx=4, pady=4)

        chat = ttk.Entry (MainFrame, width=64, xscrollcommand= "Y", font=18)
        chat.grid(column=5, row=4,rowspan=1, columnspan=1, sticky=(NSEW), padx=8, pady=2)

        textbox = tk.Text(MainFrame, width=64, height= 32)
        textbox.grid(column=5,row=3, rowspan=1,columnspan= 1, sticky= (NSEW),padx=8,pady=4)

if __name__ == "__main__":
    app = JanelaRecogination()
    app.mainloop()