#!/usr/bin/python

__author__="stephen martin <me@stephen-martin.co.uk>"
__date__ ="$Sep 10, 2011 10:50:31 AM$"
versionNo ="1.0.1.1"


import os
import sys
import smtplib
import socket
from urllib import urlopen
socket.setdefaulttimeout(60)
def selfTest():
    #check conf file
    fail =0
    fault =""
    if checkConf()==0:
        fail =1
        fault = "email.conf failed test please run email.py -s\n"
    #check intenet connection
    ping = os.system("ping -c 1 www.google.co.uk > /dev/null")
    if ping!=0:
        fail = 0
        fault=fault+"Intenet or DNS down\n"
    socket.setdefaulttimeout(10)
    if mailTest()==0:
        fault=fault+"Mailserver wont connect... check connection and config emailip -s\n"
        fail=1
    socket.setdefaulttimeout(60)
    if fail==1:
        print "Self test FAIL: "+fault
        return fault
    else:
        return 1

def netTest():
    ping = os.system("ping -c 1 www.google.co.uk > /dev/null")
    if ping==0:
        return 1
    else:
        print "Net Test: Internet or DNS down. exiting......"
        return 0

def mailTest():
    try:
        server = smtplib.SMTP(mailServer)

        if conf[mailServerAuth]=="y":
            server.login(mailUser,mailPass)
        server.quit()
        return 1
    except:
        return 0





def header():
    print "###################################################"
    print "EmailIP Version: "+versionNo
    
    print "A simple program to monitor your external IP"
    print "and mail you if it changes"
    print ""
    print "Written by Stephen Martin <me@stephen-martin.co.uk>"
  


def getConf():
    mailServer=""
    mailServerAuth=""
    mailUser=""
    mailPass=""
    mailFrom=""
    mailTo=""
    cFile = open("/opt/emailip/emailip.conf","r")
    for line in cFile:
        if "[mailServer]" in line:
            mailServer = line.split("\"")[1]
        if "[mailServerAuth]" in line:
            mailServerAuth = line.split("\"")[1]
        if "[mailUser]" in line:
            mailUser = line.split("\"")[1]
        if "[mailPass]" in line:
            mailPass = line.split("\"")[1]
        if "[mailFrom]" in line:
            mailFrom = line.split("\"")[1]
        if "[mailTo]" in line:
            mailTo = line.split("\"")[1]

    conf={"mailServer":mailServer,"mailServerAuth":mailServerAuth,"mailUser":mailUser,"mailPass":mailPass,"mailFrom":mailFrom,"mailTo":mailTo}
    cFile.close()
    return conf

def saveConf(conf):
    cFile = open("/opt/emailip/emailip.conf","w")
    cFile.write("[mailServer]=\""+conf['mailServer']+"\"\n")
    cFile.write("[mailServerAuth]=\""+conf['mailServerAuth']+"\"\n")
    cFile.write("[mailUser]=\""+conf['mailUser']+"\"\n")
    cFile.write("[mailPass]=\""+conf['mailPass']+"\"\n")
    cFile.write("[mailFrom]=\""+conf['mailFrom']+"\"\n")
    cFile.write("[mailTo]=\""+conf['mailTo']+"\"\n")
    cFile.close()

def showConf():
    conf = getConf()
    print "Current Config:"
    print "--------------------------------------"
    print"mail server: "+conf['mailServer']
    print"mail server auth: "+conf['mailServerAuth']
    print"mail user: "+conf['mailUser']
    print"mail password: "+conf['mailPass']
    print"mail from: "+conf['mailFrom']
    print"mail to: "+conf['mailTo']
    print "--------------------------------------"

def checkConf():
    conf = getConf()
    if conf['mailServer'] != "" and conf['mailUser']!="" and conf['mailPass']!="" and conf['mailTo']!="" and conf['mailFrom']!="":
        return 1
    else:
        return 0

