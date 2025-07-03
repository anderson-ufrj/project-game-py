import pgzrun, pygame
import pgzhelper 
from random import randint, choice

# -- Resolution
WIDTH= 600
HEIGHT=800
# HEIGHT= 2000

game_state=0
game_won= False

title_background = Actor("title_screen.png")

def draw_title():
    screen.clear()
    title_background.draw()
    screen.draw.text("ICARUS", (120,350), color=(255,255,255), fontsize=150)
    screen.draw.text("Press ENTER to start", (170,600), color=(255,255,255), fontsize=40)

def update_title():
    global game_state
    start=pygame.key.get_pressed()
    
    if start[pygame.K_KP_ENTER]:
        game_state+=1
        
# -- CLASSES
class Player(Actor):
    # ...
    def __init__(self, image):
        super().__init__(image)
        self.image_left="placeangel_left"
        self.image_right="placeangel"
        self.fire="angel_fire"
        self.won="angel_won"
        self.speed= 4
        self.jumpspeed= 13
        self.verticalsp = 0 # vertical speed
        self.gravity= 1
        self.falling=False

        self.life=3

        self.on_fire=False
        self.wing_counter= 0

        #variation jump
        self.min_jumpspeed = 3
        self.prev_key = pygame.key.get_pressed()
        self.onground= True

    def move(self, x, y):
        self._rect.move_ip(x,y)

    def collectwings(self,feather):
        wings_to_remove=[]

        for feather in wings or wings2 or wings3 or wings4 or wings5:
            if self.colliderect(feather):
                wings_to_remove.append(feather)
                self.wing_counter+=1
                if self.wing_counter==2:
                    self.jumpspeed+=1
                
                if self.wing_counter==6:
                    self.jumpspeed+=2

                if self.wing_counter==10:
                    self.jumpspeed+=20
                
            for feather in wings_to_remove:
                if feather in wings:
                    wings.remove(feather)
                elif feather in wings2:
                    wings2.remove(feather)
                elif feather in wings3:
                    wings3.remove(feather)
                elif feather in wings4:
                    wings4.remove(feather)
                elif feather in wings5:
                    wings5.remove(feather)

        
    def update(self):
        #horizontal and vertical speeds
        horizontalsp = 0 
        verticalsp = 0 

        # check keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            horizontalsp = -self.speed
            self.image=self.image_left
                
        elif key[pygame.K_RIGHT]:
            horizontalsp = self.speed
            self.image=self.image_right

        if key[pygame.K_UP] and self.onground and self.falling==False:
            self.verticalsp = -self.jumpspeed
                

        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.verticalsp < -self.min_jumpspeed:
                self.verticalsp = -self.min_jumpspeed

        self.prev_key = key
            
        # gravity
        if self.verticalsp < 10 and not self.onground: # 9.8 rounded up
            self.verticalsp += self.gravity
            
        # movement
        self.move(horizontalsp,self.verticalsp)
        
    def draw(self):
        global game_won
        if self.on_fire:
            self.image=self.fire
            if game_won:
                self.image=self.won
        super().draw()
    
class Platform(Actor):
    def __init__(self, image, anchor=["left", "top"]):
        super().__init__(image, anchor=anchor)
        speedchoice=[-1,-2,2,1]
        self.speed = choice(speedchoice)
        self.moving = False
        
    def position(self,x,y):
        self.y
        self.x
        
    def collide(self,player):
        if player.colliderect(self):
            return True
        
        return False
        
    def move(self):
        self.moving= True
        if self.moving == True:  
            self._rect.move_ip(self.speed,0)
            if self.speed > 0 and self._rect.left > 500:
                self._rect.right = 0
            if self.speed < 0 and self._rect.right < 0:
                self._rect.left = 500
    
    # def disappear(self,player):
    #     time=0
    #     cloud_to_remove=[]
    #     while player.colliderect(self):
    #         time+=1
        
    #     if time==3:
    #         cloud_to_remove.append(self)
    #         for cloud in cloud_to_remove:
    #             bricks3.remove(cloud)

    def update(self):
        pass

