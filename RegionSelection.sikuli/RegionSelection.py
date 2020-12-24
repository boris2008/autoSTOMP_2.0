Dir = "C:\\ZEN"
import os
import shutil
popup("EOE sample!?\nframe size to 512X512\nSPEED:7\npixel dwell 2.05us\n8/16framesum")
folder = input("Enter a new folder name")
path = '\\'.join(['D:\\Bocheng',folder])
tsDir='\\'.join(['D:\\Bocheng',folder,'tileScan'])
RoiDir='\\'.join(['D:\\Bocheng',folder,'ROIs'])
stpTDir='\\'.join(['D:\\Bocheng',folder,'stpTile'])
###export the info of the directories to a txt file
###the directories can be directly read by imagej and python code
pathValueFile =''.join([Dir, '\\','pwd_mROIs.txt'])
if (os.path.isfile(pathValueFile)):
        os.remove(pathValueFile)
wait(0.1)
f = open(pathValueFile,"w")
print >> f,'/'.join(['D:/Bocheng',folder,''])
print >> f,'/'.join(['D:/Bocheng',folder,'tileScan',''])
print >> f,'/'.join(['D:/Bocheng',folder,'ROIs',''])
print >> f,'/'.join(['D:/Bocheng',folder,'stpTile',''])
f.close()
wait(0.1)   
#######################################
if os.path.exists(path):
    shutil.rmtree(path, ignore_errors=True)
if not os.path.exists(path):    
    os.mkdir(path)
if not os.path.exists(tsDir):     
    os.mkdir(tsDir)
if not os.path.exists(RoiDir):       
    os.mkdir(RoiDir)
if not os.path.exists(stpTDir):     
    os.mkdir(stpTDir)
popup("three subfolders are also created under the folder.")
popup("set! ZEN BLACK => POSITIONS\nautofocus OFF\nclick OK after finish")
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
conTinue = True
stn=1
print(conTinue)

#tune the layout
def tuneLayoutSavePos():
    click(Pattern("1591454070456.png").targetOffset(178,107))
    wait(0.5)
    #resize the save As window
    fixCorner= find("1591454241890.png")
    slideCorner = find(Pattern("1542143453397-1.png").targetOffset(15,24))
    drop_point = fixCorner.getTarget().offset(434, 214)
    dragDrop(slideCorner, drop_point)
    click("1591454592706.png")
#the end of function tuneLayoutSavePos()     

def saveSecBoundaryPos(n):
    click(Pattern("1591454070456-1.png").targetOffset(178,107))
    wait(0.5)
    click(Pattern("1591454301122.png").targetOffset(57,3))
    file1 =''.join([tsDir, '\\','t',str(n),'_relative.pos'])
    if (os.path.isfile(file1)):
        os.remove(file1)
    paste(file1)
    click(Pattern("1591454489569.png").similar(0.75))
    wait(0.5)
    if (os.path.isfile(file1)):
        #remove the points
        click("1591454926489.png")
        wait(0.5)
        click(Pattern("1591454954291.png").targetOffset(-24,40))
# the end of function, saveSecBoundaryPos(n)
    
while(conTinue):
    conTinue = popAsk(''.join(['want to set up for section ',str(stn),'? continue?']))
    if(conTinue):
        done = popAsk(''.join(['begin to record boundary points for section ',str(stn),'\n','waiting...\n','...\n','When finish, click yes!']))
        if done:
            if(stn==1):
                tuneLayoutSavePos()
            else:
                pass
            saveSecBoundaryPos(stn)
            stn=stn+1
        else:
            break
    else:
        break
print("boundary points are all set!!! Hahahaha!")    
popup("finish setting all the section?\nif yes, click OK")
#call the python code
python = r"C:\Users\LSM_User\Anaconda3\python.exe"
pyscript = r"C:\Users\pzsn2TS_eoe.py"
cmd = "%s %s" % (python, pyscript)
result=run(cmd)
print result
popup("TS style pos conversion finished\nto CONTINUE?\nif yes, CHECK BOTH Positions && Tile Scan\nshow two panels FULLY\ndrag the side bar all way down\nclick OK after finish")


