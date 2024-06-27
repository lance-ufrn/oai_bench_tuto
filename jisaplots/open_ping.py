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

def open_ping(folder_path):
    # List of file paths
    #folder_path = '1_UE_ideal_ping'
    #folder_path = '2_UEs_ideal_ping'

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
    combined_current_prb = []
    combined_data = []

    for subpath in subpaths: 

        # List of file paths
        files = os.listdir(subpath)
        # Print the list of file names
        #print("Files in the folder:")
        #for file in files:
        #    print(file)

        # List to hold Bandwidth and Interval data
        packetlosses = []
        read_data = []
        
        # Iterate over each file
        for file_name in files:
            full_path = os.path.join( subpath, file_name)
            print('Reading file {}'.format(full_path))
            packet_loss = None
            rtt_samples = []
            with open(full_path, 'r') as f:
                # Read all lines from the file
                lines = f.readlines()
                # Loop through each line to find ping statistics
                for line in reversed(lines):
                    line = line.strip()
                    
                    # Use regular expressions to find packet loss and RTT values
                    # Packet loss percentage
                    packet_loss_match = re.search(r'(\d+)% packet loss', line)
                    if packet_loss_match:
                        packet_loss = np.array(packet_loss_match.group(1))
                    
                    # Extract time values from each ping response line
                    time_match = re.search(r'time=(\d+(\.\d+)?) ms', line)
                    if time_match:
                        rtt_value = float(time_match.group(1))
                        rtt_samples.append(rtt_value)
                        
                                        
                rtt_min = np.min(rtt_samples)
                rtt_avg = np.mean(rtt_samples)
                rtt_max = np.max(rtt_samples)
                rtt_mdev = np.std(rtt_samples)
                rtt_number_of_samples = np.array(range(1, len(rtt_samples)+1))
                                        
            read_data.append((rtt_samples, rtt_number_of_samples, packet_loss, rtt_min, rtt_avg, rtt_max, rtt_mdev ))
                
        # Combine data from all files into a single list
        combined_rtt_samples = []
        combined_rtt_number_of_samples = []
        combined_packet_loss = []
        combined_rtt_min = []
        combined_rtt_avg  = []
        combined_rtt_max = []
        combined_rtt_mdev = []
        
        for rtt_samples, rtt_number_of_samples, packet_loss, rtt_min, rtt_avg, rtt_max, rtt_mdev in read_data:
            combined_rtt_samples.extend(rtt_samples)
            combined_rtt_number_of_samples.extend(rtt_number_of_samples)
            combined_rtt_min.append(rtt_min)
            combined_rtt_avg.append(rtt_avg)
            combined_rtt_max.append(rtt_max)
            combined_rtt_mdev.append(rtt_mdev)
        
        combined_current_prb.append(subpath[-3:])
            
        combined_rtt_samples = np.array(combined_rtt_samples)
        combined_packet_loss = np.array(combined_packet_loss)
    
        #print(combined_times) 
        #print(combined_packet_loss) 
        
        # Final metrics (regarding the hole vector of RTTs from all jobs)
        rtt_min = np.min(combined_rtt_samples)
        rtt_avg = np.mean(combined_rtt_samples)
        rtt_max = np.max(combined_rtt_samples)
        rtt_mdev = np.std(combined_rtt_samples)  
        
        print('rtt_min (from the mean of RTT min of each job) = {} and rtt_min (from all samples of all jobs) = {}'. format(np.mean(combined_rtt_min), rtt_min) )
        print('rtt_mean (from the mean of RTT mean of each job) = {} and rtt_mean (from all samples of all jobs) = {}'. format(np.mean(combined_rtt_avg), rtt_avg) )
        print('rtt_max (from the mean of RTT max of each job) = {} and rtt_max (from all samples of all jobs) = {}'. format(np.mean(combined_rtt_max), rtt_max) )
        print('rtt_std (from the mean of RTT std of each job) = {} and rtt_std (from all samples of all jobs) = {}'. format(np.mean(combined_rtt_mdev), rtt_mdev) )

        # create a table with values for all PRBs
        table_all.append((np.mean(combined_rtt_max), np.mean(combined_rtt_avg), np.mean(combined_rtt_mdev)))
        
        unique_intervals = np.unique(combined_rtt_number_of_samples)
        average_rtt_by_time = [np.mean(combined_rtt_samples[combined_rtt_number_of_samples == interval]) for interval in unique_intervals]

        combined_data.append((unique_intervals,average_rtt_by_time))

        #print(unique_intervals) 
        #print(average_bandwidths)  

        # Plot Bandwidth values vs Interval
        plt.figure(figsize=(10, 7))

        # Plot average Bandwidth values
        #xTime = np.linspace(0,180,len(unique_intervals))
        xTime = unique_intervals
        plt.plot(xTime, average_rtt_by_time, linestyle='-', color='black', label='Measured')

        average_rtt = np.mean(average_rtt_by_time)
        # Create a vector of average bandwidths with the same length as bandwidths
        average_rtt_vector = np.full_like(unique_intervals, average_rtt)

        # Plot average Bandwidth value
        plt.plot(xTime, average_rtt_vector, linestyle='--', color='red', label='Mean')

        # Customize plot
        #plt.title('Bandwidth vs Interval')
        plt.xlabel('Time (seconds)')
        plt.ylabel('RTT (ms)')
        plt.legend()
        plt.grid(True)
        #plt.xticks(xTime)
        plt.xlim(xTime[0],xTime[-1])
        plt.xticks(range(0,int(xTime[-1]+1),20))

        # Save plot as EPS
        plt.savefig(subpath + '_RTT_plot.eps', format='eps')

        # Save plot as PNG
        plt.savefig(subpath + '_RTT_plot.png', format='png')
        

        # Show plot (optional)
        plt.tight_layout()
        #plt.show()

    # plot two PRbs in the same plot
    plt.figure(figsize=(10, 7))
    i = 1
    ic = 1
    vtPlot_PRB = ['106', '273']
    vtline_color = ['black', 'red', 'blue', 'Orange' ]
    vtcolumns = combined_current_prb

    for unique_intervals,average_rtt_by_time in combined_data:
        if vtcolumns[i-1] in vtPlot_PRB:    
            # Plot average Bandwidth values
            plt.plot(unique_intervals, average_rtt_by_time, linestyle='-', color=f'{vtline_color[2*ic - 2]}', label=f'Measures - {vtcolumns[i-1]} PRBs')

            average_bw = np.mean(average_rtt_by_time)
            # Create a vector of average bandwidths with the same length as bandwidths
            average_bw_vector = np.full_like(unique_intervals, average_bw)

            # Plot average Bandwidth value
            plt.plot(unique_intervals, average_bw_vector, linestyle='--', color=f'{vtline_color[2*ic-1]}', label=f'Mean - {vtcolumns[i-1]} PRBs')
            ic = ic + 1
        i = i + 1
    plt.xlabel('Time (seconds)')
    plt.ylabel('RTT (ms)')
    plt.legend(loc='best')
    plt.xlim(xTime[0],xTime[-1])
    plt.xticks(range(0,int(xTime[-1]+1),20))
            
    plt.ylim(8,30)
    plt.grid(True)
    # Save plot as EPS
    plt.savefig(subpath + '_RTT_PRB_' + "_".join(vtPlot_PRB) + '_plot.svg', format='svg')

    # Save plot as PNG
    plt.savefig(subpath + '_RTT_PRB_' + "_".join(vtPlot_PRB) + '_plot.png', format='png')
    #plt.show()


    # Create a DataFrame
    # Additional headers as strings
    column_headers = ['Max RTT (ms)', 'Mean RTT (ms)', 'Std RTT (ms)']
    df = pd.DataFrame(data=table_all, columns=column_headers)
    df['PRB'] = pd.Series( combined_current_prb )
    df = df[['PRB','Max RTT (ms)', 'Mean RTT (ms)', 'Std RTT (ms)']] 
    df = df.sort_values(by='PRB')
    df = df.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
    print(df)
    # Convert DataFrame to LaTeX format
    latex_table = df.to_latex(index=False)
    # Print or save the LaTeX table
    print(latex_table)

