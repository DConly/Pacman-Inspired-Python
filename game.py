# Name: Duncan Conly
# Description: Python pacman inspired project for Assignment 8
# Date: May 2nd, 2024

import pygame
import time
import json

from pygame.locals import* # type: ignore
from time import sleep

####################################################
########### Sprite Class ###########################
####################################################
class Sprite():
	def __init__(self, x, y, w, h, image):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.image = pygame.image.load(image)

	def update(self):
		pass

	def checkCollision(self, otherSprite) :
		if self.x >= otherSprite.x + otherSprite.w or self.x + self.w <= otherSprite.x:
			return False
		if self.y + self.h <= otherSprite.y or self.y >= otherSprite.y + otherSprite.h:
			return False
		#I am colliding with the other sprite
		return True
	
	def isWall(self) : return False
	def isPacman(self) : return False
	def isPellet(self) : return False
	def isGhost(self) : return False
	def isFruit(self) : return False
	
	def handleCollision(self) : pass
	def ghostCollided(self) : pass

	def draw(self, screen, cameraPosition): #scroll)
		pass
	
####################################################
############ Wall Class ############################
####################################################

class Wall(Sprite):
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h, "wall.png")
		
	def isWall(self) :
		return True
	
	def update(self) :
		return True
	
	def draw(self, screen, cameraPosition): #scroll)
		LOCATION = (self.x, self.y - cameraPosition)
		SIZE = (self.w, self.h)
		screen.blit(pygame.transform.scale(self.image, SIZE), LOCATION)

####################################################
########### Pacman Class ###########################
####################################################
class Pacman(Sprite):
	def __init__(self, x, y):
		super().__init__(x, y, 25, 25, "pacman1.png")
		self.px = self.x
		self.py = self.y
		self.images = []
		self.MAX_IMAGES_PER_DIRECTION = 3
		self.currentImage = 0
		self.direction = 0

		for i in range(1, 13) :
			self.images.append(pygame.image.load("pacman{}.png".format(i)))


	def update(self) :
		self.px = self.x
		self.py = self.y
		return True;

	def right(self) :
		self.x += 5
		self.direction = 2;
		self.currentImage = self.currentImage + 1
		if self.x > 500 - self.w/2 :
			self.x = 0
		
		if self.currentImage > 2 :
			self.currentImage = 0



	def left(self) :
		self.x -= 5
		self.direction = 0;
		self.currentImage = self.currentImage + 1
		if  self.x < -(self.w/2):
			self.x = 500 - self.w/2
		if self.currentImage > 2 :
			self.currentImage = 0


	def up(self) :
		self.y -= 5
		self.direction = 1;
		self.currentImage = self.currentImage + 1
		if self.currentImage > 2 :
			self.currentImage = 0


	def down(self) :
		self.y += 5
		self.direction = 3;
		self.currentImage = self.currentImage + 1
		if self.currentImage > 2 :
			self.currentImage = 0

		
	def isPacman(self) :
		return True
	
	#def getOutOfWall(self) :

	
	def handleCollision(self):
		self.x = self.px
		self.y = self.py


	def draw(self, screen, cameraPosition) :
		LOCATION = (self.x, self.y - cameraPosition)
		SIZE = (self.w, self.h)
		IMAGE_NUM = self.currentImage + self.direction * self.MAX_IMAGES_PER_DIRECTION
		screen.blit(pygame.transform.scale(self.images[IMAGE_NUM], SIZE), LOCATION)
			

####################################################
########### Fruit Class ############################
####################################################
class Fruit(Sprite) :
	def __init__(self, x, y) :
		super().__init__(x, y, 30, 30, "fruit.png")
		self.direction = 1

	def draw(self, screen, cameraPosition): #scroll)
		LOCATION = (self.x, self.y - cameraPosition)
		SIZE = (self.w, self.h)
		screen.blit(pygame.transform.scale(self.image, SIZE), LOCATION)

	def update(self) :
		self.x += self.direction*5
		if self.x < 0 :
			self.x = 500 - self.w

		elif self.x + self.w > 500 :
			self.x = 0
		return True

	def handleCollision(self) :
		self.direction *= -1
		#self.x += self.direction*3
	
	def isFruit(self) : return True
		
####################################################
########### Pellet Class ###########################
####################################################
class Pellet(Sprite) :
	def __init__(self, x, y) :
		super().__init__(x, y, 30, 30, "pellet.png")

	def draw(self, screen, cameraPosition): #scroll)
		LOCATION = (self.x, self.y - cameraPosition)
		SIZE = (self.w, self.h)
		screen.blit(pygame.transform.scale(self.image, SIZE), LOCATION)

	def update(self) :
		return True
	
	def isPellet(self) : return True


####################################################
########### Ghost Class ############################
####################################################
class Ghost(Sprite) :
	def __init__(self, x, y) :
		super().__init__(x, y, 30, 30, "ghost1.png")
		self.images = []
		self.counter = 200
		self.collided = False

		for i in range(1, 4) :
			self.images.append(pygame.image.load("ghost{}.png".format(i)))

	def ghostCollided(self) :
		self.collided = True

	def update(self) :
		if self.collided == True :
			self.counter = self.counter - 5
			if self.counter <= 0 :
				return False
			
		return True
		

	def draw(self, screen, cameraPosition): #scroll)
		LOCATION = (self.x, self.y - cameraPosition)
		SIZE = (self.w, self.h)
		if self.counter >= 200 :
			screen.blit(pygame.transform.scale(self.images[0], SIZE), LOCATION)
		elif self.counter < 200 and self.counter >= 100 :
			screen.blit(pygame.transform.scale(self.images[1], SIZE), LOCATION)
		elif self.counter < 100 and self.counter > 0 :
			screen.blit(pygame.transform.scale(self.images[2], SIZE), LOCATION)
	



	def isGhost(self) : return True

