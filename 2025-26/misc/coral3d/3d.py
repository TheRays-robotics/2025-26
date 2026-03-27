import cv2 
import os
import numpy as np
from math import *

measure = True
if measure:
	# Initialize globals
	clicks = []
	box_w = 1  # Using box_w to avoid conflict with image width

	def detect_yellow_color(image):
		# 1. Convert to HSV
		hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		h, s, v = cv2.split(hsv_image)
		hue_shift = 25  # <--- CHANGED FROM 0 TO 40
		h = (h.astype(int) + hue_shift) % 180
		hsv_image = cv2.merge([h.astype(np.uint8), s, v])
		# 2. Define yellow range for detection ON THE ORIGINAL COLORS
		yellow_lower = np.array([20, 100, 100]) 
		yellow_upper = np.array([30, 255, 255])
		mask = cv2.inRange(hsv_image, yellow_lower, yellow_upper)

		# 3. APPLY HUE SHIFT to the whole image for visual effect
	
		
		# 4. Convert the SHIFTED image back to BGR for display
		output_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

		# 5. Draw boxes on the shifted image using the original mask
		contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		global box_w
		for contour in contours:
			if cv2.contourArea(contour) > 0:
				x, y, w, h_box = cv2.boundingRect(contour)
				box_w = w
				cv2.rectangle(output_image, (x, y), (x + w, y + h_box), (0, 255, 0), 2)
				break 

		return output_image


	def click_event(event, x, y, flags, params):
		global img, box_w
		global clicks
		if event == cv2.EVENT_LBUTTONDOWN:
			clicks.append((x, y))
			
			# Draw a point where clicked
			cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
			
			if len(clicks) >= 2 and len(clicks) % 2 == 0:
				p1 = clicks[-2]
				p2 = clicks[-1]
				
				# Calculate distance using box_w as a scale (e.g., 10cm wide)
				pixel_dist = dist(p1, p2)
				real_dist = round(pixel_dist / (box_w / 10), 2)
				
				cv2.line(img, p1, p2, (255, 0, 0), 2)
				cv2.putText(img, f"{real_dist} cm", p2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
				
			cv2.imshow('image', img)

	# 1. Path Fix: Ensure the file exists
	script_dir = os.path.dirname(__file__)
	file_path = os.path.join(script_dir, "fire.png")

	if not os.path.exists(file_path):
		print(f"Error: Could not find {file_path}")
	else:
		img_raw = cv2.imread(file_path)
		img = detect_yellow_color(img_raw)
		
		cv2.imshow('image', img)
		cv2.setMouseCallback('image', click_event)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	cable = []
	if len(clicks) >= 2 and len(clicks) % 2 == 0:
		for p in range(int(len(clicks)/2)):
				p1 = clicks[p*2]
				p2 = clicks[p*2+1]
				
				# Calculate distance using box_w as a scale (e.g., 10cm wide)
				pixel_dist = dist(p1, p2)
				real_dist = round(pixel_dist / (box_w / 10), 2)
				print(real_dist)
				cable.append(real_dist)
L1 = 40
L2 = 20
L3 = 15
if measure:
	L1 = cable[0]
	L2 = cable[1]
	L3 = cable[2]


import pyxel  
import stl_reader
import PyxelUniversalFont as puf
writer = puf.Writer("mononoki-Regular.ttf")
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
	qx = px * cos(angle) - py * sin(angle)
	qy = px * sin(angle) + py * cos(angle)
	return qx, pz, qy



def rotate_z(point, angle):
	pz, px, py = point
	qx = px * cos(angle) - py * sin(angle)
	qy = px * sin(angle) + py * cos(angle)
	return pz,qx, qy

x= 0
y= 1
z= 2
prevertices = []
indices = []
length = 0

def pipe(X, Y, Z, L, A):
	global modelcount
	
	PIPEvert, PIPEind = stl_reader.read(str(os.path.relpath(__file__).replace("3d.py","pipe"+str(A)+".stl")))
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
		I.append(A)
	modelcount+=1
	indices.extend(PIPEind)
def square(X, Y, Z):
	global modelcount
	
	PIPEvert, PIPEind = stl_reader.read(str(os.path.relpath(__file__).replace("3d.py","square.stl")))
	length =+ len(PIPEvert)
	for P in PIPEvert:
		P[x] += X*10
		P[y] += Y*10
		P[z] += Z*10
	prevertices.extend(PIPEvert)
	PIPEind = PIPEind.tolist()
	for I in PIPEind:
		I[0]+=(len(prevertices)-length)
		I[1]+=(len(prevertices)-length)
		I[2]+=(len(prevertices)-length)
		I.append(5)
	modelcount+=1
	indices.extend(PIPEind)
def ball(X, Y, Z):
	global modelcount
	PIPEvert, PIPEind = stl_reader.read(str(os.path.relpath(__file__).replace("3d.py","ball.stl")))
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





L3S = L3+10
pipe(-15,0,0,45,z)
pipe(-15,12.5,22.5,25,y)
pipe(-15,7.5,-22.5,15,y)
pipe(-15,12.5,22.5+L1,25,y)
pipe(-15,0,L1/2+22.5,L1,z)
pipe(-15,25,L1/2+22.5,L1,z)
pipe(-15,15,-L2/2-22.5,L2,z)
pipe(-15,0,-L2/2-22.5,L2,z)
pipe(-15,7.5,-22.5-L2,15,y)
pipe(-15,25+L3/2,22.5,L3,y)
pipe(-15,15+L3S/2,-22.5,L3S,y)
pipe(-15,L3+25,0,45,z)

pipe(15,0,0,45,z)
pipe(15,12.5,22.5,25,y)
pipe(15,7.5,-22.5,15,y)
pipe(15,12.5,22.5+L1,25,y)
pipe(15,0,L1/2+22.5,L1,z)
pipe(15,25,L1/2+22.5,L1,z)
pipe(15,15,-L2/2-22.5,L2,z)
pipe(15,0,-L2/2-22.5,L2,z)
pipe(15,7.5,-22.5-L2,15,y)
pipe(15,25+L3/2,22.5,L3,y)
pipe(15,15+L3S/2,-22.5,L3S,y)
pipe(15,L3+25,0,45,z)

pipe(0,L3+25,0,30,x)
pipe(0,25,22.5+L1,30,x)
pipe(0,0,22.5+L1,30,x)
pipe(0,15,-22.5-L2,30,x)
pipe(0,0,-22.5-L2,30,x)

square(16.5,5,0)
square(16.5,10,-22.5-L2+5)
square(16.5,20,+22.5+L1-5)
square(16.5,L3+20,-22.5+5)

square(-16.5,5,0)
square(-16.5,10,-22.5-L2+5)
square(-16.5,20,+22.5+L1-5)
square(-16.5,L3+20,22.5-5)



def project(pos,slop):
	FOC = 2000
	return([(float(pos[x])*FOC)/(FOC+float(pos[z]))*slop,
		 	(float((pos[y]*-1)+300)*FOC)/(FOC+float(pos[z]))*slop,
			float(pos[z])])
class App:
	def __init__(self):
		pyxel.init(600, 600)
		self.points = []
		self.tris = []
		self.c = 8
		self.FOC = 0.1
		pyxel.colors.from_list([0x000000,0x88ffff,0xff88ff,0xffff88,0xffffff,0xff0000])
		pyxel.run(self.update, self.draw)
		

	def update(self):
		pass

		
	def draw(self):
		pyxel.cls(0) 
		self.FOC += pyxel.mouse_wheel/100
		pyxel.camera(-300,-300)
		vertices = []
		for vert in prevertices:
			rotv = rotate(vert,radians(pyxel.mouse_x))
			rotv2 = rotate_z(rotv,radians(pyxel.mouse_y))
			#rotv2 = rotv 
			vertices.append(rotv2)
		self.points.clear()
		self.tris.clear()
		for vert in vertices:
			self.points.append(project(vert,self.FOC))
		
		# Fix: Use enumerate to get the index count safely
		for i, ind in enumerate(indices):
			self.c = 8
			self.center = (((self.points[ind[0]][x]+self.points[ind[1]][x]+self.points[ind[2]][x])/3),(self.points[ind[0]][y]+self.points[ind[1]][y]+self.points[ind[2]][y])/3)
			self.tris.append(((self.points[ind[0]][x],self.points[ind[0]][y]),
								(self.points[ind[1]][x],self.points[ind[1]][y]),
								(self.points[ind[2]][x],self.points[ind[2]][y]),
								ind[3],
								int(self.points[ind[2]][z]))) 
		writer.draw(-300, -300, "length : "+str(round(L1+L2+45,2))+"cm", 30, 4)
		writer.draw(-300, -250, "height : "+str(round(L3+25,2))+"cm", 30, 4)
		self.tris = qsort(self.tris)
		for tri in self.tris:
			if triangle(tri[0],tri[1],tri[2],tri[4]):
				pyxel.tri(tri[0][x],tri[0][y],tri[1][x],tri[1][y],tri[2][x],tri[2][y],(tri[3]%15)+1)
		
		

				
		

App()