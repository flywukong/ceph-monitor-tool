# -*- coding: UTF-8 -*-

#计算指定pool上所有osd 上的PG分布数的方差
#ceph pg dump|grep '^ $pool_id\.' |awk '{print $15}' > pg.1 ; python pg_stat.py pg.1|sort -k2 -rn|awk '{print $2}'|python dispersion.py
import sys, math

vlist = []
for line in sys.stdin:
    vlist.append(int(line.strip()))

avg = float(sum(vlist))/len(vlist)
sum1 = 0
for v in vlist:
    sum1 += (v-avg)*(v-avg)

print math.sqrt(sum1/len(vlist))
