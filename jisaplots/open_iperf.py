import matplotlib.pyplot as plt
import numpy as np
import os
import re
import pandas as pd

import scipy.stats as stats

def confidence_interval(data):
    # Calculate sample mean and standard deviation
    sample_mean = np.mean(data)
    sample_std = np.std(data, ddof=1)
    n = len(data)

    # 99% confidence level
    confidence_level = 0.99
    alpha = 1 - confidence_level

    # Degrees of freedom
    df = n - 1

    # t critical value for 99% confidence level
    t_critical = stats.t.ppf(1 - alpha/2, df)

    # Margin of error
    margin_of_error = t_critical * (sample_std / np.sqrt(n))

    return margin_of_error 

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

def open_iperf(folder_path, nRemove):
    # List of file paths
    #folder_path = '2_UEs_ideal_iperf'
    #folder_path = 'arquivos_primeira_versao'

    # Adjustment of last samples
    #nRemove = 2 # 1, if only receiver or sender is present in the end of file
                # 2, if receiver are sender are present in the end of file

    # Set the default linewidth and font size for axis labels
    plt.rcParams['lines.linewidth'] = 4
    plt.rcParams['axes.labelsize'] = 24
    plt.rcParams['xtick.labelsize'] = 24
    plt.rcParams['ytick.labelsize'] = 24
    plt.rcParams['legend.fontsize'] = 20
    # Set font properties
    plt.rcParams['font.family'] = 'serif'  # Set font family
    plt.rcParams['font.serif'] = 'Times New Roman'  # Set serif font to Times New Roman
    # List of subpaths
    subpaths = getsubpaths(folder_path)

    table_all = []
    BW_all = []
    combined_current_prb = []

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
        confidence_bandwidths = []
        average_bandwidths = []
        
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
                bandwidth_data.append((intervals, bandwidths, bw_min, bw_avg, bw_max, bw_mdev))
                            
        # Combine data from all files into a single list
        combined_intervals = []
        combined_bandwidths = []
        combined_bw_min = []
        combined_bw_avg  = []
        combined_bw_max = []
        combined_bw_mdev = []
        for intervals, bandwidths, bw_min, bw_avg, bw_max, bw_mdev in bandwidth_data:
            combined_intervals.extend(intervals)
            combined_bandwidths.extend(bandwidths)
            combined_bw_min.append(bw_min)
            combined_bw_avg.append(bw_avg)
            combined_bw_max.append(bw_max)
            combined_bw_mdev.append(bw_mdev)
            
        combined_intervals = np.array(combined_intervals)
        combined_bandwidths = np.array(combined_bandwidths)
        
        #print(combined_times) 
        #print(combined_packet_loss) 
        
        # Final metrics (regarding the hole vector from all jobs)
        bw_min = np.min(combined_bandwidths)
        bw_avg = np.mean(combined_bandwidths)
        bw_max = np.max(combined_bandwidths)
        bw_mdev = np.std(combined_bandwidths)
         
        
        print('bw_min (from the mean of BW min of each job) = {} and bw_min (from all samples of all jobs) = {}'. format(np.mean(combined_bw_min), bw_min) )
        print('bw_mean (from the mean of BW mean of each job) = {} and bw_mean (from all samples of all jobs) = {}'. format(np.mean(combined_bw_avg), bw_avg) )
        print('bw_max (from the mean of BW max of each job) = {} and bw_max (from all samples of all jobs) = {}'. format(np.mean(combined_bw_max), bw_max) )
        print('bw_std (from the mean of BW std of each job) = {} and bw_std (from all samples of all jobs) = {}'. format(np.mean(combined_bw_mdev), bw_mdev) )

        
        conf_int = confidence_interval(combined_bw_avg)        
        print('Avg = {}, Max and Min for 0.99 confidence = {}, {}'. format(np.mean(combined_bw_avg), np.mean(combined_bw_avg)-conf_int, np.mean(combined_bw_avg)+conf_int) )

        # create a table with values for all PRBs (average of all jobs)
        table_all.append((np.mean(combined_bw_max), np.mean(combined_bw_avg), np.mean(combined_bw_mdev)))
        
                
        unique_intervals = np.unique(combined_intervals)
        average_bandwidths = [np.mean(combined_bandwidths[combined_intervals == interval]) for interval in unique_intervals]

        # condidence intervals
        #confidence_bandwidths = [confidence_interval(combined_bandwidths[combined_intervals == interval]) for interval in unique_intervals]


        #print(unique_intervals) 
        #print(average_bandwidths)  

        # Plot Bandwidth values vs Interval
        plt.figure(figsize=(10, 7))

        # Plot average Bandwidth values
        #xTime = np.linspace(0,180,len(unique_intervals))
        xTime = unique_intervals
        plt.plot(xTime, average_bandwidths, linestyle='-', color='black', label='Measured')

        average_bw = np.mean(average_bandwidths)
        # Create a vector of average bandwidths with the same length as bandwidths
        average_bw_vector = np.full_like(unique_intervals, average_bw)

        # Plot average Bandwidth value
        plt.plot(xTime, average_bw_vector, linestyle='--', color='red', label='Mean')

        # Customize plot
        #plt.title('Bandwidth vs Interval')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Throughput (Mbps)')
        plt.legend()
        plt.grid(True)
        #plt.xticks(xTime)
        plt.xlim(xTime[0],xTime[-1])
        plt.xticks(range(0,int(xTime[-1]+1),20))

        # Save plot as EPS
        plt.savefig(subpath + '_BW_plot.eps', format='eps')

        # Save plot as PNG
        plt.savefig(subpath + '_BW_plot.png', format='png')
        
        # Show plot (optional)
        plt.tight_layout()
        #plt.show()
        
        # append bw vector from multiples PRB sizes
        BW_all.append(average_bandwidths)
        
        # build a vector with the PRB sequence read from folder
        combined_current_prb.append(subpath[-3:])

    #vtcolumns = ['106', '162', '273']
    vtcolumns = combined_current_prb
        
    # Plot Bandwidth CDFs
    #BW_all = np.array(BW_all)
    plt.figure(figsize=(10, 7))
    for i, data in enumerate(BW_all, start=1):
        sorted_data = np.sort(data)
        yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
        plt.plot(sorted_data, yvals, label=f'{vtcolumns[i-1]} PRBs')

    plt.xlabel('Throughput (Mbps)')
    plt.ylabel('CDF')
    plt.legend()
    plt.grid(True)
    
    
    # Save plot as EPS
    plt.savefig(subpath + '_CFD_plot.eps', format='eps')

    # Save plot as PNG
    plt.savefig(subpath + '_CDF_plot.png', format='png')
    
    #plt.show()
    
    

    # Create a DataFrame
    # Additional headers as strings
    column_headers = ['Max BW (Mbps)', 'Mean BW (Mbps)', 'Std BW (Mbps)']
    df = pd.DataFrame(data=table_all, columns=column_headers)
    # Select PRBs sizes read
    nPRBs = len(subpaths)
    vtcolumns = vtcolumns[0:nPRBs]
    #print(vtcolumns)
    df['PRB'] = pd.Series( vtcolumns )
    df = df[['PRB','Max BW (Mbps)', 'Mean BW (Mbps)', 'Std BW (Mbps)']] 
    df = df.sort_values(by='PRB')
    df = df.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
    print(df)
    # Convert DataFrame to LaTeX format
    latex_table = df.to_latex(index=False)
    # Print or save the LaTeX table
    print(latex_table)
    
#folder_path = '2_UEs_ideal_iperf'
#open_iperf(folder_path ,1)