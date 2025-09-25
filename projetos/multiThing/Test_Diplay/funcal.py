def separaChar(ValorTela):
   sinais = ['+','-','*','/','^']
   oper = []
   num = []
   tela = str(ValorTela)
   d = 0
   print(tela)
   for i in tela.strip():      
      if i in sinais:
         num.append(i)
      else:
         oper.append(i)
         d = str(d) + str(i)
   return d
             