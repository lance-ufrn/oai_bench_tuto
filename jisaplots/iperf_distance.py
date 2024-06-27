import matplotlib.pyplot as plt
import numpy as np
import os
import re
import pandas as pd

def getsubpaths(folder_path):
    # Get subpaths using os.walk()
    subpaths = []
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            subpath = os.path.join(root, dir)
            subpaths.append(subpath)

    # Print subpaths
    print("Subpaths in the folder:")
    for subpath in subpaths:
        print(subpath)
    return subpaths

def remove_outliers_zscore(data, threshold=3):
    mean = np.mean(data)
    std_dev = np.std(data)
    z_scores = [(x - mean) / std_dev for x in data]
    
    filtered_data = []
    removed_indexes = []
    
    for i, (x, z) in enumerate(zip(data, z_scores)):
        if abs(z) < threshold:
            filtered_data.append(x)
        else:
            removed_indexes.append(i)
    
    return filtered_data, removed_indexes

def remove_outliers_iqr(data):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    filtered_data = []
    removed_indexes = []
    
    for i, x in enumerate(data):
        if lower_bound <= x <= upper_bound:
            filtered_data.append(x)
        else:
            removed_indexes.append(i)
    
    return filtered_data, removed_indexes

# List of file paths
#folder_path = '2_UEs_ideal_iperf'
#folder_path = 'arquivos_primeira_versao'
folder_path = '1_UE_distance'


# Adjustment of last samples
nRemove = 2 # 1, if only receiver or sender is present in the end of file
            # 2, if receiver are sender are present in the end of file

# List of subpaths
subpaths = getsubpaths(folder_path)

table_all = []
BW_all = []
data_all = []
distances = []

# Set the default linewidth and font size for axis labels
plt.rcParams['lines.linewidth'] = 4
plt.rcParams['axes.labelsize'] = 24
plt.rcParams['xtick.labelsize'] = 24
plt.rcParams['ytick.labelsize'] = 24
plt.rcParams['legend.fontsize'] = 20
# Set font properties
plt.rcParams['font.family'] = 'serif'  # Set font family
plt.rcParams['font.serif'] = 'Times New Roman'  # Set serif font to Times New Roman


for subpath in subpaths: 

    # List of file paths
    files = os.listdir(subpath)
    # Print the list of file names
    #print("Files in the folder:")
    #for file in files:
    #    print(file)

    # List to hold Bandwidth and Interval data
    read_data = []
    bandwidth_data = []
    
    # Iterate over each file
    for file_name in files:
        full_path = os.path.join( subpath, file_name)
        print('Reading file {}'.format(full_path))
        
        with open(full_path, 'r') as f:
            # Read all lines from the file
            lines = f.readlines()

            # Initialize variables to capture data
            intervals = []
            bandwidths = []

            # Process each line
            for line in lines:
                if 'sec' in line:  # Lines with 'sec' contain Interval and Bandwidth data
                    parts = line.split()
                    interval = float(parts[2].split('-')[0])  # Extract Interval start
                    bandwidth = float(parts[6])  # Extract Bandwidth in Mbits/sec
                    if (parts[7] == 'Kbits/sec'):
                        bandwidth = bandwidth/1000

                    intervals.append(interval+1)
                    bandwidths.append(bandwidth)

            # remove the last line (it is a summary)
            intervals = intervals[:-nRemove]
            bandwidths = bandwidths[:-nRemove]
            
            #filtered_data, removed_indexes = remove_outliers_iqr(bandwidths)
            filtered_data, removed_indexes = remove_outliers_zscore(bandwidths)
            bandwidths = filtered_data
            intervals = [value for i, value in enumerate(intervals) if i not in removed_indexes]
            
            bw_min = np.min(bandwidths)
            bw_avg = np.mean(bandwidths)
            bw_max = np.max(bandwidths)
            bw_mdev = np.std(bandwidths)       
            # Store data from current file
            #bandwidth_data.append((intervals, bandwidths, bw_min, bw_avg, bw_max, bw_mdev))                
    
            print('bw_min = {}'. format( bw_min) )
            print('bw_mean = {}'. format( bw_avg) )
            print('bw_max  = {}'. format( bw_max) )
            print('bw_std = {}'. format( bw_mdev) )

            # create a table with values for all PRBs
            table_all.append((bw_max, bw_avg, bw_mdev))
    
            # Plot Bandwidth values vs Interval
            plt.figure(figsize=(10, 7))

            # Plot average Bandwidth values
            #xTime = np.linspace(0,180,len(unique_intervals))
            xTime = intervals
            plt.plot(xTime, bandwidths, linestyle='-', color='black', label='Measured')

            average_bw = np.mean(bandwidths)
            # Create a vector of average bandwidths with the same length as bandwidths
            average_bw_vector = np.full_like(intervals, average_bw)

            # Plot average Bandwidth value
            plt.plot(xTime, average_bw_vector, linestyle='--', color='red', label='Mean')

            # build a vector with the PRB sequence read from folder
            number = file_name.split('_')[1]
            distances.append(number)

            # Customize plot
            #plt.title('Bandwidth vs Interval')
            plt.xlabel('Time (seconds)')
            plt.ylabel('Throughput (Mbps)')
            plt.legend(loc='best')
            plt.grid(True)
            #plt.xticks(xTime)
            plt.xlim(xTime[0],xTime[-1])
            plt.xticks(range(0,int(xTime[-1]+1),20))
            #plt.ylim(85,136.5)

            # Save plot as EPS
            plt.savefig(subpath + '_BW_distance_' + number + '_plot.svg', format='svg')

            # Save plot as PNG
            plt.savefig(subpath + '_BW_distance_' + number + '_plot.png', format='png')
            
            # Show plot (optional)
            plt.tight_layout()
            #plt.show()
        
            # append bw vector from multiples distances
            BW_all.append(bandwidths)
            data_all.append((intervals, bandwidths))
            

