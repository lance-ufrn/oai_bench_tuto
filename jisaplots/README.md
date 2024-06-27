# Information about some plots

This repository contains the scripts used to generate the plots presented in the tutorial "Virtualized 5G Tesbed using OpenAirInterface: Tutorial and Benchmarking Tests". The tutorial is available at the Journal of Internet Services and Applications (JISA).

# How to generate the plots

Three auxiliary scripts are available to generate the plots. The scripts are:   

- `open_iperf.py`: This script generates the plots and tables of the throughput of the iperf3 tests. The script receives the path to the iperf3 log file as an argument. The script generates a plot with the throughput of the iperf3 tests. The plot is saved in the same directory as the log file in PNG and VSG format. A Latex table is also generated with the throughput values (min, max, average and standard deviation).

- `open_ping.py`: This script generates the plot of the ping tests. The script receives the path to the ping log file as an argument. The script generates a plot with the ping tests. The plot is saved in the same directory as the log file in PNG and VSG format. A Latex table is also generated with the throughput values (min, max, average and standard deviation).

- `all_figures.py`: This script generates all the plots and tables of the iperf3 and ping tests. The script calls the corresponding auxiliary scripts with the proper path to the directory containing the log files. 

- `iperf_distance.py`: This script generates the plot of the throughput of the iperf3 tests for different distances between the UE and the gNB. 

# Citation

If you use this tutorial, please cite our paper to appear in the Journal of Internet Services and Applications (JISA). Here is a suitable BibTeX entry:

```python
@inproceedings{OAITuto2024,
  title = {{Virtualized 5G Tesbed using OpenAirInterface: Tutorial and Benchmarking Tests}},
  author = {Antonio Campos and Vicente Sousa and Nelson Oliveira and Paulo Eduardo and Paulo Filho and Matheus Dória and Carlos Lima and João Guilherme and Daniel Luna and Iago Rego and Marcelo Fernandes and Augusto Neto},
  booktitle = {Journal of Internet Services and Applications, 2024},
  year = {2024}
}
```