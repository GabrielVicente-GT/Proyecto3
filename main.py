#Gabriel Alejandro Vicente lorenzo
#Proyecto 3 20498


from cast import *
#Se inicia pygame
pygame.init()

#Musica de fondo con volumen bajo
pygame.mixer.music.load('./MP3/Music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

#Se esconde el mouse para que sea una experiencia mas plena
pygame.mouse.set_visible(0)

#La pantalla tiene un ancho y alto determinado
Proyecto_3_20498 = pygame.display.set_mode((600,500))

#FPS a renderizad con ayuda de clock
renderizado_fps = 25

#Se renderiza el Raycaster
PantallaUnica = Raycaster(Proyecto_3_20498)
#Se carga el mapa como arreglo
PantallaUnica.load_map('./MAPA/map.txt')

#Mientras la pantalla sea verdadera
while PantallaUnica.programa_principal:

    #Fondo del piso
    Proyecto_3_20498.fill((255,255,255), (0,PantallaUnica.height/2,PantallaUnica.width,PantallaUnica.height/2))
    #Fondo del cielo
    Proyecto_3_20498.fill((93, 173, 226), (0,0,PantallaUnica.width,PantallaUnica.height/2))
    
    #Se renderiza el mundo 3d
    PantallaUnica.render()
    
    #Encima del mundo 3d se renderiza un cuadro negro
    Proyecto_3_20498.fill((0,0,0),(0,0,250,120))
    #Se renderiza minimapa
    PantallaUnica.render_minimap()
    
    #Se carga texto que muetras el objetivo del nuvel y los FPS
    Proyecto_3_20498.blit(pygame.font.SysFont('Comic Sans',15).render('Frames/s: ' + str(pygame.time.Clock().tick(renderizado_fps)),30,(255,255,255),(0,0,0)),(120,0))
    Proyecto_3_20498.blit(pygame.font.SysFont('Comic Sans',20).render('Encuentra el',0,(255,255,255),(0,0,0)),(120,25))
    Proyecto_3_20498.blit(pygame.font.SysFont('Comic Sans',20).render('   espejo   ',0,(255,255,255),(0,0,0)),(120,55))
    Proyecto_3_20498.blit(pygame.font.SysFont('Comic Sans',20).render(' correcto!!!',0,(255,255,255),(0,0,0)),(120,88))

    #Si se finaliza el juego
    if PantallaUnica.final:
        #Pintar la pantalla de naranja y mostrar mensaje
        Proyecto_3_20498.fill((243, 156, 18 ))
        Proyecto_3_20498.blit(pygame.font.SysFont('Comic Sans',50).render('GANASTEEEEE!!!!',0,(255,255,255),(243, 156, 18)),(110,200))

    #Actualizar toda la ventana
    pygame.display.flip()

    #Escuchar los eventos de la ventana
    for event in pygame.event.get():
        
        #Si la patnalla no es el final del juego
        if PantallaUnica.final == False:
            #Si el movimiento del mouse en x es positivo o negativo
            #Incrementar o decrementar el angulo
            if event.type == pygame.MOUSEMOTION:
                Movimiento_mouse = pygame.mouse.get_rel()
                mouse_x = Movimiento_mouse[0]
                if mouse_x > 0:
                    PantallaUnica.player["a"] +=pi/10
                elif mouse_x < 0:
                    PantallaUnica.player["a"] -=pi/10

            #Si se presiona una tecla
            elif event.type == pygame.KEYDOWN:

                #Si la tecla es g o h, incrementar o decrementar el angulo
                if event.key == pygame.K_g:
                    PantallaUnica.player["a"] -=pi/10
                elif event.key == pygame.K_h:
                    PantallaUnica.player["a"] +=pi/10

                #Si las flechas se presionan incrementar x o y al igual que su mini dependiendo
                #De la presionada
                elif event.key == pygame.K_UP:
                    PantallaUnica.player["y"] -=10
                    PantallaUnica.player["y_mini"] -=2
                elif event.key == pygame.K_DOWN:
                    PantallaUnica.player["y"] +=10
                    PantallaUnica.player["y_mini"] +=2
                elif event.key == pygame.K_RIGHT:
                    PantallaUnica.player["x"] +=10
                    PantallaUnica.player["x_mini"] +=2
                elif event.key == pygame.K_LEFT:
                    PantallaUnica.player["x"] -=10
                    PantallaUnica.player["x_mini"] -=2

                #Si las teclas WASD se presionan incrementar x o y al igual que su mini dependiendo
                #De la presionada
                elif event.key == pygame.K_w:
                    PantallaUnica.player["y"] -=10
                    PantallaUnica.player["y_mini"] -=2
                elif event.key == pygame.K_s:
                    PantallaUnica.player["y"] +=10
                    PantallaUnica.player["y_mini"] +=2
                elif event.key == pygame.K_d:
                    PantallaUnica.player["x"] +=10
                    PantallaUnica.player["x_mini"] +=2
                elif event.key == pygame.K_a:
                    PantallaUnica.player["x"] -=10
                    PantallaUnica.player["x_mini"] -=2

                #Si la tecla ESC se presiona se termina el programa_principal
                elif event.key == pygame.K_ESCAPE:
                    PantallaUnica.programa_principal = False

                pygame.mixer.Sound('./MP3/Efecto.mp3').play()

            #Si se presiona la X se presiona se termina el programa_principal
            elif event.type == pygame.QUIT:
                r,programa_principal = False



        # Si se finaliza el juego
        if PantallaUnica.final == True:
            #Si se presiona la X se presiona se termina el programa_principal
            if event.type == pygame.QUIT:
                PantallaUnica.programa_principal = False

            #Si se presiona una tecla
            if event.type == pygame.KEYDOWN:
                #Si la tecla ESC se presiona se termina el programa_principal
                if event.key == pygame.K_ESCAPE:
                    PantallaUnica.programa_principal = False
