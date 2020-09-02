#!/usr/bin/env python
import sys
import glob
import re
import json
from urllib2 import urlopen


from collections import defaultdict  # available in Python 2.5 and newer
from collections import Counter      # available in Python 2.5 and newer


debug  = False
nfiles = -1

class HtmlHistograms:
    htmllist=(
        'uk/index.html',
        'about/index.html',
        'systemrequirements/index.html',
        'download/index.html',
        'pop-ups/ConservationMomentum.html',
        'pool/index.html',
        'pool/collisions.html',
        'pop-ups/spherecollisions.html',
        'pool/masses.html',
        'annihilation/index.html',
        'lifetime/kaonlifetime.html',
        'pop-ups/decaytime.html',
        'motioninb/index.html',
        'lifetime/index.html',
        'neutrinos/index.html',
        'neutrinos/theory.html',
        'neutrinos/simulation.html',
        'higgs/index.html',
        'higgs/higgs.html',
        'higgs/detector.html',
        'higgs/measurement.html')
    
    
class LogFile:

    def __init__(self, infname="161118_LPPP/access-lppp-20161031.log"):
        self.fname      = infname
        self.content    = list()
        #self.htmldic    = defaultdict(int)
        self.htmldic    = Counter()
        self.countrydic = Counter()
        self.ipset      = set()
        self.readfile   = False
        self.parsedfile = False

    def SetName(self, inname):
        self.fname = inname

    def SetHtmlDic(self, indic):
        self.htmldic = indic

    def ReadFile(self):
        print("reading file " + self.fname)
        with open( self.fname, 'r' ) as f:
            self.content = f.readlines()
        print(str(len(self.content)) + " lines read from " + self.fname)
        self.readfile = True


    def ParseContent(self):
        if (not self.readfile):
            self.ReadFile()

        linecount = 0
        for thisline in self.content:
            linecount += 1
            if (debug):
                if (linecount < 10): print(thisline)
            thisline.strip('\n')
            htmlpos = thisline.find(".html")
            if (htmlpos > 0):
                spos = thisline.rfind("/", 0, htmlpos-2)
                spos = thisline.rfind("/", 0, spos)
                htmlname = thisline[ spos+1 : htmlpos+5 ]
                if (debug): 
                    if (linecount < 50): print htmlname
                

                # collect all IP addresses in the .html line
                fieldlist = thisline.split("-", 4)

                ipadd = fieldlist[1].lstrip(" ").rstrip(" ")
                if (debug): print("IP Address: 1: \"" + ipadd + "\"")

                if (ipadd.find("66.249.") > -1): continue # Google
                if (ipadd.find("46.229.") > -1): continue # DataWeb
                if (ipadd.find("157.55.") > -1): continue # Microsoft
                

                self.ipset.add( ipadd )
                self.htmldic[ htmlname ] += 1

 
    def PrintHtmlDic(self):
        print "\nsummary for file " + self.fname
        print "================================"
        for url in self.htmldic.keys():
            print url + "  ----  " + str( self.htmldic[ url ] )

    def GetHtmlDic(self):
        if (not self.parsedfile): self.ParseContent()
        return self.htmldic

    def GetCountryDic(self):
        if (not self.parsedfile): self.ParseContent()
        return self.countrydic
            
    def GetIPSet(self):
        if (not self.parsedfile): self.ParseContent()
        return self.ipset

    def PrintIPSet(self):
        print "\nsummary for file " + self.fname
        print "================================"
        for ipadd in self.ipset:
            print "\nIP Address: " + ipadd


            #data = str(urlopen('http://checkip.dyndns.com/').read())
            #print "data: " + data
            IP = re.compile(r'(\d+.\d+.\d+.\d+)').search(ipadd).group(1)
            url = 'http://ipinfo.io/' + IP + '/json'
            response = urlopen(url)
            data = json.load(response)
            
            org = data['org']
            city = data['city']
            country = data['country']
            reg = data['region']
        
            try:
                print 'Your IP detail:'
                print "Country: " + country
                print "Region: " + reg
                print "City: " + city
                print "Organisation: " + org
                print "IP: " + IP
            except:
                continue

            self.countrydic[ country ] += 1


    def GetIPSet(self):
        return self.ipset




class LogFileDir:

    def __init__(self, indirname="161118_LPPP"):
    	self.filelist      = list()
    	#self.htmldic       = defaultdict(int)
    	self.htmldic       = Counter()
        self.countrydic    = Counter()
    	self.ipset         = set()
    	self.dirname       = indirname
    	self.gotFileList   = False
    	self.parsedcontent = False

    def GetFiles(self):
        self.filelist = glob.glob(self.dirname + "/*.log")
        self.gotFileList = True

    def PrintFileList(self):
        if (not self.gotFileList): self.GetFiles()
        print "\n\nFile list:"
        print "============="
        for ifile in self.filelist:
            print ifile

    def ParseContent(self):
        if (not self.gotFileList): self.GetFiles()
        self.parsedcontent = True
        filecount=0
        for ifile in self.filelist:
            thisfile = LogFile(ifile)
            self.htmldic.update( thisfile.GetHtmlDic() )
            self.ipset.update( thisfile.GetIPSet() )
            #thisfile.PrintHtmlDic()
            #self.PrintHtmlDic()
            filecount += 1
            if (nfiles>0 and filecount>nfiles): break 

    def PrintHtmlDic(self):
        if (not self.parsedcontent): self.ParseContent()
        print "\n======================"
        print "summary for all files "
        print "======================"

        for url in self.htmldic.keys():
            print url + "  ----  " + str( self.htmldic[ url ] )

    def PrintCountryDic(self):
        if (not self.parsedcontent): self.ParseContent()
        print "\n=============================="
        print "country summary for all files "
        print "=============================="

        for cntry in self.countrydic.keys():
            print cntry + "  ----  " + str( self.countrydic[ cntry ] )

    def GetHtmlDic(self):
        if (not self.parsedcontent): self.ParseContent()
        return self.htmldic
            
    def GetIPSet(self):
        if (not self.parsedcontent): self.ParseContent()
        return self.ipset

    def PrintIPSet(self):
        print "\n======================"
        print "summary for all files "
        print "======================"
        for ipadd in self.ipset:
            print "\nIP Address: " + ipadd


            #data = str(urlopen('http://checkip.dyndns.com/').read())
            #print "data: " + data
            if (ipadd == None): continue
            if (ipadd == ""): continue
            if (ipadd == 'known"'): continue
            try:
                IP = re.compile(r'(\d+.\d+.\d+.\d+)').search(ipadd).group(1)
                url = 'http://ipinfo.io/' + IP + '/json'
                response = urlopen(url)
                data = json.load(response)
                org = data['org']
                city = data['city']
                country = data['country']
                reg = data['region']
            except:
                continue
            
            
            try:
                print 'Your IP detail:'
                print "Country: " + country
                print "Region: " + reg
                print "City: " + city
                print "Organisation: " + org
                print "IP: " + IP
            except:
                continue

            self.countrydic[country] += 1

# ExampleFile = LogFile()
# ExampleFile.ParseContent()
# ExampleFile.PrintHtmlDic()
# ExampleFile.PrintIPSet()


LogDir = LogFileDir()
LogDir.PrintFileList()
LogDir.PrintHtmlDic()
LogDir.PrintIPSet()
LogDir.PrintCountryDic()

