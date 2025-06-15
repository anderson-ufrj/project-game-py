# -*- coding: latin-1 -*-

import pygame, sys, os 
from pygame.locals import *

bola = 'bola.png' 
campo = 'campo.jpg'
images_dir = os.path.join( "", "imagens" )

pygame.init()

screen=pygame.display.set_mode((620,390),0,0)

background=pygame.image.load(os.path.join( images_dir, campo )).convert()

mouse_c=pygame.image.load(os.path.join( images_dir, bola )).convert_alpha()

pygame.mouse.set_visible( 0 )

while True: 
   for event in pygame.event.get(): 
      if event.type == QUIT: 
         pygame.quit() 
         sys.exit() 
      screen.blit(background, (0,0))

      #captura a posição do mouse
      x,y = pygame.mouse.get_pos()

      #captura eventos de clique do mouse
      botao = pygame.mouse.get_pressed()

      #se o botão esquerdo do mouse foi clicado

      if botao[0]:
         print("Botao esquerdo")

      #se o botão direito do mouse foi clicado

      elif botao[2]:
         print("Botao direito")
      
      x -= mouse_c.get_width()//2
      y -= mouse_c.get_height()//2 
      screen.blit(mouse_c, (x,y))
      pygame.display.update() 
