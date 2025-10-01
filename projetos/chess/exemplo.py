import tkinter as tk

class TabuleiroXadrez:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabuleiro de Xadrez")
        
        # Configurações do tabuleiro
        self.tamanho_casa = 60
        self.cor_clara = "#F0D9B5"
        self.cor_escura = "#B58863"
        
        # Criar canvas
        tamanho_total = self.tamanho_casa * 8
        self.canvas = tk.Canvas(root, width=tamanho_total, height=tamanho_total)
        self.canvas.pack(padx=20, pady=20)
        
        # Desenhar o tabuleiro
        self.desenhar_tabuleiro()
        
        # Adicionar coordenadas
        self.adicionar_coordenadas()
        
    def desenhar_tabuleiro(self):
        """Desenha as 64 casas do tabuleiro"""
        for linha in range(8):
            for coluna in range(8):
                x1 = coluna * self.tamanho_casa
                y1 = linha * self.tamanho_casa
                x2 = x1 + self.tamanho_casa
                y2 = y1 + self.tamanho_casa
                
                # Alternar cores
                if (linha + coluna) % 2 == 0:
                    cor = self.cor_clara
                else:
                    cor = self.cor_escura
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="")
    
    def adicionar_coordenadas(self):
        """Adiciona letras (a-h) e números (1-8) ao redor do tabuleiro"""
        letras = "abcdefgh"
        tamanho_total = self.tamanho_casa * 8
        
        # Frame para as coordenadas
        frame_coord = tk.Frame(self.root)
        frame_coord.pack()
        
        # Letras na parte inferior
        frame_letras = tk.Frame(frame_coord)
        frame_letras.pack()
        
        tk.Label(frame_letras, text="  ", width=2).pack(side=tk.LEFT)
        for i, letra in enumerate(letras):
            tk.Label(frame_letras, text=letra, width=7, font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        
        # Números na lateral (já incluídos visualmente no canvas)
        for i in range(8):
            x = -15
            y = i * self.tamanho_casa + self.tamanho_casa // 2
            self.canvas.create_text(x, y, text=str(8-i), font=("Arial", 10, "bold"))

# Criar janela principal
root = tk.Tk()
tabuleiro = TabuleiroXadrez(root)
root.mainloop()