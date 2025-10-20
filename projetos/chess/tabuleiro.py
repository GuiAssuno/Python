import tkinter as tk
from tkinter import *
from tkinter import ttk


class Tabuleiro (tk.Tk):
    def __init__(self):
        super().__init__()

        self.title ("Chess Tab")
        tab = ttk.Frame(self, padding='2 2 2 2')
        tab.grid(columnspan=8,rowspan=8, sticky=(N, S, W, E))
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.canvas = tk.Canvas(self, width=(80*8), height=(80*8))
        

       # (ttk.Frame(tab).grid(columnspan=1,rowspan=1,sticky=(NSEW)))
    
        for linha in range(8):
            for coluna in range(8):
                x1 = coluna * 80
                y1 = linha * 80
                x2 = x1 + 80
                y2 = y1 + 80
                
                # Alternar cores
                if (linha + coluna) % 2 == 0:
                    cor = "#000000"
                else:
                    cor = "#ffffff"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="")
        
    


if __name__ == '__main__':
    app = Tabuleiro()
    app.mainloop()