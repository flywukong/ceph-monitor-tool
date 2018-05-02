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
        printmonmemtable("table")
    elif sys.argv[1] == 'json':
        printmonmemtable("json")

def printmonmemtable(chosse):
        data_dic = {}
        mon_list={}
        row = PrettyTable()
        row.header = True
        memlist = ["OSD\MEM"]
        memchose = [ 'VIRT','RES']
        for meminfo in memchose:
            memlist.append("%s" %meminfo )
        row.field_names = memlist
        for root, dirs, files in os.walk('/var/run/ceph/'):
            for name in files:
                if "mon"  in name and "asok" in name :
                    monlist = []
                    monthlist=[]
                    for monmem in range(len(memchose)):
                        monlist.append(" ")
                      
                    pidfile=root+ name
                    monid=commands.getoutput('ls  %s|cut -d "." -f 2 2>/dev/null'  %pidfile )
                  #  monpid = commands.getoutput('cat %s  2>/dev/null' %pidfile)
                  #  usedPercents=commands.getoutput("df -h|grep sda|awk '{print $5}'|grep -Eo '[0-9]+'").split('\n')

                    monpid = commands.getoutput("netstat -nlp|grep %s |awk '{print $9}'" %pidfile).split("/")[0]
                     
                    mon_runmemvsz = commands.getoutput('ps -p %s  -o vsz |grep -v VSZ 2>/dev/null' %monpid)
                    mon_runmemrsz = commands.getoutput('ps -p %s  -o rsz |grep -v RSZ 2>/dev/null' %monpid)
                    print "mon_runmemvsz",mon_runmemvsz
                    print "mon_runmemrsz",mon_runmemrsz
                    monname="mon."+monid
                    monlist.insert(0,monname)
                    monlist[1] = str(int(mon_runmemvsz)/1024)+"KB"
                    monlist[2] = str(int(mon_runmemrsz)/1024)+"KB"
                    vm_dic = {}
                    vm_dic['VSZ']= str(int(mon_runmemvsz)/1024)+"KB"
                    vm_dic['RSZ']= str(int(mon_runmemrsz)/1024)+"KB"
                    mon_list[monname] = vm_dic
                    data_dic['monmemused'] = mon_list
                    if chosse == "table":
                        row.add_row(monlist)
                    elif chosse == "json":
                        row = json.dumps(data_dic,separators=(',', ':'))
        print row

if __name__ == '__main__':
    main()
