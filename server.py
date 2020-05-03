#server v7
import socket
import sys
import pickle
import gamepacket as gp
import concurrent.futures
import random
import math
from contextlib import suppress
from bitstring import BitArray
from time import sleep,time

def point_circle_collide(px, py, cx, cy, r):
	dx=px-cx
	dy=py-cy
	distance=math.sqrt((dx*dx)+(dy*dy))
	if distance<r:
		return True
	else:
		return False

def monit():
	#method which only print stuff to console to aid debugging.
	global world
	global PORT
	print('monit started:PORT',PORT)
	while True:
		print('players:',world.players)
		#print('wallpos:',world.wallpos)
		sleep(2)

def serve(port):
	'''
	this function is job for ThreadPoolExecutor. 
	the job is simple, just open up a socket exclusively
	for one client only.
	'''
	global world 
	global players
	global wallpos
	global explpos
	
	global intro 
	global walls
	ggp=gp.GamePacket()
	
	debug_freq=0 #print the screen every ten times over loop.
	print('prepareing {}'.format(port))
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, port))
		s.listen(1)
		conn, addr = s.accept()
		with conn:
			print('REConnected by', addr)
			#send intro packet
			#TODO: intro packet.
			#then in main loop
			while True:
				#update explpos since it is intrim.
				world.explpos={e for e in world.explpos if e[1]>=time()-0.05}
				#problem: we need to keep a wall in world, and a wall timed for sending!
				#world.wallpos={e for e in world.wallpos if e[1]>=time()-0.55}
				#read updates from client.
				data = pickle.loads(conn.recv(PACKSIZE))
				if data.quit == 0: 
					world.players[data.player_id]= data
					if data.newwall>-1:
						intro.walls.overwrite('0b1',data.newwall)
						world.wallpos.add((data.newwall,time(),1)) #added wall
					if data.explode>-1:
						world.explpos.add((data.explode,time()))
						#send a negative wall to client.
						rst=set()
						for wp in world.wallpos:
							x,y=ggp.bstoXY(wp[0])
							cx,cy=ggp.bstoXY(data.explode)
							if point_circle_collide(x,y,cx,cy,ggp.explosionRange/4):
								print('collided at',wp,'clearing to neg 1')
								rst.add((wp[0],wp[1],-1))
							else:
								rst.add((wp[0],wp[1],1))
						world.wallpos=rst
				else:#if quit.
					world.players.pop(data.player_id)
				conn.send(pickle.dumps(world))
				
				
#main program starts here.
e=concurrent.futures.ThreadPoolExecutor(max_workers=10)
HOST = '0.0.0.0' #for heroku?
PORT = 80
if len(sys.argv)>1 and sys.argv[1] != '':
  PORT=int(sys.argv[1])
running=True
players=dict()
bitwallLen=int(gp.GamePacket.gameTileWidth*gp.GamePacket.gameTileHeight)
print(f'bitwallLen:{bitwallLen}')
walls=BitArray(length=bitwallLen)
wallpos=set()
#explosion set are only kept by server.
explpos=set()
intro=gp.IntroPacket(players,walls,explpos)
world=gp.WorldPacket(players,wallpos,explpos)
PACKSIZE=gp.WorldPacket.packSize
#setup monitor work
e.submit(monit)
while running:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen(1)	
		print('accepting connections...')
		conn, addr = s.accept()
		#non-blocking, instantly free up so other clients can connect almost without waiting:
		s.settimeout(0)
		#s.setblocking(0)
		with conn:
			print('Connected by', addr)
			data = pickle.loads(conn.recv(PACKSIZE))
			data.port=random.randint(40000,42000)
			players[data.player_id]= data
			print(data.username+' connected.')
			e.submit(serve,data.port)
			conn.send(pickle.dumps(data))
			
		