class Wing(Actor):
    def __init__(self, image):
        super().__init__(image)

    def follow(self,cloud):
        self.pos=(cloud.x+20,cloud.y-20)

    def update(self):
        pass

class Hostile(Actor):
    def __init__(self, image,cloud):
        super().__init__(image)
        self.pos=(cloud.x+50,cloud.y+55)
        self.strike= False
    
    def update(self,player,cloud):
        strike=True
        storm=[2,3,4,5]
        storm_speed=choice(storm)
        global game_state

        while strike == True:
            self.y = self.y + storm_speed
            if self.pos[1]+10 >= HEIGHT:
                self.pos=(cloud.x+50,cloud.y+55)
            strike=False

        # -- check collision avec player
        if self.colliderect(player) and game_state<3:
            player.pos= (500, HEIGHT-70)
        elif self.colliderect(player) and game_state<6:
            player.pos= (100, HEIGHT-70)

background1= Actor("placesky.png")
background2= Actor("sky2")
background3= Actor("sky3")
background4= Actor("sky4")
background5= Actor("sky5")
background6= Actor("sky6")
background7= Actor("sky7")
background8= Actor("sky8")
background9= Actor("gameover_sky")

# -- sprites du jeu
player=Player("placeangel.png")
player.pos=[100,HEIGHT- 70]

# --- feathers GAME 1
wings=[]
feather1= Wing("smallfeather.png")
feather1.pos=[50, HEIGHT-520]
wings.append(feather1)

# --- Platforms
bricks=[]
for x in range(0, WIDTH,100):
    for y in range(HEIGHT-30,(HEIGHT-30)-30*2,-30):
        brick=Platform("pillar2.png")
        brick.pos=[x,y]
        bricks.append(brick)

# --- Platforms GAME 1  
platform_100= Platform("pillar2.png")
platform_100.pos=[0, HEIGHT-180]
bricks.append(platform_100)

platform_102= Platform("pillar2.png")
platform_102.pos=[100, HEIGHT-150]
bricks.append(platform_102)

platform_250= Platform("pillar2.png")
platform_250.pos=[WIDTH-300, HEIGHT-250]
bricks.append(platform_250)

platform_252= Platform("pillar2.png")
platform_252.pos=[WIDTH-200, HEIGHT-250]
bricks.append(platform_252)

platform_400= Platform("small_cloud.png")
platform_400.pos=[100, HEIGHT-400]
bricks.append(platform_400)

platform_500= Platform("pillar2.png")
platform_500.pos=[200, HEIGHT-600]
bricks.append(platform_500)

platform_502= Platform("pillar2.png")
platform_502.pos=[0, HEIGHT-500]
bricks.append(platform_502)

platform_600= Platform("pillar2.png")
platform_600.pos=[WIDTH-200, HEIGHT-600]
bricks.append(platform_600)

platform_750= Platform("small_cloud.png")
platform_750.pos=[250, HEIGHT-740]
bricks.append(platform_750)


# --- Platforms Game 2
bricks2=[]
platform_1= Platform("pillar2.png")
platform_1.pos=[100, HEIGHT-50]
bricks2.append(platform_1)

platform_2= Platform("pillar2.png")
platform_2.pos=[300, HEIGHT-190]
bricks2.append(platform_2)

platform_3= Platform("small_cloud.png")
platform_3.pos=[200, HEIGHT-340]
bricks2.append(platform_3)

platform_5= Platform("pillar2.png")
platform_5.pos=[400,200]
bricks2.append(platform_5)

platform_6= Platform("tallpillar.png")
platform_6.pos=[400, 225]
bricks2.append(platform_6)

platform_7= Platform("pillar2.png")
platform_7.pos=[400,320]
bricks2.append(platform_7)

platform_8= Platform("small_cloud.png")
platform_8.pos=[200,70]
bricks2.append(platform_8)

# ---Feathers GAME 2
wings2=[]

