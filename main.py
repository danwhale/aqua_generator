from generator import *

g = Generator(100,2,0.05)
for i in range(100):
	g.step()
	print(len(g.G.edges))