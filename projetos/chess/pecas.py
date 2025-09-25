class king():
    def __init__(self):
        self.walk = (1)
        self.score = 6 

class Queen():
    def __init__(self):
        self.walk = (30)
        self.score = 5 

class Bispo():
    def __init__(self):
        self.walk = (8)
        self.score = 4 

class House():
    def __init__(self):
        self.walk = (3, 2)
        self.score = 3 

class Tower():
    def __init__(self):
        self.walk = (8)
        self.score = 2 

class Solder():
    def __init__(self):
        self.walk = (1,2)
        self.score = 1 


def andar(posicao_atual,movimento, codigo, cor):

    dirK = ('N','NO','O','SO','S','SU','E','NE')
    dirQ = ('N','NO','O','SO','S','SU','E','NE')
    dirJ = ('NO','SO','SU','NE')
    dirH = ('N','O','S','E')
    dirT = ('N','O','S','E')
    dirP = ('N','NO','NE')

    coordenadas = {K: dirK, Q:dirQ, J:dirJ, H:dirH, T:dirT, P:dirP}
    
    cor 
    posicao_atual
    movimento



    return posicao_final