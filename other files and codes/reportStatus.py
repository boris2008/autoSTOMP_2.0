# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 23:18:08 2019

@author: boris
"""
import time
import os
def sendFail():
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "xxxx@gmail.com"  # Enter your address
    receiver_email = "xxxxx@gmail.com"
    #password = input("Type your password and press enter: ")
    password = "##########"
    message = MIMEMultipart("alternative")
    message["Subject"] = "STOMP failed"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = """\
           send from python
           """
    html = """\
    <html>
      <body>
        <p>STOMP failed<br>
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
def sendSuccess(MESSAGE):
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "xxxxxx@gmail.com"  # Enter your address
    receiver_email = "xxxxxx@gmail.com"
    #password = input("Type your password and press enter: ")
    password = "################"
    message = MIMEMultipart("alternative")
    message["Subject"] = MESSAGE
    message["From"] = sender_email
    message["To"] = receiver_email
    text = """\
           send from python
           """
    html = """\
    <html>
      <body>
        <p>this proposed job is done!<br>
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


f = open("C:/ZEN/STOMPstatus.txt")

#1 for succeed, 0 for fail
l1 = f.readline()#contains the .pos file
l2= f.readline()
l2=int(l2)
l3=f.readline()#it contains other information can explict in the email title
f.close()
if l2==1:
    sendSuccess(l3)
else:
    sendFail()
    
        