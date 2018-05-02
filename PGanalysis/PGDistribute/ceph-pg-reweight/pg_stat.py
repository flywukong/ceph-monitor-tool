# -*- coding: UTF-8 -*-

#打印指定pool上的PG分布

#ceph pg dump|grep '^$poolid \.' |awk '{print $15}' > test
import sys

d = {}
for line in sys.stdin:
    slist = line.strip().replace('[', '').replace(']', '').split(',')
    for x in slist:
        if x in d.keys():
            d[x] += 1
        else:
            d[x] = 1

for k,v in d.items():
    print '%2s %2d' % ( k,v )

