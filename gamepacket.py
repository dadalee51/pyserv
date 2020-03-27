#gamepacket v6
import random
class GamePacket:
	def __init__(self,id=-1):
		self.player_id=id
		self.pos_x=random.randint(0,800)
		self.pos_y=random.randint(0,600)
		self.color=(255,255,255)
		self.size=4
		self.port=0
		self.quit=0

	def __str__(self):
		return f'port:{self.port},x:{self.pos_x},y:{self.pos_y},color:{self.color}'
	
	def __repr__(self):
		return self.__str__()