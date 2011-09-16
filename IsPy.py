#!/usr/bin/python
# Copyright 2011, Stephen Martin
# This program is distributed under the terms of the GNU General Public License 
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
        self.fileLocation="IsPy.conf"
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
            cFile.write("[mailServer]=\""+self.mailServer+"\"\n")
            cFile.write("[mailServerAuth]=\""+self.mailServerAuth+"\"\n")
            cFile.write("[mailUser]=\""+self.mailUser+"\"\n")
            cFile.write("[mailPass]=\""+self.mailPass+"\"\n")
            cFile.write("[mailFrom]=\""+self.mailFrom+"\"\n")
            cFile.write("[mailTo]=\""+self.mailTo+"\"\n")
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

class IP:
    def __init__(self):
        self.address =""
    
    def getCurrent(self):
        self.address = urlopen("http://www.stephen-martin.co.uk/index.php/IPy/externalip").read()
        
    
    def getLast(self):
        try:
            infile = open("IsPy.dat","r")
            self.address = infile.readline()
            infile.close()
            return 1
        except Exception, e:
            print "file open failed :("+" "+e
            return 0
    def testIp(self,ip):
        try:
            socket.inet_aton(ip)
            return 1
        except:
            return 0
    
    def save(self,ip):
        try:
            infile = open("IsPy.dat","w")
            infile.write(ip)
            infile.close()
            return 1
        except:
            return 0

class Mailer:
    def __init__(self):
        self.mailTo =""
        self.mailFrom =""
        self.subject = ""
        self.body = ""
    def send(self):
        cfig=Conf()
        cfig.get()
        head = 'To:' +self.mailTo + '\n' + 'From: ' + self.mailFrom+ '\n' + 'Subject:'+self.subject+' \n'
        msg = head + self.body+"\n\n"
        try:
            server2 = smtplib.SMTP(cfig.mailServer)
            if cfig.mailServerAuth=="y":
                server2.login(cfig.mailUser,cfig.mailPass)
            server2.sendmail(cfig.mailFrom,cfig.mailTo, msg)
            server2.quit()
            log = Logger()
            log.log("Mail", "Email successfully sent to "+cfig.mailTo)
            
            return 1
        except smtplib.SMTPException,e:
            print "failed to connect to mail server \n"+str(e)
            log = Logger()
            log.log("ERROR", "Email failed to send to "+cfig.mailTo)
            return 0
        
        
        
            
class Test:
    def __init__(self):
        self.result=""
        self.fault=""

    def mail_test(self):
        cfig = Conf()
        cfig.get()
       
        try:
            server = smtplib.SMTP(cfig.mailServer)
            #server.connect(cfig.mailServerAuth,25)
            if cfig.mailServerAuth=="y":
                server.login(cfig.mailUser, cfig.mailPass)
            server.quit()

            return 1
        except smtplib.SMTPException, e:
            print e
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
        if cfig.check()==0:
            
            self.fault="There was a problem with your config file please run IPy.oy -s"
            self.result=0
        if self.net_test()==0:
            self.result=0
            print "net test failed"
        
        if self.mail_test()==0:
            
            self.fault=self.fault+"There was a problem with your mailserver"
            self.result=0
        if self.result==0:
            return 0
        else:
            return 1

class Logger:
    def __init__(self):
        
        self.type =""
        self.text =""
        self.time = ""
        
    
    def log(self,logType,logText):
        now = datetime.datetime.now()
        self.time = now.strftime("%Y-%m-%d %H:%M")
        self.type = logType
        self.text = logText
        logfile =open("IsPy.log","a")
        logfile.write(self.time+" "+self.type+": "+self.text+"\n")
        logfile.close()
        
        
def header():
    print "###################################################"
    print "IPy Version: "+versionNo
    
    print "A simple program to monitor your external IP"
    print "and mail you if it changes"
    print ""
    print "Written by Stephen Martin <me@stephen-martin.co.uk>"
  

def run():
    cfig=Conf()
    cfig.get()
    log = Logger()
    log.log("RUN","The program was executed in run mode\n")
    oIp = IP()
    if oIp.getLast()==1:
        print "old ip: "+oIp.address
        cIp =IP()
        cIp.getCurrent()
        if cIp.testIp(cIp.address)==1:
            print "current ip: "+cIp.address
            if not oIp.address == cIp.address:
                log.log("IP","External IP Changed from "+oIp.address+" to "+cIp.address+"\n")
                print "Changed"
                try:
                    cIp.save(cIp.address)
                except Exception,e:
                    print "Failed to save current IP to file"+" "+e
                mail = Mailer()
                mail.mailTo=cfig.mailTo
                mail.mailFrom=cfig.mailFrom
                mail.subject="External IP address has changed"
                mail.body ="Your external IP address has changed from "+oIp.address+" to: "+cIp.address +"\n"
                try:
                    mail.send()
                    print "mail sent to:"+cfig.mailTo
                except Exception,e:
                    print "failed to send mail..."+str(e)
            else:
                log.log("IP","External IP has not changed")
                print "no change exiting"
        else:
            #ip address was invalid do something
            print "there was a problem parsing the current IP exiting...."

if __name__ == "__main__":
    if  len(sys.argv)==1:
        tst=Test()
        res = tst.self_test()
        if tst.self_test()==1:
            run()
        else:

            print res
    elif len(sys.argv)==2:
        args=['-c','-o','-C','-s']
        tst = Test()
        cfig = Conf()
        cfig.get()
        if sys.argv[1]=="-c" and tst.net_test()==1:
            cIp = IP()
            cIp.getCurrent()
            print "Current IP: "+cIp.address
        if sys.argv[1]=="-C":
            cfig.show()
        elif sys.argv[1]=="-o":
            oIp = IP()
            oIp.getLast()
            log=Logger()
            log.log("RUN","The program was executed in get last IP mode\n")
           
            print "Last IP: "+oIp.address
        elif sys.argv[1]=="-s":
            cfig.setup()
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