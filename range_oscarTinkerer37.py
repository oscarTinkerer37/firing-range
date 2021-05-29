#Shooting range
#10.05.2021
#inspired by Clear code's sprites tutorials (https://youtu.be/hDu8mcAlY4E)
#12.05.2021 Works well for single target. Still need to decompose to account for head-shoulders cutout on target.
#15.05.2021 Implemented drop animation and reset function. Still need to account for head-shoulders cutout.
#15.05.2021 learning to use pygame.draw.polygon(); got body and head polygons working for bodyshot/headshot (insta-kill) working.
                    #clearly defined boundaries for headshot and bodyshot
                    #NEED TO GENERALIZE POLYGON FOR ANY AND ALL TARGET SIZES + POSITIONS ON WINDOW
                    #headG (generalized head hitbox) is still on top left corner of window
#29.05.2021 Generalized head and body hit polygons - target can be placed anywhere on screen now and polygons will follow


import pygame
import random
import sys
import os

myDir = '/Users/mypygame'
os.chdir(myDir)

sightPic = 'ironSights.tif'
#target = 'steelTarget0.tif'

fire = os.path.join(myDir, 'audio_assets/singleShot.wav')
ping = os.path.join(myDir, 'audio_assets/steelTarget1.wav')
clang = os.path.join(myDir, 'audio_assets/fallingPlate.wav')
newMag = os.path.join(myDir, 'audio_assets/m4reload.wav')
loudPing = os.path.join(myDir, 'audio_assets/loudPing.wav')


bg = 'firingRange.png'
steelW = 175
steelH = 283
windowSize = (1800, 600) #display.set.mode(()) can take tuple inside parens
#tarX = windowSize[0]*0.45
randX = random.randint(175, windowSize[0]-steelW)

tarX = randX
tarY = windowSize[1]*0.45
hitTuple = (tarX, tarY)

numHits = random.randint(1, 10)

#BUILDING CLASSES
class Irons(pygame.sprite.Sprite): #inherits from Sprite class
    #def __init__(self, width, height, posX, posY, color):#attributes to create image and rect around it
    def __init__(self): #no h or w needed since it is an image
        super().__init__() #initiating object
        #self.image = pygame.Surface([width, height])#empty surface
        self.image = pygame.image.load(sightPic)
        #self.image.fill(color)
        self.rect = self.image.get_rect() #draws rect around image
        #self.rect.center = [posX, posY] #specifically calling center of rect
    def update(self): #predefined in sprite class
        self.rect.center = pygame.mouse.get_pos()

class Dummy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.roundsFired = 0
        self.image = pygame.image.load('impactPoint.tif')
        self.rect = self.image.get_rect()
        
        self.single = pygame.mixer.Sound(fire) #load sound
        self.rel = pygame.mixer.Sound(newMag)
        
    def shotSound(self):
        self.single.play() #play sound when called upon in mainloop
        self.roundsFired += 1
        print("Shots fired:", self.roundsFired, end= ' | ')
        pygame.time.delay(5)
        print(self.rect.center)
    def reload(self):
        pygame.time.delay(5)
        self.rel.play()
        self.roundsFired = 0
        pygame.time.delay(5900)
        print("*WEAPON READY*")

    def update(self): #predefined in sprite class
        self.rect.center = pygame.mouse.get_pos() #get xy position of mouse
        #print(pygame.mouse.get_pos())
        #updates every frame with mouse position

