import pyxel  
import math
import os
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
FOC = 3
x= 0
y= 1
z= 2
prevertices = []
indices = []
def pipe(X, Y, Z, L, A):
	PIPEvert, PIPEind = stl_reader.read(str(os.path.relpath(__file__).replace("3d.py","pipe.stl")))
	length = len()
	for P in PIPEvert:
		P[A] *= L
		P[x] += X
		P[y] += Y
		P[z] += Z
	prevertices.extend(PIPEvert)
	indices.extend(PIPEind)
pipe(0,0,0,45,z)
pipe(0,100,0,45,z)
print(prevertices)
def project(pos):
	# return([(float(pos[x]*1000))/(FOC+float(pos[y]*10)),
	# 	 	(float(pos[z]*1000))/(FOC+float(pos[y]*10)),
	# 		float(pos[z])])
	return([float(pos[x])/FOC,
		 	float(pos[y])/FOC,
			float(pos[z])])
class App:
	def __init__(self):
		pyxel.init(700, 700)
		self.points = []
		self.tris = []
		self.c = 8
		pyxel.run(self.update, self.draw)
		

	def update(self):
		pass

		
	def draw(self):
		pyxel.cls(0) 
		pyxel.camera(-350,-500)
		vertices = []
		for vert in prevertices:
			rotv = rotate(vert,radians(pyxel.mouse_x))
			vertices.append([rotv[0],vert[y],vert[1]])
		self.points.clear()
		self.tris.clear()
		for vert in vertices:
			self.points.append(project(vert))
			
		# Fix: Use enumerate to get the index count safely
		for i, ind in enumerate(indices):
			self.c = 8
			self.center = (((self.points[ind[0]][x]+self.points[ind[1]][x]+self.points[ind[2]][x])/3),(self.points[ind[0]][y]+self.points[ind[1]][y]+self.points[ind[2]][y])/3)
			self.tris.append(((self.points[ind[0]][x],self.points[ind[0]][y]),
								(self.points[ind[1]][x],self.points[ind[1]][y]),
								(self.points[ind[2]][x],self.points[ind[2]][y]),
								(i % 14) + 1)) # Use 'i' instead of 'indices.index(ind)'
		for p in self.points:
			pyxel.pset(p[x],p[y],7)
		self.tris = bubble_sort(self.tris)
		for tri in self.tris:
			if triangle(tri[0],tri[1],tri[2]):
				print(tri)
				pyxel.tri(tri[0][x],tri[0][y],tri[1][x],tri[1][y],tri[2][x],tri[2][y],tri[3])
				
		

				
		

App()