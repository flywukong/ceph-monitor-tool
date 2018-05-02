#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 打印当前集群每个 osd的存储使用量
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
        memlist = ["OSD\size"]
        memchose = [ 'USED','Utilizatioin']
        for meminfo in memchose:
            memlist.append("%s" %meminfo )
        row.field_names = memlist
        
        jsondata=commands.getoutput("ceph osd df --format json-pretty" ) 
        text=json.loads(jsondata)
	for i in range(0,len(text['nodes'])):
                
                osdlist = []
                for osdmem in range(len(memchose)):
                    osdlist.append(" ")

        	#osdlist.append(text['nodes'][i]['id'])
                osdid=text['nodes'][i]['id']
                osdname="osd."+str(osdid)
                osd_size = text['nodes'][i]['kb_used']
	        osd_util = text['nodes'][i]['utilization'] 
                osdlist.insert(0,osdname)
                osdlist[1] = str(float(osd_size)/1024.0/1024.0)+"G"
                osdlist[2] = str(osd_util)+"%"
                vm_dic = {}
                vm_dic['USED']= str(float(osd_size)/1024.0/1024.0)+"G"
                vm_dic['Utilizatioin']= str(osd_util)+"%"
                osd_list[osdname] = vm_dic
   
                data_dic['osdmemused'] = osd_list
                if chosse == "table":
                    row.add_row(osdlist)

                elif chosse == "json":
                    row = json.dumps(data_dic,separators=(',', ':'))
        osdlist = []
        for osdmem in range(len(memchose)):
            osdlist.append(" ")
        summary = text['summary']['total_kb_used']
        average_utilization = text['summary']['average_utilization']
        osdname = "summary"
        osdlist.insert(0,osdname)
        osdlist[1] = str(float(summary)/1024.0/1024.0)+"G"
        osdlist[2] = str(average_utilization)+"%"
        vm_dic = {}
        vm_dic['USED']= str(summary)+"KB"
        vm_dic['Utilizatioin']= str(average_utilization)+"%"
        osd_list[osdname] = vm_dic
        data_dic['osdmemused'] = osd_list
        if chosse == "table":
            row.add_row(osdlist)
        elif chosse == "json":
            row = json.dumps(data_dic,separators=(',', ':'))

        print row

if __name__ == '__main__':
    main()
