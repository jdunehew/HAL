# Script to send picture to user by text or email
# Author - Jeff Dunehew
# April 2018

#USER - HAL.10K.2018@gmail.com
#PW - HAL10K2018!

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#Notes
# - Need to combine text and email functions into one. Code uses very similar syntax.


SmsGateways = [
   'tmomail.net',             # tmobile
   'mms.att.net',             # at&t
   'vtext.com',               # verizon
   'page.nextel.com',         # sprint
   'sms.mycricket.com',       # cricket 
   'vmobl.com',               # virgin mobile US
   'sms.myboostmobile.com'    # boost mobile
    ]

def sendText(emailaddress, personname, picfilename):


    for gateway in SmsGateways:
        fromaddr = "HAL.10K.2018@gmail.com"
        toaddr = emailaddress + "@" + gateway
        msg = MIMEMultipart()
        #msg['FROM'] = fromaddr
        #msg['To'] = toaddr
        #msg['Subject'] = "Email from HAL10K!"
        body = "Hello, it was nice to meet you " + personname + "."
        msg.attach(MIMEText(body, 'plain'))
        attachment = open(picfilename, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % picfilename)
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "HAL10K2018!")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        

        print("To Address: " + toaddr)
        
    server.quit()
    return;

##def sendText(phonenumber, personname, picfilename, picfilepath):
##    server = smtplib.SMTP("smtp.gmail.com", 587)
##    server.starttls()
##    server.login('HAL.10K.2018@gmail.com', 'HAL10K2018!')
##    #Need to figure out from user what service their phone uses
##    #Sprint:@pm.sprint.com
##    #Verizon:@vtext.com
##    #AT&T:@mms.att.net
##
##    filename = "image.jpg"
##    attachment = open("/home/pi/Pictures/HAL10K/" + filename, "rb")
##    
##    part = MIMEBase('application', 'octet-stream')
##    part.set_payload((attachment).read())
##    encoders.encode_base64(part)
##    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
##                
##    msg.attach(MIMEText(body, 'plain'))
##    msg.attach(part)
##
##    text = msg.as_string()
##    
##    phonedestination = phonenumber+"@mms.att.net"
##    server.sendmail('HAL10K', phonedestination, text)
##    return;

