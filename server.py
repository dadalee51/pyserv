#server v7
import socket
import pickle
import gamepacket as gp
import concurrent.futures
import random
from contextlib import suppress
from bitstring import BitArray

def monit():
	#method which only print stuff to console to aid debugging.
	global world	
	while True:
		Thread.sleep(1)
		print(world.players)

def serve(port):
	'''
	this function is job for ThreadPoolExecutor. 
	the job is simple, just open up a socket exclusively
	for one client only.
	'''
	global world #one gigantic packet
	global players
	global walls
	debug_freq=0 #print the screen every ten times over loop.
	print('prepareing {}'.format(port))
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, port))
		s.listen(1)
		conn, addr = s.accept()
		with conn:
			print('REConnected by', addr)
			while True:
				#receive and dictate if required.
				#from client we only receive its version of the world.
				data = pickle.loads(conn.recv(PACKSIZE))
				if data.quit == 0 : 
					world.players[data.player_id]= data
					if data.newwall:
						world.walls.overwrite('0b1',data.newwall)
				else:#if quit.
					world.players.pop(data.player_id)
				#print(world.walls)
				conn.send(pickle.dumps(world))
				debug_freq+=1
				debug_freq%=30
				if debug_freq==1:
					pass
					#for p in players.items():
					#		print(p,end='')
					#print('ok.')

e=concurrent.futures.ThreadPoolExecutor(max_workers=10)
HOST = '' 
PORT = 50007
running=True
players=dict()
bitwallLen=int(gp.GamePacket.gameTileWidth*gp.GamePacket.gameTileHeight)
print(f'bitwallLen:{bitwallLen}')
walls=BitArray(length=bitwallLen)
world=gp.WorldPacket(players,walls)
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
			print(data)
			e.submit(serve,data.port)
			conn.send(pickle.dumps(data))
			
		