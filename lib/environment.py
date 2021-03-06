from itertools import product
from helpers import *
import random

def generate(len, wid):
	env = {}
	for x,y in product(xrange(len), xrange(wid)):
		seed = random_seed()
		env[x, y] = (int(translate(noise2D(x, y, "s", sharp=50.), -1, 1, 0, 40))+random.randint(1, 10), random.randint(10, 40))
		env[x, y] = (random.randint(1, 50), random.randint(10, 40))
	return env