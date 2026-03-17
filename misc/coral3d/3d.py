import pyxel  
import math
from math import *
import stl_reader
def sideofline(A,B,P):
	val = ((B[x] - A[x])*(P[y] - A[y]) - (B[y] - A[y])*(P[x] - A[x]))
	if val >= 0:
		return 0
	elif val <= -0:
		return 1
def triangle(P0,P1,P2):
	X = (P0[x]+P1[x]+P2[x])/3
	Y = (P0[y]+P1[y]+P2[y])/3
	if sideofline(P0,P1,[X,Y])==1:
		if sideofline(P1,P2,[X,Y])==1:
			if sideofline(P2,P0,[X,Y])==1:
				return True
	return False
def bubble_sort(array):
    n = len(array)

    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            if array[j][3] < array[j + 1][3]:
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False
        if already_sorted:
            break
    return array
def rotate(point, angle):
    ox, oy = 0,0
    px, pz, py = point
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy
FOC = 610
x= 0
y= 1
z= 2
verticesn, indicesn = stl_reader.read("cube.stl")
vertices = verticesn.tolist()
indices = indicesn.tolist()
print(vertices)
def project(pos):
	return([(float(pos[x])*FOC)/(FOC+float(pos[z])),
		 	(float(pos[y])*FOC)/(FOC+float(pos[z])),
			float(pos[z])])
	return([(float(pos[x]*1)*FOC)/(FOC+float(pos[z]*1)),
		 	(float(pos[y]+0)*FOC)/(FOC+float(pos[z]*1)),
			float(pos[z])])
class App:
	def __init__(self):
		pyxel.init(500, 500)
		self.points = []
		self.tris = []
		self.c = 8
		self.center=()
		pyxel.run(self.update, self.draw)
		

	def update(self):
		pass

		
	def draw(self):
		pyxel.cls(0)
		pyxel.camera(-250,-250)
		for vert in vertices:
			vert[x],vert[z] = rotate(vert,0.1)
		self.points.clear()
		self.tris.clear()
		for vert in vertices:
			self.points.append(project(vert))
		for ind in indices:
			self.c = 8
			self.center = (((self.points[ind[0]][x]+self.points[ind[1]][x]+self.points[ind[2]][x])/3),(self.points[ind[0]][y]+self.points[ind[1]][y]+self.points[ind[2]][y])/3)
			self.tris.append(((self.points[ind[0]][x],self.points[ind[0]][y]),
								(self.points[ind[1]][x],self.points[ind[1]][y]),
								(self.points[ind[2]][x],self.points[ind[2]][y]),
								(indices.index(ind)%14)+1))
		for p in self.points:
			pyxel.pset(p[x],p[y],7)
		self.tris = bubble_sort(self.tris)
		for tri in self.tris:
			if triangle(tri[0],tri[1],tri[2]):
				pyxel.tri(tri[0][x],tri[0][y],tri[1][x],tri[1][y],tri[2][x],tri[2][y],tri[3])
				
		

				
		

App()