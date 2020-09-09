### Nvidia CUDA installation

This tutorial shows installation of Nvidia driver 435, and CUDA 10.1 on Ubuntu16.04.

Remark: A good reference can be found [here](https://gist.github.com/wangruohui/df039f0dc434d6486f5d4d098aa52d07)


Typically you do,
	```
	sudo -E add-apt-repository ppa:graphics-drivers/ppa
	sudo apt install nvidia-driver-435
	```

However, this does not always work, you may see something like:

	```
	Reading package lists... Done
	Building dependency tree
	Reading state information... Done
	E: Unable to locate package nvidia-driver-435
	```

An alternative is to directly use the installation file provided by Nvidia:

1. Check your Nvidia card info:
	`sudo lshw -C display`

	You should see something like (very old card I know):
	```
	display UNCLAIMED
       description: 3D controller
       product: GP100GL [Tesla P100 PCIe 16GB]
       vendor: NVIDIA Corporation
       physical id: 0
       bus info: pci@0000:04:00.0
       version: a1
       width: 64 bits
       clock: 33MHz
       capabilities: pm msi pciexpress bus_master cap_list
       configuration: latency=0
     ```
2. Obtain the .run file. Go to [Nvidia Download page](https://www.nvidia.com/Download/index.aspx),
fill in:
    * the correct product (in our case, Tesla P100)
    * OS info (in our case Linux 64bit)
    * CUDA version (in our case 10.1)
    
    and do search. In return, we get this [page](https://www.nvidia.com/Download/driverResults.aspx/160657/en-us).
Click the download link to be directed to a new page. Agree and Download, 
the run file will start to be downloaded via your browser.

    If you want to download the run file to a remote machine, copy the download link,
    and do e.g.:
    
    `wget https://us.download.nvidia.com/tesla/418.152.00/NVIDIA-Linux-x86_64-418.152.00.run`
    
3. Run .run file in remote:
    `sudo sh path/to/NVIDIA-Linux-x86_64-418.152.00.run`

4. Verify:
    `nvidia-smi`