feather2= Wing("smallfeather.png")
feather2.pos=[450, 300]
wings2.append(feather2)

feather3= Wing("smallfeather.png")
feather3.pos=[450, 200]
wings2.append(feather3)

# --- Platforms GAME 3
bricks3=[]
platform_10= Platform("pillar2.png")
platform_10.pos=[500, HEIGHT-50]
bricks3.append(platform_10)

platform_20= Platform("pillar2.png")
platform_20.pos=[350, HEIGHT-200]
bricks3.append(platform_20)

platform_30= Platform("pillar2.png")
platform_30.pos=[150, HEIGHT-300]
bricks3.append(platform_30)

platform_50= Platform("tallpillar.png")
platform_50.pos=[150, 100]
bricks3.append(platform_50)

platform_60= Platform("tallpillar.png")
platform_60.pos=[400, 70]
bricks3.append(platform_60)

platform_70= Platform("tallpillar.png")
platform_70.pos=[500, 320]
bricks3.append(platform_70)

platform_80= Platform("thunder_cloud.png")
platform_80.pos=[500, 320]
bricks3.append(platform_80)

# --- lightning
light_1=Hostile("smalllightning.png",platform_80)

# --- Feathers GAME 3
wings3=[]

feather4= Wing("smallfeather.png")
feather4.pos=[410, 50]
wings3.append(feather4)

feather5= Wing("smallfeather.png")
feather5.pos=[510, 300]
wings3.append(feather5)

feather6= Wing("smallfeather.png")
feather6.pos=[160, 80]
wings3.append(feather6)

# --- Platforms GAME 4
bricks4=[]
platform_40= Platform("tallpillar.png")
platform_40.pos=[80, HEIGHT-50]
bricks4.append(platform_40)

platform_42= Platform("tallpillar.png")
platform_42.pos=[450, HEIGHT-50]
bricks4.append(platform_42)

platform_41= Platform("tallpillar.png")
platform_41.pos=[400, 300]
bricks4.append(platform_41)

platform_43= Platform("thunder_cloud.png")
platform_43.pos=[500, 570]
bricks4.append(platform_43)

platform_45= Platform("thunder_cloud.png")
platform_45.pos=[100, 100]
bricks4.append(platform_45)

platform_44= Platform("tallpillar.png")
platform_44.pos=[200, 100]
bricks4.append(platform_44)


# --- Lightning GAME 4
light_2=Hostile("smalllightning.png",platform_43)
light_3=Hostile("smalllightning.png",platform_45)

# --- Feathers GAME 4
wings4=[]

feather7= Wing("smallfeather.png")
feather7.pos=[460, 730]
wings4.append(feather7)

feather8= Wing("smallfeather.png")
feather8.pos=[410, 280]
wings4.append(feather8)

feather9= Wing("smallfeather.png")
feather9.pos=[210,80]
wings4.append(feather9)

# --- Platforms GAME 5
bricks5=[]
platform_50= Platform("pillar2.png")
platform_50.pos=[350, HEIGHT-20]
bricks5.append(platform_50)

platform_50= Platform("pillar2.png")
platform_50.pos=[100, HEIGHT-20]
bricks5.append(platform_50)

# --- Feathers GAME 5
wings5=[]

feather10= Wing("smallfeather.png")
feather10.pos=[400, 700]
wings5.append(feather10)


# --- Platforms GAME 6
bricks6=[]
platform_91= Platform("pillar2.png")
platform_91.pos=[350, 400]
bricks6.append(platform_91)

platform_92= Platform("pillar2.png")
platform_92.pos=[250, 550]
bricks6.append(platform_92)

# --- Platforms GAME 7
bricks7=[]
platform_93= Platform("pillar2.png")
platform_93.pos=[350, 400]
bricks7.append(platform_93)

platform_94= Platform("pillar2.png")
platform_94.pos=[250, 550]
bricks7.append(platform_94)

platform_95= Platform("pillar2.png")
platform_95.pos=[50, 750]
bricks7.append(platform_95)

