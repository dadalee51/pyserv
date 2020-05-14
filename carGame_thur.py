#MR LEE's pygame test
import pygame
screen = pygame.display.set_mode((800,600))
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(120,120,250)
GREEN=(0,255,0)
RED=(255,0,0)
GREY=(170,170,170)
clock=pygame.time.Clock()
carX=100
carY=200
accelX=1
#MR Lee's code
def drawCar(screen, x, y):
    pygame.draw.circle(screen, BLACK, [x,y],30)
    pygame.draw.circle(screen, BLACK, [x+100,y],30)
    pygame.draw.rect(screen,GREEN,[x,y,100,-50])
while True:
    screen.fill(WHITE)
    drawCar(screen,carX,carY)
    carX+=accelX
    accelX+=1
    if carX > 400:
        carX=400
    clock.tick(10)
    pygame.display.flip()
    
   