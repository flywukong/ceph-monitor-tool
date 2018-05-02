#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#打印每个osd id 的进程 具体是跑在机器上的哪一个核上
import os
import sys
import json
import psutil
import commands
from prettytable import PrettyTable

def main():
    if len(sys.argv) == 1:
        printosdcputable("process")
    elif sys.argv[1] == 't':
        printosdcputable("thread")

def printosdcputable(choose):
    print choose
    row = PrettyTable()
    row.header = True
    cpulist = ["OSD\CPU"]
    corelist=["Core ID"]
    phylist = ["Physical ID"]
    emplist=["-----------"]
    for cpupro in range(psutil.cpu_count()):
        cpulist.append("%s" %cpupro )

        coreid=commands.getoutput('egrep \'processor|physical id|core id\' /proc/cpuinfo | cut -d : -f 2 | paste - - -  | awk  \'$1==%s {print $3 }\'' %cpupro)
        corelist.append("%s" %coreid)

        phyid = commands.getoutput('egrep \'processor|physical id|core id\' /proc/cpuinfo | cut -d : -f 2 | paste - - -  | awk  \'$1==%s {print $2 }\'' % cpupro)
        phylist.append("%s" %phyid)
        emplist.append("--")

    row.field_names = cpulist
    row.add_row(corelist)
    row.add_row(phylist)
    row.add_row(emplist)

    for root, dirs, files in os.walk('/var/run/ceph/'):
        for name in files:
            if "osd"  in name and "pid" in name :
                osdlist = []
                osdthlist=[]
                for osdcpu in range(psutil.cpu_count()):
                    osdlist.append(" ")
                    osdthlist.append("0")
                pidfile=root+ name
                osdid=commands.getoutput('ls  %s|cut -d "." -f 2 2>/dev/null'  %pidfile )
                osdpid = commands.getoutput('cat %s  2>/dev/null' %pidfile)
                osd_runcpu = commands.getoutput('ps -o  psr -p %s |grep -v PSR 2>/dev/null' %osdpid)
                th_list = commands.getoutput('ps -o  psr -L  -p %s |grep -v PSR|awk \'gsub(/^ *| *$/,"")\'  2>/dev/null' % osdpid)

                osdname="osd."+osdid
                osdlist[int(osd_runcpu)]="+"
                for osdth in th_list.split('\n'):
                    osdthlist[int(osdth)] = int(osdthlist[int(osdth)])+1
                osdlist.insert(0,osdname)
                osdthlist.insert(0,osdname)
                if choose == "process":
                    row.add_row(osdlist)
                elif choose == "thread":
                    row.add_row(osdthlist)
    print row

if __name__ == '__main__':
    main()
