#MR Lee pygame test for Sat 3-5pm as at 5/9/2020
import pygame
import sys
from random import randint as ri
pygame.init()
pygame.mixer.music.load('MariobrosPhase1.mid')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()
mntImg = pygame.image.load('mountains.jpg')
screen = pygame.display.set_mode((800,600))
clock=pygame.time.Clock()
font=pygame.font.SysFont(None, 40)
WHITE=(255,255,255)
BLACK=(0,0,0)
GREEN=(0,255,0)
RED=(255,0,0)
GREY=(170,170,170)
BLUE=(120,120,250)
carX=100
carY=400
cloudX=300
cloudY=200
speedX=1
speedY=0
gravity=1
altitude=0
back2X=0
back2Y=-500
backY=0
#MR LEE
def drawCar(screen,x,y):
    pygame.draw.circle(screen,BLACK,[x,y],30)
    pygame.draw.circle(screen,BLACK,[x+100,y],30)
    pygame.draw.rect(screen,GREEN,[x,y,100,-50])
def drawBackground(screen,x,y):
    pygame.draw.rect(screen,BLUE,[x,y,800,400])
    screen.blit(mntImg,(back2X,back2Y))
    pygame.draw.rect(screen,GREY,[x,y+400,800,200])
def drawCloud(screen,x,y):
    pygame.draw.ellipse(screen,WHITE,[x,y,50,20])
    pygame.draw.ellipse(screen,WHITE,[x-25,y+15,50,20])
def drawText(screen,x,y,text):
    img=font.render(text, True, WHITE)
    screen.blit(img,(x,y))
#MR LEE's code
while True:
    carX+=speedX #carX=carX+speedX
    carY+=speedY #carY=carY+speedY
    altitude+=speedY
    print(altitude)
    screen.fill(WHITE)
    drawBackground(screen,0,backY)
    if altitude > 0:
        altitude =0
        speedY=0
    if altitude > -400:
        backY-=speedY
        back2Y-=speedY/100
    if altitude < 0:
        back2Y-=speedY/100
    if backY <= 0:
        backY=0
    elif backY >= 200:
        backY=200
    if carY > 400:
        carY=400
    if carY < 0:
        carY=0
    if carX > 400:
        carX=400
        back2X-=speedX/50
        cloudX-=speedX
    if carX < 0 :
        carX=0
        speedX=0
    if cloudX < -20:
        cloudX=1000
        cloudY=ri(0,300)
    if speedX > 100:
        speedX = 100
    #MR LEE's code
    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        speedY-=1 #speedY=speedY-1
    else:
        speedY+=gravity
    #print(speedY)
    if keys[pygame.K_RIGHT]:
        speedX+=1
    elif keys[pygame.K_LEFT]:
        speedX-=1
    elif keys[pygame.K_q]:
        pygame.quit()
        sys.exit()#remember to import sys
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    drawCloud(screen,cloudX, cloudY)#dont' forget cloudX and Y
    drawText(screen,20,20,'SpeedX:'+str(speedX))
    drawText(screen,20,60,'Altitude:'+str(altitude))
    drawCar(screen,carX,carY)
    
    clock.tick(60)
    pygame.display.flip()
