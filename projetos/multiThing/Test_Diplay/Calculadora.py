import funcal as F
import tkinter as tk
from tkinter import *
from tkinter import ttk

class JanelaCalcula(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.geometry('372x255')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        MainFrame = ttk.Frame(self)
        MainFrame.grid(column=0, row=0, sticky=(N, E, S, W))

        #MainFrame.columnconfigure(1,weight=2)
        #MainFrame.columnconfigure(2,weight=2)
        #MainFrame.columnconfigure(3,weight=2)
        #MainFrame.columnconfigure(4,weight=2)
        
        ####################### ----- DISPLAY CALCULADORA ----- #######################
        
        
        self.display=  Text(MainFrame, width=32,height=2,wrap='none',
                       relief='solid', state='disabled')
        self.display.grid(column=1,row=1, columnspan=3 ,sticky= (NSEW), padx=5, pady=5)
        
        self.display.tag_configure('linha', justify='right')
        #self.display.tag_configure()

        ################################ T E C L A D O ################################


        botaoUM = ttk.Button(MainFrame, text="1", command= lambda: self.digito('1'))
        botaoUM.grid(column=1, columnspan=1 ,row=3, sticky= (NSEW), padx=5, pady=5)

        botaoDOIS = ttk.Button(MainFrame, text="2", command= lambda: self.digito('2'))
        botaoDOIS.grid(column=2,columnspan=1 , row=3, sticky= (NSEW), padx=5, pady=5)
        
        botaoTRES = ttk.Button(MainFrame, text="3", command= lambda: self.digito('3'))
        botaoTRES.grid(column=3, columnspan=1 ,row=3, sticky= (NSEW), padx=5, pady=5)
        
        botaoQUATRO = ttk.Button(MainFrame, text="4", command= lambda: self.digito('4'))
        botaoQUATRO.grid(column=1, columnspan=1 ,row=4, sticky= (NSEW), padx=5, pady=5)

        botaoCINCO = ttk.Button(MainFrame, text="5", command= lambda: self.digito('5'))
        botaoCINCO.grid(column=2, columnspan=1 ,row=4, sticky= (NSEW), padx=5, pady=5)

        botaoSEIS = ttk.Button(MainFrame, text="6", command= lambda: self.digito('6'))
        botaoSEIS.grid(column=3, columnspan=1 ,row=4, sticky= (NSEW), padx=5, pady=5)
        
        botaoSETE = ttk.Button(MainFrame, text="7", command= lambda: self.digito('7'))
        botaoSETE.grid(column=1, columnspan=1 ,row=5, sticky= (NSEW), padx=5, pady=5)
        
        botaoOITO = ttk.Button(MainFrame, text="8", command= lambda: self.digito('8'))
        botaoOITO.grid(column=2, columnspan=1 ,row=5, sticky= (NSEW), padx=5, pady=5)
        
        botaoNOVE = ttk.Button(MainFrame, text="9", command= lambda: self.digito('9'))
        botaoNOVE.grid(column=3, columnspan=1 ,row=5, sticky= (NSEW), padx=5, pady=5)
        
        botaoZERO = ttk.Button(MainFrame, text="0", command= lambda: self.digito('0'))
        botaoZERO.grid(column=2, columnspan=1 ,row=6, sticky= (NSEW), padx=5, pady=5)

        botaoTROCA = ttk.Button(MainFrame, text="-/+", command= lambda: self.digito('^^'))
        botaoTROCA.grid(column=1, columnspan=1 ,row=6, sticky= (NSEW), padx=5, pady=5)

        botaoPONTO = ttk.Button(MainFrame, text=".", command= lambda: self.digito('.'))
        botaoPONTO.grid(column=3, columnspan=1 ,row=6, sticky= (NSEW), padx=5, pady=5)

        botaoCLEAR = ttk.Button(MainFrame, text=" Cc ", command= lambda: self.digito('+'))
        botaoCLEAR.grid(column=2, columnspan=1 ,row=2, sticky= (N, S), padx=5, pady=5)

        botaoLOG = ttk.Button(MainFrame, text=" LOG ", command= lambda: self.digito('LOG'))
        botaoLOG.grid(column=1, columnspan=1 ,row=2, sticky= (N, S), padx=5, pady=5)

        

    ############################### -- Operadores  -- ######################################

        botaoADD = ttk.Button(MainFrame, text=" + ", command= lambda: self.digito('+'))
        botaoADD.grid(column=3, columnspan=1 ,row=2, sticky= (N, S), padx=5, pady=5)
        
        botaoSUB = ttk.Button(MainFrame, text=" - ", command= lambda: self.digito('-'))
        botaoSUB.grid(column=4, columnspan=1 ,row=2, sticky= (N, S), padx=5, pady=5)
        
        botaoMULT = ttk.Button(MainFrame, text=" X ", command= lambda: self.digito('x'))
        botaoMULT.grid(column=4, columnspan=1 ,row=3, sticky= (N, S), padx=5, pady=5)
        
        botaoDIV = ttk.Button(MainFrame, text=" / ", command= lambda: self.digito('/'))
        botaoDIV.grid(column=4, columnspan=1 ,row=4, sticky= (N, S), padx=5, pady=5)

        botaoEQU = ttk.Button(MainFrame, text=" = ", command= self.calculo())
        botaoEQU.grid(column=4, columnspan=1 ,row=6, sticky= (N, S), padx=5, pady=5)

        botaoSair = ttk.Button(MainFrame, text="Sair",command= self.destroy)
        botaoSair.grid(column=4, columnspan=1 ,row=1, sticky= (N), padx=5, pady=5)

        botaoSQRT = ttk.Button(MainFrame, text=" SQRT ", command= lambda: self.digito('SQRT'))
        botaoSQRT.grid(column=4, columnspan=1 ,row=5, sticky= (N, S), padx=5, pady=5)



########################################## FUNCTION #############################################


    def digito(self,numero):                        # função para exibir numero do botão
        """funcao para inserir char no textbox"""   # no display Text
        self.display['state'] = 'normal' # habilita textbox para edição     
        
        #self.display.insert('2.0', numero, ('linha')) 
        conteudo =  '' #limpa conteudo
        conteudo = self.display.get('1.0', '2.end')     #conteudo recebe valor do textbox
        conteudo = conteudo + numero    #concatena o valor do conteudo com o valor do botão digitado
        self.display.delete('1.0','end')    #deleta todo conteudo do display
        self.display.insert('end', conteudo )      # insere conteudo no display
        self.display.tag_add('linha','1.0', '2.end') # adiciona tag 'linha' tem alinha na direita
        
        self.display['state'] = 'disable'    #desabilita o textfield novamente

    def calculo(self):
        tela = self.display.get('1.0', '1.end')
        self.display.delete('1.0', '2.end')
        prin = F.separaChar(tela)
        self.display.insert('1.0', prin)

        
        


    #def equa ():
    #    exibe = resultado()

if __name__ == "__main__":
    app = JanelaCalcula()
    app.mainloop()