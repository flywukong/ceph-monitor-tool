#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#打印每个osd的CPU利用率，如果利用率超过20%会标记为警告

import os
import sys
import json
import psutil
import commands
from prettytable import PrettyTable
import time


def main():
    if len(sys.argv) == 1:
        printosdmemtable("table")
    elif sys.argv[1] == 'json':
        printosdmemtable("json")

def printosdmemtable(chosse):
        data_dic = {}
        osd_list={}
        row = PrettyTable()
        row.header = True
        memlist = ["OSD\CPU"]
        memchose = [ 'CPU','WARN']
        for meminfo in memchose:
            memlist.append("%s" %meminfo )
        row.field_names = memlist
        for root, dirs, files in os.walk('/var/run/ceph/'):
            for name in files:
                if "osd"  in name and "asok" in name :
                    osdlist = []
                    osdthlist=[]
                    for osdmem in range(len(memchose)):
                        osdlist.append(" ")
                      
                    pidfile=root+ name
                    osdid=commands.getoutput('ls  %s|cut -d "." -f 2 2>/dev/null'  %pidfile )
                    osdpid = commands.getoutput("netstat -nlp|grep %s |awk '{print $9}'" %pidfile).split("/")[0]
               
                    process = psutil.Process(int(osdpid))
                     
   #                 process.cpu_percent(interval=5)
                    process.cpu_percent(interval=None)
                    #time.sleep(5)
#                    osd_runmemvsz = commands.getoutput('ps -p %s  -o vsz |grep -v VSZ 2>/dev/null' %osdpid)
                    cpucount = process.cpu_percent(interval=5)
                    osdname="osd."+osdid
                    osdlist.insert(0,osdname)
                    osdlist[1] = str(cpucount)+"%"
                    if cpucount < 20:
                        osdlist[2] = "ok"
                    else:
                        osdlist[2] = "Warning"
                    vm_dic = {}
                    vm_dic['CPU']= osdlist[1]
                    vm_dic['WARN']= osdlist[2]
                    osd_list[osdname] = vm_dic
                    data_dic['osdmemused'] = osd_list
                    if chosse == "table":
                        row.add_row(osdlist)
                    elif chosse == "json":
                        row = json.dumps(data_dic,separators=(',', ':'))
        print row

if __name__ == '__main__':
    
    start = time.time()

    main()

    end = time.time()

    print end-start