# --- Platforms GAME 8
bricks8=[]
seas=[]
for x in range(0, WIDTH,100):
    for y in range(HEIGHT-30,(HEIGHT-30)-30*2,-30):
        sea=Platform("pillar2.png")
        sea.pos=[x,y]
        seas.append(sea)

platform_96= Platform("pillar2.png")
platform_96.pos=[350, 370]
bricks8.append(platform_96)

platform_97= Platform("pillar2.png")
platform_97.pos=[250, 550]
bricks8.append(platform_97)


# --- Game page 1
def draw_game1():
    screen.clear()

    background1.draw()
    player.draw()

    for brick in bricks:
        brick.draw()
        
    for feather in wings:
        feather.draw()
        
    screen.draw.text('Feathers: ' + str(player.wing_counter)+"/10", (15,10), color=(255,255,255), fontsize=30)
 
def update_game1():

    player.update()
    player.falling=False

    player.collectwings(feather1)

    # -- Moving platforms
    platform_750.move()
    platform_400.move()

    player.onground = False
    for brick in bricks:
        brick.update()
        if not player.onground:
            if brick.collide(player):
                if player.verticalsp <= 0:
                    player.verticalsp = 1
                else:
                    player.y= brick.y-25
                    player.onground = True
        
    for feather in wings:
        feather.update()
            
    # -- check bounds x
    if player.pos[0] - 10 <=0 or player.pos[0]+10 >= WIDTH:
            player.pos= [100,HEIGHT- 70]
    
    # -- check bounds y
    if player.pos[1]+10 >= HEIGHT:
        player.pos= [125,HEIGHT- 70]

    global game_state

    if player.pos[1] - 10 < 0 and player.wing_counter>= 1:
        game_state+=1
        player.pos=(100, HEIGHT-70)

# --- Game page 2
def draw_game2():
    screen.clear()

    background2.draw()

    player.draw()

    for brick in bricks2:
        brick.draw()
        
    for feather in wings2:
        feather.draw()
        
    screen.draw.text('Feathers: ' + str(player.wing_counter)+"/10", (15,10), color=(255,255,255), fontsize=30)

def update_game2():
    player.update()

    player.collectwings(feather2)
    player.collectwings(feather3)

    platform_3.move()
    platform_8.move()

    feather3.follow(platform_8)

    player.onground = False
    for brick in bricks2:
        brick.update()
        if not player.onground:
            if brick.collide(player):
                if player.verticalsp <= 0:
                    player.verticalsp = 1
                else:
                    player.y= brick.y-25
                    player.onground = True
        
    for feather in wings2:
        feather.update()
            
    # -- check bounds x
    if player.pos[0] - 10 <=0 or player.pos[0]+10 >= WIDTH:
        player.pos= [125,HEIGHT- 70]

    if player.pos[1]+10 >= HEIGHT:
        player.pos= [125,HEIGHT- 70]

    global game_state

    if player.pos[1] - 10 < 0 and player.wing_counter>= 3:
        game_state+=1
        player.pos=(500, HEIGHT-70)

# --- Game page 3
def draw_game3():
    screen.clear()

    background3.draw()

    player.draw()

    for brick in bricks3:
        brick.draw()
        
    for feather in wings3:
        feather.draw()

    light_1.draw()
        
    screen.draw.text('Feathers: ' + str(player.wing_counter)+"/10", (15,10), color=(255,255,255), fontsize=30)

def update_game3():
    player.update()

    platform_80.move()

    player.collectwings(feather4)
    player.collectwings(feather5)
    player.collectwings(feather6)

    light_1.update(player,platform_80)

    player.onground = False
    for brick in bricks3:
        brick.update()
        if not player.onground:
            if brick.collide(player):
                if player.verticalsp < 0:
                    player.verticalsp = 1
                else:
                    player.y= brick.y-25
                    player.onground = True
        
    for feather in wings3:
        feather.update()
            
    # -- check bounds x
    if player.pos[0] - 10 <=0 or player.pos[0]+10 >= WIDTH:
        player.pos= [500,HEIGHT- 70]

    if player.pos[1]+10 >= HEIGHT:
        player.pos= [500,HEIGHT- 70]

    global game_state

    if player.pos[1] - 10 < 0 and player.wing_counter>=6:
        game_state+=1
        player.pos=(100, HEIGHT-70)

