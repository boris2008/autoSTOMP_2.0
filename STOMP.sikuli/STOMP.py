######## author:  Bocheng Yin Date: 05/21/2020
import os
posdir = "C:\\ZEN"
posdir2 = "C:\\Users"
listF = []
listTile =[]
currentTilex = 0
f = open(''.join([posdir2, '\\','sikuliInput.txt']))
#where to resume the sikuli stomping
f.readline()
numPosFile = f.readline().replace('\n','')
numPosFile =int(numPosFile)
print(numPosFile)
f.readline()
numTiles = f.readline().replace('\n','')
numTiles =int(numTiles)
f.readline()
mpf = f.readline().replace('\n','')
mpf =int(mpf)

lines=f.readlines()
nlines=len(lines)
ntileposfile = nlines/2
for i in range(ntileposfile):
    numTileF= lines[2*i+1].replace('\n','')
    numTileF=int(numTileF)
    listF.append(numTileF)
    listTile.append(currentTilex)
f.close()
print(nlines)
print(listF)
print(listTile)
f = open(''.join([posdir, '\\','pwd_mROIs.txt']))
hostPath =f.readline().replace('\n','')
hostPath = hostPath.rstrip('/')
hostPath =hostPath.replace('/','\\')
f.close()
print(hostPath)

def rCurrentInfo():
    import shutil

    fp1=''.join([posdir, '\\','currentInfo.txt'])
    if not(os.path.isfile(fp1)):
            shutil.copy2('Z:\\Bocheng\\currentInfo.txt', fp1) 
    f = open(fp1)
    for i in range(5):
        f.readline()
    #line 6
    FileIdx = f.readline().replace('\n','')
    FileIdx =int(FileIdx)

    TileIdx = f.readline().replace('\n','')
    TileIdx =int(TileIdx)
    f.close()
    return (FileIdx,TileIdx)
FileIdx,TileIdx=rCurrentInfo()    
#*******************************
#********* USER'S INPUT*********
#   used to resume STOMP   *****
#*******************************
#*******************************
popup("turn off Tile Scan!")
popup("autofocus ON !!!!\nframe size to 512X512\nSPEED:7\npixel dwell 2.05us\n8/16framesum")
popup("load the right ijm macro in imageJ")
popup("load the STOMP macro in Zen")
popup("start a new section?\nIf yes,ENTER 0 and 0 for the incoming two dialogue boxes\nNO?\nresume your work because STOMP stopped?\nCheck Z:\Bocheng\currentInfo.txt")
currentPosFile = input(''.join(["#which File(.pos) you want to resume your work\n New job?:ENTER 0\n","resume work?!\n suggested TileFileIndex:",str(FileIdx-1)]))
currentPosFile =int(currentPosFile)
currentTile =input(''.join(["#which Tile in the designated file?\nNew job?:ENTER 0\n","resume work?!\n suggested TileIndex:",str(TileIdx)]))
currentTile = int(currentTile)
timepass=input("what is the longest frozen time in seconds?\nsuggested: 1800   =30 min")
popup("Desktop\bocheng STOMP\python\nspyder=>checkFreezingCode.py?")
#currentPosFile = 0 #default is 0 #which position file you want to resume your work, i.e. 3 is tilePosfile 4
#currentTile = 0#***default is 0 # which position you want to resume in the list of the position file chosen above, count from 0
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
laser = "720"
power = "3"  ######P/I/D =3/1/1
#script2beCall = "./stp_beCalledTest.sikuli"
script2beCall = "./stp_becalled_oneChannel.sikuli"
#######################################################
###           END OF INPUT PARAMETERS              ####
#######################################################
# author:  Bocheng Yin Date: Bocheng Yin Date: 05/21/2020
#cannot load too many position per time to zen black
# different position files
#cannot load too many position per time to zen black
# otherwise, it will numb the software
#now each time only load 120 positions

#save the input parameters as a text file
#pass the parameters to the beCalled script

def wtimepass():
    # x is the index of the position file
    #if currentValue file exists, delete
    pathValueFile =''.join([posdir, '\\','frozentimeTolerance.txt'])
    if (os.path.isfile(pathValueFile)):
            os.remove(pathValueFile)
    wait(0.1)
    f = open(pathValueFile,"w")
    print >> f,timepass
    f.close()
wtimepass()    

for i in listF:
    print(i)
for i in listTile:
    print(i)

#replace currentTiles in the list
listTile[currentPosFile]= currentTile
print("resume the work, how the list looks like now?")
for i in listTile:
    print(i)
