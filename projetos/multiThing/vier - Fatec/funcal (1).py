class caluladora:
   def __init__ (self, operacao):
      self.indice = 0
      self.display = []
      self.sinal = []
      if operacao == 0:
         operacao = 0
   
   def resultado(self):
      #x = self.indice
      #if '(' and ')' in self.guarda[]:

      for x in self.guarda: #buscar prioridade dentro da memoria de operação "guarda"
         
         if x == '^': # busca pelo operador de potencia 
            s = self.guarda

         if x == '*': # busca pelo operador de multiplicação
            s = self.guarda
         
         if x == '/': # busca pelo operador de divisão
            s = self.guarda
         
         if x == '+': # busca pelo operador de adição
            s = self.guarda
         
         if x == '-': # busca pelo operador de subtração
            s = self.guarda
         
         if x == '^': # busca pelo operador de parente (
            s = self.guarda
         
         if x == '^': # busca pelo operador de potencia parente )
            s = self.guarda


         if x in prefente:
            c = self.display.index(x)
            result = self.display[c-1] * self.display[c+1]

      return result


   def operador(self, operacao, opera):        #funcao para quando o usuario digitar o sinal da operação
      c = int                                #essa função tem que armazenar em um arrey o valor da tela
      self.guarda = []
      if tela == ' ':
         self.guarda.append = tela
      self.display [indice] = operacao       #e armazenar o sinal digitado. O Problema aqui é armazenar os numeros
      self.sinal = [c] = opera               #e conectar ao seu operador e ao mesmo tempo respeitar a ordem de operações
#inicialmente pensei em organizar o array de sinais, o problema disso é que vou perder a de quais numeros eles foram usados
#a solução que pensei é deixar no lugar e procurar a prioridade apenas na hora do resultado e deixar o sinal ligado a operação
      indice = indice + 1       # array da operacoes
                      
      if self.sinal[c] < self.sinal[c + 1]:           #  9) ()
         troca = self.sinal[c + 1]
         self.sinal[c + 1] = self.sinal[c]            #  5) ^ 
         self.sinal [c] = troca                       #  4) *
#                                                     #  3) /
#                                                     #  2) +
#                                                     #  1) -

   