#vtcolumns = ['1', '4', '8', '12']
vtcolumns = distances

# plot two distances in the same plot
plt.figure(figsize=(10, 7))
i = 1
ic = 1
vtPlot_distance = ['1', '12']
vtline_color = ['black', 'red', 'blue', 'Orange' ]

for interval, data in data_all:
    if vtcolumns[i-1] in vtPlot_distance:    
        # Plot average Bandwidth values
        plt.plot(interval, data, linestyle='-', color=f'{vtline_color[2*ic - 2]}', label=f'Measures at distance {vtcolumns[i-1]} m')

        average_bw = np.mean(data)
        # Create a vector of average bandwidths with the same length as bandwidths
        average_bw_vector = np.full_like(interval, average_bw)

        # Plot average Bandwidth value
        plt.plot(interval, average_bw_vector, linestyle='--', color=f'{vtline_color[2*ic-1]}', label=f'Mean at distance {vtcolumns[i-1]} m')
        ic = ic + 1
    i = i + 1
plt.xlabel('Time (seconds)')
plt.ylabel('Throughput (Mbps)')
plt.legend(loc='best')
plt.xlim(xTime[0],xTime[-1])
plt.xticks(range(0,int(xTime[-1]+1),20))
           
plt.ylim(60,140)
plt.grid(True)
# Save plot as EPS
plt.savefig(subpath + '_BW_distance_' + "_".join(vtPlot_distance) + '_plot.svg', format='svg')

# Save plot as PNG
plt.savefig(subpath + '_BW_distance_' + "_".join(vtPlot_distance) + '_plot.png', format='png')
#plt.show()



# Plot Bandwidth CDFs
#BW_all = np.array(BW_all)
plt.figure(figsize=(10, 6))
for i, data in enumerate(BW_all, start=1):
    sorted_data = np.sort(data)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
    plt.plot(sorted_data, yvals, label=f'{vtcolumns[i-1]} m')

plt.xlabel('Throughput (Mbps)')
plt.ylabel('CDF')
plt.legend()
plt.grid(True)
#plt.show()

# Create a DataFrame
# Additional headers as strings
column_headers = ['Max BW (Mbps)', 'Mean BW (Mbps)', 'Std BW (Mbps)']
df = pd.DataFrame(data=table_all, columns=column_headers)
# Select PRBs sizes read
#print(vtcolumns)
vtcolumns = [float(x) for x in vtcolumns]
df['Distances'] = pd.Series( vtcolumns )
df = df[['Distances','Max BW (Mbps)', 'Mean BW (Mbps)', 'Std BW (Mbps)']] 
df = df.sort_values(by='Distances')
df = df.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
print(df)
# Convert DataFrame to LaTeX format
latex_table = df.to_latex(index=False)
# Print or save the LaTeX table
print(latex_table)

#folder_path = '2_UEs_ideal_iperf'
#open_iperf(folder_path ,1)