####################################################
########### Model Class ############################
####################################################
class Model():
	def __init__(self):
		self.sprites = []
		self.pacman = Pacman(250, 250)
		self.sprites.append(self.pacman)
		self.marshall()
		
		#open the json map and pull out the individual lists of sprite objects
		

	def marshall(self) :
		with open("map.json") as file:
			data = json.load(file)
			#get the list labeled lists from the map.json file
			walls = data["walls"]
			ghosts = data["ghosts"]
			pellets = data["pellets"]
			fruits = data["fruits"]
		file.close()
		
		#for each entry inside the walls list, pull the key:value pair out and create 
		#a new Lettuce object with (x,y,w,h)
		for entry in walls:
			self.sprites.append(Wall(entry["x"], entry["y"], entry["w"], entry["h"]))

		#for each entry inside the ghosts list, pull the key:value pair out and create 
		#a new Lettuce object with (x,y,w,h)
		for entry in ghosts :
			self.sprites.append(Ghost(entry["x"], entry["y"]))

		#for each entry inside the pellets list, pull the key:value pair out and create 
		#a new Lettuce object with (x,y,w,h)
		for entry in pellets:
			self.sprites.append(Pellet(entry["x"], entry["y"]))

		#for each entry inside the fruits list, pull the key:value pair out and create 
		#a new Lettuce object with (x,y,w,h)
		for entry in fruits :
			self.sprites.append(Fruit(entry["x"], entry["y"]))
	
	def update(self):
		for sprite1 in self.sprites:

			#collision detection and fixing
			for sprite2 in self.sprites:
				if sprite1 != sprite2 and sprite1.checkCollision(sprite2) :

					if sprite1.isPacman() and sprite2.isWall() :
						sprite1.handleCollision()

					if sprite1.isWall() and sprite2.isFruit() :
						
						sprite2.handleCollision()
						sprite2.update()

					if sprite1.isFruit() and sprite2.isWall() :
						sprite1.handleCollision()
						
					if sprite1.isPacman() and sprite2.isPellet() :
						self.sprites.remove(sprite2)

					if sprite1.isPacman() and sprite2.isFruit() :
						self.sprites.remove(sprite2)
					
					if sprite1.isPacman() and sprite2.isGhost() :
						sprite2.ghostCollided()


			if not(sprite1.update()) :
				self.sprites.remove(sprite1)


	def addPellet(self, pos, cameraPosition) :
		self.sprites.append(Pellet(pos[0], pos[1] + cameraPosition ))
	
	def addGhost(self, pos, cameraPosition) :
		self.sprites.append(Ghost(pos[0], pos[1] + cameraPosition))

	def addFruit(self, pos, cameraPosition) :
		self.sprites.append(Fruit(pos[0], pos[1] + cameraPosition))
		
####################################################
############ View Class ############################
####################################################

class View():
	def __init__(self, model):
		screen_size = (500,500)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model
		self.cameraPosition = 250
	
	def setCamera(self, y) :
		self.cameraPosition = y - 250

	def getCamera(self) :
		return self.cameraPosition


	def update(self):
		self.screen.fill([0,0,155])
		for sprite in self.model.sprites:

			if sprite.isPacman():
				self.setCamera(sprite.y)

			sprite.draw(self.screen, self.cameraPosition)

				
		pygame.display.flip()
		
####################################################
########### Controller Class #######################
####################################################

class Controller():
	def __init__(self, model, view):
		self.model = model
		self.view = view
		self.keep_going = True
		self.ghostMode = False
		self.pelletMode = False
		self.fruitMode = False
		self.editMode = False

	def setAllToFalse(self) :
		self.ghostMode = False
		self.pelletMode = False
		self.fruitMode = False


	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:
					self.keep_going = False
				if event.key == K_g:
					if self.editMode:
						self.setAllToFalse()
						self.ghostMode = True
				if event.key == K_f :
					if self.editMode:
						self.setAllToFalse()
						self.fruitMode = True
				if event.key == K_p :
					if self.editMode:
						self.setAllToFalse() 
						self.pelletMode = True	
				if event.key == K_e :
					self.editMode = not(self.editMode)
					if not(self.editMode) :
						self.setAllToFalse()
				if event.key == K_l :
					self.model.marshall()
			elif event.type == pygame.MOUSEBUTTONUP:

				if self.editMode :
					if self.pelletMode :
						self.model.addPellet(pygame.mouse.get_pos(), self.view.getCamera())

					if self.fruitMode :
						self.model.addFruit(pygame.mouse.get_pos(), self.view.getCamera())
				
					if self.ghostMode :
						self.model.addGhost(pygame.mouse.get_pos(), self.view.getCamera())

				pass
			elif event.type == pygame.KEYUP: #this is keyReleased!
				pass
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.pacman.left()
		if keys[K_RIGHT]:
			self.model.pacman.right()
		if keys[K_UP]:
			self.model.pacman.up()
		if keys[K_DOWN]:
			self.model.pacman.down()

pygame.init()
m = Model()
v = View(m)
c = Controller(m, v)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)