import os
import sys
import subprocess


#python pro.py  project  interface  metric
#METRIC = private-dom,  private-msg, public-dom
if __name__ == '__main__':
    project = sys.argv[1]
    interface = sys.argv[2]
    metric = sys.argv[3]

    if project == 'bvn13':
        servnum_start = 3
        servnum_end = 20
        if interface == 'public':
            api_file_name = ''
        elif interface == 'private':
            api_file_name =     'data/blog-bvn13/clusters/afterFilter/bvn13_'


    elif project == 'jforum219':
        servnum_start = 16
        servnum_end = 47
        if interface == 'public':
            api_file_name =     'data/jforum219/jforum219_public_'
        elif interface == 'private':
            api_file_name =     'data/jforum219/jforum219_'

    elif project == 'jpetstore6':
        servnum_start = 1
        servnum_end = 23
        if interface == 'public':
            api_file_name =     'data/jpetstore6/jpetstore6_public_'
        elif interface == 'private':
            api_file_name =     'data/jpetstore6/jpetstore6_'

    elif project == 'roller520':
        servnum_start = 2
        servnum_end = 72
        if interface == 'private':
            api_file_name =     'data/roller520/clustersAPI/roller520_'

    if metric == 'private-dom':
        cmd = 'python ../measure/tosc-interf-dom-cohesion.py '
    elif metric == 'private-msg':
        cmd = 'python ../measure/tosc-interf-msg-cohesion.py '
    elif metric == 'public-dom':
        cmd = 'python ../measure/tosc-interf-dom-cohesion-public.py '

    for servnum in range(servnum_start, servnum_end + 1):
        this_api_file_name = (api_file_name + str(servnum) + '_clusterAPI.csv')
        this_cmd = (cmd + this_api_file_name)
        returncode  = subprocess.call(this_cmd, shell=True)