def setup():
    conf = getConf()
    print "Welcome to setup"
    print "To accept a [default] leave blank"
    mailServer2 = raw_input("Mailserver host name:["+conf['mailServer']+"]")
    if mailServer2 !="":
        conf['mailServer'] = mailServer2
    
    mailServerAuth2 = raw_input("Mailserver Authentication y/n:["+conf['mailServerAuth']+"]")
    if mailServerAuth2 !="":
        conf['mailServerAuth']= mailServerAuth2
    if conf['mailServerAuth']=="y":
        mailUser2 = raw_input("Mailserver username:["+conf['mailUser']+"]")
        if mailUser2 !="":

            conf['mailUser'] = mailUser2
        mailPass2 = raw_input("Mailserver password:["+conf['mailPass']+"]")
        if mailPass2 !="":
            conf['mailPass'] = mailPass2
    mailFrom2 = raw_input("Mail From:["+conf['mailFrom']+"]")
    if mailFrom2 !="":
        conf['mailFrom'] = mailFrom2
    mailTo2 = raw_input("Mail To:["+conf['mailTo']+"]")
    if mailTo2 !="":
        conf['mailTo'] = mailTo2
    saveConf(conf)
    print "setup complete exiting...."



def sendMail():
    conf = getConf()
    header = 'To:' + mailTo + '\n' + 'From: ' + mailFrom + '\n' + 'Subject:External IP changed \n'
    msg = header + '\n Your IP address has changed to:'+ip+'  \n\n'
    try:
        server = smtplib.SMTP(mailServer)
        if conf[mailServerAuth]=="y":
            server.login(mailUser,mailPass)
        server.sendmail(mailFrom, mailTo, msg)
        server.quit()
    except:
        print "failed to connect to server"

def getCurrentIP():
    ip = urlopen("http://www.stephen-martin.co.uk/index.php/emailip/externalip").read()
    return ip

def getLastIP():
    try:
        infile = open("/opt/emailip/emailip.dat","r")
        oldIp = infile.readline()
        infile.close()
        return oldIp
    except:
        print "file open failed :("
        return 0

def saveIP(ip):
    try:
        infile = open("/opt/emailip/emailip.dat","w")
        infile.write(ip)
        infile.close()
        return 1
    except:
        infile.close()
        return 0

def run():
    if getLastIP():
        oldIp = getLastIP()
        print "old ip: "+oldIp

        ip = getCurrentIP()

        try:
            socket.inet_aton(ip)
            print "current ip: "+ip

            if not oldIp == ip:
                print "Changed"
                try:
                    saveIP(ip)
                    sendMail()
                    print "mail sent to:"+mailTo
                except:
                    print "failed to send mail..."
            else:
                print "no change exiting"
        except:
            print "invalid"

conf = getConf()
mailServer  = conf['mailServer']
mailUser    = conf['mailUser']
mailPass    = conf['mailPass']
mailFrom    = conf['mailFrom']
mailTo      = conf['mailTo']

if __name__ == "__main__":
    if  len(sys.argv)==1 and selfTest()==1:
        run()
        
        
    elif len(sys.argv)==2:
        args=['-c','-o']
        if sys.argv[1]=="-c" and netTest()==1:
          
            print "Current IP: "+getCurrentIP()
        if sys.argv[1]=="-C":
          
            print showConf()
        elif sys.argv[1]=="-o":
           
            print "Last IP: "+getLastIP()
        elif sys.argv[1]=="-s":
           
            print setup()
        elif sys.argv[1]=="-r":
            
            print getConfig()
        elif sys.argv[1]=="-a":

            print header()
        elif sys.argv[1]=="-t":
            res = selfTest()
            if res ==1:
                print "test passed"
            else:
                print res
            
        elif sys.argv[1] not in args:
            print "Usage: ./emailip.py [option]"
            print ""
            print "[Options]"
            print "[-c] Print current external IP to screen"
            print "[-C] Print current config to screen"
            print "[-o] Print last known external IP to screen"
            print "[-s] enter setup"
            print "[-a] Prints the about emailip info to screen"
