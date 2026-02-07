## Pastes Lexis surface diagrams and HAPC plots together
from random import randint as rnd
import os
import glob
from subprocess import call
from PIL import Image, ImageDraw, ImageFont
from os import listdir
from os.path import isfile, join
from math import dist

crabs = ["crab/normal1.png","crab/normal2.png","crab/freak.png"]
crabs = []
crabsPATH = listdir("crab")
for C in crabsPATH:
    pcrab = str(os.path.relpath(__file__).replace("gererator.py",C))
    if "png" in pcrab:
        crabs.append(pcrab)
for count in range(20):
    canvas = Image.new("RGBA", (2048, 2048), color = (233, 234, 228,255))
    I = 10
    poss = []

    while I > 0:
            I -= 1
            crab = Image.open(crabs[rnd(0,len(crabs)-1)]).convert("RGBA")
            new_w = rnd(300,600)
            new_h = int(crab.height * (new_w / crab.width))
            crab = crab.resize((new_w, new_h), Image.BICUBIC)
            crab = crab.rotate(rnd(0,360),fillcolor=(0,0,0,0))
            pos = [rnd(100,1948),rnd(100,1948)]    
            fakepos = pos
            fakepos[1] -= int(crab.height/2)
            fakepos[0] -= int(crab.width/2)
            pos = tuple(pos)
            shouldpaste = True
            for P in poss:
                if dist(pos,P) < 400:
                    shouldpaste = False
                    break
            if shouldpaste:
                poss.append(pos)
                canvas.paste(crab,fakepos,crab)
            else:
                I+=1

            print(I)
    canvas.save(os.path.abspath(__file__).replace("gererator.py","out\\"+str(hex(rnd(0,100)))+".png"))
    #canvas.show()
    