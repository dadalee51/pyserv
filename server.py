#server v7
import socket
import pickle
import gamepacket as gp
import concurrent.futures
import random
from contextlib import suppress
from bitstring import BitArray
from time import sleep,time

def monit():
	#method which only print stuff to console to aid debugging.
	global world
	print('monit started')
	while True:
		print(world.players)
		sleep(1)

def serve(port):
	'''
	this function is job for ThreadPoolExecutor. 
	the job is simple, just open up a socket exclusively
	for one client only.
	'''
	global world #one gigantic packet
	global players
	global walls
	global explode
	global explpos
	
	debug_freq=0 #print the screen every ten times over loop.
	print('prepareing {}'.format(port))
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, port))
		s.listen(1)
		conn, addr = s.accept()
		with conn:
			print('REConnected by', addr)
			while True:
				#update world based on history
				for exp in explpos:
					#convert the exp to xy position, anywalls
					#within the radius will be removed.
					if exp[1]<time()-1:
						world.explode.overwrite('0b0',exp[0])
				#if explpos is outdated, remove it.
				explpos={e for e in explpos if e[1]<time()-1}
				#read updates from client.
				data = pickle.loads(conn.recv(PACKSIZE))
				if data.quit == 0 : 
					world.players[data.player_id]= data
					if data.newwall>-1:
						world.walls.overwrite('0b1',data.newwall)
					if data.explode>-1:
						#record the explosion centre,
						#pass the explosion to other clients
						#which they keep track of the state 
						#themselves.
						world.explode.overwrite('0b1',data.explode)
						explpos.add((data.explode,time()))
				else:#if quit.
					world.players.pop(data.player_id)
				conn.send(pickle.dumps(world))
				
e=concurrent.futures.ThreadPoolExecutor(max_workers=10)
HOST = '' 
PORT = 50007
running=True
players=dict()
bitwallLen=int(gp.GamePacket.gameTileWidth*gp.GamePacket.gameTileHeight)
print(f'bitwallLen:{bitwallLen}')
walls=BitArray(length=bitwallLen)
explode=BitArray(length=bitwallLen)
#explosion lists are only kept by server.
explpos=set()
world=gp.WorldPacket(players,walls,explode)
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
			
		