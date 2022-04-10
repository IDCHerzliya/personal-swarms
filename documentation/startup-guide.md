# Getting Starting with the Loco Swarm Bundle

This document contains the following sections:
- setting up the crazyflie drones
- setting up the programming environment for swarm control

*photos coming soon*

## Setting up the Crazyflie drones

For more info you can visit the Loco Positioning System documentation found in this [link](https://store.bitcraze.io/products/the-swarm-bundle). 

The complete guide for unpacking and setting up your CrazyFlie can be followed in this [guide](https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyflie-2-x/#unpacking-the-crazyflie). 


## Setting up the programming environment for swarm control

For more info you can visit the Loco Positioning System documentation found in this [link](https://www.bitcraze.io/documentation/system/positioning/loco-positioning-system/)

### Software, programs and modules used
- MagicLab C2 Laptop used for Virtual
- username: Swarm 
- Computer specs: Processor	Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz   2.59 GHz, Installed RAM	32.0 GB (31.9 GB usable), System type	64-bit operating system, x64-based processor
- Edition	Windows 10 Home, Version	20H2, OS build	19042.1288
- The latest update of the CrazyFlie 2.X firmware. You will need to install pip if the computer does not have it yet. Make sure that python is installed in your machine as it is one of the easiest way to install pip. 
- You will need the CrazyRadio PA when operating the drones via computer. Hint, you need a gamepad to fully control the CrazyFlie (like those PS4 controllers). 


#### Installing CrazyFlie PA on your computer
- Preliminaries: Install python first. Go to this [link](https://www.python.org/downloads/windows/) and follow instructions. To install, simply open cmd and type `'python'`. You can also use this to check whether you have the latest version of python in your computer. 
- Preliminaries: Install pip. To do this, download the file `'get-pip.py'` from this [site](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/) and then paste it in your local folder where python is installed. The folder directory should look something like this `'C:\Users\Swarm\AppData\Local\Programs\Python\Python310'` where `'Swarm'` is the local user account in Windows. Then opem command prompt and go the directory of the file. Run the command `'python get-pip.py'`. Wait for the download and installation to finish. Should have no issues. To verify if you have pip simply type `'pip -v'` in cmd and should return the latest details of your pip version. Now you can proceed to installing CrazyFlie PA in your system.
- The full installation instructions can be found [here](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/installation/install/). But for convenience some of the steps can be guided here. 
- The default pip package is on v2 and we need v3 on this. Thankfully the guide tells us to upgrade to pip3 first. In command prompt we can do this by simply typing `pip3 install --upgrade pip`. 
- We will also install `git` since we need it to get some files hosted in some online repositories. Install it from this [link](https://git-scm.com/). Once done to verify that you have git, simply type the command `git --version` in command prompt. It should show the details of the version installed. 
- Once ready we can proceed with installing the CrazyFlie radio drivers. The full instructions, which uses git, can be followed or reviewed in this [link](https://github.com/bitcraze/crazyradio-firmware/blob/master/docs/building/usbwindows.md). The instructions I did will be seen in the next bullets below. 
- We need Zadig as another preliminaries to use crazyradio PA for the crazyflie. You can download it from this [link](https://zadig.akeo.ie/). We need Zadig because most Bitcraze systems run on libusb (the windows generic usb library) to be able to utilize it for external controls which may have been updated or changed with the later windows versions. Download the executable and install it. 
- Zadig window should open. Plug the crazyradio PA usb dongle into the PC. Then you will be notified that the CrazyFlie has been setup and is ready to go (pun intended haha). 
- Once installed, check out Zadig and the crazyflie should be visible. Select it in the interface and select **libusb** (or in this case `libusb-win 32 v1.2.6.0` and click Install. Once Install is complete, proceed to the next step. 
- We proceed with installing from source option. It should redirect you to instructions found in this [link](https://github.com/bitcraze/crazyflie-lib-python). 
- To do this, clone the project by typing this command in cmd `git clone https://github.com/bitcraze/crazyflie-clients-python`. Wait for the instructions to complete. 
- After installing, change directory by typing `cd crazyflie-clients-python`. 
- Then install by typing the command `cd crazyflie-clients-python .`. Yes the period is included as an argument. Wait for the install to complete. 
- To test if you have installed the client, you can call it by executing the command `python3 -m cfclient.gui`. This will unpack some stuff and open the GUI and youre ready to proceed to the next step. 

#### Configuring the CF client 
##### Configure your controller (kinda of optional i think - will revise soon)
- At this stage you will need the gamepad controller to configure it properly. 
- If you are not sure or not willing to do this yet, proceed to the next step

##### Making sure your firmware is always updated
- At this stage, plug in the crazradio PA USB dongle since updates happen through this and not directly from the USB connection of the crazyflie drone 
- Select the radio frequency and choose `Connect`. 
- When the drone changes colors (red blinking once every second and a constant yellow around M4) then you are ready to fly.

Fly away!



