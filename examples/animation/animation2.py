# -*- coding: utf-8 -*-
# fazendo o personagem atravessar a tela andando uma única vez...

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

#carregando a lista de imagens
QUANT_IMAGES = 6 # o total de imagens

imagesListMan = [] # uma lista para armazenar as images carregadas

#lendo as imagens...

for i in range(QUANT_IMAGES): 
	image = pygame.image.load('images'+os.sep+'rightman'+str(i+1)+".gif").convert()
	imagesListMan.append(image)
	

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
	
	counter = 0
	#criar o loop Principal
	while True:
	
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
				
	
		screen.fill(WHITE)
		
		screen.blit(imagesListMan[counter],(posx, posy))			
		
		#atualiza o contador da imagem atual na tela	
		counter+=1
	
		#move a imagem 
		if posx < WIDTH - IMAGE_SIZE:
			posx+=10
		
		#reinicia o contador
		if counter == QUANT_IMAGES:
			counter = 0
		
		#time
		clock.tick(4)
			
		#atualiza a tela
		pygame.display.flip()
			

#chama a funcao main  
if __name__ == "__main__":
	main()
 
