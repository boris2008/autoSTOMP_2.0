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
sdir="C:/Users/"
parentdir=f.readline()
parentdir = parentdir.replace('\n','')
path = f.readline()#contains the .pos file
path = path.replace('\n','')
ROIPosDir= f.readline()
ROIPosDir = ROIPosDir.replace('\n','')
tilePosDir = f.readline()
tilePosDir = tilePosDir.replace('\n','')
f.close()
print(parentdir)
print(path)
print(ROIPosDir)
print(tilePosDir)
"""
#here the coordinates are in unit pixels
#here 25x objective lens used, 1024x1024 image format is used
"""
positionFileStyle = 1
tileSize=340.1
tileDilate=1
"""
#image fortmat is 512x512"""
pixelsize = 0.66
m = 100#maxium tiles that split into each tile position file
stageCo_m=[]
picCo_m=[]

for r, d, f in os.walk(path):
    for file in f:
        s=re.match('t\d+_ts_relative.pos', file)
        if s:
            #files.append(os.path.join(r, file))
            stageCo_m.append(file)
        p=re.match('t\d+_ROICo.txt', file)
        if p:
            #files.append(os.path.join(r, file))
            picCo_m.append(file)
print ("there are ",len(stageCo_m)," sections")




def readCoordinates(posFileName):
    
    """
    RelativePositions = 0 for absolute position file
    RelativePositions = 1 for relative position file
    """
    
    
    """====================================================="""
    """start to read the position file"""
    text_file = open(posFileName,"r")
    lines = text_file.readlines()
    print(len(lines))
    print(lines)
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
    return x, y, z
 #the end of the function readCoordinates(posFileName):    
#x, y, z = readCoordinates(stageCo)

def readPicCo(posFileName):
    #read these coordinates in pixels
    """
    RelativePositions = 0 for absolute position file
    RelativePositions = 1 for relative position file
    """
    
    
    """====================================================="""
    """start to read the position file"""
    with open(posFileName) as f:
        for length, l in enumerate(f):
            pass
    length = length+1
    print('the length of the txt file is {0}'.format(length))
    text_file = open(posFileName,"r")
    lines = text_file.readlines()
    #print(len(lines))
    #print(lines)
    
    """here I assume the z is the same everywhere"""

    nroi=0
    nline=0
    rois=[]#the ROIs
    roibreakline = []
    sroi=[]#the selection coordinates of each ROI

    for line in lines:
        nline=nline+1
        s=re.match('---ROI \d+---has \d+ coordinates x & y in pixels', line)
        if s and (nline>1) :
            rois.append(sroi)
            sroi=[]
            roibreakline.append(nline)
            nroi=nroi+1
        elif (not s) and (nline>1):
            s=re.findall('-?\d*\.?\d+', line)
            sroi.append([float(s[0]),float(s[1])])
        elif s and (nline==1):
            roibreakline.append(nline)
            sroi=[]#the selection coordinates of each ROI
            nroi=nroi+1
        else:
            pass
        if nline==length:
            rois.append(copy.copy(sroi))        

    text_file.close()
    return nroi, rois # numbers of ROIs AND the ROI list
 #the end of the function readPicCo(posFileName)
#nroi, rois = readPicCo(picCo)



"""start to simulate tileScan"""

def flipXY(x,y):
    y1= copy.copy(y)
    x1 =copy.copy(x)
    return (y1,x1)

#get pointsfromaPic and regain its stage cooridnates
#inputs are lists
def mapPicCo2StageCo(picx,picy,stagex,stagey):
    #the stagex and stagey should be the right upper vextice of the minRecCover
    
    sbx,sby= stagex,stagey
    """
    #here if the image is the smallest rectagle that can contain all the points
    x_max = max(sbx)
    y_max = max(sby)
    """
    #we assume that with tilescan(overlap 0%, rotation 0), 
    #the image has the length of an integer times the tile size in x and y
    xmax=max(sbx)
    ymax = max(sby)
    xmin=min(sbx)
    ymin=min(sby)
    lenx=xmax-xmin
    leny=ymax-ymin
    lenxt = math.ceil(lenx/tileSize)*tileSize
    lenyt = math.ceil(leny/tileSize)*tileSize
    
    xmax2 = 0.5*(xmin+xmax+lenxt)
    ymax2= 0.5*(ymin+ymax+lenyt)

        
    #cannot directly run math on tuple list
    #numpy array should be used
    sx = -pixelsize*np.array(picy)+xmax2
    sy = -pixelsize*np.array(picx)+ymax2

    return sx,sy




