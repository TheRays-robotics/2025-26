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
def triangle(P0,P1,P2,z):
	X = (P0[x]+P1[x]+P2[x])/3
	Y = (P0[y]+P1[y]+P2[y])/3
	if sideofline(P0,P1,[X,Y])==1:
		if sideofline(P1,P2,[X,Y])==1:
			if sideofline(P2,P0,[X,Y])==1:
				return True
	return False
def qsort(inlist):
    if inlist == []: 
        return []
    else:
        pivot = inlist[0]
        # Compare based on the 3rd element (index 2)
        lesser = qsort([x for x in inlist[1:] if x[4] > pivot[4]])
        greater = qsort([x for x in inlist[1:] if x[4] <= pivot[4]])
        return lesser + [pivot] + greater


def rotate(point, angle):
	px, pz, py = point
	qx = px * math.cos(angle) - py * math.sin(angle)
	qy = px * math.sin(angle) + py * math.cos(angle)
	return qx, pz, qy



def rotate_z(point, angle):
	pz, px, py = point
	qx = px * math.cos(angle) - py * math.sin(angle)
	qy = px * math.sin(angle) + py * math.cos(angle)
	return pz,qx, qy

x= 0
y= 1
z= 2
prevertices = []
indices = []
length = 0

def pipe(X, Y, Z, L, A):
	global modelcount
	
	print("pipe"+str(A)+".stl")
	PIPEvert, PIPEind = stl_reader.read(str(os.path.relpath(__file__).replace("balls.py","pipe"+str(A)+".stl")))
	length =+ len(PIPEvert)
	for P in PIPEvert:
		P[A] *= L
		P[x] += X*10
		P[y] += Y*10
		P[z] += Z*10
	prevertices.extend(PIPEvert)
	PIPEind = PIPEind.tolist()
	for I in PIPEind:
		I[0]+=(len(prevertices)-length)
		I[1]+=(len(prevertices)-length)
		I[2]+=(len(prevertices)-length)
		I.append(modelcount)
	modelcount+=1
	indices.extend(PIPEind)
def ball(X, Y, Z):
	global modelcount
	PIPEvert, PIPEind = stl_reader.read(str(os.path.relpath(__file__).replace("balls.py","ball.stl")))
	PIPEind = PIPEind.tolist()
	length =+ len(PIPEvert)
	for P in PIPEvert:
		P[x] += X*10
		P[y] += Y*10
		P[z] += Z*10
	prevertices.extend(PIPEvert)
	for I in PIPEind:
		I[0]+=(len(prevertices)-length)
		I[1]+=(len(prevertices)-length)
		I[2]+=(len(prevertices)-length)
		I.append(modelcount)
	modelcount+=1
	indices.extend(PIPEind)
modelcount = 0



L1 = 40
L2 = 20
L3 = 15

L3S = L3+10
# pipe(-15,0,0,45,z)
# pipe(-15,12.5,22.5,25,y)
# pipe(-15,7.5,-22.5,15,y)
# pipe(-15,12.5,22.5+L1,25,y)
# pipe(-15,0,L1/2+22.5,L1,z)
# pipe(-15,25,L1/2+22.5,L1,z)
# pipe(-15,15,-L2/2-22.5,L2,z)
# pipe(-15,0,-L2/2-22.5,L2,z)
# pipe(-15,7.5,-22.5-L2,15,y)
# pipe(-15,25+L3/2,22.5,L3,y)
# pipe(-15,15+L3S/2,-22.5,L3S,y)
# pipe(-15,L3+25,0,45,z)

# pipe(15,0,0,45,z)
# pipe(15,12.5,22.5,25,y)
# pipe(15,7.5,-22.5,15,y)
# pipe(15,12.5,22.5+L1,25,y)
# pipe(15,0,L1/2+22.5,L1,z)
# pipe(15,25,L1/2+22.5,L1,z)
# pipe(15,15,-L2/2-22.5,L2,z)
# pipe(15,0,-L2/2-22.5,L2,z)
# pipe(15,7.5,-22.5-L2,15,y)
# pipe(15,25+L3/2,22.5,L3,y)
# pipe(15,15+L3S/2,-22.5,L3S,y)
# pipe(15,L3+25,0,45,z)

ball(-15,0,22.5)
ball(-15,0,-22.5)
ball(-15,0,L1+22.5)
ball(-15,25,22.5)
ball(-15,25,L1+22.5)
ball(-15,0,-L2-22.5)
ball(-15,15,-L2-22.5)
ball(-15,15,-22.5)
ball(-15,L3+25,-22.5)
ball(-15,L3+25,22.5)

ball(15,0,22.5)
ball(15,0,-22.5)
ball(15,0,L1+22.5)
ball(15,25,22.5)
ball(15,25,L1+22.5)
ball(15,0,-L2-22.5)
ball(15,15,-L2-22.5)
ball(15,15,-22.5)
ball(15,L3+25,-22.5)
ball(15,L3+25,22.5)




def project(pos,slop):
	FOC = 1000
	return([(float(pos[x])*FOC)/(FOC+float(pos[z]))*slop,
		 	(float((pos[y]*-1)+300)*FOC)/(FOC+float(pos[z]))*slop,
			float(pos[z])])
class App:
	def __init__(self):
		pyxel.init(600, 600)
		self.points = []
		self.tris = []
		self.c = 0
		self.FOC = 0.3
		pyxel.run(self.update, self.draw)
		

	def update(self):
		pass

		
	def draw(self):
		pyxel.cls(0) 
		print(self.FOC)
		self.FOC += pyxel.mouse_wheel/100
		pyxel.camera(-300,-300)
		vertices = []
		
		for vert in prevertices:
			rotv = rotate(vert,radians(self.c))
			#rotv2 = rotate_z(rotv,radians(pyxel.mouse_y))
			rotv2 = rotv 
			vertices.append(rotv2)
			#vertices.append([rotv[0],vert[1],vert[z]])
		self.points.clear()
		self.tris.clear()
		for vert in vertices:
			self.points.append(project(vert,self.FOC))
		self.c += 5
		
		# Fix: Use enumerate to get the index count safely
		for i, ind in enumerate(indices):
			self.center = (((self.points[ind[0]][x]+self.points[ind[1]][x]+self.points[ind[2]][x])/3),(self.points[ind[0]][y]+self.points[ind[1]][y]+self.points[ind[2]][y])/3)
			self.tris.append(((self.points[ind[0]][x],self.points[ind[0]][y]),
								(self.points[ind[1]][x],self.points[ind[1]][y]),
								(self.points[ind[2]][x],self.points[ind[2]][y]),
								ind[3],
								int(self.points[ind[2]][z]))) 

		self.tris = qsort(self.tris)
		for tri in self.tris:
			if triangle(tri[0],tri[1],tri[2],tri[4]):
				pyxel.tri(tri[0][x],tri[0][y],tri[1][x],tri[1][y],tri[2][x],tri[2][y],(tri[3]%15)+1)
		
		

				
		

App()