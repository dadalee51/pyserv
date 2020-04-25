#gamepacket v7
import random
from bitstring import BitArray
import socket
import pickle
class GamePacket:
	explosionRange=100
	gameTileSize=4
	gameWidth=800
	gameHeight=600
	gameTileWidth=gameWidth//gameTileSize
	gameTileHeight=gameHeight//gameTileSize
	gameMode=(gameWidth,gameHeight)
	def __init__(self,id=-1):
		self.player_id=id
		self.pos_x=random.randint(0,self.gameWidth)
		self.pos_y=random.randint(0,self.gameHeight)
		self.color=(255,255,255)
		self.size=4
		self.port=0
		self.quit=0
		self.username=''
		self.drag=0
		#self.wall=BitArray()
		self.newwall=-1 # a bitarray position of the new wall, one brick at a time.
		self.explode=-1 #create a wave around self from the location of the map and remove walls.
		
	def __str__(self):
		return f'name:{self.username},port:{self.port},x:{self.pos_x},y:{self.pos_y},color:{self.color},newwall:{self.newwall},explode:{self.explode}'
	
	def __repr__(self):
		return self.__str__()
		
	def bstoXY(self,bpos):
		return (bpos%self.gameTileWidth+1, bpos//self.gameTileWidth)
	def XYtobs(self,x,y):
		return x+(y*self.gameTileWidth)
	
class WorldPacket:
	#packSize=int(GamePacket.gameTileWidth*GamePacket.gameTileHeight/3)
	packSize=4096
	def __init__(self,p,w,e):
		self.players=p
		self.wallpos=w
		self.explpos=e
		
#intro packet contains full detail to catch up with latest information.
class IntroPacket:
	packSize=12000
	def __init__(self,p,w,e):
		self.players=p
		self.walls=w
		self.explpos=e
	