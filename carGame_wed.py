#MR Lee's pygame car moving as at Wed4pm
import pygame
import sys
screen=pygame.display.set_mode((800,600))
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(120,120,250)
GREEN=(0,255,0)
RED=(255,0,0)
GREY=(170,170,170)
clock=pygame.time.Clock()
carX=100
carY=400
cloudX=300
cloudY=200
speedX=0
speedY=0
gravity=3
#MR LEE's code
def drawCar(screen,x,y):
    pygame.draw.circle(screen,BLACK, [x,y], 30)
    pygame.draw.circle(screen,BLACK, [x+100,y], 30)
    pygame.draw.rect(screen,GREEN,[x,y,100,-50])
def drawBackground(screen,x,y):
    pygame.draw.rect(screen,GREY,[x,y+400,800,200])
    pygame.draw.rect(screen,BLUE,[x,y,800,400])
def drawCloud(screen,x,y):
    pygame.draw.ellipse(screen,WHITE,[x,y,50,20])
    pygame.draw.ellipse(screen,WHITE,[x-25,y+15,50,20])
#MR LEE's code
while True:
    screen.fill(WHITE)
    clock.tick(60)#60 fastest, 30 normal, 10 slow...
    carX+=speedX
    carY+=speedY
    print(speedY, carY)
    if carX > 400:
        carX=400
        cloudX-=speedX
    if cloudX <= -20:
        cloudX=1000
    if carY > 400:
        carY=400
        speedY=0
    print("speedX:",speedX)
    if speedX > 100:
        speedX=100
    #MR LEE - handle keys
    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        speedY-=1
    else:
        speedY+=gravity
    if keys[pygame.K_RIGHT]:
        speedX+=1
    if keys[pygame.K_LEFT]:
        speedX-=1
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    drawBackground(screen,0,0)
    drawCar(screen,carX,carY)
    drawCloud(screen,cloudX,cloudY)
    pygame.display.flip()
    
