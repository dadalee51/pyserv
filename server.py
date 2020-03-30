#server v7
import socket
import pickle
import gamepacket
import concurrent.futures
import random
from contextlib import suppress

def serve(port):
	'''
	this function is job for ThreadPoolExecutor. 
	the job is simple, just open up a socket exclusively
	for one client only.
	'''
	global players
	debug_freq=0 #print the screen every ten times over loop.
	print(f'prepareing {port}')
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, port))
		s.listen(1)
		conn, addr = s.accept()
		with conn:
			print('REConnected by', addr)
			while True:
				data = pickle.loads(conn.recv(1024))
				if data.quit == 0 : 
					players[data.player_id]= data
				else:
					players.pop(data.player_id)
				conn.send(pickle.dumps(players))
				debug_freq+=1
				debug_freq%=30
				if debug_freq==1:
					for p in players.items():
							print(p,end='')
					print('ok.')

e=concurrent.futures.ThreadPoolExecutor(max_workers=10)
HOST = '' 
PORT = 50007
running=True
players=dict()
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
			data = pickle.loads(conn.recv(1024))
			data.port=random.randint(40000,42000)
			players[data.player_id]= data
			print(data)
			e.submit(serve,data.port)
			conn.send(pickle.dumps(data))
			
		