# --- Game page 4
def draw_game4():
    screen.clear()

    background4.draw()

    player.draw()

    light_2.draw()
    light_3.draw()

    for brick in bricks4:
        brick.draw()
        
    for feather in wings4:
        feather.draw()

    screen.draw.text('Feathers: ' + str(player.wing_counter)+"/10", (15,10), color=(255,255,255), fontsize=30)

def update_game4():

    player.update()

    platform_43.move()
    platform_45.move()

    light_2.update(player,platform_43)
    light_3.update(player,platform_45)

    player.collectwings(feather7)
    player.collectwings(feather8)
    player.collectwings(feather9)

    player.onground = False
    for brick in bricks4:
        brick.update()
        if not player.onground:
            if brick.collide(player):
                if player.verticalsp < 0:
                    player.verticalsp = 1
                else:
                    player.y= brick.y-25
                    player.onground = True
        
    for feather in wings4:
        feather.update()
            
    # -- check bounds x
    if player.pos[0] - 10 <=0 or player.pos[0]+10 >= WIDTH:
        player.pos= [100,HEIGHT- 70]

    if player.pos[1]+10 >= HEIGHT:
        player.pos= [100,HEIGHT- 70]

    global game_state

    if player.pos[1] - 10 < 0 and player.wing_counter>=9:
        game_state+=1
        player.pos=(200, HEIGHT-50)

# --- Game page 5
def draw_game5():
    screen.clear()

    background5.draw()

    player.draw()

    for brick in bricks5:
        brick.draw()
        
    for feather in wings5:
        feather.draw()
    
    screen.draw.text("That's the last one! SOAR ICARUS", (120,490), color=(255,255,255), fontsize=30)

    screen.draw.text('Feathers: ' + str(player.wing_counter)+"/10", (15,10), color=(255,255,255), fontsize=30)

def update_game5():

    player.update()

    player.collectwings(feather10)

    player.onground = False
    for brick in bricks5:
        brick.update()
        if not player.onground:
            if brick.collide(player):
                if player.verticalsp < 0:
                    player.verticalsp = 1
                else:
                    player.y= brick.y-25
                    player.onground = True
        
    for feather in wings5:
        feather.update()

    # -- check bounds x
    if player.pos[0] - 10 <=0 or player.pos[0]+10 >= WIDTH:
        player.pos= [200,HEIGHT- 50]

    global game_state

    if player.pos[1]+10 >= HEIGHT:
        player.pos= [200,HEIGHT- 50]
        if player.falling==True:
            game_state+=1
            player.pos=(300, 50)
    
    bricks_to_remove=[]

    if player.y<180:
        player.on_fire=True
        player.falling=True
        
        for brick in bricks5:
            bricks_to_remove.append(brick)
            bricks5.remove(brick)


# --- Game page 6
def draw_game6():
    screen.clear()

    background6.draw()

    player.draw()

    for brick in bricks6:
        brick.draw()
    
    screen.draw.text('Lives: ' + str(player.life), (15,10), color=(255,255,255), fontsize=30)
        
def update_game6():
    player.falling=True
    player.update()
    bricks_to_remove=[]
    player.gravity=0.1

    global game_state

    if player.life<=0:
       game_state=9

    player.onground = False
    for brick in bricks6:
        brick.update()
        if not player.onground:
            if brick.collide(player):
                bricks_to_remove.append(brick)
                bricks6.remove(brick)
                player.life-=1
                player.pos= [300, 50]
        
    if player.pos[0] - 10 <=0 or player.pos[0]+10 >= WIDTH:
        player.pos= [300, 50]
    
    if player.pos[1]+10 >= HEIGHT and player.life>0:   
            game_state+=1
            player.pos=(300, 50)

