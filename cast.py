#Clase cast vista en el curso
from math import *
import pygame

#Paredes con imagen
PAREDES = {
    "4" : pygame.image.load('./IMAGENES/Pared_espejo.png'),
    "3" : pygame.image.load('./IMAGENES/Pared_unica.png'),
    "2" : pygame.image.load('./IMAGENES/Pared_espejo.png'),
    "1" : pygame.image.load('./IMAGENES/Pared_unica.png'),
}

#Clase del Raycaster
class Raycaster(object):
    def __init__(self,pantalla_principal):
        #Obtener el ancho y largo inicial
        _,_,self.width, self.height     = pantalla_principal.get_rect()
        self.pantalla_principal         = pantalla_principal
        self.programa_principal         = True
        
        #Definir block_size y el block_size del mininapa
        self.block_size     = 50
        self.block_size_2   = int(self.block_size/5)
        
        #Saber si esta el final del programa
        self.final          = False
        
        #Mapa con 1,2,3,4
        self.map            = []
        
        #Caracteristicas del jugador
        self.player =   {
            "x_mini":   int(self.block_size_2 + self.block_size_2/2),
            "y_mini":   int(self.block_size_2 + self.block_size_2/2),
            "x":        int(self.block_size + self.block_size/2),
            "y":        int(self.block_size + self.block_size/2),
            "fov":      int(pi/3),
            "a":        int(pi/3)
        }

    #Cambiar el color de la pantalla en un punto pixeles
    def point(self,x,y,c = (255,255,255)):
        self.pantalla_principal.set_at((x,y),c)

    #Block que permite construir mundo 3d
    def block(self,x,y,pared):
        for i in range(x,x+self.block_size):
            for j in range(y,y+self.block_size):
                tx = int((i-x)*128/self.block_size)
                ty = int((j-y)*128/self.block_size)
                try:
                    c = pared.get_at((tx,ty))
                except:
                    c = (255,255,255)

                self.point(i,j,c)

    #Block que permite construir mapa
    def block_mini(self,x,y,pared):
        for i in range(x,x+self.block_size_2):
            for j in range(y,y+self.block_size_2):

                tx = int((i-x)*128/self.block_size_2)
                ty = int((j-y)*128/self.block_size_2)

                c = pared.get_at((tx,ty))
                self.point(i,j,c)

    #Se carga el mapa en self.map para saber donde colocar bloques
    def load_map(self,filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    #Se dibuja el mapa con bloques
    def draw_map(self):
        for x in range(0,100,self.block_size_2):
            for y in range(0,100,self.block_size_2):
                i = int(x/self.block_size_2)
                j = int(y/self.block_size_2)
                if self.map[j][i] != ' ':
                    self.block_mini(x,y, PAREDES[self.map[j][i]])

    #Se dibuja el player 
    def draw_player(self):
        self.point(self.player["x_mini"], self.player["y_mini"], (255,0,0))

    #Rayo que permite saber que esta viendo el jugador
    def cast_ray(self, a):
        d = 0
        ox = self.player["x"]
        oy = self.player["y"]

        while True:
            x = int(ox + d*cos(a))
            y = int(oy + d*sin(a))

            i = int(x/self.block_size)
            j = int(y/self.block_size)

            if self.map[j][i] != ' ':
                hitx = x - i*self.block_size
                hity = y - j*self.block_size

                if 1 < hitx < self.block_size-1:
                    maxhit =   hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128/self.block_size)
                return d, self.map[j][i], tx

            d += 1

    #Representacion del rayo en minimapa
    def cast_ray_mini(self, a):
        d = 0
        ox = self.player["x_mini"]
        oy = self.player["y_mini"]

        while True:
            x = int(ox + d*cos(a))
            y = int(oy + d*sin(a))

            i = int(x/self.block_size_2)
            j = int(y/self.block_size_2)

            if self.map[j][i] != ' ':
                return d, self.map[j][i]

            self.point(x,y)
            d += 1

    #Dibuja horizontalmente paredes dependiendo del raycaster
    def draw_stake(self, x,h,c,tx):
        start_y = int(self.height/2 - h/2)
        end_y   = int(self.height/2 + h/2)
        height = end_y - start_y

        for y in range(start_y, end_y):
            ty = int((y-start_y)*128/height)
            try:
                color = PAREDES[c].get_at((tx,ty))
            except:
                color = (255,255,255)
            self.point(x,y,color)

    #Render del mundo 3d que permite mostrar los bloques dependiendo de la posicion y el raycaster
    def render(self):
        #Dibujo 3d
        for i in range(0, int(self.width)):
            a           = self.player["a"] - self.player["fov"]/2+  self.player["fov"]*i/(self.width)
            d, c, tx    = self.cast_ray(a)
            try:
                x = i
                h = (self.height/(d*cos(a-self.player["a"])))*self.block_size
                self.draw_stake(x,h,c,tx)
            except:
                if 450 < self.player["x"] < 480 and 380 < self.player["y"] < 470:
                    pygame.mixer.Sound('./MP3/Ganar.mp3').play()
                    self.player["x_mini"]   = int(self.block_size_2 + self.block_size_2/2)
                    self.player["y_mini"]   = int(self.block_size_2 + self.block_size_2/2)
                    self.player["x"]        = int(self.block_size + self.block_size/2)
                    self.player["y"]        = int(self.block_size + self.block_size/2)
                    self.final = True
                else:
                    pygame.mixer.Sound('./MP3/Muerte.mp3').play()
                    self.player["y_mini"]   = int(self.block_size_2 + self.block_size_2/2)
                    self.player["x_mini"]   = int(self.block_size_2 + self.block_size_2/2)
                    self.player["y"]        = int(self.block_size + self.block_size/2)
                    self.player["x"]        = int(self.block_size + self.block_size/2)

    #Renderizar minimapa en esquina
    def render_minimap(self):
        self.draw_map()

        #MiniMapa
        density = 100
        for i in range(0,density):
            a = self.player["a"] - self.player["fov"]/2+  self.player["fov"]*i/density
            d, c = self.cast_ray_mini(a)
