# Information about the environment used

* Kernel version
  * Before installing other packages, install the indicated kernel. After installation, perform a reboot.
  * Installation command: `sudo apt install linux-image-5.15.0-89-lowlatency -y`
  * After the reboot, make sure that the installed kernel has been loaded with the `uname -a` command.

* Host used: Lenovo SR630 - 64bit x84 architecture
  * **Processor:** Intel Xeon Gold 5218R
  * **RAM:** 128GB DDR4 (4x 32GB) - Dual Channel
  * **HDD:** 10TB
  * **Operating System:** Ubuntu Desktop 20.04 LTS (Fresh install)
  * **Ettus driver:** version v4.4.0.0

* USRP Ettus N310
  * Ettus driver: version v4.4.0.0

# Environment installation
## Step 1: Clone this Repository
After installing the indicated `Kernel` on a clean installation of Ubuntu Desktop 20.04 LTS, perform the following procedures:

Clone this repository on your Linux system:
```
git clone https://github.com/lance-ufrn/oai_bench_tuto.git
```

## Step 2: Install Docker and Ettus driver
Run the `./oai_5g_core_install.sh` script. It will be responsible for installing Docker and the necessary OpenAirInterface resources. Do not use `sudo` to execute the script, but the user must have permission to use the `sudo` command (which is present when executing the script's internal commands).

```bash
./oai_5g_core_install.sh
```


# Using the environment
## Step 1: Initializing 5GC
To initialize the core services you must use the `core-start.sh` script.

```bash
./core-start.sh
```

## Step 2: Run the gNodeB Docker container
Make sure that the USRP (Ettus N310 or Ettus B210) is connected **directly** to the host machine.
* Ettus N310: Make sure that the IP address of the USRP communication interface is correctly indicated in the configuration files (from the `conf` directory, the `addr` parameter of the `sdr_addrs` property);
* Ettus B210: Make sure it is connected to the host via a USB3 port or higher.

To initialize the container, run the following command:
```bash
./services.sh [parameter]
```

Available parameters:
- `n106` to use PRB = 106 on USRP N310
- `n162` to use PRB = 162 in USRP N310
- `n273` to use PRB = 273 in USRP N310
- `b106` to use PRB = 106 in USRP B210
- `b162` to use PRB = 162 in USRP B210
- `stop` to end the containers

Example: `./services.sh n106`

This will run a shell script that will start a container with the settings mentioned above.


## Stopping 5GC services
To stop core services you must use the `core-stop.sh` script.

```bash
./core-stop.sh
```

# How to configure
* [USRP Ettus N310](docs/conf-n310/README-usrp-n310.md)
* [Performance Mode](docs/conf-performance/README.md)
* [Configure SIMCard](docs/conf-simcard/README.md)
* [UE Motorola G50](docs/conf-Motorola-G50/README.md)

# Troubleshooting

In this section, we discuss common issues encountered during the setup and deployment phases of the OAI 5G network and provide solutions. 

* Docker Container Failures:
   - **Issue**: Containers fail to start due to missing dependencies.
   - **Solution**: Ensure all dependencies are installed before running the containers. Use the command `docker logs [container_id]` to get detailed error messages. 

* USRP Connection Problems:
   - **Issue**: USRP device not recognized by the host machine.
   - **Solution**: Verify the USRP is properly connected and the correct IP address is configured. Use the command `uhd_find_devices` to detect connected USRP devices.

* Network Configuration Errors:
   - **Issue**: No communication between gNB and 5GC.
   - **Solution**: Check IP forwarding and iptables settings. Ensure that the gNB configuration file has the correct IP addresses for the 5GC components.

* Signal Quality Issues:
   - **Issue**: Poor signal quality or no signal detected.
   - **Solution**: Verify antenna connections and ensure they are properly placed. Adjust the transmission power settings in the configuration file.
    
* Performance Bottlenecks:
   - **Issue**: Suboptimal throughput performance.
   - **Solution**: Monitor CPU and memory usage to identify bottlenecks. Adjust the configuration parameters such as `nb_tx`, `nb_rx`, and `max_rxgain` to optimize performance.
 
# Citation
If you use this tutorial, please cite our paper to appear in the Journal of Internet Services and Applications (JISA). Here is a suitable BibTeX entry:

```bibtex
@article{Virtualized_5G_2024,
    title = {Virtualized 5G Testbed using OpenAirInterface: Tutorial and Benchmarking Tests},
    author = {Dória, Matheus and Sousa, Vicente and Campos, Antonio and Oliveira, Nelson and
              Eduardo, Paulo and Filho, Paulo and Lima, Carlos and Guilherme, João and
              Luna, Daniel and Rego, Iago and Fernandes, Marcelo and Neto, Augusto},
    journal = {Journal of Internet Services and Applications},
    volume = {15},
    number = {1},
    pages = {523–535},
    year = {2024},
    month = {Oct.},
    url = {https://journals-sol.sbc.org.br/index.php/jisa/article/view/4454},
    DOI = {10.5753/jisa.2024.4454}
}
```

