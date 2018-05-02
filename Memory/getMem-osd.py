#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import json
import psutil
import commands
from prettytable import PrettyTable
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
        memlist = ["OSD\MEM"]
        memchose = [ 'VIRT','RES']
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
                  #  osdpid = commands.getoutput('cat %s  2>/dev/null' %pidfile)
                  #  usedPercents=commands.getoutput("df -h|grep sda|awk '{print $5}'|grep -Eo '[0-9]+'").split('\n')

                    osdpid = commands.getoutput("netstat -nlp|grep %s |awk '{print $9}'" %pidfile).split("/")[0]
                     
                    osd_runmemvsz = commands.getoutput('ps -p %s  -o vsz |grep -v VSZ 2>/dev/null' %osdpid)
                    osd_runmemrsz = commands.getoutput('ps -p %s  -o rsz |grep -v RSZ 2>/dev/null' %osdpid)
                    osdname="osd."+osdid
                    osdlist.insert(0,osdname)
                    osdlist[1] = str(int(osd_runmemvsz)/1024)+"KB"
                    osdlist[2] = str(int(osd_runmemrsz)/1024)+"KB"
                    vm_dic = {}
                    vm_dic['VSZ']= str(int(osd_runmemvsz)/1024)+"KB"
                    vm_dic['RSZ']= str(int(osd_runmemrsz)/1024)+"KB"
                    osd_list[osdname] = vm_dic
                    data_dic['osdmemused'] = osd_list
                    if chosse == "table":
                        row.add_row(osdlist)
                    elif chosse == "json":
                        row = json.dumps(data_dic,separators=(',', ':'))
        print row

if __name__ == '__main__':
    main()