def drawTile(centralpoint,tilesize):
    """central point =[x,y]
    """
    [xs,ys] = centralpoint
    minx = xs-0.5*tilesize
    maxx = xs+0.5*tilesize
    miny = ys-0.5*tilesize
    maxy = ys+0.5*tilesize
    xr = (minx, minx,maxx,maxx,minx)
    yr = (miny,maxy,maxy,miny,miny)
    vertice =[]
    for i in range(4):
        vertice.append([xr[i],yr[i]])
    #plt.figure()
    #plt.plot(xr,yr,dashes=[2, 2],color='#f92874')
    #plt.show()
    return (vertice)#vertice
#t = drawTile([1,2],3)
#y1=y[1]

"""make a function to create tiles 
and excludes out the ones outside the polygon
1> one input is a list of coordinates that define the polygon
2> the other input is the tile size
"""
def TriPntDefSurface(points):
    """take in a list of 3 points (x,y,z)
    three points define a surface
    """
    p1 = np.array(points[0])
    p2 = np.array(points[1])
    p3 = np.array(points[2])
    # These two vectors are in the plane
    v1 = p3-p1
    v2 = p2-p1
    # the cross product is a vector normal to the plane
    cp = np.cross(v1, v2)
    a, b, c = cp
    # This evaluates a * x3 + b * y3 + c * z3 which equals d
    #p1, p2 or p3 could be used to calculate d
    d = np.dot(cp, p2)
    print('The equation is {0}x + {1}y + {2}z = {3}'.format(a, b, c, d))
    # z = (d-a*x-b*y)/c
    return (a,b,c,d)

#tri3 = [[1,2,3],[2,4,4],[5,6,2]]
#TriPntDefSurface(tri3)

def findzInSurf(x,y,TriPoints):
    """x,y is from a dot on a surface determined by three points (x,y,z).
    z will be calculated
    """
    a,b,c,d= TriPntDefSurface(TriPoints)
    z= (d-a*x-b*y)/c
    return z
#findzInSurf(0,0,tri3)
    
def findzInLine(x,y, BiPoints):
    """x,y is from a dot on a line determined by two points (x,y,z).
    if x,y is in the line, then z will be calculated
    return the boolean and z value (boolean, z)
    """
    p1 = np.array(BiPoints[0])
    p2 = np.array(BiPoints[1])
    #check if (x,y) is on the line
    a_xy= (p2[1]-p1[1])/(p2[0]-p1[0])
    b_xy = p1[1]-a_xy*p1[0]
    if y==x*a_xy+b_xy:
        #This evaluates a * x + b =z
        a_xz=(p2[2]-p1[2])/(p2[0]-p1[0])
        b_xz = p1[2]-a_xz*p1[0]
        print('the equation is {0}x+{1}=z'.format(a_xz,b_xz))
        z=a_xz*x+b_xz
        boo = True
        return (boo,z)
    else:
        print("the point is not on the line")
        boo =False
        z = np.nan
    return (boo,z)
    
#two2 = [[1,2,3],[2,6,6]]
#findzInLine(3,10,two2)

def ndivide(len,divider):
    m = len//divider
    n = len%divider
    if n==0:
        nt=m
    else:
        nt=m+1
    nt=int(nt)
    return nt
#print(ndivide(5,2))

