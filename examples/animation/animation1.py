# -*- coding: utf-8 -*-

import pygame, sys
from pygame.locals import*
import os
import random
import random as Random

WIDTH, HEIGHT = 600, 300

#COLOR
#BLACK = (255,0,0)

#inicializa o pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT),0,32)
pygame.display.set_caption("Animation")

#preencha a tela
#screen.fill(BLACK)

#cria sprite de imagem
class ImageBlock(pygame.sprite.Sprite):
   max_speed = 120.0
   __speed = 30.0
   
   def __init__( self, imagefile, width=-1, height=-1 ):
      pygame.sprite.Sprite.__init__(self)
      #carrega a imagem para a sprite
      self.image = pygame.image.load(imagefile)
      #se definiu parametros de largura e altura da imagem...
      if((width>0)and(height>0)):
         #redimensiona a imagem de acordo com os parametros
         self.image = pygame.transform.smoothscale(self.image,(width,height))
      #captura a colorkey em um determinado pixel da imagem
      colorkey = self.image.get_at((0,0))
      #define colorkey para criacao de efeito
      self.image.set_colorkey(colorkey, RLEACCEL)
      #redefine dimensoes
      self.rect = self.image.get_rect()
      #redefine velocidades
      self.speed = [0.0,0.0]

   #atualiza a sprite verticalmente
   def update(self,dt):
      #movimenta a sprite
      self.rect = self.rect.move((self.speed[0]*dt,self.speed[1]*dt))

      #captura a tela
      screen = pygame.display.get_surface()
      #captura as dimensoes da tela
      screen_size = screen.get_size()


      #se atingiu o chao da tela...
      if(self.rect.bottom > screen_size[1]):
         #volta a sprite ao teto
         self.rect.bottom = 30
      #se atinge o teto...
      elif (self.rect.top < 0):
         #inverte o deslocamento (nao mostra na execucao)
         self.speed[1] = abs(self.speed[1])
      
   

   #metodo para mover a sprite horizontalmente
   def move( self, x, y ):
      #muda a posicao da sprite
      self.rect.move_ip(x,y)
      #captura as dimensoes da tela
      screen_size = pygame.display.get_surface().get_size()
      #se a movimentacao fez sair a sprite pela esquerda ...
      if(self.rect.left < 0):
         #desloca para o limite da esquerda
         self.rect.left = 0
      #se ultrapassar o limite da direita
      elif (self.rect.right > screen_size[0]):
         #desloca para o limite da direita
         self.rect.right = screen_size[0]


#metodo para criacao do fundo da tela
def create_background(image):
   screen = pygame.display.get_surface()
   screen_size = screen.get_size()
   tile=pygame.image.load(image).convert()
   back = pygame.Surface(screen.get_size()).convert()
   tile = pygame.transform.smoothscale(tile,screen_size)
   back.blit(tile,(0,0))
   return back

#carregando a lista de imagens
QUANT_IMAGES = 25 # o total de imagens

#imagesListMan = [] # uma lista para armazenar as images carregadas

#lendo as imagens...

#for i in range(QUANT_IMAGES): 
#	image = pygame.image.load('images'+os.sep+'explosion'+str(i+1)+".png").convert()
#	imagesListMan.append(image)

def main():
	global direction
	global posx
	global posy
	global QUANT_IMAGES
	
	#IMAGE_SIZE = 40
	
	#cria o clock
	clock = pygame.time.Clock()

	counter = 0

	block_list = pygame.sprite.LayeredUpdates()	
	
	#criar o loop Principal
	while True:
	
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
				
		if(counter==0):

			#escolhe uma entre as palavras que estão exibidas na tela

			vetor_categorias = [1,2,3,4,5,6,7,8,9,10]
		
			opcao1 = random.choice(vetor_categorias)*10
			opcao2 = random.choice(vetor_categorias)*10
			 

			background = create_background(os.path.join('images','beach.png'))
			screen.blit(background,(0,0))

			pygame.display.flip()		

		if(counter<25):
			block_list = pygame.sprite.LayeredUpdates()
			block = ImageBlock(os.path.join('images','explosion'+str(counter+1)+'.png'),30, 30)
			block.move(opcao1,opcao2)			
		block_list.add(block)

		#reimprime as sprites na tela
		block_list.draw(screen)  		

		#atualiza os contadores da imagem atual na tela	
		counter+=1
	
		#reinicia o contador
		if counter == QUANT_IMAGES:
			counter = 0
		
		#time
		clock.tick(16)
			
		#atualiza a tela
		pygame.display.flip()
			
#chama a funcao main  
if __name__ == "__main__":
	main()
 