#steel targets
class Targets(pygame.sprite.Sprite): 
    def __init__(self, posX, posY):
        super().__init__()
        self.frames = [pygame.image.load('steelTarget0.tif'), pygame.image.load('steelTarget1.tif'), pygame.image.load('steelTarget2.tif'),
        pygame.image.load('steelTarget3.tif'), pygame.image.load('steelTarget4.tif')]
        self.sfx = pygame.image.load('hit_effect.png')
        self.targetState = 0
        self.image = self.frames[self.targetState]
        self.rect = self.image.get_rect()
        self.rect.topleft = [posX, posY] #position specified when instantiating object
        #self.hitPoly = pygame.draw.polygon(win, (0,255,0), [(840, 438), (816.1, 383), (816, 237), (831, 214), (967, 214), (987, 237), (987, 383), (963, 438), (840, 438)], width = 1)
        #self.headPoly = pygame.draw.polygon(win, (255,0,0), [(923, 166), (923, 213), (873, 213), (873, 166)], width = 1)
        #self.headG = pygame.draw.polygon(win, (0,0,255), [(0.486*steelW, 0), ((0.486+0.177+0.24)*steelW, 0), ((0.486+0.177+0.24)*steelW, 0.166*steelH), (0.486*steelW, 0.166*steelH), (0.486*steelW,0)], width = 0)
        self.headG = pygame.draw.polygon(win, (0,0,255), [((0.486-0.145)*steelW+tarX, 0+tarY), ((0.486+0.177)*steelW+tarX, 0+tarY), ((0.486+0.177)*steelW+tarX, 0.166*steelH+tarY), ((0.486-0.145)*steelW+tarX, 0.166*steelH+tarY), ((0.486-0.145)*steelW+tarX, 0+tarY)], width = 0)
        self.bodyG = pygame.draw.polygon(win, (0,255,0), [(0+tarX, (0.0813+0.166)*steelH+tarY), (0.097*steelW+tarX, 0.166*steelH+tarY), (0.874*steelW+tarX, 0.166*steelH+tarY), (0.971*steelW+tarX, (0.0813+0.166)*steelH+tarY),
                                                          (0.971*steelW+tarX, (0.597+0.166)*steelH+tarY), (0.84*steelW+tarX, (0.774+0.166)*steelH+tarY), (0.097*steelW+tarX, (0.774+0.166)*steelH+tarY), (0+tarX, (0.597+0.166)*steelH+tarY), (0+tarX, (0.0813+0.166)*steelH+tarY)], width = 0)
        self.hit = pygame.mixer.Sound(ping)
        self.loud = pygame.mixer.Sound(loudPing)
        self.drop = pygame.mixer.Sound(clang)
        self.counter = 0
        self.down = False
    def hIT(self):
        pygame.time.delay(10)
        self.hit.play()
        pygame.time.delay(5)
    def headShot(self):
        pygame.time.delay(10)
        self.loud.play()
        pygame.time.delay(10)
    def dead(self):
        pygame.time.delay(180) #needs delay to be audible
        self.drop.play()
        pygame.time.delay(5)
        print("\n*TARGET DOWN* - PRESS r TO RESET AND RELOAD")
    def reset(self):
        self.counter = 0
        self.down = False
        self.targetState = 0
        self.counter = 0
        self.image = self.frames[self.targetState]
        print("\n**TARGET RESET**")

pygame.init()

clock = pygame.time.Clock()

#SCREEN SETTING

win = pygame.display.set_mode((windowSize))
pygame.display.set_caption("Firing range")
background = pygame.image.load(bg)


pygame.mouse.set_visible(False) #hides mouse pointer

#MAIN LOOP

#instantiating objects as part of groups
#iron sight
#ironSight = Irons(204, 203, 100, 100, (255,255,255)) #blank square
ironSight = Irons()
ironSight_group = pygame.sprite.Group()
ironSight_group.add(ironSight)

point = Dummy()
point_group = pygame.sprite.Group()
point_group.add(point)

#targets
target_group = pygame.sprite.Group()
for t in range(1):
    #new_target = Targets(random.randrange(0, 1800), 350)
    new_target = Targets(tarX, tarY)
    #tarX += 275 #comment out for single target
    target_group.add(new_target)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if point.roundsFired < 30:
                point.shotSound() #calls upon sound stored in Irons by ironSight instance
                if new_target.down == False:
                    if new_target.headG.collidepoint(pygame.mouse.get_pos()) == True:
                        new_target.headShot()
                        print("*HEAD SHOT*")
                        new_target.dead()
                        new_target.down = True
                    if new_target.bodyG.collidepoint(pygame.mouse.get_pos()) == True:
                        new_target.hIT()
                        new_target.counter += 1
                        print("HITS: %s" %(new_target.counter), end = ' | ')
                        print(pygame.mouse.get_pos()[0], end = ', ')
                        print(pygame.mouse.get_pos()[1], end = ' - ')
                        print("Body shots required: %s" %(numHits - new_target.counter))
                    if new_target.counter == numHits:
                        new_target.dead()
                        new_target.down = True
                    if new_target.down == True:
                        for s in range (0, 4):
                            new_target.targetState += 1
                            new_target.image = new_target.frames[new_target.targetState]
                            pygame.time.delay(25)
                    
            #print("BODY-POLY: ", new_target.hitPoly.collidepoint(pygame.mouse.get_pos()))
            #print("HEAD-POLY: ", new_target.headPoly.collidepoint(pygame.mouse.get_pos()))
                    
            elif point.roundsFired == 30:
                print("\n*MAGAZINE EMPTY*\n")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                point.reload()
                new_target.reset()
                #target_group.update()
                numHits = random.randint(1, 10)
    pygame.display.flip() #
    win.fill((0, 0, 0))
    #win.blit(background, (0,0))
    
    target_group.draw(win)
    ironSight_group.draw(win)#updates entire group (all instances)
    
    ironSight_group.update()
    point_group.draw(win)
    point_group.update()
    
    clock.tick(24)
