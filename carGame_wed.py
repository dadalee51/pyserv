#MR Lee's pygame car moving as at Wed4pm
import pygame
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
accelX=1
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
    clock.tick(10)
    carX+=accelX
    accelX+=1
    if carX > 400:
        carX=400
    drawBackground(screen,0,0)
    drawCar(screen,carX,carY)
    drawCloud(screen,300,200)
    pygame.display.flip()
    
