#!/usr/bin/env python
# -*- coding: utf-8 -*-
#对比集群数据迁移的PGmap 获取PG迁移的数量和objects 对象迁移数量
#集群迁移前 pg dump pgs|awk '{print $1,$2,$15,$17}' > pgmap1
#集群数据迁移后 pg dump pgs|awk '{print $1,$2,$15,$17}' > pgmap2
#执行python compair.py pgmap1 pgmap2  


__author__ ="zp"
import os,sys

class filetojson(object):
    def __init__(self,orin,new):
        self.origin=orin
        self.new=new

    def tojson(self,filename):
        data={}
        pginfo={}
        for line in open(filename):
            if "pg_stat" in line:
                continue
            lines=line.split()
            pg=lines[0]
            objects=lines[1]

            print "objects",objects           
            withosd=lines[2]
            print "withosd",withosd

            data[pg]={'objects':objects,'osd':list(eval(withosd))}
            print "data[pg]",data[pg]
        return data

    def compare(self):
        movepg=0
        allmovepg=0
        allmoveobject=0
        moveobject=0
        oringinmap=self.tojson(self.origin)
        newmap=self.tojson(self.new)
        for key in oringinmap:
            amapn=set(oringinmap[key]['osd'])
            print "amapn",amapn
            bmapn=set(newmap[key]['osd'])
            print "bmapn",bmapn
            movepg=len(list(amapn.difference(bmapn)))
            if movepg != 0:
                moveobject=int(oringinmap[key]['objects']) * int(movepg)
                allmovepg=allmovepg+movepg
                allmoveobject=allmoveobject+moveobject
        return [allmovepg,allmoveobject]

mycom=filetojson(sys.argv[1],sys.argv[2])
print "| pgs | objects |"
print "-----------------"
print mycom.compare()
