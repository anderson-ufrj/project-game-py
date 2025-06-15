# -*- coding: cp1252 -*-
import os,sys,string
import pygame
from pygame.locals import *
import random
import random as Random

class Block(pygame.sprite.Sprite):
   __speed = 10.0
   
   def __init__(self, color, width, height):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.Surface([width, height])
      self.image.fill((255,255,255))
      self.image.set_colorkey((255,255,255))
      pygame.draw.ellipse(self.image,color,[0,0,width,height])
      self.rect = self.image.get_rect()
   def update(self,dt):
      self.rect = self.rect.move((0,max(self.__speed*dt,1)))

      screen = pygame.display.get_surface()
      screen_size = screen.get_size()
      if (self.rect.top > screen_size[1]):
          self.kill()

class ImageBlock(pygame.sprite.Sprite):
   max_speed = 120.0
   __speed = 10.0
   
   def __init__( self, imagefile, width=-1, height=-1):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load(imagefile)
      if((width>0)and(height>0)):
         self.image = pygame.transform.smoothscale(self.image,(width,height))
      colorkey = self.image.get_at((0,0))
      self.image.set_colorkey(colorkey, RLEACCEL)
      self.rect = self.image.get_rect()
      self.speed = [0.0,0.0]

   def update(self,dt):
      self.rect = self.rect.move((self.speed[0]*dt,self.speed[1]*dt))

      screen = pygame.display.get_surface()
      screen_size = screen.get_size()

      #fazer a imagem voltar ao topo quando atinge o chão
      if(self.rect.bottom > screen_size[1]):
         self.rect.bottom = 30

      elif (self.rect.top < 0):
         self.speed[1] = abs(self.speed[1])
      
      if (self.rect.top > screen_size[1]):
          self.kill()
      if (self.rect.left > screen_size[0]):
          self.kill()          

   def move( self, x, y ):
      #print self.rect.left
      #if(self.rect.left>=0)and(self.rect.left<=500):
      #   self.rect.move_ip( x, y )
      #else:
      #   self.rect.move_ip( -x, y )      
      #self.update(1);
      self.rect.move_ip(x,y)
      screen_size = pygame.display.get_surface().get_size()
      if(self.rect.left < 0):
         self.rect.left = 0
      elif (self.rect.right > screen_size[0]):
         self.rect.right = screen_size[0]


#imagem com efeito diferente
class ImageBlock2(pygame.sprite.Sprite):
   max_speed = 120.0
   __speed = 10.0
   
   def __init__( self, imagefile, width=-1, height=-1):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load(imagefile)
      if((width>0)and(height>0)):
         #redimensiona a imagem conforme os parâmetros
         self.image = pygame.transform.smoothscale(self.image,(width,height))
      colorkey = self.image.get_at((0,0))
      self.image.set_colorkey(colorkey, RLEACCEL)
      self.rect = self.image.get_rect()
      self.speed = [0.0,0.0]

   def update(self,dt):
      self.rect = self.rect.move((self.speed[0]*dt,self.speed[1]*dt))

      screen = pygame.display.get_surface()
      screen_size = screen.get_size()

      #fazer a imagem subir e descer
      if(self.rect.bottom > screen_size[1]):
         #self.rect.bottom = 30
         self.speed[1] = -1 * abs(self.speed[1])
      elif (self.rect.top < 0):
         self.speed[1] = abs(self.speed[1])
      
      if (self.rect.top > screen_size[1]):
          self.kill()
      if (self.rect.left > screen_size[0]):
          self.kill()          

   def move( self, x, y ):
      self.rect.move_ip(x,y)
      screen_size = pygame.display.get_surface().get_size()
      #define os limites laterais
      if(self.rect.left < 0):
         self.rect.left = 0
      elif (self.rect.right > screen_size[0]):
         self.rect.right = screen_size[0]
         

class PlayerBlock(ImageBlock):
   def __init__(self, imageFile, name):
      ImageBlock.__init__(self,imageFile)
      self.name=name


class TextBlock(pygame.sprite.Sprite):
   def __init__(self, text, color, font_size):
      pygame.sprite.Sprite.__init__(self)
      self.color = color
      self.font = pygame.font.Font(None, font_size)
      self.text = text
      text = self.font.render(text,True,color)
      self.image = text
      self.rect = self.image.get_rect()

