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
sndCh2=''
sndCh3=''
try:
    engSound=pygame.mixer.Sound("sfx_vehicle_engineloop.wav")
    carSound=pygame.mixer.Sound("sfx_vehicle_carloop1.wav")
    fastSound=pygame.mixer.Sound("sfx_vehicle_carloop2.wav")
    outfuelSound=pygame.mixer.Sound("sfx_movement_stairs4a.wav")
    sndCh=pygame.mixer.Channel(0)
    sndCh2=pygame.mixer.Channel(1)
    sndCh3=pygame.mixer.Channel(2)
    sndCh2.set_volume(0.5)
    pygame.mixer.music.load("ff7choco.mid")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
except:
    pass #don't do anything if we can't play music.
#MR LEE set mode and clock
screen=pygame.display.set_mode((800,600))
clock=pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
font2 = pygame.font.SysFont(None, 40)
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
gravity=3
distX=0
distY=0
altitude=0#the real height of car
blasting=0
inAir=0
oldAlt=0
crashed=0
bestAlt=0
bestDst=0
fuel=1000
gameOver=0
#MR LEE's code
def drawCar(screen,x,y,fly):
    if fly:
        pygame.draw.ellipse(screen,RED,[x-10,y+20,20,ri(20,40)])
        pygame.draw.ellipse(screen,RED,[x+90,y+20,20,ri(20,40)])
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
def drawGameOver(screen,x,y):
    img = font2.render("GAME OVER! Your High Score is:"+str(-1*bestAlt+bestDst), True, RED)
    img2 = font.render("Press  Q  to close this window.", True, RED)
    screen.blit(img, (x,y))
    screen.blit(img2, (x,y+20))
#MR LEE main program loop starts here.
while not gameOver:
    #update car position by speed in x/y direction
    carX+=speedX
    carY+=speedY
    if altitude < bestAlt:
        bestAlt=altitude
    oldAlt=altitude
    altitude+=speedY
    if inAir and speedY>60 and backY <= 0:
        crashed=1
        bestAlt=0
    if altitude>0 and backY<=0:
        altitude=0
        inAir=0
    #limit car position
    if carY > 400: #on lowest screen position.
        carY=400
    elif carY < 50: # in air
        carY=50
        inAir=1
    #when altitude is greater than -400, backY will not be effected by speedY
    #this allows us to feel that the car is still falling.
    if altitude > -400:
        backY-=speedY
    if altitude < 0:
        cloudY-=speedY
    if altitude >= 0:
        speedY=0
    #moving background
    if backY<=0:
        backY=0
    elif backY>=200:
        backY=200
    #horizontal positions
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
        if inAir:
            if oldAlt > altitude: #going up
                cloudY=ri(-300,300)
            else:#going down
                cloudY=ri(300,900)
        else:
            cloudX=1000
            cloudY=ri(0,380)
    if altitude < -600:
        if oldAlt > altitude: #going up
            if cloudY > 700:
                cloudX=ri(0,800)
                cloudY=-20
        else:#going down
            if cloudY < -100 :
                cloudX=ri(0,800)
                cloudY=700
    distX+=speedX
    bestDst = max(distX,bestDst)
    try: sndCh.set_volume(speedX/100+0.2)
    except: pass
    
    #allow gameplay when fuel is greater than zero
    if fuel <= 0 and not inAir and altitude==0:
        gameOver=1
    #handle keys
    keys = pygame.key.get_pressed()
    if gameOver:#disable keys
        drawGameOver(screen,200,200)
        break
    if keys[pygame.K_UP]:
        if fuel>0:
            fuel-=2
            blasting=1
            speedY-=1
            #play sound when speeding up
            try: sndCh2.play(engSound)
            except: pass
        else: #no fuel left.
            blasting=0
            speedY+=gravity
            try: sndCh2.play(outfuelSound)
            except: pass
    else: #not up
        blasting=0
        if speedY < 100 and altitude < 0:
            speedY+=gravity
        try: sndCh2.stop()
        except: pass
    if keys[pygame.K_RIGHT]:
        if fuel>0:
            fuel-=1
            speedX+=1
            #play sound when speederation
            try:sndCh.play(carSound,maxtime=200)
            except:pass
        else: #no fuel left.
            try: sndCh2.play(outfuelSound)
            except: pass
    else:#if not right
        if speedX>0:
            speedX=int(0.99*speedX)
    if keys[pygame.K_DOWN]:
        #fix car, reset high score.
        carX=0
        carY=400
        backY=0
        speedY=100
        speedX=0
        altitude=0
        crashed=0
        bestAlt=0
        bestDst=0
        distX=0
        gameOver=0
        fuel=1000
    if keys[pygame.K_LEFT]:
        if fuel>0:
            fuel-=1
            speedX-=1
            #play sound when speederation
            try: sndCh.stop()
            except: pass
        else: #no fuel left.
            try: sndCh2.play(outfuelSound)
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
    drawCloud(screen,cloudX,cloudY)
    drawText(screen,20,20,'Speed:'+str(speedX)+' pixels per frame')
    drawText(screen,20,40,'Distance:'+str(distX)+' pixels')
    drawText(screen,20,60,'Altitude:'+str(altitude)+' pixels')
    drawText(screen,20,80,'backY:'+str(backY)+' pixels')
    drawText(screen,20,100,'speedY:'+str(speedY)+' pixels')
    drawText(screen,20,120,'inAir:'+str(inAir))
    drawText(screen,20,140,'crashed:'+str(crashed))
    drawText(screen,20,160,'fuel:'+str(fuel))
    drawText(screen,20,180,'bestScore:'+str(-1*bestAlt + bestDst))
    
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
    #simulate wind
    if blasting or speedX>60 or speedY > 30:
        drawCar(screen,carX,carY+ri(-1,1),blasting)
    else:
        drawCar(screen,carX,carY,blasting)
    pygame.display.flip()
    clock.tick(30)

#after the first while loop:
while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
    clock.tick(30)        