# --- Game page 7
def draw_game7():
    screen.clear()

    background7.draw()

    player.draw()

    for brick in bricks7:
        brick.draw()
    
    screen.draw.text('Lives: ' + str(player.life), (15,10), color=(255,255,255), fontsize=30)

def update_game7():
    player.falling=True
    player.update()
    bricks_to_remove=[]
    player.gravity=0.1

    global game_state

    if player.life<=0:
       game_state=9

    platform_93.move()
    platform_94.move()
    platform_95.move()

    player.onground = False
    for brick in bricks7:
        brick.update()
        if not player.onground:
            if brick.collide(player):
                bricks_to_remove.append(brick)
                bricks7.remove(brick)
                player.life-=1
                player.pos= [300, 50]
    
    if player.pos[0] - 10 <=0 or player.pos[0]+10 >= WIDTH:
        player.pos= [300, 50]
    
    if player.pos[1]+10 >= HEIGHT and player.life>0:   
            game_state+=1
            player.pos=(300, 50)

# --- Game page 8
def draw_game8():
    screen.clear()

    background8.draw()

    player.draw()

    for brick in bricks8:
        brick.draw()
    
    screen.draw.text('Lives: ' + str(player.life), (15,10), color=(255,255,255), fontsize=30)

    global game_won
    if game_won==True:
        screen.draw.text("YOU WON!", (55,350), color=(255,255,255), fontsize=120)
        screen.draw.text("Press ENTER to restart", (150,500), color=(255,255,255), fontsize=40)
        update_final()

def update_game8():
    player.falling=True
    player.update()
    bricks_to_remove=[]
    player.gravity=0.2
    global game_state, game_won

    if player.life<=0:
       game_state=9

    platform_96.move()
    platform_97.move()

    player.onground = False
    for brick in bricks8:
        brick.update()
        if not player.onground:
            if brick.collide(player):
                bricks_to_remove.append(brick)
                bricks8.remove(brick)
                player.life-=1
                player.pos= [300, 50]

    for sea in seas:
        sea.update()
        if not player.onground:
            if sea.collide(player):
                if player.verticalsp < 0:
                    player.verticalsp = 1
                else:
                    player.y= sea.y-25
                    player.onground = True
                if player.life>0:
                    game_won=True

    if player.pos[0] - 10 <=0 or player.pos[0]+10 >= WIDTH:
        player.pos= [300, 50]

# --- Game page final
def draw_final():
    screen.clear()
    background9.draw()
    screen.draw.text("GAME OVER", (55,350), color=(255,255,255), fontsize=120)
    screen.draw.text("Press ENTER to restart", (150,500), color=(255,255,255), fontsize=40)

def update_final():         
    global game_state
    game_over=pygame.key.get_pressed()
    
    if game_over[pygame.K_KP_ENTER]:
        game_state=0

# -- directionnal
def draw():
    cheat=pygame.key.get_pressed()

    global game_state

    if player.life==0:
        game_state=9

    if game_state == 0:
        draw_title()
    elif game_state == 1:
        draw_game1()
    elif game_state == 2:
        draw_game2()
    elif game_state == 3:
        draw_game3()
    elif game_state == 4:
        draw_game4()
    elif game_state == 5:
        draw_game5()
    elif game_state == 6:
        draw_game6()
    elif game_state == 7:
        draw_game7()
    elif game_state == 8:
        draw_game8()
    elif game_state == 9:
        draw_final()

def update(dt):
    cheat=pygame.key.get_pressed()
    global game_state

    if game_state == 0:
        update_title()
    elif game_state == 1:
        update_game1()
    elif game_state == 2:
        update_game2()
    elif game_state == 3:
        update_game3()
    elif game_state == 4:
        update_game4()
    elif game_state == 5:
        update_game5()
    elif game_state == 6:
        update_game6()
    elif game_state == 7:
        update_game7()
    elif game_state == 8:
        update_game8()
    elif game_state == 9:
        update_final()


# -- Lance le jeu
pgzrun.go()