#if the Tile Scan under "Experiment Manager" is checked
def setTileScan():
    setFindFailedResponse(RETRY)
    reg = find("1578103152880.png")
    if reg:
        #setFindFailedResponse(ABORT)
        click(Pattern("1578103152880.png").targetOffset(152,1))
        wait(0.3)
    reg2 = find("1578068925693.png")
    if reg2:
        #setFindFailedResponse(ABORT)
        #setup the overlap to 0
        click(reg2.find(Pattern("1578104107433.png").targetOffset(64,1)))
        wait(0.3)
        type("0.00")
        type(Key.ENTER)
        wait(0.3)
        click(reg2.find(Pattern("1578104072121.png").targetOffset(61,1)))
        wait(0.3)
        type("0.00")
        type(Key.ENTER)
        wait(0.3)        
        click(reg2.find("1578070158703.png"))
        wait(0.3)
        if not exists("1578070229566.png"):
            click(Pattern("1578076044923.png").targetOffset(-57,2))
            wait(0.2)
# the end of function setTileScan()
def uncheckPos():
    n=0
    while(n<2):
        n+=1
        if exists(Pattern("1591302404814.png").similar(0.92)):
            click(Pattern("1591302404814.png").targetOffset(-31,1))
            wait(0.5)
def checkPos():
    n=0
    while(n<2):
        n+=1
        if exists(Pattern("1591302681950.png").similar(0.97)):
            click(Pattern("1591302681950.png").targetOffset(-31,-9))
            wait(0.5)

def runTileScan(tsDir,n):
    #clear the previously loaded positions
    click(Pattern("1578080407646.png").targetOffset(75,0))
    wait(0.2)
    #the file name is like "t1_relative.pos"
    file1 =''.join([tsDir, '\\','t',str(n),'_ts_relative.pos'])
    #load the file
    if exists("1578070229566.png"):
        click(Pattern("1578070229566.png").targetOffset(109,10))
        click(Pattern("1578080906145.png").targetOffset(40,1))
        paste(file1)
        click("1578080943440.png")
        wait(0.2)
    # if the autofocus is checked.then
    # it is ready to start tile scan
    click("1578081105543.png")
    wait(0.2)
# the end of function, runTileScan(tsPosDir,n)
def loadPosFile():
    #n starts from 0
    wait(0.5)
    posFile = ''.join([tsDir,'\\','z4scn.pos'])
    #remove all the current positions
    click(Pattern("1578956549978.png").targetOffset(172,0))
    wait(0.5)
    if exists("1557922477004.png"):
        click(Pattern("1557922477004.png").targetOffset(-29,38))
    #load new posFile
    while (1):
        if not exists("1557922697301.png"):
            click(Pattern("1558142138135.png").similar(0.72).targetOffset(147,93))
            wait(0.5)
        else:
            n=0
            while(n<2):
                n+=1
                if not exists("1557923810995.png"):
                    #click(Pattern("1557922697301.png").similar(0.67).targetOffset(-89,192))
                    if exists(Pattern("1564111440321.png").targetOffset(22,-17)):
                        click(Pattern("1564111440321.png").targetOffset(22,-17))
                        type(posFile)
                        type(Key.ENTER)
                        wait(5)
                    else:
                        break
                else:
                    break
            break
#the end of the loadPosFile() function


def waitTS2finish():
    #wait("1537103643599.png",FOREVER)
    wait(5)
    print("now focusing fine")
    #once starts the experiment, there would be a spinning dynamic icon
    #wait for this icon disappear
    wait("1578082738775.png",FOREVER)
# the end of function, waitTS2finish()

def saveTSPic(n):
    
    #find("1537099262131.png")
    while(1):
        if exists("1547265076633.png"):
            click(Pattern("1547310449106.png").targetOffset(-12,0))
            break
        else:
            wait(1)
    wait(1)

    while(1):
        if exists("1546869423394.png"):
            click("1546869478218.png")
            wait(1)
            break
        else:
            while(1):
                if exists("1547265035418.png"):
                    click(find(Pattern("1537099262131.png").targetOffset(-11,1)))
                    break
                else:
                    wait(1)
            wait(1)
    type(Key.DELETE)
    ####it is critically important to use [\\] instead of [\] for the path
    #find("1537105389619-2.png")
    #click(Pattern("1537105389619-2.png").targetOffset(368,-1))
    #type("a", KeyModifier.CTRL)
    #type(Key.DELETE)
    paste(''.join([tsDir, '\\','t',str(n),'.czi']))
    find("1537105834742-2.png")
    click("1537105834742-2.png")
# the end of function, saveTSPic(n)    
    