class TextBlock2(pygame.sprite.Sprite):
   def __init__(self, text, color, font_size, nome_categoria):
      pygame.sprite.Sprite.__init__(self)
      self.color = color
      self.font = pygame.font.Font(None, font_size)
      text = self.font.render(text,True,color)
      self.image = text
      self.rect = self.image.get_rect()
      self.nome_categoria = nome_categoria

class PointsBlock(TextBlock):
   def __init__(self, color, font_size, points):
      TextBlock.__init__(self, "Points: 0000", color, font_size)
      self._points = points

   @property
   def points(self):
      return self._points


   #atualiza o texto de pontos
   @points.setter
   def points(self, points):
      self._points = points
      if(points>999):
         self.image = self.font.render("Points: "+str(points),True, self.color)
      elif(points>99):
         self.image = self.font.render("Points: 0"+str(points),True, self.color)         
      elif(points>9):
         self.image = self.font.render("Points: 00"+str(points),True, self.color)
      else:
         self.image = self.font.render("Points: 000"+str(points),True, self.color)
      new_rect = self.image.get_rect()
      new_rect.x = self.rect.x
      new_rect.y = self.rect.y
      self.rect = new_rect

#lista de fases
vetor_fases = []

#método para ler o arquivo de configuração
def read_config():
   #importação do parser do arquivo
   import configparser
   #instancia um objeto da classe ConfigParser
   cfg = configparser.ConfigParser()
   #providencia a leitura do arquivo
   cfg.read('fases.ini')
   #captura o número de fases, que está em texto e converte para inteiro
   fases = cfg.getint('fases','num')
   #captura informação fase a fase
   for i in range(fases):
      #captura a quantidade de objetos da fase
      objs = cfg.getint('fase{0}'.format(i),'objetos')
      #captura a imagem de fundo e quantidade de acertos
      fase = {'fundo' : cfg.get('fase{0}'.format(i),'fundo'),
              'acertos' : cfg.getint('fase{0}'.format(i),'acertos'),
              'objetos' : {} }
      #verifica informações objeto a objeto
      for j in range(objs):
         #captura informação do objeto
         obj_info =  cfg.get('fase{0}'.format(i),'objeto{0}'.format(j)).split(";")
         #adiciona informações dos objetos à fase
         fase['objetos'][obj_info[0]] = [obj_info[1],obj_info[1]]
      #adiciona a fase à lista de fases
      vetor_fases.append(fase)


#cria a imagem de fundo do jogo
def create_background(image):
   screen = pygame.display.get_surface()
   screen_size = screen.get_size()
   tile=pygame.image.load(image).convert()
   back = pygame.Surface(screen.get_size()).convert()
   tile = pygame.transform.smoothscale(tile,screen_size)
   back.blit(tile,(0,0))
   return back

#inicia a tela do jogo
def init(size,fullscreen):
   pygame.init()
   flags = HWSURFACE|DOUBLEBUF
   screen = pygame.display.set_mode(size,flags)
   pygame.mouse.set_visible(1)
   pygame.display.set_caption('CURSO DE JOGOS')

