#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#打印当前集群每个 mon的存储使用量

import os
import sys
import json
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
        memlist = ["Mon\size"]
        memchose = [ 'USED','avail_percent']
        for meminfo in memchose:
            memlist.append("%s" %meminfo )
        row.field_names = memlist
        
        jsondata=commands.getoutput("ceph -s --format json-pretty" ) 
        text=json.loads(jsondata)
        
        for i in range (0, len(text['health']['health']['health_services'][0]['mons'])):

	    monlist = []
            for monmem in range(len(memchose)):
                monlist.append(" ")

            #monlist.append(text['nodes'][i]['id'])
            monid= text['health']['health']['health_services'][0]['mons'][i]['name']
            monname="mon."+str(monid)
            mon_size = text['health']['health']['health_services'][0]['mons'][i]['kb_used']
            mon_util = text['health']['health']['health_services'][0]['mons'][i]['avail_percent']
            monlist.insert(0,monname)
            monlist[1] = str(float(mon_size)/1024.0/1024.0)+"G"
            monlist[2] = str(mon_util)+"%"
            vm_dic = {}
            vm_dic['USED']= str(float(mon_size)/1024.0/1024.0)+"G"
            vm_dic['Utilizatioin']= str(mon_util)+"%"
            mon_list[monname] = vm_dic
          
            data_dic['monmemused'] = mon_list
            if chosse == "table":
                row.add_row(monlist)

            elif chosse == "json":
                row = json.dumps(data_dic,separators=(',', ':'))


        print row

if __name__ == '__main__':
    main()
