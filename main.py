import pygame
import random
pygame.init()
pygame.display.set_caption("Bootleg Space Invaders")
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
gameover = False
timer = 0;

#player vatiables
xpos = 400
ypos = 750
moveLeft = False
moveRight = False
shoot = False
#----------------------------------------------------------------------------------------------------------------------
class wall:
    def __init__ (self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.numHits = 0

    def draw(self):
        #print("drawing wall at", self.xpos, self.ypos)
        if self.numHits ==0:
            pygame.draw.rect(screen, (250, 250, 20), (self.xpos, self.ypos, 30, 30))
        if self.numHits ==1:
            pygame.draw.rect(screen, (150, 150, 10), (self.xpos, self.ypos, 30, 30))
        if self.numHits ==2:
            pygame.draw.rect(screen, (50, 50, 0), (self.xpos, self.ypos, 30, 30))
         
    def collide(self, BulletX, BulletY):
        if self.numHits < 3:
            if BulletX > self.xpos:
                if BulletX < self.xpos + 30:
                    if BulletY < self.ypos + 30:
                        if BulletY > self.ypos:
                            print("hit!")
                            self.numHits += 1
                            return False
        return True
#instantiate a bunch of walls    
walls = []
for k in range (4):
        for i in range (2):
            for j in range (3):
                walls.append(wall(j*30+200*k+50, i*30+600))

#----------------------------------------------------------------------------------------------------------------------
class Bullet:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = False

    def move(self, xpos, ypos):
        global shoot
        if self.isAlive == True: #only shoot live bullets
            self.ypos-=5 #move up when shoot
        if self.ypos < 0: #check if you've hit the top of the screen
            self.isAlive = False #set to dead
            self.xpos = xpos #reset player position
            self.ypos = ypos

    def draw(self):
        pygame.draw.rect(screen, (255, 0 , 0), (self.xpos, self.ypos, 3, 20))

#instantiate bullet object
bullet = Bullet(xpos+28, ypos) #create bullet object and pass player position
#----------------------------------------------------------------------------------------------------------------------
class Alien:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = True
        self.direction = 1
    def draw(self):
        pygame.draw.rect(screen, (255,255,255), (self.xpos, self.ypos, 40, 40))
        if (self.isAlive == False):
            pygame.draw.rect(screen, (0,0,0), (self.xpos, self.ypos, 40, 40))
    
    def move(self, time):
        #reset what direction you are moving every 8 moves:
        if time % 800 == 0:
            self.ypos+=30 #moves down
            self.direction*=-1 #flip direction
            return 0 #resets timer to 0
   
        #mover every time the timer invreases by 100:
        if time%100==0:
            self.xpos+=50*self.direction #move right
   
        return time #doesn't reset if first if statement hasn't executed!
    
    def collide(self, BulletX, BulletY):
        if self.isAlive:
            if BulletX > self.xpos:
                if BulletX < self.xpos + 40:
                    if BulletY < self.ypos + 40:
                        if BulletY > self.ypos:
                            print("hit")
                            self.isAlive = False
                            return False
        return True

   

#instantiate a bunch of aliens
armada = []
for i in range (4):
    for j in range (5):
        armada.append(Alien(j*80+60, i*80+50))

#----------------------------------------------------------------------------------------------------------------------

class missle:
    def __init__(self, xpos, ypos):
        self.xpos = -10
        self.ypos = -10
        self.isAlive = False
    def move(self):
        if self.isAlive == True:
            self.ypos += 5
        if self.ypos > 800:
            self.isAlive = False
            self.xpos = -10
            self.ypos = -10
    def draw(self):
        if self.isAlive == True:
            pygame.draw.rect(screen, (250, 0, 250), (self.xpos, self.ypos, 3, 20))

missleBag = []
for i in range(10):
    missleBag.append(missle(i*80+75, 100))

       
#---------------------------------------------------------------------------------------------------------------------------

while not gameover: # start game loop#######################################################################################
    clock.tick(60)
    timer += 1
   
    #input section----------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True #quit ggame if X is pressed in corner
           
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveLeft = True
            if event.key == pygame.K_RIGHT:
                moveRight = True
            if event.key == pygame.K_SPACE:
                shoot = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                    moveLeft = False
            if event.key == pygame.K_RIGHT:
                    moveRight = False
            if event.key == pygame.K_SPACE:
                    shoot = False
       
    #physics section--------------------------------------------------------------------------
   
   
   
    # PLAYER MOVEMENT: check variables from the intup section
    if moveLeft == True:
        vx = -3
    elif moveRight == True:
        vx = 3
    else:
        vx = 0
       
    # update player position
    xpos += vx
   
   
    #shoot player bullet--------------
    if shoot == True:
        bullet.isAlive = True

    if bullet.isAlive == True:
        bullet.move(xpos+28, ypos)
        if bullet.isAlive == True:
        #check for collision
            for i in range (len(armada)):
                bullet.isAlive = armada[i].collide(bullet.xpos, bullet.ypos)
                if bullet.isAlive == False:
                    break
           
        if bullet.isAlive == True:
        #check for collision between bullet and enemy
            for i in range (len(walls)):
                bullet.isAlive = walls[i].collide(bullet.xpos, bullet.ypos)
                if bullet.isAlive == False:
                    break
    else:
        bullet.xpos = xpos + 28
        bullet.ypos = ypos

   
    #Enemy shoot Missle----------------------------------------------------------------------

    #check for wall/missle collison
    for i in range(len(walls)): #check each wall box
        for j in range(len(missleBag)): #against each missle
            if missleBag[j].isAlive == True: # check if missle is true
                if walls[i].collide(missleBag[j].xpos, missleBag[j].ypos)== False: #call wall collision for each combo
                    missleBag[j].isAlive = False #kill missle
                    break #stop killing walls if you're dead


    for i in range(len(missleBag)):
        missleBag[i].move()

    chance = random.randrange(100)
    if chance < 2:

        pick = random.randrange(len(armada))
        if armada[pick].isAlive == True:
            for i in range(len(missleBag)):
                if missleBag[i].isAlive == False:
                    missleBag[i].isAlive = True
                    missleBag[i].xpos = armada[pick].xpos+5
                    missleBag[i].ypos = armada[pick].ypos
                    break

               
    #check for player/missle collision
    for i in range (len(missleBag)):
        if missleBag[i].isAlive:
            if missleBag[i].xpos > xpos:
                if missleBag[i].xpos < xpos + 40:
                    if missleBag[i].ypos < ypos + 40:
                        if missleBag[i].ypos > ypos:
                            print("player hit!")
           

    #Render section---------------------------------------------------------------------------
   
    screen.fill((0,0,0))

    #move all the aliens                
    for i in range (len(armada)):
        timer = armada[i].move(timer)

    pygame.draw.rect(screen, (200, 200, 100), (xpos, ypos, 60, 20))
   
    for i in range (len(armada)):
        armada[i].draw()

    for e in range (len(walls)):
        walls[e].draw()

    for e in range (len(missleBag)):
        missleBag[e].draw()
       
    bullet.draw()

    pygame.display.flip()
   
#end game loop-----------------------
   
pygame.quit()
