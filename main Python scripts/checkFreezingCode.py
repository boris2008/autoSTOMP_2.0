# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 23:18:08 2019

@author: boris
"""
import time
import os
f = open("C:/ZEN/frozentimeTolerance.txt")
dire = "C:/ZEN/"#fixed directory to store the position files for ZEN BLACK
sdir="C:/Users/"
timepass =f.readline()
timepass =timepass.replace('\n','')
timepass =int(timepass)
print(timepass,type(timepass))
f.close()

def sendWMess():
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "*********@gmail.com"  # Enter your address
    #receiver_email = "**********@gmail.com"  # Enter receiver address
    #do multiple receivers, separated by ","
    receiver_email = "$$$$$$$$@gmail.com"
    #receiver_email = "####@virginia.edu,######@gmail.com"
    #password = input("Type your password and press enter: ")
    password = "@@@@@@@@@@@"
    message = MIMEMultipart("alternative")
    message["Subject"] = " the code freezes for a while"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = """\
           send from python
           """
    html = """\
    <html>
      <body>
        <p>the code freezes for a while<br>
        </p>
      </body>
    </html>
    """
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email.split(","),message.as_string()
    )

def checkTime(timepass):
    #timepass is in second
    
    import datetime
    #import os
    #get the current time
    tc= time.time()
    ct = datetime.datetime.fromtimestamp(tc).strftime('%Y-%m-%d %H:%M:%S')
    pathValueFile =''.join(['C:\\ZEN', '\\','currentInfo.txt'])
    
    tori=tc
    orit=ct
    if (os.path.isfile(pathValueFile)):
        with open(pathValueFile,"r") as f:
            tori= f.readline()
            tori= float(tori)
            orit = f.readline()
        time.sleep(1)
    print("old time",tori)
    print(orit)
    print("current time",tc)
    print(ct)
    x=0
    gap = tc-tori
    print("time passed ",gap)
    if(float(tori)):
        if(gap>timepass):
            print("the logTime code freeze for too long!")
            x=True
    return (x)
if(1):
    if(checkTime(timepass)):
        pathValueFile =''.join(['C:\\ZEN', '\\','currentInfo.txt'])
        if (os.path.isfile(pathValueFile)):
            os.remove(pathValueFile)
        time.sleep(1)

while(True):
    if(checkTime(timepass)):
        sendWMess()
        break
    time.sleep(timepass)
    
        