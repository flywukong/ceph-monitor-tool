#!/bin/bash

#sata_osd=(0 3 6 11 17 20 23 1 5 8 10 13 15 18 22 2 4 7 9 14 16 19 21)


ceph osd getcrushmap -o crushmap.bin


echo -e " \033[43;31mprint CrushMap\033[0m "
echo "echo crushmap"
crushtool  -i crushmap.bin  --tree  

echo -e " \033[43;31mtest rule1\033[0m "
echo "----------"
crushtool  -i crushmap.bin  --tree  --test  --rule 0 --min-x 1  --max-x 5  --num-rep 3  --show-mappings  -o newmap | grep  "CRUSH"

#crushtool  -i crushmap.bin  --tree  --test  --rule 0 --min-x 1  --max-x 5  --num-rep 3  --show-mappings  -o newmap | grep  "CRUSH"|awk '{print $6;}'


echo -e " \033[43;31mtest rule2\033[0m "
echo "---------"
crushtool  -i crushmap.bin  --tree  --test  --rule 1 --min-x 1  --max-x 5  --num-rep 3  --show-mappings  -o newmap | grep  "CRUSH"


echo -e " \033[43;31mrules setting\033[0m "
echo "---------"

ceph osd crush rule dump|grep "rule_name\|item_name"



