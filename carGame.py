#adding key and event handling
#MR Lee's pygame
import pygame
import sys
from random import randint as ri
pygame.init()
#MR LEE music
try:
    pygame.mixer.music.load("ff7choco.mid")
    pygame.mixer.music.play()
except:
    pass #don't do anything if we can't play music.
#MR LEE set mode and clock
screen=pygame.display.set_mode((800,600))
clock=pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
#MR LEE set colours
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(120,120,250)
GREEN=(0,255,0)
RED=(255,0,0)
GREY=(170,170,170)
#MR LEE variables for shapes
carX=100
carY=400
cloudX=300
cloudY=200
signXList=[0,100,200,300,400,500,600,700,800,900,1000]
accelX=0
accelY=0
gravity=5
distX=0
distY=0
isFlying=0
#MR LEE's code
def drawCar(screen,x,y,fly):
    if fly:
        pygame.draw.ellipse(screen,RED,[x-10,y+20,20,20])
        pygame.draw.ellipse(screen,RED,[x+90,y+20,20,20])
    pygame.draw.circle(screen,BLACK, [x,y], 30)
    pygame.draw.circle(screen,BLACK, [x+100,y], 30)
    pygame.draw.rect(screen,GREEN,[x,y,100,-50])
def drawBackground(screen,x,y):
    pygame.draw.rect(screen,GREY,[x,y+400,800,200])
    pygame.draw.rect(screen,BLUE,[x,y,800,400])
def drawCloud(screen,x,y):
    pygame.draw.ellipse(screen,WHITE,[x,y,50,20])
    pygame.draw.ellipse(screen,WHITE,[x-25,y+15,50,20])
def drawRoadSign(screen,x,y):
    pygame.draw.rect(screen,WHITE,[x,y,50,15])
def drawText(screen,x,y,text):
    img = font.render(text, True, BLACK)
    screen.blit(img, (x,y))
#MR LEE main program loop starts here.
while True:
    screen.fill(WHITE)
    carX+=accelX
    carY+=accelY
    
    if carY >= 400:
        accelY=0
        carY=400
    elif carY < 0:
        carY=0
    
    if carX > 400:
        carX=400
    elif carX < 0:
        carX=0
        accelX=0
    if accelX >= 400:
        accelX=400
    if carX>399:
        cloudX-=accelX
    if cloudX <= -20:
        cloudX=1000
        cloudY=ri(0,200)
    
    distX+=accelX
    #update positions
    
    #handle keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        isFlying=1
        accelY-=1
    elif keys[pygame.K_RIGHT]:
        accelX+=1
    elif keys[pygame.K_LEFT]:
        accelX-=1
    elif keys[pygame.K_q]:
        pygame.quit()
        sys.exit()
    else:
        isFlying=0
        accelY+=gravity
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    #drag all shapes
    drawBackground(screen,0,0)
    drawText(screen,20,20,'Speed:'+str(accelX))
    drawText(screen,20,40,'Distance:'+str(distX))

    #road signs needs to be above background
    if carX >= 400:
        for i,xs in enumerate(signXList):
            if xs<=-200:
                xs+=1100
            drawRoadSign(screen,xs,500)
            xs-=accelX
            signXList[i]=xs
    else:
        for xs in signXList:
            drawRoadSign(screen,xs,500)
            
    #draw anything could be in front of the backgrounds.
    drawCloud(screen,cloudX,cloudY)
    drawCar(screen,carX,carY,isFlying)
        
    pygame.display.flip()
    clock.tick(30)