def find_middle_y(coord,tileSize):
    coord.append(coord[0])
    """coord is a list of x,y"""
    #repeat the first point to create a 'closed loop'
    xs, ys= zip(*coord) #create lists of x and y values
    """
    xmin xmax ymin ymax are the coordinate values for the rectangle
    """
    xmin = min(xs)
    xmax = max(xs)
    ymin = min(ys)
    ymax = max(ys)
    lenx=xmax-xmin
    leny=ymax-ymin
    cenx = 0.5*(xmin+xmax)
    ceny = 0.5*(ymin+ymax)
    #number of tiles along x axis
    ntx= ndivide(lenx,tileSize)
    nty= ndivide(leny,tileSize)  #number of tiles along y axis
    # find the edge along y
    middleEdgey=[]
    if nty%2 ==0: 
        for i in range(nty):
            middleEdgey.append(ceny+(i-nty/2)*tileSize)
        middleEdgey.append(ceny+(nty-nty/2)*tileSize) 
    else:
        for i in range(nty):
            middleEdgey.append(ceny+(i-(nty//2)-0.5)*tileSize)
        middleEdgey.append(ceny+(nty-(nty//2)-0.5)*tileSize)

    # find the center dots along y
    middleCy=[]
    if nty%2 ==0: 
        for i in range(nty):
            middleCy.append(ceny+(i-nty/2+0.5)*tileSize)
    else:
        for i in range(nty):
            middleCy.append(ceny+(i-(nty//2)-0.5+0.5)*tileSize)
            
    return(middleEdgey,middleCy)        
            
#mey1,mcy1 = find_middle_y(r1,tileSize) 
def rep(value,len):
    list=[]
    for i in range(len):
        list.append(value)
    return (list)
#mex1= rep(15000, len(mey1))    
#mcx1= rep(15000, len(mcy1))       
def centeredtiles(r1,tileSize,mey1,mcy1):        
    r1sort=copy.deepcopy(r1)
    r1sort.sort(key = lambda x: x[1]) 
    ycutoff =mey1[1:(len(mey1)-1)]
    def findCutIndex(r1sort,ycut):
        for i in range(len(r1sort)):
            if(r1sort[i][1]<ycut):
                continue
            else:
                return(i)
                break
    #get the cutoff subsets of r1sort        
    cpis=[]
    for i in range(len(ycutoff)):
        cpi = findCutIndex(r1sort,ycutoff[i])
        cpis.append(cpi)
    ipi= [0]
    cpis=ipi+cpis+[len(r1sort)-1]
    r1subsets=[]
    for i in range(len(cpis)-1):
        r1subsets.append(r1sort[cpis[i]:cpis[i+1]])
    def mylist(x):
        x=int(x)
        lst =[]
        lst1=list(range(x+1))
        lst1.reverse()
        lst11=[]
        for i in range(len(lst1)):
            lst11.append(lst1[i]*(-1))
        lst=lst+lst11
        lst2=list(range(x+1))
        lst2.pop(0)
        lst=lst+lst2
        return lst
    #print(mylist(4))
        
    #the tile centers along the axis
    tcxs=[]
    tcys=[]
    meanxs=[]
    meanys=[]
    f=0.2
    yi=0
    for r1subset in r1subsets:
        subx,suby= zip(*r1subset)
        lenx=max(subx)-min(subx)
        cy=mcy1[yi]
        #n is the distance (in the unit of tileSize) between two tile centers along x axis
        n= (lenx-f*tileSize)//tileSize
        if n==0:
            tcxs=tcxs+[mean(subx)]
            tcys=tcys+[cy]
        else:
            nlst=mylist(n)
            for j in range(len(nlst)):
                tcxs=tcxs+[mean(subx)+nlst[j]*tileSize]
                tcys=tcys+[cy]
        meanxs.append(mean(subx))
        meanys.append(cy)
        yi+=1
    return (meanxs,meanys,tcxs,tcys)
    
def makeTilesExcludeOut(coord,tileSize,ax):

    """coord is a list of x,y,z"""
    #repeat the first point to create a 'closed loop'
    xs, ys, zs = zip(*coord) #create lists of x and y values
    """
    xmin xmax ymin ymax are the coordinate values for the rectangle
    """
    

    xmin = min(xs)
    xmax = max(xs)
    ymin = min(ys)
    ymax = max(ys)
    lenx=xmax-xmin
    leny=ymax-ymin
    plotlines=[]
    if (lenx>=1.5*tileSize) and (leny>=1.5*tileSize):
        print("how are you")
        print("the smallest rectagle to contains all the tiles: length/width "+ str(lenx) +" "+str(leny))
        xr = (xmin, xmin,xmax,xmax,xmin)
        yr = (ymin,ymax,ymax,ymin,ymin)
        #fig, ax = plt.subplots()
        #ax = fig.gca(projection="3d")
        #ax = fig.add_subplot(111, projection='3d')
        # Using set_dashes() to modify dashing of an existing line
        line1, = ax.plot(xs, ys, 'ro',label='polygon')
        #line1.set_dashes([2, 2, 10, 2]) 
        # 2pt line, 2pt break, 10pt line, 2pt break
        # Using plot(..., dashes=...) to set the dashing when creating a line
        line2, = ax.plot(xr, yr, color='#f16824',dashes=[6, 2], label='minRectCover')
        """get the convext hull vertices"""
        coord.pop()                 
        xyz_narray = np.asarray(coord)
        xynarray = xyz_narray[:,range(2)]
        hull = ConvexHull(xynarray)
        indV=hull.vertices
        """this is a numpy array of indices of points forming the vertices of the convex hull.
        be very careful about numpy array
        """
        indVclose =np.append(indV,[indV[0]], axis=0)
        """convert numpy array to a list"""
        coordConvexH=xynarray[indVclose].tolist()
        plt.plot(xyz_narray[indVclose,0], xyz_narray[indVclose,1], 'ko')
        plt.plot(xyz_narray[indVclose,0], xyz_narray[indVclose,1], 'r--', lw=2)
        
      
        xq,yq,zq=zip(*coord)
        coord2d=list(zip(xq,yq))
        mey1,mcy1 = find_middle_y(coord2d,tileSize) 
        meanxs,meanys,tcxs,tcys= centeredtiles(coord2d,tileSize,mey1,mcy1)
        tilelist=list(zip(tcxs,tcys))
        

        tileInsideVlist=[]#all the tiles inside
        tileInsideList=[]

        """
        divide the surface into several triangles
        """
        polygonVertices = xyz_narray[indV].tolist()
        triV=[]
        triaVList =[]#contains the coordinate of (x,y,z)
        triV_xy=[]
        triaVList_xy=[]#contains the coordinate of (x,y)
        """find the lines between the triangels
        """
        lineV = []
        lineVlist = []#contains the coordinates of (x,y)
        for i in range(len(indV)-2):
            
            triV.append([polygonVertices[0][0],polygonVertices[0][1],polygonVertices[0][2]])
            triV.append([polygonVertices[i+1][0],polygonVertices[i+1][1],polygonVertices[i+1][2]])
            triV.append([polygonVertices[i+2][0],polygonVertices[i+2][1],polygonVertices[i+2][2]])
            triaVList.append(triV)
            triV=[]
            triV_xy.append([polygonVertices[0][0],polygonVertices[0][1]])
            triV_xy.append([polygonVertices[i+1][0],polygonVertices[i+1][1]])
            triV_xy.append([polygonVertices[i+2][0],polygonVertices[i+2][1]])
            triaVList_xy.append(triV_xy)
            triV_xy=[]
            lineV.append([polygonVertices[0][0],polygonVertices[0][1],polygonVertices[0][2]])
            lineV.append([polygonVertices[i+2][0],polygonVertices[i+2][1],polygonVertices[i+2][2]])
            lineVlist.append(lineV)
            lineV = []
        
        
        #coordConvexH.remove(coordConvexH[-1])
        coordConvexH.pop()
        
        #check the path of convex hull shape
        #path = mpltPath.Path(coordConvexH)# input is a list of (x,y)
        
        #what if I don't care if the drawing is a convex shape?
        #input for func,mpltPath.Path(),'vertices' must be a 2D list or array with shape Nx2
        path = mpltPath.Path(coord2d)
        """calculate the central coordinates of tiles within a rectangle
        defined by four vertice and exclude those fall out of the polygon
        """
        #check the tile central points not the tile vertices
        inside = path.contains_points(tilelist)
        for i in range(len(tilelist)):
            if not inside[i]:
                continue
            else:
                #keep that tile central point
                tileInsideList.append(tilelist[i])
                st= drawTile(tilelist[i],tileSize)#st is a list of (x,y)
                tileInsideVlist.append(st)
        print("the length of tile sc:",len(tileInsideList))
        print("the length of tile vertices:",len(tileInsideVlist))
        """
        time to calculate z
        """
        zc=[]
        """++++++++++++++++++++++++++++++
        The break statement, like in C, 
        breaks out of the innermost enclosing for or while loop.
        +++++++++++++++++++++++++++++++++++"""
        xc,yc=zip(*tileInsideList)
        for i in range(len(tileInsideList)):
            inside1=False
            j=0        
            while(inside1==False & j<len(triaVList_xy)):
                path1 = mpltPath.Path(triaVList_xy[j])
                inside1= path1.contains_point(tileInsideList[i])
                if inside1 == True:
                    zc.append(findzInSurf(xc[i],yc[i],triaVList[j]))
                    j=0
                    break
                else:
                    j+=1
            """check if the central point of the tile inside the triangle
            """
            boo1=False    
            for z in range(len(lineVlist)):
                if inside1== True:
                    break
                else:
                    boo1, z1 = findzInLine(xc[i],yc[i], lineVlist[z])#return (boo,z)
                    if boo1 == True:
                        print("find the point on the line")
                        zc.append(z1)
                        break
                    else:
                        continue
             
            xs,ys=zip(*tileInsideVlist[i])
            xs=list(xs)
            xs.append(xs[0])#make a close drawing
            ys=list(ys)
            ys.append(ys[0])#make a close drawing
            line3,= ax.plot(xs,ys,color='blue')
            line4,=ax.plot(xc,yc,'go')# the center of the tile
        tileNewList=list(zip(xc,yc,zc))
        
        #ax.legend()
        #plt.savefig('plane.png')
        #plt.show()
        plotlines.extend([line1,line2,line3,line4])
        return (len(tileNewList),tileNewList,plotlines)#return a list of tile center coordinates
    else:
        xr = (xmin, xmin,xmax,xmax,xmin)
        yr = (ymin,ymax,ymax,ymin,ymin)
        #fig, ax = plt.subplots()
        #ax = fig.gca(projection="3d")
        #ax = fig.add_subplot(111, projection='3d')
        # Using set_dashes() to modify dashing of an existing line
        #line1, = ax.plot(xs, ys, 'ro',label='polygon')
        line1, = ax.plot(xs, ys, 'ro')
        #line1.set_dashes([2, 2, 10, 2]) 
        # 2pt line, 2pt break, 10pt line, 2pt break
        # Using plot(..., dashes=...) to set the dashing when creating a line
        #line2, = ax.plot(xr, yr, color='#f16824',dashes=[6, 2], label='minRectCover')
        line2, = ax.plot(xr, yr, color='#f16824',dashes=[6, 2])
        """get the convext hull vertices"""
        coord.pop()                 
        
        #a tile is generated in the center of polygon selection
        xc= 0.5*(xmin+xmax)
        yc= 0.5*(ymin+ymax)
        zc= mean(zs)
        tileV= drawTile([xc,yc],tileSize)
             
        xs1,ys1=zip(*tileV)
        xs1=list(xs1)
        xs1.append(xs1[0])#make a close drawing
        ys1=list(ys1)
        ys1.append(ys1[0])#make a close drawing
        line3,= ax.plot(xs1,ys1,color='blue')
        
        line4,=ax.plot(xc,yc,'go')# the center of the tile
        tileNewList= (xc,yc,zc)#this is a tuple
        plotlines.extend([line1,line2,line3,line4])
        #ax.legend()
        #plt.savefig('plane.png')
        #plt.show()
        return (1,tileNewList,plotlines)#return the coordinate of the single tile center as a tuple
        
# the end of function, makeTilesExcludeOut(xyz,tileSize,ax)



def XYZinPolygon(coord,newx,newy):
    #the coord is a list of xyz defining the boundary of polygon.
    #newx and newy is a list of x or y of points inside the polygon. 
    #newz should be derived. here export a list new xyz of the points
    coord.append(coord[0])
    """coord is a list of x,y,z"""
    #repeat the first point to create a 'closed loop'
    xs, ys, zs = zip(*coord) #create lists of x and y values
    """
    xmin xmax ymin ymax are the coordinate values for the rectangle
    """
    xmin = min(xs)
    xmax = max(xs)
    ymin = min(ys)
    ymax = max(ys)
    lenx=xmax-xmin
    leny=ymax-ymin
    print("how are you")
    print("the smallest rectagle to contains all the tiles: length/width "+ str(lenx) +" "+str(leny))
    xr = (xmin, xmin,xmax,xmax,xmin)
    yr = (ymin,ymax,ymax,ymin,ymin)
    #fig, ax = plt.subplots()
    #ax = fig.gca(projection="3d")
    #ax = fig.add_subplot(111, projection='3d')
    # Using set_dashes() to modify dashing of an existing line
    #line1, = ax.plot(xs, ys, 'ro',label='polygon')
    #line1.set_dashes([2, 2, 10, 2]) 
    # 2pt line, 2pt break, 10pt line, 2pt break
    # Using plot(..., dashes=...) to set the dashing when creating a line
    #line2, = ax.plot(xr, yr, color='#f16824',dashes=[6, 2], label='minRectCover')
    """get the convext hull vertices"""
    coord.pop()                 
    xyz_narray = np.asarray(coord)
    xynarray = xyz_narray[:,range(2)]
    hull = ConvexHull(xynarray)
    indV=hull.vertices
    """this is a numpy array of indices of points forming the vertices of the convex hull.
    be very careful about numpy array
    """
    indVclose =np.append(indV,[indV[0]], axis=0)
    """convert numpy array to a list"""
    #coordConvexH=xynarray[indVclose].tolist()
    plt.plot(xyz_narray[indVclose,0], xyz_narray[indVclose,1], 'ko')
    plt.plot(xyz_narray[indVclose,0], xyz_narray[indVclose,1], 'r--', lw=2)
    
    """
    divide the surface into several triangles
    """
    polygonVertices = xyz_narray[indV].tolist()
    triV=[]#vertice (x,y,z) of each triangle
    triaVList =[]#list of the triangle
    triV_xy=[]
    triaVList_xy=[]#contains the coordinate of (x,y)
    """find the lines between the triangels
    """
    lineV = [] #terminal points (x,y,z)of a single edge 
    lineVlist = [] #a list of edges
    for i in range(len(indV)-2):
        
        triV.append([polygonVertices[0][0],polygonVertices[0][1],polygonVertices[0][2]])
        triV.append([polygonVertices[i+1][0],polygonVertices[i+1][1],polygonVertices[i+1][2]])
        triV.append([polygonVertices[i+2][0],polygonVertices[i+2][1],polygonVertices[i+2][2]])
        triaVList.append(triV)
        triV=[]
        triV_xy.append([polygonVertices[0][0],polygonVertices[0][1]])
        triV_xy.append([polygonVertices[i+1][0],polygonVertices[i+1][1]])
        triV_xy.append([polygonVertices[i+2][0],polygonVertices[i+2][1]])
        triaVList_xy.append(triV_xy)
        triV_xy=[]
        lineV.append([polygonVertices[0][0],polygonVertices[0][1],polygonVertices[0][2]])
        lineV.append([polygonVertices[i+2][0],polygonVertices[i+2][1],polygonVertices[i+2][2]])
        lineVlist.append(lineV)
        lineV = []


    """
    time to calculate z
    """
    zc=[]
    xc= newx
    yc= newy     
    newxy = list(zip(newx,newy))
    """++++++++++++++++++++++++++++++
   The break statement, like in C, 
   breaks out of the innermost enclosing for or while loop.
   +++++++++++++++++++++++++++++++++++"""
    for i in range(len(newx)):

        
        #print(''.join(['begin to check tile point_',str(i+1)]))
        inside1=False
        j=0        
        while inside1==False and j<len(triaVList_xy):
            path1 = mpltPath.Path(triaVList_xy[j])
            inside1= path1.contains_point(newxy[i])
            if inside1 == True:
                zc.append(findzInSurf(xc[i],yc[i],triaVList[j]))
                j=0
                break
            else:
                j+=1
        """check if the central point of the tile inside the triangle
        """
        boo1=False            
        for z in range(len(lineVlist)):
            if inside1== True:
                break
            else:
                boo1, z1 = findzInLine(xc[i],yc[i], lineVlist[z])#return (boo,z)
                if boo1 == True:
                    print("find the point on the line")
                    zc.append(z1)
                    break
                else:
                    continue
        if boo1== False:
            zc.append(np.float64(mean(zs)))
    newxyz=list(zip(xc,yc,zc))
    """        
    xc=list(xc)
    xc.append(xc[0]) 
    yc=list(yc)
    yc.append(yc[0]) 
    line2,=ax.plot(xc,yc,'b-') 
    xc.pop()     
    yc.pop()         
    line1,=ax.plot(xc,yc,'go')
    ax.legend()
    plt.savefig('plane.png')
    plt.show()
    """
    return (len(newxyz),newxyz)
# the end of function, XYZinPolygon(coord,newx,newy)
     

"""start to write the position file"""
"""+++create x,y,z lists for tiles+++++"""
def writePosF(xt,yt,zt,parentDir,fileName,llen):
    #xt,yt,zt =zip(*xyz_Tile)
    
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
        write_file.write(''.join(['\t\tX = ',str(round(xt,3)),' µm\n']))
        write_file.write(''.join(['\t\tY = ',str(round(yt,3)),' µm\n']))
        write_file.write(''.join(['\t\tZ = ',str(round(zt,3)),' µm\n']))
        write_file.write('\tEND\n')
    else:
        for i in range(llen):
            positionIndex=i+1
            write_file.write(''.join(['\tBEGIN Position',str(positionIndex),' Version = 10001\n']))
            write_file.write(''.join(['\t\tX = ',str(round(xt[i],3)),' µm\n']))
            write_file.write(''.join(['\t\tY = ',str(round(yt[i],3)),' µm\n']))
            write_file.write(''.join(['\t\tZ = ',str(round(zt[i],3)),' µm\n']))
            write_file.write('\tEND\n')
        
    write_file.write('END\n')
    write_file.close()
# the end of function writePosF()
    
def readSection(x, y, z,nroi, rois, nSCN):     
    """
    #read a single section in the tile scan image
    x,y,z the list of x, y or z stage coordinates of boundary points of the section
    nroi: the number of ROIs from this section
    rois: the boundary points of the ROIs, pixel x,y within the section picture
    nSCN: the index of section, 1,2,3,...
    """
    #map multiple ROIs to the boundary fo the tile scan image
    newxyz_m=[]#the list of ROIs, (x,y,z)
    fig, ax = plt.subplots()
    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)
    xr = (xmin, xmin,xmax,xmax,xmin)
    yr = (ymin,ymax,ymax,ymin,ymin)  
    line1, = ax.plot(x, y, 'ro',label='polygon')
    line2, = ax.plot(xr, yr, color='#f16824',dashes=[6, 2], label='minRectCover')
    xyz = list(zip(x,y,z))  
    
    for i in range(nroi):
        xp,yp=zip(*rois[i])
        xp = list(xp)
        yp=list(yp)
        #get the stage coordinates of the points within the tile scan boundary points (irregular polygon typically)
        newx,newy = mapPicCo2StageCo(xp,yp,x,y)
        # the coordinates of the boundary points to setup  tileScan scan
        
        npnt, newxyz = XYZinPolygon(xyz,newx,newy)# a figure is created in the function, but not shown yet
        #the figure will not display until we add more 
        newxyz_m.append(newxyz)
        xc,yc,zc= zip(*newxyz)
        xc=list(xc)
        xc.append(xc[0]) 
        yc=list(yc)
        yc.append(yc[0]) 
        line2,=ax.plot(xc,yc,'b-') 
        xc.pop()     
        yc.pop()         
        line1,=ax.plot(xc,yc,'go')
    # the end of the for loop
    ax.legend()
    #plt.savefig('plane.png')
    plt.show()
        
    
    #map the tiles within multiple ROIs 
    newx_al = []
    newy_al =[]
    newz_al=[]
    xt_al=[]
    yt_al=[]
    zt_al=[]
    fig, ax = plt.subplots() 
    for i in range(len(newxyz_m)):
        newx,newy,newz= zip(*newxyz_m[i])
        newx=list(newx)
        newy=list(newy)
        newz=list(newz)
        print("this selection within the image contains ", len(newx), " points")
        #now calculate the tile contained in the selection from the tile scan image
        #several layers have been added in the function, makeTilesExcludeOut
        NumOfTiles, xyz_Tile,plotlines = makeTilesExcludeOut(newxyz_m[i],tileSize,ax)
        print("print one xyz_Tile")
        print(xyz_Tile)
        newx_al = newx_al + newx
        newy_al =newy_al + newy
        newz_al= newz_al + newz
        if NumOfTiles > 1:#concatenate the lists, not append
            xt,yt,zt= zip(*xyz_Tile)
            xt=list(xt)
            yt=list(yt)
            zt=list(zt)
            xt_al=xt_al + xt
            yt_al=yt_al + yt
            zt_al=zt_al +zt
        else:#there is only one tile
            if isinstance(xyz_Tile,tuple):
                xt_al.append(xyz_Tile[0])
                yt_al.append(xyz_Tile[1])
                zt_al.append(xyz_Tile[2])
            elif isinstance(xyz_Tile,list):
                xt_al.append(xyz_Tile[0][0])
                yt_al.append(xyz_Tile[0][1])
                zt_al.append(xyz_Tile[0][2])
            else:
                continue
                
            
    ax.legend((plotlines[0],plotlines[1],plotlines[2],plotlines[3]),('boundary points ROI','miniRect ROI','tile','tile center'))
    plt.savefig(''.join([tilePosDir,'/tilesFmultiROIs',str(nSCN),'.png']))
    plt.show()        
    
    """plot the tile dots in 3d"""
    #total number of the tiles from all the ROIs 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(xt_al,yt_al,zt_al, color='r', linestyle=' ', marker='o')
    #the plot function just cannot plot a single point in 3d
    #Error : object of type 'numpy.float64' has no len()
    
    #ax.set_zlim3d(30,400)
    ax.view_init(10, 70)#adjust the elevation and azimuth
    plt.tight_layout()
    plt.savefig(''.join([tilePosDir,'/tileCenter3d',str(nSCN),'.png']))
    plt.show()
    
    return (newx_al,newy_al,newz_al,xt_al,yt_al,zt_al)
# the end of function, readSection()

"""
read through all the sections and sum up all the tiles derived from ROIs
"""
newx_allSec=[]
newy_allSec=[]
newz_allSec=[]
xt_allSec=[]
yt_allSec=[]
zt_allSec=[]
for q in range(len(stageCo_m)):
    stageCo = ''.join([path,stageCo_m[q]])
    #here the coordinates are in unit micrometer
    #I set 4 positions in tilescan. But it will export 16 positions
    picCo  = ''.join([path,picCo_m[q]])
    x, y, z = readCoordinates(stageCo)
    nroi, rois = readPicCo(picCo)    
    newx_al,newy_al,newz_al,xt_al,yt_al,zt_al=readSection(x, y, z,nroi, rois,(q+1))
    newx_allSec.extend(newx_al)
    newy_allSec.extend(newy_al)
    newz_allSec.extend(newz_al)
    xt_allSec.extend(xt_al)
    yt_allSec.extend(yt_al)
    zt_allSec.extend(zt_al)
    
writePosF(newx_allSec,newy_allSec,newz_allSec,ROIPosDir,"stageC_ROIs_boundary.pos",len(newx_allSec))
writePosF(xt_allSec,yt_allSec,zt_allSec,tilePosDir,"tilePos.pos",len(xt_allSec))



"""delete the old position files
"""
for filename in os.listdir(dire):
    #print(filename)
    if "tilePos-" in filename and ".pos" in filename:
        #print("Deleting old file \"{}\"".format(filename))
        os.remove(dire+filename)
       
def writeFile(x, m, n, NumOfTiles, dire, positionFileStyle):
    """"
    x: the index of the position file, 1,2,3...
    m: the maxium number of tile per .pos file
    n: the number of position files
    """ 
    filename =''.join(['tilePos-',str(x),'.pos'])
    if(n==1):
        NumT = NumOfTiles
    elif x<n and n>1:
        NumT = m
    elif x==n and n>1:
        NumT = NumOfTiles%m
        if(NumT==0):
            NumT=m
    else:
        NumT = 0
    write_file = open(''.join([dire,filename]),"w")
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
    write_file.write(''.join(['\tNumberPositions = ',str(NumT),'\n']))
    
    """
    
    """
    print("#"+str(x)+"file contains "+str(NumT)+" tiles")
    
    for i in range(NumT):
        positionIndex=i+1
        
        if (n==1):
            DataIndex = i 
        else:
            DataIndex = i+m*(x-1)
        write_file.write(''.join(['\tBEGIN Position',str(positionIndex),' Version = 10001\n']))
        #xt_allSec,yt_allSec,zt_allSec
        write_file.write(''.join(['\t\tX = ',str(round(xt_allSec[DataIndex],3)),' µm\n']))
        write_file.write(''.join(['\t\tY = ',str(round(yt_allSec[DataIndex],3)),' µm\n']))
        write_file.write(''.join(['\t\tZ = ',str(round(zt_allSec[DataIndex],3)),' µm\n']))
        write_file.write('\tEND\n')
        
    write_file.write('END\n')
    write_file.close()
    return

NumOfTiles = len(xt_allSec)
n= NumOfTiles//m
rem = NumOfTiles%m
if (rem>0):
    NumOfPosF= n+1
else:
    NumOfPosF = n
for j in range(NumOfPosF):
    writeFile(j+1, m, NumOfPosF, NumOfTiles, dire, positionFileStyle)
    
def writeSTPsikuli():
    """"
    x: the index of the position file, 1,2,3...
    m: the maxium number of tile per .pos file
    n: the number of position files
    x, m, n, NumOfTiles, dire, positionFileStyle
    """ 
    
    filename ="sikuliInput.txt"
    
    write_file = open(''.join([sdir,filename]),"w")
    write_file.write('number of .pos files\n')
    write_file.write(''.join([str(NumOfPosF),'\n']))
    write_file.write('total tiles\n')
    write_file.write(''.join([str(NumOfTiles),'\n']))
    write_file.write('maximum tile per file\n')
    write_file.write(''.join([str(m),'\n']))    
    
    for i in range(NumOfPosF):
        write_file.write(''.join(['posfile#'+str(i+1)+'has tiles:\n']))
        if i==(NumOfPosF-1):
            if rem==0:
                write_file.write(''.join([str(m),'\n']))
            else:
                write_file.write(''.join([str(rem),'\n']))
        else:
            write_file.write(''.join([str(m),'\n']))
    write_file.close()
    return     

"""delete the old sikuliInput.txt
"""
for filename in os.listdir(sdir):
    #print(filename)
    if "sikuliInput" in filename:
        #print("Deleting old file \"{}\"".format(filename))
        os.remove(sdir+filename)    
writeSTPsikuli()

print("numberOfPositionFiles = "+str(NumOfPosF))
print("****tile positions are calculated!")    
print("***********************************")
print("***********************************")

# print(blue('This is blue'))
from colorama import Fore
from colorama import Style
print(f'{Fore.RED}1. minimize this Spyder window{Style.RESET_ALL}')
print(f'{Fore.GREEN}   # "TuneSTPLayout.sikuli" to tune the layout for autoSTOMP if you want!{Style.RESET_ALL}')
print("***********************************")
print(f'{Fore.BLUE}2. go to sikuliX and run {Fore.RED}"STOMP.sikuli"{Style.RESET_ALL}')