print("the one has been changed")
print(listTile[currentPosFile])
def exportValue(x,listF,listTile):
    # x is the index of the position file
    import os
    #if currentValue file exists, delete
    pathValueFile =''.join([posdir, '\\','currentValue.txt'])
    if (os.path.isfile(pathValueFile)):
            os.remove(pathValueFile)
    wait(0.1)
    f = open(pathValueFile,"w")
    print >> f,hostPath
    print >> f,str(x)
    print >> f,str(listF[x])
    print >> f,str(listTile[x])
    print >> f,str(laser)
    print >> f,str(power)
    f.close()

def wSTOMPStatus(stpcode,otherMsg):
    #stomp code (stpcode: 1 or 0)
    import os
    #if currentValue file exists, delete
    pathValueFile =''.join([posdir, '\\','STOMPstatus.txt'])
    if (os.path.isfile(pathValueFile)):
            os.remove(pathValueFile)
    wait(0.1)
    f = open(pathValueFile,"w")
    title= "STOMP CODE: 1 for succeed, 0 for fail"
    print >> f,title
    print >> f,str(stpcode)
    print >> f,str(otherMsg)
    f.close()    


#####################################################
def sendMessage():
    #call the python code
    python = r"C:\Users\LSM_User\Anaconda3\python.exe"
    pyscript = r"C:\Users\reportStatus.py"
    cmd = "%s %s" % (python, pyscript)
    result=run(cmd)
    print result

def loadPosFile(posdir, n):
    #n starts from 0
    wait(0.5)
    posFile = ''.join([posdir,'\\','tilePos-',str(n+1),'.pos'])
    #remove all the current positions
    click(Pattern("1578956549978.png").targetOffset(172,0))
    wait(0.5)
    if exists("1557922477004.png"):
        click(Pattern("1557922477004.png").targetOffset(-29,38))
    #load new posFile
    while (1):
        if not exists("1557922697301.png"):
            click(Pattern("1600214495246.png").targetOffset(104,15))
            wait(0.5)
        else:
            while(1):
                if not exists("1557923810995.png"):
                    #click(Pattern("1557922697301.png").similar(0.67).targetOffset(-89,192))
                    click(Pattern("1564111440321.png").targetOffset(22,-17))
                    type(posFile)
                    type(Key.ENTER)
                    wait(5)
                else:
                    break
            break
#the end of the loadPosFile() function
def moveD2cPos(currentTile):
    for i in range(currentTile-4):
        #move the list down by one 
        #here assume that you have more than 4 positions in the list
        click(Pattern("1558134555833.png").similar(0.65).targetOffset(213,53))
        wait(0.2)
## the end of currentTile function
def empty(src):#empty a folder
    for c in os.listdir(src):
        full_path = os.path.join(src, c)
        if os.path.isfile(full_path):
            os.remove(full_path)
## the end of empty() function

def wrapFile2folder(hostPath,n):
    # n starts from 0
    import os
    import shutil
    src = ''.join([hostPath,'\\workdir'])
    dst = ''.join([hostPath,'\\',str(n+1)])
    #The destination directory, named by dst, must not already exist
    shutil.copytree(src, dst, symlinks=False, ignore=None)
    wait(8)
    #shutil.rmtree(src,ignore_errors=True)
    #wait(5)
    #if not os.path.exists(src):
    #    os.mkdir(src)# it is easy to cause permission access is denied.
    empty(src)
    wait(5)
#the end of the wrapFile2folder() function

j = currentPosFile
pwd= ''.join([hostPath,'\\workdir'])
if not os.path.exists(pwd):
    os.mkdir(pwd)
for i in range(numPosFile-currentPosFile):
    loadPosFile(posdir, j)
    moveD2cPos(listTile[j])
    exportValue(j,listF,listTile)
    exitValue = runScript(script2beCall)
    #exitValue = runScript("./testClick.sikuli")
    titleF= ''.join(["sikuli crashes!!!!", "is ",str(j+1)])
    messageF=''.join(["sikuli crashes!!!!", "is ",str(j+1)])
    titleS =''.join(['congradulation!', '#',str(j+1),'finishes'])
    messageS= ''.join(['congradulation!', '#',str(j+1),'finishes'])
        
    if exitValue == 1:
        wSTOMPStatus(0,titleF)
        #stomp code 1 for succeed, 0 for fail
        sendMessage()    
        print "there was an exception"
        exit(1)
        
    else:
        wSTOMPStatus(1,titleS)
        #stomp code 1 for succeed, 0 for fail
        sendMessage()    
        print "ran with success"
        wrapFile2folder(hostPath,j)
        #exit(exitValue)
    j=j+1
# the end of the for loop