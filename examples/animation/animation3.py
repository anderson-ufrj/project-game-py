# -*- coding: utf-8 -*-

# Andando para direita e para a esquerda controlado pela teclas...
 
import pygame, sys
from pygame.locals import*
 
import os
 
WIDTH, HEIGHT = 600, 300
#COLOR
WHITE = (255,255,255)
 
#inicializa o pygame
pygame.init()
 
screen = pygame.display.set_mode((WIDTH, HEIGHT),0,32)
pygame.display.set_caption("Animation")
 
#preencha a tela
screen.fill(WHITE)
 
#carregando as listas de imagens
QUANT_IMAGES = 6 # o total de imagens
 
#personagem andando para direita
listManRight = []
 
#personagem andando para esquerda
listManLeft = []
 
#lendo as imagens dos personagens para direita..
for i in range(QUANT_IMAGES):
 image = pygame.image.load('images'+os.sep+'rightman'+str(i+1)+".gif").convert()
 listManRight.append(image)
  
#lendo as imagens dos personagens andando para esquerda...
for i in range(QUANT_IMAGES):
 image = pygame.image.load('images'+os.sep+'leftman'+str(i+1)+".gif").convert()
 listManLeft.append(image)
 
  
#definindo a direcao inicial do movimento
direction  = "r"
 
posx = 10
posy = 100
 
def main():
 global direction
 global posx
 global posy
 global QUANT_IMAGES
  
 IMAGE_SIZE = 40
  
 #cria o clock
 clock = pygame.time.Clock()
 
 
 counter = 0 # contar a imagem atual
 aux = 0
  
 #criar o loop Principal
 while True:
  
  for event in pygame.event.get():
   if event.type == QUIT:
    exit()
     
  #verifica as teclas pressionadas
  pressedKeys = pygame.key.get_pressed()
  
  #movimenta na posição da tecla pressionada
  if pressedKeys[K_RIGHT]:
   direction = "r"
  if pressedKeys[K_LEFT]:
   direction = "l"
   
  screen.fill(WHITE)
   
  #atualiza o contadar da imagen atual na tela
   
  #move a imagem
  if direction == "r":
   screen.blit(listManRight[counter],(posx, posy))  
   if posx < WIDTH-IMAGE_SIZE:
    posx+= 5
   
  if direction == "l":
   screen.blit(listManLeft[counter],(posx, posy))  
   if posx >0:
    posx -= 5
    
   
  #reinicia o contador
  counter+=1
 
  if counter > QUANT_IMAGES-1:
   counter = 0
   
  #time
  clock.tick(10)
    
  #atualiza a tela
  pygame.display.flip()
    
 
#chama a funcao main 
if __name__ == "__main__":
 main()
