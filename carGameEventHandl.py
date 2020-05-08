#adding key and event handling
#MR Lee's pygame
import pygame
import sys
from random import randint as ri
pygame.init()
#MR LEE music and sound
engSound=''
carSound=''
fastSound=''
sndCh=''
sndCH2=''
try:
    engSound=pygame.mixer.Sound("sfx_vehicle_engineloop.wav")
    carSound=pygame.mixer.Sound("sfx_vehicle_carloop1.wav")
    fastSound=pygame.mixer.Sound("sfx_vehicle_carloop1.wav")
    sndCh=pygame.mixer.Channel(0)
    sndCh2=pygame.mixer.Channel(1)
    sndCh2.set_volume(0.5)
    #pygame.mixer.music.load("ff7choco.mid")
    #pygame.mixer.music.set_volume(0.5)
    #pygame.mixer.music.play()
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
backY=0
signXList=[0,400,800,1200]
speedX=0
speedY=0
gravity=5
distX=0
distY=0
altitude=0
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
    pygame.draw.rect(screen,BLUE,[x,y-200,800,600])
def drawCloud(screen,x,y):
    pygame.draw.ellipse(screen,WHITE,[x,y,50,20])
    pygame.draw.ellipse(screen,WHITE,[x-25,y+15,50,20])
def drawRoadSign(screen,x,y):
    pygame.draw.rect(screen,WHITE,[x,y,100,15])
def drawText(screen,x,y,text):
    img = font.render(text, True, BLACK)
    screen.blit(img, (x,y))
#MR LEE main program loop starts here.
while True:
    screen.fill(WHITE)
    carX+=speedX
    carY+=speedY
    
    if carY >= 400: #on lowest screen position.
        carY=400
        backY-=speedY
        speedY=0
    elif carY < 50: # in air
        carY=50
        backY-=speedY#moving up
    if backY<=0:
        backY=0
    elif backY>=200:
        backY=200
    if carX > 400:
        carX=400
    elif carX < 0:
        carX=0
        speedX=0
    if speedX >= 100:
        speedX=100
    if carX>399:
        cloudX-=speedX
    if cloudX <= -20:
        cloudX=1000
        cloudY=ri(0,200)
    
    distX+=speedX
    try: sndCh.set_volume(speedX/100+0.2)
    except: pass
    #update positions
    
    #handle keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        isFlying=1
        speedY-=1
        #play sound when speederation
        try: sndCh2.play(engSound)
        except: pass
    else:
        isFlying=0
        if speedY < 100: speedY+=gravity
        try: sndCh2.stop()
        except: pass
    if keys[pygame.K_RIGHT]:
        speedX+=1
        #play sound when speederation
        try:sndCh.play(carSound,maxtime=200)
        except:pass
    else:
        if speedX>0:
            speedX=int(0.99*speedX)
    if keys[pygame.K_LEFT]:
        speedX-=1
        #play sound when speederation
        try: sndCh.stop()
        except: pass
    if keys[pygame.K_q]:
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    #drag all shapes
    drawBackground(screen,0,backY)
    drawText(screen,20,20,'Speed:'+str(speedX)+' pixels per frame')
    drawText(screen,20,40,'Distance:'+str(distX)+' pixels')
    drawText(screen,20,60,'Altitude:'+str(altitude)+' pixels')
    drawText(screen,20,80,'backY:'+str(backY)+' pixels')
    drawText(screen,20,100,'speedY:'+str(speedY)+' pixels')

    #road signs needs to be above background
    if carX >= 400:
        for i,xs in enumerate(signXList):
            if xs<=-200:
                xs+=1200
            drawRoadSign(screen,xs,500+backY)
            xs-=speedX
            signXList[i]=xs
    else:
        for xs in signXList:
            drawRoadSign(screen,xs,500+backY)
            
    #draw anything could be in front of the backgrounds.
    drawCloud(screen,cloudX,cloudY)
    if speedX<80:
        drawCar(screen,carX,carY,isFlying)
    else:
        drawCar(screen,carX,carY+ri(-3,3),isFlying)
    
    pygame.display.flip()
    clock.tick(30)
