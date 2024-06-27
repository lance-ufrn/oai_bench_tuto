from open_iperf import *
from open_ping import *
# Figures 8, 9, 10 e 11 
folder_path = '1_UE_ideal_iperf'
open_iperf(folder_path ,1)

# Figure 12
folder_path = '1_UE_ideal_ping'
open_ping(folder_path)

# Figure 13
folder_path = '2_UEs_ideal_iperf'
open_iperf(folder_path ,1)

# Figure 14
folder_path = '2_UEs_ideal_ping'
open_ping(folder_path)

# Figure 15
# run iperf_distance.py
