try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    from socket import *
    from pygame.locals import *
except ImportError as err:
    print ("couldn't load module. %s" % (err))
    sys.exit(2)

pygame.init()
display_width = 800
display_height = 800

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('gra')

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()

monety=1000
'''
def load_png(name):
    """ Load image and return image object"""
    fullname = "D:\Pygame\puste.bmp"
    print(os.getcwd())
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print ('Cannot load image:', fullname)
        raise SystemExit(message)
    return image, image.get_rect()
'''
class uniwersalne:
    def __init__(self, x, y, kier, zawartosc, img):
        self.x=x
        self.y=y
        self.kier=kier
        self.zawartosc=zawartosc
 
    def przenies(self, x, y, kier, zawartosc):
        kierunki=[[0,1],[1,0],[0,-1],[-1,0]]
        for i in tablica[x][y].zawartosc:
            if i not in tablica[x+kierunki[kier][0]][y+kierunki[kier][1]].zawartosc:
                tablica[x+kierunki[kier][0]][y+kierunki[kier][1]].zawartosc.append(i)
                tablica[x][y].zawartosc.remove(i)
        gameDisplay.blit(self.image, (x*16,y*16))
 
class puste(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('puste.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        
        self.x=x
        self.y=y
        self.kier=0
        self.zawartosc=[]
   
    def przenies(self, x, y, kier, zawartosc):
        gameDisplay.blit(self.image, (x*16,y*16))
 
class tasma(uniwersalne):
    def __init__(self, x, y, kier):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('conveyor'+str(kier)+'.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        
        self.x=x
        self.y=y
        self.kier=kier
        self.zawartosc=[]
        uniwersalne.__init__(self, x, y, kier, self.zawartosc, self.image)
        self.cena=10
 
class rafineria(uniwersalne):
    def __init__(self, x, y, kier):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('piec.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        
        self.x=x
        self.y=y
        self.kier=kier
        self.zawartosc=[]
        self.przepisy={"plytkiFe":["stal"],"Cu":["kabelCu"],"Fe":["plytkiFe"],"kamien":["Fe","Ni","Si"]}
        uniwersalne.__init__(self, x, y, kier, self.zawartosc, self.image)
        self.cena=1000
 
    def przenies(self, x, y, kier, zawartosc):
        for i in self.przepisy.keys():
            if i in zawartosc:
                zawartosc.extend(self.przepisy[i])
                zawartosc.remove(i)
        uniwersalne.__init__(self, x, y, kier, self.zawartosc, self.image)
 
class skladacz(uniwersalne):
    def __init__(self, x, y, kier, numPrzepisu):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('skladacz.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        
        self.x=x
        self.y=y
        self.kier=kier
        self.zawartosc=[]
        self.zawartosc2=[]
        self.numPrzepisu=numPrzepisu
        uniwersalne.__init__(self, x, y, kier, self.zawartosc, self.image)
        self.przepisy=["plytkaDrukowana","rebar"]
        self.skladniki=[["Si","kabelCu","plytkiFe"],["stal","kamien"]]
        self.cena=2000
 
    def przenies(self, x, y, kier, zawartosc):
        for i in self.skladniki[self.numPrzepisu]:
            if i in zawartosc:
                self.zawartosc2.append(zawartosc.pop(zawartosc.index(i)))
        wszystkoJest=True
        for i in self.skladniki[self.numPrzepisu]:
            if i not in self.zawartosc2:
                wszystkoJest=False
                break
        if wszystkoJest:
            for i in self.skladniki[self.numPrzepisu]:
                self.zawartosc2.remove(i)
            zawartosc.append(self.przepisy[self.numPrzepisu])
        uniwersalne.__init__(self, x, y, kier, self.zawartosc, self.image)
 
class maker:
    def __init__(self, x, y, kier, zawartosc):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('maker.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        
        self.x=x
        self.y=y
        self.kier=kier
        self.zawartosc2=zawartosc
        self.zawartosc=[]
        self.cena=500
   
    def przenies(self, x, y, kier, zawartosc):
        kierunki=[[0,1],[1,0],[0,-1],[-1,0]]
        for i in self.zawartosc2:
            if i not in tablica[x+kierunki[kier][0]][y+kierunki[kier][1]].zawartosc:
                tablica[x+kierunki[kier][0]][y+kierunki[kier][1]].zawartosc.append(i)
        gameDisplay.blit(self.image, (x*16,y*16))
 
class seller:
    def __init__(self, x, y, kier):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('seller.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        
        self.x=x
        self.y=y
        self.kier=kier
        self.zawartosc=[]
        self.ceny={"kamien":10,"Fe":20,"Cu":20,"Ni":20,"Si":20,"plytkiFe":100,"kabelCu":150,"stal":200,"plytkaDrukowana":500,"rebar":300} #dodaj ceny sprzedazy
        self.cena=500
 
    def przenies(self, x, y, kier, zawartosc):
        for i in self.zawartosc:
            monety+=ceny[i]
            self.zawartosc.remove(i)
        gameDisplay.blit(self.image, (x*16,y*16))

'''
class sorter(uniwersalne):
    def __init__(self, x, y, kier1, kier2, odsortowac):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sorter.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        
        self.x=x
        self.y=y
        self.kier1=kier1
        self.kier2=kier2
        self.odsortowac=odsortowac #lista!
        self.zawartosc=[]
        uniwersalne.__init__(self,x,y,kier2,self.zawartosc)
        self.cena=1000
       
    def przenies(self, x, y, kier, zawartosc):
        kierunki=[[0,1],[1,0],[0,-1],[-1,0]]
        for i in self.odsortowac:
            if i in zawartosc:
                if i not in tablica[x+kierunki[self.kier2][0]][y+kierunki[self.kier2][1]].zawartosc:
                    tablica[x+kierunki[self.kier2][0]][y+kierunki[self.kier2][1]].zawartosc.append(i)
                    tablica[x][y].zawartosc.remove(i)
        uniwersalne.przenies(self, x, y, kier2, zawartosc)
'''

def aktualizuj():
    for i in range(50):
        for j in range(50):
            tablica[i][j].przenies(tablica[i][j].x,tablica[i][j].y,tablica[i][j].kier,tablica[i][j].zawartosc)
 
def postaw(numEl, x, y, kier, zawartosc, monety):
    ceny=[0, 10, 1000, 2000, 500, 500]
    if(monety<ceny[numEl]):
        return "Not enough cashmoney!"
    monety-=ceny[numEl]
    if(numEl==0):
        tablica[x][y]=puste(x,y)
    elif(numEl==1):
        tablica[x][y]=tasma(x,y,kier)
    elif(numEl==2):
        tablica[x][y]=rafineria(x,y,kier)
    elif(numEl==3):
        tablica[x][y]=skladacz(x,y,kier,zawartosc) #numPrzepisu, nie zawartosc
    elif(numEl==4):
        tablica[x][y]=maker(x,y,kier,zawartosc)
    elif(numEl==5):
        tablica[x][y]=seller(x,y,kier)
    return "Placed!"

tablica=[[puste(j,i) for i in range(50)] for j in range(50)]

def savings():
    print("You have "+str(monety)+" cashmoney.")

crashed=False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONUP:
            numEl=input("What element ID? \n")
            x=input("What is the x? \n")
            y=input("What is the y? \n")
            kier=input("What is the direction? \n")
            zawartosc=input("What are the special settings (if any)? \n")
            print(postaw(int(numEl),int(x),int(y),int(kier),zawartosc,int(monety)))

    aktualizuj()
    pygame.display.update()
    clock.tick(60)
    

exit()