def closePic():
    ### close the image ######
    click(find(Pattern("1537142778142-2.png").targetOffset(-47,3)))
    wait(1)
    while(1):
        if exists("1577111326608.png"):
            click(Pattern("1577111326608.png").targetOffset(19,49))
        elif exists(Pattern("1577109842694.png").similar(0.67)):
            click(Pattern("1577109842694.png").similar(0.67).targetOffset(74,40))
        else:
            break
        wait(1)    
# the end of function, closePic()
def dragSBdown():
    #have to drage the side bar all the way down to show the panel below Tile Scan
    dock = find(Pattern("1591313309462.png").similar(0.75))
    dragDrop(dock.offset(140,0),Location(dock.x+140,dock.y+500))
    
def doNothing():
    pass
    
def clickPos1():
    click(Pattern("1558133984152.png").targetOffset(-137,-10))
    #click move to 
    click(Pattern("1558133984152.png").targetOffset(-184,102))
def clickPos2():
    click(Pattern("1558134555833-1.png").targetOffset(-127,13))
    #click move to 
    click(Pattern("1558133984152.png").targetOffset(-184,102))    
def clickPos3():
    click(Pattern("1558134555833-1.png").similar(0.68).targetOffset(-155,31))
    #click move to 
    click(Pattern("1558133984152.png").similar(0.69).targetOffset(-184,102))
def clickPos4():
    click(Pattern("1558134555833-1.png").targetOffset(-125,51))
    #click move to 
    click(Pattern("1558133984152.png").targetOffset(-184,102)) 
def TSss(j):
    uncheckPos()
    runTileScan(tsDir,j)
    waitTS2finish()
    saveTSPic(j)
    closePic()
    checkPos()
    dragSBdown()
#the end of the function TSss()

#+++++++++++++++test movedown the position l++++++++++++++++++++++++++++
def clickForfirst4Pos(nTile):
    count=0
    p = nTile
    #find("1558133984152.png")
    #++++++++++choose position 1+++++++++++++++++++++
    count+=1
    clickPos1()
    TSss(count)
    p=p-1
    
        #++++++++++choose position 2+++++++++++++++++++++
    if p>0: 
        count+=1
        clickPos2()
        TSss(count)
        p=p-1
    else:
        doNothing()
    
    #++++++++++choose position 3+++++++++++++++++++++
    if p>0: 
        count+=1
        clickPos3()
        TSss(count)
        p=p-1
    else:
        doNothing()
    #++++++++++choose position 4+++++++++++++++++++++
    if p>0:  
        count+=1
        clickPos4()
        TSss(count)
        p=p-1
    else:
        doNothing()
    return count
def clickForPosMT4(x):
    #x is the number of the leftover positions after position 4
    count=4
    for i in range(x):
        count+=1
        #move the list down by one
        click(Pattern("1558134555833-1.png").similar(0.65).targetOffset(213,53))
        #select the new position
        click(Pattern("1558133984152.png").similar(0.65).targetOffset(-129,47))
        #click move to 
        click(Pattern("1558133984152.png").similar(0.65).targetOffset(-184,102))

        TSss(count)
    return(count)

# the end of function of clickForPosMT4()

#Prologue

# step 1 #
setTileScan()
# step 2 #
import fnmatch
import os
count = 0
#count the number of tile scan boundary position files
for c in os.listdir(tsDir):
    if fnmatch.fnmatch(c, 't*_ts_relative.pos'):
            print(c)
            count = count+1
print count
# step 3 #
#load the z4scn.pos to Positions
loadPosFile()
popup("load any t*_ts_relative.pos\ndrag the side bar all the way down\nthis will help to tune the layout and avoid errors")
# step 4 #
#for each section, what needs to do after move to its center where z position is adjusted??
#in \'Position', read z position from the center point of that section., then uncheck it. Back to Tile scan and do tile scan on that section without autofocus.

#begin the looping through the section list
if count < 4 or count ==4:
    cc= clickForfirst4Pos(count)
#+++++++++++after position 4+++++++++
if count>4:
    #for the first 4 position, returns the
    cc = clickForfirst4Pos(count)
    # from the 5th position
    cc = clickForPosMT4(count-4)    
popup("END OF TILE SCAN\nload FIJI macro=> bocheng STOMP\n=>EOE--Eosinophilic esophagitis\n=>ROICo_sc.ijm")

    