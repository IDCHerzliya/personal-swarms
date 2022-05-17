# 01 Flying (at least) two drones autonomously. 

The instructions in this walkthrough have been based from this [code](https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/swarm/swarmSequence.py). However, I'll include here instructions specific to the VR lab PC of the Magic Lab. 

## Preliminaries
- This assumes that you have done and completed all the steps found in the [01 Flying with  Python startup guide](https://github.com/IDCHerzliya/personal-swarms/blob/bc0bb27759ca780b2abc79ea94e0a4634f721e0c/documentation/01_flying-with-python.md). The rest of the codes that you can try can be found in this [repository](https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/swarm/swarmSequence.py).
- It assumes all preliminaries from previous guides are implemented. 

## Running the first flight scripts
There are many ways to do this however I would suggest we go the route of composing your code in a text editor such as Sublime and then compiling it in a command prompt. So you will see the instructions to be based on these platforms. 

- For this step, you will need to use this code: [02 Fly Multiple 01](https://github.com/IDCHerzliya/personal-swarms/blob/d84cea05babedcb2d72df3f9672f50e479d7b526/documentation/02_flymultiple_01.py).
- Dont forget to attach the crazyRadio PA dongle before you proceed any further. 
- In this specific walkthrough you we only added two drones. You will see in the script that all URIs 3 onwards are commented out. If you wish to add more drones, just uncomment them and add the respective channels and sequence combinations. The rest of the instructions in helping you build and modify the code can be 
- In your command prompt, run the code. You can do this by typing ``python 02_flymultiple_01.py``. The drones should fly and follow the programmed sequence. 
- In this scenario it is important to note that the initial position of the drone plays an important role in the behaviour that you want to show. 

Have fun! 





            

