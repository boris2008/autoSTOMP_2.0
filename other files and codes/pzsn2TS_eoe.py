# -*- coding: utf-8 -*-
"""
this is a part of workflow for multiple section 
and multiple ROI per section project
EOE--Eosinophilic esophagitis
@author: BOCHENG YIN 02-28-2020
"""

"""the important variables
========================================================"""
import math
import os
import re
import copy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.path as mpltPath
import numpy as np
from scipy.spatial import ConvexHull
from statistics import mean 
f = open("C:/ZEN/pwd_mROIs.txt")
dire = "C:/ZEN/"#fixed directory to store the position files for ZEN BLACK
parentdir=f.readline()
parentdir = parentdir.replace('\n','')
path = f.readline()#contains the .pos file
path = path.replace('\n','')

f.close()
print(parentdir)
print(path)

"""
#here the coordinates are in unit pixels
#here 25x objective lens used, 1024x1024 image format is used
"""
positionFileStyle = 1
tileSize=340.1
tileDilate=1

pos_pos=[]#position files created from the "Positions" panel


for r, d, f in os.walk(path):
    for file in f:
        s=re.match('t\d+_relative.pos', file)
        if s:
            #files.append(os.path.join(r, file))
            pos_pos.append(file)

print ("there are ",len(pos_pos)," sections")




def readCoordinates(posFileName):
    
    """
    RelativePositions = 0 for absolute position file
    RelativePositions = 1 for relative position file
    """
    
    
    """====================================================="""
    """start to read the position file"""
    text_file = open(posFileName,"r")
    lines = text_file.readlines()
    #print(len(lines))
    #print(lines)
    x=[]
    y=[]
    z=[]
    """here I assume the z is the same everywhere"""

    for line in lines:
        if '\t\tX' in line:
            s=re.findall('-?\d*\.?\d+', line)
            x.append(float(s[0]))
        elif '\t\tY' in line:
            s=re.findall('-?\d*\.?\d+', line)
            y.append(float(s[0]))
        elif '\t\tZ' in line:
            s=re.findall('-?\d*\.?\d+', line)
            z.append(float(s[0]))
        else:
            continue
    text_file.close()
    xyz= list(zip(x,y,z))
    return xyz #return the a list of points [x,y,z]
 #the end of the function readCoordinates(posFileName):    
#x, y, z = readCoordinates(stageCo)


"""start to calculate the vertices of the box centered at the boundary point"""

def tuple2list(x):
    lst=[]
    for i in x:
        lst.append(float(i))
    return lst



def drawVertices(centralpoint,tilesize):
    """central point =[x,y,z]
    """
    xs,ys,zs = centralpoint
    #xs=tuple2list(xs)
    #ys=tuple2list(ys)
    #zs=tuple2list(zs)
    minx = xs-0.5*tilesize
    maxx = xs+0.5*tilesize
    miny = ys-0.5*tilesize
    maxy = ys+0.5*tilesize
    xr = (minx, minx,maxx,maxx,minx)
    yr = (miny,maxy,maxy,miny,miny)
    zr = (zs,zs,zs,zs)
    vertice =[]
    for i in range(4):
        vertice.append([xr[i],yr[i],zr[i]])
    #plt.figure()
    #plt.plot(xr,yr,dashes=[2, 2],color='#f92874')
    #plt.show()
    return (vertice) #return as a list of 4 coordinates [x,y,z]
#t = drawTile([1,2],3)
#y1=y[1]


     

"""start to write the position file"""
"""+++create x,y,z lists for tiles+++++"""
def writePosF(xyz,parentDir,fileName,llen):
    xt,yt,zt =zip(*xyz)
    
    write_file = open(''.join([parentDir,fileName]),"w",encoding="utf-8")
    write_file.write('Carl Zeiss LSM 510 - Position list file - Version = 1.000\n')
    write_file.write('BEGIN PositionList Version = 10001\n')
    
    write_file.write('\tBEGIN  10001\n')
    write_file.write(''.join(['\t\tRelativePositions = ',str(positionFileStyle),'\n']))
    write_file.write('\t\tReferenceX = 0.000 µm\n')
    write_file.write('\t\tReferenceY = 0.000 µm\n')
    write_file.write('\t\tReferenceZ = -0.000 µm\n')
    write_file.write('\tEND\n')
    
    """
    write in the numbers of positions
    """
    #write_file.write()
    write_file.write(''.join(['\tNumberPositions = ',str(llen),'\n']))
    
    """
    
    """
    if llen==1:
        positionIndex=1
        write_file.write(''.join(['\tBEGIN Position',str(positionIndex),' Version = 10001\n']))
        write_file.write(''.join(['\t\tX = ',str(round(xt[0],3)),' μm\n']))
        write_file.write(''.join(['\t\tY = ',str(round(yt[0],3)),' μm\n']))
        write_file.write(''.join(['\t\tZ = ',str(round(zt[0],3)),' μm\n']))
        write_file.write('\tEND\n')
    else:
        for i in range(llen):
            positionIndex=i+1
            write_file.write(''.join(['\tBEGIN Position',str(positionIndex),' Version = 10001\n']))
            write_file.write(''.join(['\t\tX = ',str(round(xt[i],3)),' μm\n']))
            write_file.write(''.join(['\t\tY = ',str(round(yt[i],3)),' μm\n']))
            write_file.write(''.join(['\t\tZ = ',str(round(zt[i],3)),' μm\n']))
            write_file.write('\tEND\n')
        
    write_file.write('END\n')
    write_file.close()
# the end of function writePosF()
    
def z4focus(centralpoints):
    xzf,yzf,zzf=zip(*centralpoints)
    xzfc=mean(xzf)
    yzfc=mean(yzf)
    zzfc=mean(zzf)
    return (xzfc,yzfc,zzfc)
# the end of function of z4focus 

"""delete the old position files
"""
for filename in os.listdir(path):
    #print(filename)
    if "_ts_relative" in filename and ".pos" in filename:
        #print("Deleting old file \"{}\"".format(filename))
        os.remove(path+filename)
       

"""
read the position files, calculate and write
"""

print("numberOfsections = "+str(len(pos_pos)))
nsec=0
focusZ=[]
for posf in pos_pos:
    allV=[]
    nsec+=1
    print("section #"+str(nsec))
    centralpoints=readCoordinates(''.join([path,posf]))
    print("boundary points #"+str(len(centralpoints)))
    focusZ.append(z4focus(centralpoints))
    for cp in centralpoints:
        vertices=drawVertices(cp,tileSize)
        for vertex in vertices:
            allV.append(vertex)
    print("points for tilescan #"+str(len(allV)))
    fn=posf.replace("_relative.pos","")
    fileName=''.join([fn,"_ts_relative.pos"])
    zfileName=''.join(["z4scn.pos"])
    writePosF(allV,path,fileName,len(allV))

writePosF(focusZ,path,zfileName,len(focusZ))
print(str(len(focusZ))+" z_positions recorded")
# print(blue('This is blue'))
from colorama import Fore
from colorama import Style
print(f'{Fore.RED}finish conversion{Style.RESET_ALL}')



