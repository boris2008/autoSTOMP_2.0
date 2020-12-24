# set the positions of various windows
#set the saveAs window of Zen black edition
#%%%%%%%%%%%%%%%%%%%%#
popat()
name = popup("have you snap a new image in the zen black? if yes, enter ok")
find("1537099262131.png")
click(Pattern("1537099262131.png").targetOffset(-11,1))
if exists("1542142678187.png"):
    click(Pattern("1542142678187.png").targetOffset(72,40))
#open saveAs window
wait(1)
t= find("1539787226173.png")

dragDrop(t, Region(44,120,10,10))
#resize the open window
fixCorner= find("1539787226173-1.png")
slideCorner = find(Pattern("1542143453397-1.png").targetOffset(15,24))
drop_point = fixCorner.getTarget().offset(434, 214)
dragDrop(slideCorner, drop_point)
################################
###########################
click(find("1542138783631.png"))

#check the fiji window
#%%%%%%%%%%%%%%%%%%%%#
name = popup("have you opened Fiji? if yes, enter ok")
if not exists("1542138983734.png"):
    if exists("1542139032733.png"):
        click(find("1542139000149.png"))
    elif exists("1542139084519.png"):
        click(find("1542139084519.png"))
    else: pass
t2= find(Pattern("1542138983734.png").targetOffset(0,-33))
dragDrop(t2,Region(1909,114,10,10))
#click(t2)

#adjust the open window of Fiji
type("o",KeyModifier.CTRL)
if exists("1537112896608-1.png"):
    t3=find("1537112896608-1.png")

dragDrop(t3, Region(60,120,10,10))
#resize the open window
fixCorner= find("1537112896608-1.png")
slideCorner = find(Pattern("1542143453397-1.png").targetOffset(15,24))
drop_point = fixCorner.getTarget().offset(434, 214)
dragDrop(slideCorner, drop_point)
################################
click(find("1542138783631.png"))

#adjust the window "Install PlugIn" by wrong clicks in Fiji
def resizeInstallPlugIn():
    #n is the position of the macro under the "Macros" tab
    while(1):
        if exists(Pattern("1537216628985-1.png").similar(0.81)):
            click(Pattern("1537216628985-1.png").similar(0.81))
            break
        else:
            wait(1)
    wait(0.2)
    for i in range(7):
        type(Key.DOWN)
        wait(0.2)
    type(Key.ENTER)
    wait(1)
    #resize the open window
    fixCorner= find("1591451406137.png")
    slideCorner = find(Pattern("1542143453397-1.png").targetOffset(15,24))
    drop_point = fixCorner.getTarget().offset(434, 214)
    dragDrop(slideCorner, drop_point)
    ################################
    click(find("1542138783631.png"))
#the end of the function, resizeInstallPlugIn

# adjust the STOMP macro window
#%%%%%%%%%%%%%%%%%%%%#
#popat(Location(2350,720))
#popup("have you opened STOMP macro? if yes, enter ok")
#t4= find("1542140074683.png")
#dragDrop(t4,Region(1936,226,10,10))
def openZenMacro():
    while(1):
        if not exists("1558982625101.png"):
            if not exists(Pattern("1558982393940.png").similar(0.80)):
                click(Location(1160, 20))
                wait(0.2)
            click(Pattern("1558982393940.png").similar(0.80))
            for i in range(2):
                type(Key.DOWN)
                wait(0.2)
            type(Key.ENTER)
            wait(0.2)
            
            t4= find(Pattern("1542140074683-1.png").similar(0.69))
            dragDrop(t4,Region(1936,226,10,10))
        else:
            break

resizeInstallPlugIn()
openZenMacro()
popup("LayOut tuned 4 STOMP! click OK to end")