#!/usr/bin/python3
#Installing module if needed: python -m pip install xxxxx
#This is a script to check device connectivity and perform a basic nmap scan.

#import modules and libraries
import subprocess
import ipaddress
from subprocess import Popen, PIPE
import sys
import time
import datetime
import threading
from multiprocessing.dummy import Pool as ThreadPool

#set colour
bg = "\033[1;32m"
end = "\33[0;0m"
bw = "\33[1;37m"

#Function to get network information
def ipList():
    psweepstr="""
  _____ _
 |  __ (_)
 | |__) | _ __   __ _ _____      _____  ___ _ __
 |  ___/ | '_ \ / _` / __\ \ /\ / / _ \/ _ \ '_ \
 | |   | | | | | (_| \__ \\ V  V /  __/  __/ |_) |
 |_|   |_|_| |_|\__, |___/ \_/\_/ \___|\___| .__/
                 __/ |                     | |
                |___/                      |_|

"""
    info = """
  Pingsweep v1.0 by Joao Paulo (JP)
  Pingsweep and simple nmap port scan using threading.
  https://github.com/jotape75/pingsweep
  https://jpsecnetowrks.com

  Usage: network</mask>
  Exmaple: 10.10.10.0/24

"""
    print (bw+"#" * 80)
    print(psweepstr + end)
    print(bg+info+end)
    print (bw+"#" * 80 + end + "\n")
    nrange = input(bw+"Please Enter Network: "+end)
    IP_List = []
    #nrange = str(sys.argv[1])
    network = ipaddress.ip_network(nrange)
    for i in network.hosts():
        i=str(i)
        IP_List.append(i)
    return (IP_List)

#Function to perform ping to the devices.
def config_worker(IP_List):
    toping = subprocess.Popen(['ping','-c','3',IP_List], stdout=PIPE)
    output = toping.communicate()[0]
    hostalive=toping.returncode

    if hostalive ==0:
       nmap = 'nmap -sS {:s}'.format(IP_List)
       nmaprslt = Popen(nmap, shell=True,stdout=PIPE, stderr=PIPE)
       out, err = nmaprslt.communicate()
       print("\n")
       print (bg+"#" * 80 +end)
       print ("\n" + bw+str(IP_List)+end,bg + 'Host is Alive\n'+end)
       print (bw+"Please wait, scanning remote host", IP_List + "\n"+end)
       print (bw+out.decode('utf-8')+end)
       print (bg+"#" * 80+end)

#==============================================================================
# ---- Main: Get Configuration
#==============================================================================

start_time = datetime.datetime.now()

IP_List = ipList( )
num_threads = 100

#created a thread pool of devices.
print (bw+'\n--- Creating threadpool '+ str(num_threads)+' Devices\n'+end)
threads = ThreadPool( num_threads )
results = threads.map( config_worker, IP_List )
threads.close()
threads.join()

end_time = datetime.datetime.now()
total_time = end_time - start_time
print (bw+'\n---- Total of Devices: ' + str(len(IP_List))+end)
print (bw+'\n---- End get config threading ' + str(total_time)+end)
