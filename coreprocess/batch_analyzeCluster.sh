#!/bin/sh
for((i=40;i>=6;i--));
do
file='../testcase_data/jforum219/coreprocess/jforum219_testcase1_jm_AVG_'${i}'.csv'
python analyzeCluster.py    jforum219  $file    ../testcase_data/jforum219/coreprocess/jforum219_testcase1_fv.csv    ../testcase_data/jforum219/coreprocess/jforum219_testcase1_class.csv

done
