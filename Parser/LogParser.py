import glob
import re
import json
from datetime import datetime, timedelta
from urllib.request import urlopen
from collections import Counter
from bokeh.io import show, output_file
from bokeh.plotting import figure   

debug = False

# this class parses individual log files
###########################
class LogFile:

    def __init__(self, n):    # constructor, argument = number of files to parse

        # intialise variables
        self.files = glob.glob(r'C:\Users\Iliya Frolov\LPPP\UsageParser\LPPP_Logs\*.log') # files stored from the path specified
        self.content = list()                                  # lines from log file stored in list
        self.htmldic = Counter()                               # dictionary of html name
        self.countrydic = Counter()                            # dictionary of countries
        self.ipinfodic = dict()                                # dictionary: key = ip address, value = ip info
        self.requests_per_ip_dic = Counter()                   # dictionary: key = ip address, value = no. of requests
        self.sessionidinfo_dic = dict()                        # dictionary: key = session ID, value = html; date; time
        self.time_on_module = dict()
        self.time_dic = dict()                                 # dictionary: key = module, value = total time spent                     
        self.module_list = [
            'experiment.html', 
            'index_en-GB.html', 
            'index.html', 
            'detector.html', 
            'ConservationK-Energy.html', 
            'ConservationMomentum.html',
            'collisions.html', 
            'joiningcentres.html', 
            'components.html', 
            'momentum.html', 
            'masses.html', 
            'calculation.html', 
            'energy1.html', 
            'measurement.html', 
            'mexicanHat.html',
            'higgs.html', 
            'information.html',
            'theory.html',
            'simulation.html'
        ]

        self.timeonmodule_dic = {module: {
            '0<x<=10': 0,
            '10<x<=20': 0,
            '20<x<=30': 0,
            '30<x<=40': 0,
            '40<x<=50': 0,
            '50<x<=60': 0,
            '60<x': 0
        } for module in self.module_list
        }
     
        # read the file
        self.readFile(n)

        # parse the content
        self.parseContent(n)

    def readFile(self, n):
        print(f"Reading {n} file(s)...")
        
        for i, a_file in enumerate(self.files):                                   
            print(f"\nReading file {a_file}")

            with open(a_file, 'r') as f:                    # opens the file, 'r' for read, 'with' is used for clean-up
                self.content.append(f.readlines())                    # 'readlines' returns a list of all the lines

            print(f"{len(self.content[i])} lines read.")

            if i == n-1:
                break

    # parses individual file, finds IP, gets IP info, finds HTML's, session ID's and corresponding info
    #############################
    def parseContent(self, n):

        for i in range(n):
            line_count = 0

            for this_line in self.content[i]:
                line_count += 1
                this_line.strip('\n')

                # find IP address using REGEX or line.split() depending on IPv4 or IPv6
                ipaddress = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', re.ASCII).search(this_line)  # finds IPv4s

                if ipaddress:
                    ipaddress = ipaddress.group()
                    ip_index = this_line.find(ipaddress)

                    if not (this_line[ip_index - 2] == "-" or this_line[ip_index - 2] == "\""):
                        space_position = this_line.rfind(" ", 0, ip_index - 2)          # IPv6 selection from 2 IP addresses
                        ipaddress = this_line[space_position+1: ip_index-1]
                else:
                    fieldlist = this_line.split(" - ", 4)                               # IPv6 selection from 1 IP address
                    ipaddress = fieldlist[1].lstrip(" ").rstrip(" ")

                if debug: 
                    print(f"Line {line_count} : {ipaddress}")

                # skip bots
                if "bot" in this_line or "66.249." in ipaddress or "46.229." in ipaddress or "157.55." in ipaddress:
                    continue

                # check if IP info has been retrieved for this IP, if not store it in dictionary
                if ipaddress not in self.ipinfodic:
                  try:
                    data = self.getIPData(ipaddress)
                    self.countrydic[data['country']] += 1
                    self.ipinfodic[ipaddress] = (
                        f"================================\n"
                        f"IP: {data['ip']}\n"
                        f"Organisation: {data['org']}\n"
                        f"City: {data['city']}\n"
                        f"Region: {data['region']}\n"
                        f"Country: {data['country']}\n\n"
                        )

                  except:
                    raise Exception("http://ipinfo.io/ip/json will not take any more requests. IP info unretrievable.")

                # html stuff
                html_name = self.findHTMLinLine(this_line)

                if html_name != "":
                    self.requests_per_ip_dic[ipaddress] += 1
                    self.htmldic[html_name] += 1

                    if debug: 
                        print(f"Html name: {html_name}")

                # find session ID using regex
                session_id = re.compile(r'(LPPPSession=\d+)', re.ASCII).search(this_line)

                if session_id:
                    session_id = session_id.group()[12:]

                    if debug: 
                        print(f"Session ID: {session_id}")

                    if session_id not in self.sessionidinfo_dic:
                        self.sessionidinfo_dic[session_id] = list()

                    # if theres a html in the session ID line, store the html, date, time under the session ID key
                    if html_name != "":
                        date_time = this_line[this_line.find(" [")+2: this_line.find("] ")]
                        session_info = f"{html_name}, date/time visited: {date_time}"
                        self.sessionidinfo_dic[session_id].append(session_info)
    
        # finds the time spent on each module per session id, how much time was spent on each module by everyone,
        # and how many users spent a particular amount of time on a module.
        for sessionid, info in self.sessionidinfo_dic.items(): 
            time_visited = self.timeVisited(info)
            
            if len(time_visited) > 1:
                
                self.time_on_module[sessionid] = [(time_visited[i][0], time_visited[i+1][1]-time_visited[i][1]) 
                    for i in range(len(time_visited)-1) 
                    ]    # create a list of tuples in the form ('module', 'time spent on module') 

                self.timeTotal(self.time_on_module[sessionid])

                for module in self.module_list:
                    self.timeOnModule(self.time_on_module[sessionid], module) 
        
        print(f"Successfully read {n} file(s)!")

    # locates html
    ###############
    def findHTMLinLine(self, line):
        fieldlist = line.split(" - ", 4)
        line = fieldlist[0]
        html_position = line.find(".html")
        html_name = ""

        if html_position != -1:
            slash_position = line.rfind("/", 0, html_position - 2)
            slash_position = line.rfind("/", 0, slash_position)
            html_name = line[slash_position+1: html_position+5]

            if "www" in html_name:
                html_name = html_name[4:]      # removes www
        
        return html_name
    
     # returns IP info using website, website has limited no. of uses
    ###################################
    def getIPData(self, ip):
        url = f"http://ipinfo.io/{ip}/json"
        response = urlopen(url)

        return json.load(response)

    # prints all HTML's and number of hits
    ########################################
    def printHTMLInfo(self):
        print(f"\nHTML summary for files")
        print("================================")
        for url in self.htmldic.keys():
            print(f"{url}  ----  {self.htmldic[url]}")

    # prints session ID, corresponding html, date, time and no. of unique session ID's
    ###################################
    def printSessionIDInfo(self):

        for sessionid in self.sessionidinfo_dic:
            print("\n=================")
            print(f"Session ID: {sessionid}")

            if len(self.sessionidinfo_dic[sessionid]) > 0:

                for info in self.sessionidinfo_dic[sessionid]:
                    print(info)

        print(f"\n\nNumber of unique sessions ID's: {len(self.sessionidinfo_dic.keys())}")

    def printCountryInfo(self):
        print(f"\nCountry summary for files")
        print("================================")

        for country in self.countrydic.keys():
            print(f"{country}  ----  {self.countrydic[country]}")

    def printIPInfo(self):
        requests = 0

        for ip in self.requests_per_ip_dic.keys():
            requests += self.requests_per_ip_dic[ip]         # adds up the total requests in the counter

        av_requests = requests/len(self.ipinfodic.keys())    # average requests per IP

        print(f"\nIP summary for files")

        for info in self.ipinfodic.keys():
            print(self.ipinfodic[info])

        print(f"\n\nNumber of unique IP addresses: {len(self.ipinfodic.keys())}")
        print(f"Average number of requests per IP address: {float(av_requests)}")

    # finds how much time was spent on each module per session id
    #############
    def timeVisited(self, info):
        time_visited = [()]
        
        for line in info:
            module = re.search("/.*,", line).group().strip("/,") # obtains the link of the module as a string
                
            if module not in time_visited[-1]:
                time_visited.append((module, datetime.strptime(re.search("\d\d/.*:\d\d", line).group(), '%d/%b/%Y:%H:%M:%S'))) # appends a tuple in the form ('module', 'date and time accessed')

        time_visited.pop(0)

        return time_visited

    # finds how much time was spent on each module by everyone
    ########################
    def timeTotal(self, time_on_module):
        
        for module in time_on_module:

            if module[0] in self.time_dic: # checks if module is in the dictionary as a key, if not, adds it as a new key
                self.time_dic[module[0]] += module[1]
                    
            else:
                self.time_dic[module[0]] = module[1]
    
    # prints the relevant data regarding the time spent on modules
    ###############
    def printTimeInfo(self):
       
        for sessionid in self.time_on_module:
            time_on_site = timedelta(hours=0, minutes=0, seconds=0)
       
            print("\n=================", f"\nSession ID: {sessionid}")

            if self.time_on_module[sessionid]:
                
                for module in self.time_on_module[sessionid]:
                    time_on_site += module[1]
                    print(f"Time spent on module: {module[0]} - {module[1]}")

                print(f"\nTotal time spent on site: {time_on_site}")

        print("\n=================", f"\nTotal time spent on all pages: ")

        for module, timestamp in self.time_dic.items():
            print(f"{module} - {timestamp}")
    
    # finds the particular amount of time spent on a module by everyone
    ###############
    def timeOnModule(self, time_on_module, module):   
        total_module = 0 

        for element in time_on_module:

            if element[0] == module:
                total_module += element[1].total_seconds() 
    
        if total_module <= 600 and total_module > 0:
            self.timeonmodule_dic[module]['0<x<=10'] += 1

        elif total_module <= 1200 and total_module > 600:
            self.timeonmodule_dic[module]['10<x<=20'] += 1
        
        elif total_module <= 1800 and total_module > 1200:
            self.timeonmodule_dic[module]['20<x<=30'] += 1
        
        elif total_module <= 2400 and total_module > 1800:
            self.timeonmodule_dic[module]['30<x<=40'] += 1
        
        elif total_module <= 3000 and total_module > 2400:
            self.timeonmodule_dic[module]['40<x<=50'] += 1
        
        elif total_module <= 3600 and total_module > 3000:
            self.timeonmodule_dic[module]['50<x<=60'] += 1
        
        elif total_module > 3600:
            self.timeonmodule_dic[module]['60<x'] += 1

# opens histogram in browser, arguments = title of histogram; dictionary to use; width of histogram; x-axis title;
# y-axis title
# dictionaries: .htmldic, .countrydic, .requests_per_ip_dic, .time_dic, .timeonmodule_dic[module]
###################################
def showHTMLhistogram(title, dictionary, width, x_title, y_title):
    output_file(title + ".html")
    xlist = list()
    ylist = list()

    for item in dictionary:
    
        if isinstance(dictionary[item], timedelta):
            xlist.append(str(item))
            ylist.append(dictionary[item].total_seconds()) 
        
        else:
            xlist.append(str(item))
            ylist.append(dictionary[item]) 

    p = figure(x_range=xlist, plot_height=750, plot_width=width, title=title, x_axis_label=x_title,
               y_axis_label=y_title, toolbar_location=None, tools="hover", toolbar_sticky=False)
    p.vbar(x=xlist, top=ylist, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    show(p)

files = LogFile(1)



 





