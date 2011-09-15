#!/usr/bin/python

__author__="stephen martin <me@stephen-martin.co.uk>"
__date__ ="$Sep 10, 2011 10:50:31 AM$"
versionNo ="1.0.1.1"


import os
import sys
import smtplib
import socket
from urllib import urlopen
import datetime
socket.setdefaulttimeout(60)




class Conf:
    def __init__(self):
        self.fileLocation="/opt/IPy/IPy.conf"
        self.mailServer=""
        self.mailServerAuth=""
        self.mailUser=""
        self.mailPass=""
        self.mailTo=""
        self.mailFrom=""

    def get(self):
        try:
            cFile = open(self.fileLocation,"r")
            for line in cFile:
                if "[mailServer]" in line:
                    self.mailServer = line.split("\"")[1]
                if "[mailServerAuth]" in line:
                    self.mailServerAuth = line.split("\"")[1]
                if "[mailUser]" in line:
                    self.mailUser = line.split("\"")[1]
                if "[mailPass]" in line:
                    self.mailPass = line.split("\"")[1]
                if "[mailFrom]" in line:
                    self.mailFrom = line.split("\"")[1]
                if "[mailTo]" in line:
                    self.mailTo = line.split("\"")[1]
            cFile.close()
            return 1
        except:
            return 0

    def save(self):
        try:
            cFile = open(self.fileLocation,"w")
            cFile.write("[mailServer]=\""+self.mailServer+"\n")
            cFile.write("[mailServerAuth]=\""+self.mailServerAuth+"\n")
            cFile.write("[mailUser]=\""+self.mailUser+"\n")
            cFile.write("[mailPass]=\""+self.mailPass+"\n")
            cFile.write("[mailFrom]=\""+self.mailFrom+"\n")
            cFile.write("[mailTo]=\""+self.mailTo+"\n")
            cFile.close()
            return 1
        except:
            return 0

    def show(self):
        print "Current Config:"
        print "--------------------------------------"
        print"mail server: "+self.mailServer
        print"mail server auth: "+self.mailServerAuth
        print"mail user: "+self.mailUser
        print"mail password: "+self.mailPass
        print"mail from: "+self.mailFrom
        print"mail to: "+self.mailTo
        print "--------------------------------------"
        
    def check(self):
        self.get()
        if self.mailServer!= "" and self.mailServerAuth!="" and self.mailUser!="" and self.mailPass!="" and  self.mailTo!="" and self.mailFrom!="":
            return 1
        else:
            return 0

    def setup(self):
        cfig=Conf()
        cfig.get()
        print "Welcome to setup"
        print "To accept a [default] leave blank"
        mailServer2 = raw_input("Mailserver host name:["+cfig.mailServer+"]")
        if mailServer2 !="":
            cfig.mailServer = mailServer2

        mailServerAuth2 = raw_input("Mailserver Authentication y/n:["+cfig.mailServerAuth+"]")
        if mailServerAuth2 !="":
            cfig.mailServerAuth= mailServerAuth2
        if cfig.mailServerAuth=="y":
            mailUser2 = raw_input("Mailserver username:["+cfig.mailUser+"]")
            if mailUser2 !="":

                cfig.mailUser = mailUser2
            mailPass2 = raw_input("Mailserver password:["+cfig.mailPass+"]")
            if mailPass2 !="":
                cfig.mailPass = mailPass2
        mailFrom2 = raw_input("Mail From:["+cfig.mailFrom+"]")
        if mailFrom2 !="":
            cfig.mailFrom = mailFrom2
        mailTo2 = raw_input("Mail To:["+cfig.mailTo+"]")
        if mailTo2 !="":
            cfig.mailTo = mailTo2
        if cfig.save()==1:
            print "setup complete exiting...."
        else:
            print "error saving to config file... exiting"

class Test:
    def __init__(self):
        self.result=""
        self.fault=""


    def mail_test(self):
        cfig = Conf()
       
        try:
            server = smtplib.SMTP(cfig.mailServer)

            if cfig.mailSeverAuth=="y":
                server.login(cfig.mailUser, cfig.mailPass)
            server.quit()

            return 1
        except:
            return 0

    def net_test(self):
        ping = os.system("ping -c 1 www.google.co.uk > /dev/null")
        if ping==0:
            return 1
        else:
            print "Net Test: Internet or DNS down. exiting......"
            return 0

    def self_test(self):
        self.result="1"
        cfig = Conf()
        cfig.get()
        if cfig.check() ==0:
            
            self.fault="There was a problem with your config file please run IPy.oy -s"
            self.result=0
        if self.mail_test()==0:
            
            self.fault=self.fault+"There was a problem with your mailserver"
            self.result=0
        if self.result==0:
            return self.fault
        else:
            return 1





def selfTest():
    #check conf file
    fail =0
    fault =""
    cfig = Conf()
    if cfig.check()==0:
        fail =1
        fault = "email.conf failed test please run email.py -s\n"
    #check intenet connection
    ping = os.system("ping -c 1 www.google.co.uk > /dev/null")
    if ping!=0:
        fail = 1
        fault=fault+"Intenet or DNS down\n"
   
    socket.setdefaulttimeout(10)
    if fail!=1:
        tst =Test()
        if tst.mail_test()==0:
            fault=fault+"Mailserver wont connect... check connection and config IPy -s"
            fail=1
    socket.setdefaulttimeout(60)
    if fail==1:
        logger("ERROR","Self test FAIL: "+fault)
        print "Self test FAIL: "+fault
        return fault
    else:
        return 1



