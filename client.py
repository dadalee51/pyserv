#client v7
import socket
import pickle
import gamepacket
import pygame
import random
from bitstring import BitArray

gp=gamepacket.GamePacket(random.randint(50,5000)) 
gp.username=input('please enter player\'s name:')
gp.color=(random.randint(1,255),random.randint(1,255),random.randint(1,255))
#each player should assign themselves with a unique id.
HOST = '127.0.0.1'    # address of server if you run your own
#HOST = '192.168.1.30'    # address of server if you run your own
#HOST = '192.168.1.111'    # address of server if you are in class
#HOST = '123.243.118.66'    # address of server if you want to join others over the internet.
PORT = 50007          # the port for first contact
PACKSIZE=gamepacket.WorldPacket.packSize
print('press q to quit, press f to switch fullscreen...')
full_screen=False
pygame.init()
screen=pygame.display.set_mode(gp.gameMode)
#screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width,height=screen.get_size()
clock=pygame.time.Clock()
running=True
drag=False
font = pygame.font.SysFont(None, 12)
img = font.render(gp.username, True, gp.color)
#first connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	s.send(pickle.dumps(gp))
	data = pickle.loads(s.recv(PACKSIZE))
	gp.port=data.port
	#print(data)

#follow up, private connection, main loop of client.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, data.port))
	while running:
		screen.fill((0,0,0))
		
		#if dragging, we need to store the x,y position before
		#user updates using keys.
		if gp.drag:
			gp.newwall=gp.XYtobs(gp.pos_x//gp.gameTileSize,gp.pos_y//gp.gameTileSize)
		
		#motion keys
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			gp.pos_y -= 4
		if keys[pygame.K_DOWN]:
			gp.pos_y += 4
		if keys[pygame.K_LEFT]:
			gp.pos_x -= 4
		if keys[pygame.K_RIGHT]:
			gp.pos_x += 4
		#do some wrapping magic here
		if gp.pos_x < 0: gp.pos_x = gp.gameWidth
		if gp.pos_x > gp.gameWidth: gp.pos_x = 0
		if gp.pos_y < 0: gp.pos_y = gp.gameHeight
		if gp.pos_y > gp.gameHeight: gp.pos_y = 0
		
		#event keys:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running=False
			elif event.type==pygame.KEYDOWN:
				if event.key==pygame.K_q:
					running=False
					gp.quit=1
				elif event.key==pygame.K_SPACE:
					gp.drag=not gp.drag
				elif event.key==pygame.K_f:
					full_screen=not full_screen
					if full_screen: 
						screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
						width,height=screen.get_size()
					else: 
						screen=pygame.display.set_mode(gp.gameMode)
		#update drawing based on game packet.
		#player position
		screen.fill(gp.color,(gp.pos_x,gp.pos_y,gp.size,gp.size))
		screen.blit(img, (gp.pos_x+gp.size+5,gp.pos_y+gp.size-5))
		#dump and send game packet to socket.
		s.send(pickle.dumps(gp))
		if gp.quit==1:
			break
		#load world packet from server.
		world = pickle.loads(s.recv(PACKSIZE))
		#discard own data, may need in future.
		world.players.pop(gp.player_id)
		for p in world.players.items():
			p=p[1]
			screen.fill(p.color,(p.pos_x,p.pos_y,p.size,p.size))
			pname = font.render(p.username, True, p.color)
			screen.blit(pname, (p.pos_x+5,p.pos_y-5))
		#also draw the updated walls.
		#draw walls.
		for pos,exist in enumerate(world.walls):
			if exist: 
				p=gp.bstoXY(pos)
				screen.fill((255,255,255),(p[0]*gp.gameTileSize+1,p[1]*gp.gameTileSize,gp.size+1,gp.size))
		#then update the screen.
		pygame.display.flip()
		clock.tick(30)