import pygame, time
import lib.environment as environment
from lib.helpers import *
pygame.M_1 = 323
pygame.M_2 = 324
pygame.M_3 = 325

class Game:
	def __init__(self):
		pygame.init()

		self.title = "FireSim"
		self.rate = 60
		self.size = [500, 500]
		self.background = (0, 0, 0)

		self.tile_size = 5
		self.env = environment.generate(100, 100)
		self.fire_power = 10

		self.running = False
		self.frame = 0
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(self.size)
		self.font = pygame.font.Font('freesansbold.ttf', 12)

		pygame.display.set_caption(self.title)

	def fire_spread(self):
		new = {}
		for tile in self.env:
			if not self.env[tile][0]:              #if tile == 0
				
				tile_inf = self.env[tile]
				fuel = tile_inf[1]

				fuel -= 1
				if fuel <= 0:
					new[tile] = ("D", 0)
				else:
					new[tile] = (tile_inf[0], fuel)

				pts = [(tile[0], tile[1]+1),
					   (tile[0], tile[1]-1),
					   (tile[0]+1, tile[1]),
					   (tile[0]-1, tile[1])
					  ]
				for pt in pts:
					try:
						val_all = self.env[pt]
						val = val_all[0]
						if val == 0:
							pass
						elif val and val != "W" and val != "D":
							new_val = val - self.fire_power
							if new_val < 0:
								new_val = 0
							new[pt] = (new_val, val_all[1])
					except KeyError: pass
		self.env = merge_dicts(self.env, new)

	def movement(self):
		keys = control_check()
		mouse = pygame.mouse.get_pos()

		mouse_x = mouse[0]/self.tile_size
		mouse_y = mouse[1]/self.tile_size

		mat = 500

		if keys[pygame.M_1]:
			pts = [
				(mouse_x, mouse_y),
				(mouse_x+1, mouse_y),
				(mouse_x+1, mouse_y+1),
				(mouse_x, mouse_y+1)
			]
			for pt in pts:
				try:
					if self.env[pt][0] == 0:
						self.env[pt] = ("D", 0)
					else:
						self.env[pt] = (mat, 0)
				except KeyError: pass

		if keys[pygame.M_3]:
			self.env[mouse_x, mouse_y] = (0, 0)

		if keys[pygame.K_q]:
			self.tile_size -= 1
			if self.tile_size <= 0:
				self.tile_size = 1
		if keys[pygame.K_w]:
			self.tile_size += 1

	def draw(self):
		self.screen.fill(self.background)

		for tile in self.env:
			val = self.env[tile][0]
			if val == "W":
				color = (0, 0, 255)
			elif val == "D":
				color = (40, 40, 40)
			elif val:
				res = translate(val, 1, 50, 0, 180)
				if res > 255:
					color = (255, 0, 255)
				else:
					color = (0, res, 0)
			else:
				color = (200, 0, 0)
			pygame.draw.rect(self.screen, color, [tile[0]*self.tile_size, tile[1]*self.tile_size] + [self.tile_size]*2)

		words = "%iFPS" % (self.fps)
		text = self.font.render(words, True, (255, 255, 255))
		self.screen.blit(text, (10, 10))

	def start(self):
		self.running = True
		self.fps = 0
		fps_time_counter = time.time()
		fps_counter = 0

#		self.env[40, 40] = (0, 10)

		while self.running:
			fps_counter += 1
			if time.time()-fps_time_counter >= 0.5:
				fps_time_counter = time.time()
				self.fps = fps_counter*2
				fps_counter = 0

			self.frame += 1
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			self.movement()
			self.draw()
			self.fire_spread()

			pygame.display.update()
			self.clock.tick(self.rate)

game = Game()
game.start()