def header():
    print "###################################################"
    print "IPy Version: "+versionNo
    
    print "A simple program to monitor your external IP"
    print "and mail you if it changes"
    print ""
    print "Written by Stephen Martin <me@stephen-martin.co.uk>"
  

def setup():
    cfig=Conf()
    print "Welcome to setup"
    print "To accept a [default] leave blank"
    mailServer2 = raw_input("Mailserver host name:["+cfig.mailServer+"]")
    if mailServer2 !="":
        cfig.mailServer = mailServer2
    
    mailServerAuth2 = raw_input("Mailserver Authentication y/n:["+cfig.mailSeverAuth+"]")
    if mailServerAuth2 !="":
        cfig.mailSeverAuth= mailServerAuth2
    if cfig.mailSeverAuth=="y":
        mailUser2 = raw_input("Mailserver username:["+cfig.mailUser+"]")
        if mailUser2 !="":

            cfig.mailUser = mailUser2
        mailPass2 = raw_input("Mailserver password:["+cfig.mailPass+"]")
        if mailPass2 !="":
            cfig.mailPass = mailPass2
    mailFrom2 = raw_input("Mail From:["+cfig.mailFrom+"]")
    if mailFrom2 !="":
        cfig.mailFrom = mailFrom2
    mailTo2 = raw_input("Mail To:["+cfig.mailTo+"]")
    if mailTo2 !="":
        conf['mailTo'] = mailTo2
    saveConf(conf)
    print "setup complete exiting...."



def sendMail(ip):

    cfig=Conf()
    head = 'To:' +conf['mailTo'] + '\n' + 'From: ' + cfig.mailFrom+ '\n' + 'Subject:External IP changed \n'
    msg = head + '\n Your IP address has changed to:'+ip+'  \n\n'
    try:
     
        server2 = smtplib.SMTP(cfig.mailServer)
        if cfig.mailSeverAuth=="y":
           
            server2.login(cfig.mailUser,cfig.mailPass)
        server2.sendmail(cfig.mailFrom,conf['mailTo'], msg)
        server2.quit()
        logger("Mail","Email successfully sent to "+conf['mailTo'])
    except:
        print "failed to connect to server"
        logger("ERROR","Email failed to send to "+conf['mailTo'])

def getCurrentIP():
    ip = urlopen("http://www.stephen-martin.co.uk/index.php/IPy/externalip").read()
    return ip

def getLastIP():
    try:
        infile = open("/opt/IPy/IPy.dat","r")
        oldIp = infile.readline()
        infile.close()
        return oldIp
    except:
        print "file open failed :("
        return 0

def saveIP(ip):
    try:
        infile = open("/opt/IPy/IPy.dat","w")
        infile.write(ip)
        infile.close()
        return 1
    except:
        infile.close()
        return 0

def logger(type,text):
    now = datetime.datetime.now()
    logfile =open("/opt/IPy/IPy.log","a")
    logfile.write(now.strftime("%Y-%m-%d %H:%M")+" "+type+": "+text+"\n")
    logfile.close()

def run():
    cfig=Conf()
    logger("RUN","The program was executed in run mode\n")
    if getLastIP():
        oldIp = getLastIP()
        print "old ip: "+oldIp

        ip = getCurrentIP()

        try:
            socket.inet_aton(ip)
            print "current ip: "+ip

            if not oldIp == ip:
                logger("IP","External IP Changed from "+oldIp+" to "+ip+"\n")
                print "Changed"
                try:
                    saveIP(ip)
                    sendMail(ip)
                    print "mail sent to:"+conf['mailTo']
                except:
                    print "failed to send mail..."
            else:
                 logger("IP","External IP has not changed")
                 print "no change exiting"
        except:
            print "invalid "



if __name__ == "__main__":
    if  len(sys.argv)==1:
        tst=Test()
        res = tst.self_test()
        if tst.result==1:
            run()
        else:
            print res
        
        
    elif len(sys.argv)==2:
        args=['-c','-o','-C','-s']
        tst = Test()
        cfig = Conf()
        cfig.get()
        if sys.argv[1]=="-c" and tst.net_test()==1:
          
            print "Current IP: "+getCurrentIP()
        if sys.argv[1]=="-C":
           
            cfig.show()

        elif sys.argv[1]=="-o":
            logger("RUN","The program was executed in get last IP mode\n")
            print "Last IP: "+getLastIP()
        elif sys.argv[1]=="-s":
           
            cfig.setup()
        elif sys.argv[1]=="-r":
            
            print getConfig()
        elif sys.argv[1]=="-a":

            print header()
        elif sys.argv[1]=="-t":
            tst = Test()
           
            if tst.result ==1:
                print "test passed"
            else:
                print tst.fault
            
        elif sys.argv[1] not in args:
            print "Usage: ./IPy.py [option]"
            print ""
            print "[Options]"
            print "[-c] Print current external IP to screen"
            print "[-C] Print current config to screen"
            print "[-o] Print last known external IP to screen"
            print "[-s] enter setup"
            print "[-a] Prints the about IPy info to screen"