def main(args):
   fullpath = os.path.abspath(args[0])
   dir = os.path.split(fullpath)[0]
   os.chdir(dir)
   fullscreen = '-fullscreen' in args
   screensize = (640,480)
   for arg in args:
      if arg[:5] == '-res=':
         screensize = [int(x) for x in string.split(arg[5:],',')]
   init(screensize,fullscreen)


   #surface - bitmap -> blit
   #sprite -    -> draw
   screen = pygame.display.get_surface()
   screen_size = screen.get_size()

   #inicializa a biblioteca de som
   pygame.mixer.init()
   #importa o arquivo de música de fundo
   pygame.mixer.music.load(os.path.join('snd','musica.wav'))
   #informa quantas vezes a música deve tocar seguidamente (-1 reproduz infinitamente)
   pygame.mixer.music.play(-1)
   #define o volume que a música deve reproduzir
   pygame.mixer.music.set_volume(0.5)

   #criando objetos de som
   som_acerto = pygame.mixer.Sound(os.path.join('snd','up.wav'))
   som_acerto.set_volume(1)

   som_erro = pygame.mixer.Sound(os.path.join('snd','explode.wav'))
   som_erro.set_volume(1)   

   textos = pygame.sprite.LayeredUpdates();

   interface_objs = pygame.sprite.LayeredUpdates()

   pontuacao = PointsBlock((0,0,255),26,0)
   pontuacao.rect.left = 500
   pontuacao.rect.top = 10
   pontuacao.layer = 30

   interface_objs.add(pontuacao)

   #insere um rodapé na tela

   pygame_text_bg = TextBlock('PYTHON', (0,0,0) , 18)
   pygame_text_bg.rect.centerx = screen_size[0]//2+2
   pygame_text_bg.rect.centery = screen_size[1]-10+2
   pygame_text_bg.layer = 1
   
   pygame_text = TextBlock('PYTHON', (255,255,255) , 18)
   pygame_text.rect.centerx = screen_size[0]//2
   pygame_text.rect.centery = screen_size[1]-10
   pygame_text.layer = 0

   interface_objs.add(pygame_text_bg)
   interface_objs.add(pygame_text)

   block_list = pygame.sprite.LayeredUpdates()
   block_list2 = pygame.sprite.LayeredUpdates()

   #inicia a contagem de tempo do jogo
   tempo_total = 0.0;  

   clock = pygame.time.Clock()
   dt = 16

   key = { K_LEFT: False, K_RIGHT: False }
   deslocamento = 10.0;
   #block2.speed[1] = block2.max_speed

   #assim iniciamos o loop principal do programa
   for i in range(len(vetor_fases)+1):
      #limpa a lista de imagens
      block_list.empty()
      #limpa a lista de textos
      textos.empty()
      #???
      fase_up = True
      #condição a ser feita após concluídas todas as fases
      if(len(vetor_fases) == i):
         block2.kill()
         # a imagem da palavra vira a imagem final com efeito diferente
         block2 = ImageBlock2(os.path.join('images','coelho.png'),300,300)
         block2.rect.centerx = screen_size[0]//2
         block2.speed[1] = block2.max_speed
         block_list2.add(block2)
         #exibe The End no meio da tela
         the_end =  TextBlock("The End", (0,0,255),56)
         the_end.rect.centerx = screen_size[0]//2
         the_end.rect.centery = screen_size[1]//2
         the_end.layer=10
         interface_objs.add(the_end)

         #Define o texto do final do jogo
         tempo_gasto = TextBlock("Você demorou %d segundos para completar todas as fases."%(int(round(tempo_total//1000.0))),(0,0,255),26)
         #Posiciona o texto final no meio da tela horizontalmente
         tempo_gasto.rect.centerx = screen_size[0]//2
         #Posiciona o texto final no meio da tela verticalmente
         tempo_gasto.rect.centery = screen_size[1]//2+50
         interface_objs.add(tempo_gasto)
      #condição feita em todas as fases
      else:
         #cria a imagem de fundo da fase
         background = create_background(os.path.join('images',vetor_fases[i]['fundo']))
         #zera os pontos da fase
         pontuacao.points = 0
         #carrega as palavras correspondentes da fase
         vetor_categorias = list(vetor_fases[i]['objetos'].keys())
         #embaralha a lista das palavras
         random.shuffle(vetor_categorias)

         #carrega as sprites de texto iniciais (as primeiras palavras sorteadas)
         for x in range(4):
            #cria uma sprite de texto
            blk = TextBlock(vetor_categorias[x],(255,255,255),32)
            #posiciona a sprite horizontalmente
            blk.rect.left = 10 + 150*x
            #posiciona a sprite verticalmente
            blk.rect.bottom = screen_size[1] - 30
            #adiciona a palavra da vez à lista de palavras a serem exibidas
            textos.add(blk)

         #escolhe uma entre as 4 palavras
         opcao = random.choice(vetor_categorias[:4])

         #cria a sprite de imagem da palavra sorteada
         block2 = PlayerBlock(os.path.join('images',vetor_fases[i]['objetos'][opcao][0]),opcao)
         block2.rect.centerx = screen_size[0]//2
         block2.speed[1] = block2.max_speed
         block_list2.add(block2)

      #enquanto está na mesma fase
      while fase_up:
         #determina o intervalo de tempo
         ellapsed = clock.tick(1000//dt)
         #incrementa ao tempo total do jogo
         tempo_total += ellapsed
         #finaliza o jogo se a janela for fechada
         for event in pygame.event.get([QUIT]):
            #finaliza o pygame
            pygame.quit()
            #finaliza o sistema
            sys.exit(0)
         #verifica se uma tecla foi pressionada
         for event in pygame.event.get([KEYDOWN,KEYUP]):
            #???
            valor = (event.type == KEYDOWN)
            #se a tecla pressionada foi a ESC
            if (event.key == K_ESCAPE):
               #finaliza o pygame
               pygame.quit()
               #finaliza o sistema
               sys.exit(0)
            #se foi outra tecla
            elif (event.key in key.keys()):
               #fornece TRUE na posição correspondente da tecla ao vetor
               key[event.key]=valor
         #se a tecla pressionada foi a seta para esquerda
         if key[ K_LEFT ]:
            #diminui o deslocamento horizontal (move a sprite para a esquerda)
            block_list2.get_sprite(0).move( -deslocamento,   0 )
         #se a tecla pressionada foi a seta para direita
         if key[ K_RIGHT ]:
            #aumenta o deslocamento horizontal (move a sprite para a direita)
            block2.move(  deslocamento,   0 )
         #atualiza as imagens
         block_list2.update(ellapsed/1000.0)
         #atualiza os objetos
         interface_objs.update(ellapsed/1000.0)
         
         #cria lista de colisões
         collided_list = pygame.sprite.spritecollide(block2, textos, False)
         #se houve colisão ...
         if(len(collided_list)>0):
            #destrói a imagem colidida
            block2.kill()
            #se a imagem colidir com a palavra correta ...
            if(collided_list[0].text==block2.name):
               #reproduz o som de acerto
               som_acerto.play()
               #incrementa os pontos
               pontuacao.points += 1
               #captura a coordenada x da palavra colidida
               old_x = collided_list[0].rect.x
               #remove a palavra da lista das palavras sorteadas
               vetor_categorias.remove(collided_list[0].text)
               #cria a sprite de texto com a próxima palavra da lista das palavras sorteadas
               blk = TextBlock(vetor_categorias[3],(255,255,255),32)
               #posiciona a palavra nova no seu respectivo lugar horizontal
               blk.rect.left = old_x
               #posiciona a palavra nova no seu respectivo lugar vertical
               blk.rect.bottom = screen_size[1] - 30
               #adiciono a palavra nova na lista de palavras que aparecem na tela
               textos.add(blk)
               #destrói o objeto colidido
               collided_list[0].kill()
            #se colidiu com a palavra errada...
            else:
               #reproduz o som de erro
               som_erro.play()
            #se alcançou a meta de pontos da fase muda de fase   
            if(pontuacao.points >= vetor_fases[i]['acertos']):
               # modifica a flag que muda de fase
               fase_up = False
            else:
               #escolhe uma entre as palavras que estão exibidas na tela
               opcao = random.choice(vetor_categorias[:4])
               #cria a sprite de imagem correspondente ao texto
               block2 = PlayerBlock(os.path.join('images',vetor_fases[i]['objetos'][opcao][0]),opcao)
               #posiciona a sprite de imagem no meio da tela horizontalmente
               block2.rect.centerx = screen_size[0]//2
               #define a velocidade de descida da sprite de imagem
               block2.speed[1] = block2.max_speed
               #adiciona a imagem nova na lista de imagens
               block_list2.add(block2)                  

         #imprime o background na tela
         screen.blit(background,(0,0))
         #insere as sprites móveis
         block_list2.draw(screen)
         #insere as sprites fixas
         interface_objs.draw(screen)
         #insere os textos
         textos.draw(screen)
         #ao fim do desenho temos que trocar o front buffer e o back buffer
         pygame.display.flip()

#módulo principal
if __name__ == '__main__':
   #chama o método de leitura do arquivo de configuração
   read_config()
   #inicia o jogo
   main(sys.argv)
