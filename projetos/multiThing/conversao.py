from tkinter import *
from tkinter import ttk
from Python.projetos.multiThing.janela import principal

class conversao:
    conver = "classe"
    pai=principal.raiz
    conversor = Toplevel(pai)
    conversor.title("Conversor")

    frameConversor = ttk.Frame(conversor, padding= "3 3 12 12")
    frameConversor.grid(column=5,row=5,sticky=(N, E, W, S))
    conversor.columnconfigure(0, weight=5)
    conversor.rowconfigure(0, weight=5)

    BotaoConversor= ttk.Button()
    BotaoConversor(frameConversor, text= "Converter", command= exit )
    BotaoConversor.grid(column= 4, row=4, sticky= (SW))




















    raiz.mainloop()

    #base = 0
    #baseFim = 0
    #indice = 0
    #decimalConvertido = 0
    #carro = []
    #Katia = []  
    #dividido = []  
    #escolha =  {"1":2 , "2":3 , "3":8 , "4":10 ,"5":16} 
    #Letra  = {"A" : 10 , "B" :11 ,"C": 12,"D":13,"E": 14 ,"F":15}
    #letra = {10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}
    			         
    #print("Digite o Valor")
    #vaule = str(input("Digite o Valor: "))

    #print ("Escolha Entrada - Binario Ternaria Octa Decimal HexaDecimal)")
    #entrada1 = str(input("Escolha um Tipo de Dados\n1 ) Binario\n2 ) Ternaria\n3 ) Octadecimal \n4 ) Decimal \n5 ) HexaDecimal\n"))

    #if (entrada1 in escolha):
	#    base = escolha[entrada1]

    #if base != 10:
    
    #    carro = (list(vaule))    
    #    anarquia = len(carro)
    #    x=0
    
    #    while x < anarquia:

    #        if carro[x] in Letra:
    #            Katia.append(Letra [carro [x]])
        
    #        else:
    #            Katia.append(int(carro [x])) 
        
    #        x = x + 1
           
    #    hierarquia = anarquia - 1
    
    #    while hierarquia >= 0:
    #        decimalConvertido = Katia[hierarquia]*(base**expoente) + decimalConvertido	
        
    #        expoente = expoente + 1

    #        hierarquia = hierarquia - 1
    
    #    vaule = str(decimalConvertido)


    #print("Escolha a Saida- Binario Ternaria Octa Decimal HexaDecimal)")
    #saida1 = str(input("Escolha um Tipo de Dados para a Saida\n1 ) Binario\n2 ) Ternaria\n3 ) Octadecimal \n4 ) Decimal \n5 ) HexaDecimal\n"))
    #if saida1 in escolha:
	#    baseFim = escolha[saida1] 

    #if baseFim != 10:
    #    valor = int(vaule)
    #    x = 0

    #    while x != valor:
    #        resto = valor % baseFim 

    #        if resto < 10:                     
    #            dividido.append(str(resto))
    #            valor  =  valor // baseFim

    #        else:	
    #            dividido.append (letra.get(resto))                 
    #            valor = (valor//baseFim) 
    #    indice = indice + 1      

    #dividido.reverse()


    #if (base != baseFim):
    #    if (base == 10):         
    #        print (dividido)
    
    #    elif (baseFim == 10):
    #        print(vaule)
    
    #    else:
    #        print(dividido)            
    #else:
    #    print(vaule)