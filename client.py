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
print(f'PACKSIZE set to:{PACKSIZE}')
print('press q to quit, press f to switch fullscreen...')
full_screen=False
pygame.init()
screen=pygame.display.set_mode(gp.gameMode)
width,height=screen.get_size()
clock=pygame.time.Clock()
running=True
font = pygame.font.SysFont(None, 12)
img = font.render(gp.username, True, gp.color)
#local wall instance to save time.
local_wall=[[-1 for _ in range(gp.gameTileHeight+4)] for _ in range(gp.gameTileWidth+4)]
local_explode=[[-1 for _ in range(gp.gameTileHeight+4)] for _ in range(gp.gameTileWidth+4)]

#first connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	s.send(pickle.dumps(gp))
	data = pickle.loads(s.recv(PACKSIZE))
	gp.port=data.port
	
#follow up, private connection, main loop of client.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, data.port))
	while running: #socket will close after running fin.
		screen.fill((0,0,0))#wipe screen clean.
		#clean gp historical burdens
		gp.newwall=-1
		gp.explode=-1
		
		#user updates using keys.
		if gp.drag:
			gp.newwall=gp.XYtobs(gp.pos_x//gp.gameTileSize,gp.pos_y//gp.gameTileSize)
		
		#motion keys
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			if local_wall[gp.pos_x//gp.gameTileSize+1][(gp.pos_y-4)//gp.gameTileSize] == -1:
				gp.pos_y -= 4
		if keys[pygame.K_DOWN]:
			if local_wall[gp.pos_x//gp.gameTileSize+1][(gp.pos_y+4)//gp.gameTileSize]==-1:
				gp.pos_y += 4
		if keys[pygame.K_LEFT]:
			if local_wall[(gp.pos_x-4)//gp.gameTileSize+1][(gp.pos_y)//gp.gameTileSize]==-1:
				gp.pos_x -= 4
		if keys[pygame.K_RIGHT]:
			if local_wall[(gp.pos_x+4)//gp.gameTileSize+1][(gp.pos_y)//gp.gameTileSize]==-1:
				gp.pos_x += 4
		#do some wrapping magic here
		if gp.pos_x < 4: gp.pos_x = gp.gameWidth-4
		if gp.pos_x > gp.gameWidth-4: gp.pos_x = 4
		if gp.pos_y < 4: gp.pos_y = gp.gameHeight-4
		if gp.pos_y > gp.gameHeight-4: gp.pos_y = 4
		
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
				elif event.key==pygame.K_k:
					#explode
					gp.explode=gp.XYtobs(gp.pos_x//gp.gameTileSize,gp.pos_y//gp.gameTileSize)
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
		content=pickle.dumps(gp)
		s.send(content)
		#print(f'client sent to server ok:{gp}')
		if gp.quit==1:
			break
		#load world packet from server.
		r=s.recv(PACKSIZE)
		#print(f'client receives ok:{r}')
		world = pickle.loads(r)
		#print('client load ok')
		#discard own data, may need in future.
		world.players.pop(gp.player_id)

		for p in world.players.items():
			p=p[1]
			screen.fill(p.color,(p.pos_x,p.pos_y,p.size,p.size))
			pname = font.render(p.username, True, p.color)
			screen.blit(pname, (p.pos_x+5,p.pos_y-5))
		
		#record explosion from server
		for pos,exist in enumerate(world.explode):
			if exist:
				#print('something in world.explode!')
				p=gp.bstoXY(pos)
				#update the local explosions
				local_explode[p[0]][p[1]]+=1
		#draw a growing circle until the number in local list reaches 100
		#print('=================================')
		#print(local_explode)
		for k,i in enumerate(local_explode):
			for m,j in enumerate(i):
				if j >= 0 and j < 100:
					local_explode[k][m]+=5
					pygame.draw.circle(screen,(250,250,50),(k*gp.gameTileSize,m*gp.gameTileSize),j)
				else:
					local_explode[k][m]=-1
		
		#draw walls.
		for pos,exist in enumerate(world.walls):
			if exist: 
				p=gp.bstoXY(pos)
				screen.fill((255,255,255),((p[0]-0.5)*gp.gameTileSize,p[1]*gp.gameTileSize,gp.size,gp.size))
				local_wall[p[0]][p[1]]=1
				
		#then update the screen.
		pygame.display.flip()
		clock.tick(30)