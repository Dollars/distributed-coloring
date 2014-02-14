import random
import math

class Node:
	id = -1
	random.seed(0)

	@staticmethod
	def giveID():
		Node.id += 1
		return Node.id

	@staticmethod
	def getID(n):
		return n.id

	@staticmethod
	def getPower():
		p = random.randint(1, 10000)
		random.seed(p)
		return p

	def __init__(self, *nodes):
		self.id = Node.giveID()
		self.neighbors = []
		self.k = 1
		self.color = 1
		self.theta = random.random()
		self.msgStack = {}
		self.relevance = 0
		self.convergence = 0.75 #why not a value greater than 1
		self.rho = 1.1
		self.power = 0
		self.add(*nodes)

	def colorMark(self):
		sameColor = 0
		colorIndice = self.color
		for n in self.neighbors:
			colorIndice += n.color*2
			if self.color == n.color:
				sameColor += 1
		return (colorIndice + (sameColor*100))

	def hasValidColor(self):
		for n in self.neighbors:
			if self.color == n.color :
				return False
		return True

	def add(self, *nodes):
		if len(nodes) > 0:
			for n in list(nodes):
				if not n in self.neighbors:
					self.neighbors.append(n)
					n.add(self)
			
	def delete(self, n):
		if n in self.neighbors:
			self.neighbors.remove(n)
			if n.id in self.msgStack:
				del self.msgStack.pop[n.id]

	def getNeighbors(self):
		nodes = []
		for n in self.neighbors:
			nodes.append(n.id)
		return nodes

	def __hash__(self):
		return self.id

	def __eq__(self, other):
		if isinstance(other, Node):
			return self.id == other.id
		if isinstance(other, int):
			return self.id == other

	def __ne__(self, other):
		if isinstance(other, Node):
			return self.theta != other.theta
		if isinstance(other, float):
			return self.theta != other
	
	def __lt__(self, other):
		if isinstance(other, Node):
			return self.theta < other.theta
		if isinstance(other, float):
			return self.theta < other
		
	def __le__(self, other):
		if isinstance(other, Node):
			return self.theta <= other.theta
		if isinstance(other, float):
			return self.theta <= other
		
	def __gt__(self, other):
		if isinstance(other, Node):
			return self.theta > other.theta
		if isinstance(other, float):
			return self.theta > other
	
	def __ge__(self, other):
		if isinstance(other, Node):
			return self.theta >= other.theta
		if isinstance(other, float):
			return self.theta >= other
	
	def __cmp__(self, other):
		if isinstance(other, Node):
			return self.theta - other.theta
		if isinstance(other, float):
			return self.theta - other

	def __contains__(self, n):
		return self.neighbors.contains(n)

	def __str__ (self):
		colorscheme = "paired12"
		colorByindex = self.color

		if self.color > 12:
			colorscheme = "set312"
			colorByindex = self.color - 12

		strn = "{0} [label=\"{0}\", style=filled, color=black, fillcolor=\"/{1}/{2}\"];\n".format(self.id, colorscheme, colorByindex)
		for n in self.neighbors:
			strn += "{0} -- {1};\n".format(self.id, n.id)
		return strn

	def __format__ (self, labels):
		colorscheme = "paired12"
		colorByindex = self.color
		listLabel = labels.lstrip("['").rstrip("']").split("', '")

		if self.color > 12:
			colorscheme = "set312"
			colorByindex = self.color - 12

#       strn = "{0} [label=\"{{{0}}}\", style=filled, color=black, fillcolor=\"/{1}/{2}\"];\n".format(self.id, colorscheme, colorByindex)
		strn = "{0} [label=\"\", style=filled, color=black, fillcolor=\"/{1}/{2}\"];\n".format(self.id, colorscheme, colorByindex)
		for n in self.neighbors:
			strn += "{0} -- {1};\n".format(self.id, n.id)
		return strn.format(*listLabel)

	def rcvStartMsg(self, k):
		self.k = k
		self.convergence *= (1.0-(1.0/math.log1p(len(self.neighbors)+2)))
		self.relevance = 1.0
		self.rho = 1.0+(2.0/(k))

	def receiveMsg(self, sendID, m): 
		if sendID in self.msgStack:
			self.msgStack[sendID].update(m)
		else:
			self.msgStack[sendID] = m

	def sendMsg(self, m):
		for n in self.neighbors:
			n.receiveMsg(self.id, m)

	def keepHigherPower(self):
		hp = self.power
		for m in list(self.msgStack.keys()):
			if self.power > self.msgStack[m]['power']:
				del self.msgStack[m]
			else:
				if hp < self.msgStack[m]['power']:
					hp = self.msgStack[m]['power']
		self.power = hp

	def occurEvent(self, r):
		msg = {}
		if r < self.k:
			if len(self.msgStack) > 0:
				self.newTheta()
				self.minColor()
				self.setRelevance()
			else:
				self.relevance = 1
			self.convergence /= self.rho 
			msg = dict(theta=self.theta, color=self.color, relevance=self.relevance)
		else:
			if r == self.k:
				if self.color == 1:
					self.power = Node.getPower()
			elif len(self.msgStack) > 0:
				self.keepHigherPower()
				self.minColor()
			msg = dict(power=self.power, color=self.color)
		self.sendMsg(msg)
		self.msgStack.clear()

	def inc(self, mtheta):
		x = float(mtheta-self.theta)
		if x >= 0.0:
			return (x-0.5)
		else:
			return (x+0.5)

	def setRelevance(self):
		self.relevance = 1/(len(self.msgStack.keys())**2)

	def newTheta(self):
		tmp = 0.0
		for m in self.msgStack:
			mtheta = self.msgStack[m]['theta']
			mrelevance = self.msgStack[m]['relevance']
			tmp += mrelevance*self.inc(mtheta) 
		self.theta += self.convergence*tmp
		#self.theta = (math.ceil(self.theta*10000)/10000)
		if self.theta < 0.0 or self.theta >= 1.0:
			if self.theta < 0.0:
			 	self.theta = math.fabs(self.theta)
			if self.theta >= 1.0:
			 	self.theta = 0.0
			#self.theta = 0.0
			# while self.theta < 0.0:
			#  	self.theta += 0.5
			# while self.theta >= 1.0:
			#  	self.theta -= 0.5

	def minColor(self):
		self.color = 1
		colors = set()
		for m in self.msgStack:
			colors.add(self.msgStack[m]['color'])
		colors = list(colors)
		colors.sort()
		for c in colors:
			if self.color == c:
				self.color += 1
			else:
				break
