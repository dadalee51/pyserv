#MR LEE's carGameBasic
import pygame
screen = pygame.display.set_mode((800,600))
WHITE=(255,255,255)
BLACK=(0,0,0)
BLUE=(120,120,250)
GREEN=(0,255,0)
RED=(255,0,0)
GREY=(170,170,170)
clock=pygame.time.Clock()
carX=0
speedX=1
def drawCar(screen, x, y):
    pygame.draw.circle(screen,BLACK,[x,y],30)
    pygame.draw.circle(screen,BLACK,[x+100,y],30)
    pygame.draw.rect(screen,GREEN,[x,y,100,-50])
def drawBackground(screen, x, y):
    pygame.draw.rect(screen,BLUE,[x,y,800,400])
    pygame.draw.rect(screen,GREY,[x,y+400,800,200])
while True:
    drawBackground(screen,0,0)
    carX=carX+speedX
    speedX=speedX+1
    drawCar(screen,carX,400)
    clock.tick(10)
    pygame.display.flip()
    
    