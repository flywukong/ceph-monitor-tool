#! /bin/python
# -*- coding: UTF-8 -*-
# 使用火焰图分析PG分布
# 1. python getmap.py >  map.txt 获取crush 结构和 对象分布
# 2. flamegraph  --title  "Ceph crush flame graph" --width "1800" --countname "num" map.txt > mycrush.svg
# 3. mycrush.svg拷贝到windows机器，然后用浏览器打开即可，推荐chrome


import os
import commands
import json


def main():
    global list_all_host
    list_all_host = commands.getoutput('ceph osd tree -f json-pretty  2>/dev/null')
#    print getosd("osd.16")  
    getpgmap()
def getosd(osd):
    mylist=[]
    crushid={}
    json_str = json.loads(list_all_host)
  
    for item in json_str['nodes']:
        if item.has_key('children'):
            crushid[str(item['id'])]=str(item['name'])
            for child in item['children']:
                tmplist=[item['id'],child]
                mylist.append(tmplist)
        if item['type'] == "osd":
            crushid[str(item['id'])]=str(item['name'])
    listnum=len(mylist)
    compareindex=0
###从数组开始跟后面的数组进行比较，如果有就改变后面的数组，然后删除当前比较的list(index),进行list更新
###如果没有改变，就把索引往后推即可
    while compareindex < len(mylist):
        change = False
        for index,num in enumerate(mylist):
            if compareindex != index and compareindex < index:
                if str(mylist[compareindex][-1]) == str(num[0]):
                    del mylist[index][0]
                    mylist[index]=mylist[compareindex]+mylist[index]
                    change=True
                if str(mylist[compareindex][0]) == str(num[-1]):
                    del mylist[index][-1]
                    mylist[index]=mylist[index]+mylist[compareindex]
                    change=True
        if change == True:
            del mylist[compareindex]
        if change == False:
            compareindex = compareindex + 1

    for index,crushlist in enumerate(mylist):
        osdcrushlist=[]
        for osdlocaltion in crushlist:
            local=str(crushid['%s' %osdlocaltion])
            osdcrushlist.append(local)
        if osdcrushlist[-1] == osd:
            return osdcrushlist

def getpgmap():
    list_all_host = commands.getoutput('ceph pg  ls --format json-pretty  2>/dev/null')
    json_str = json.loads(list_all_host)
    for item in json_str:
        for osdid in item['up']:
            osd="osd."+str(osdid)
            b=""
            for a in getosd(osd):
                b=b+str(a)+";"
            print b+item['pgid']+" "+str(item['stat_sum']['num_objects']+1)

if __name__ == '__main__':
    main()
