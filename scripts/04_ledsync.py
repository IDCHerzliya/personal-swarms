"""
Simple example of a synchronized swarm choreography using the High level
commander.

The swarm takes off and flies a synchronous choreography before landing.
The take-of is relative to the start position but the Goto are absolute.
The sequence contains a list of commands to be executed at each step.

This example is intended to work with any absolute positioning system.
It aims at documenting how to use the High Level Commander together with
the Swarm class to achieve synchronous sequences.
"""

import math
import time

# LED related scripts 
import logging
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.mem import MemoryElement
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

# sync related scripts
import threading
import time
from collections import namedtuple
from queue import Queue
#import cflib.crtp commented cos redundant
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm

# ======================================================
# some inefficient code to light up LEDS 
# this way you know if the crazyflie is about to flie 
# =====================================================

# Change uris according to your setup
URI0 = 'radio://0/100/2M'
URI1 = 'radio://0/102/2M'
#URI2 = 'radio://0/94/2M/E7E7E7E7E7'
URI3 = 'radio://0/104/2M'
URI4 = 'radio://0/106/2M'

#URI = uri_helper.uri_from_env(default='radio://0/106/2M')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI0, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        # Set virtual mem effect effect
        cf.param.set_value('ring.effect', '13')

        # Get LED memory and write to it
        mem = cf.mem.get_mems(MemoryElement.TYPE_DRIVER_LED)
        if len(mem) > 0:
            mem[0].leds[0].set(r=0, g=100, b=0)
            mem[0].leds[3].set(r=0, g=0, b=100)
            mem[0].leds[6].set(r=100, g=0, b=0)
            mem[0].leds[9].set(r=100, g=100, b=100)
            mem[0].write_data(None)

        time.sleep(2)

#URI = uri_helper.uri_from_env(default='radio://0/104/2M')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI1, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        # Set virtual mem effect effect
        cf.param.set_value('ring.effect', '13')

        # Get LED memory and write to it
        mem = cf.mem.get_mems(MemoryElement.TYPE_DRIVER_LED)
        if len(mem) > 0:
            mem[0].leds[0].set(r=0, g=100, b=0)
            mem[0].leds[3].set(r=0, g=0, b=100)
            mem[0].leds[6].set(r=100, g=0, b=0)
            mem[0].leds[9].set(r=100, g=100, b=100)
            mem[0].write_data(None)

        time.sleep(2)

#URI = uri_helper.uri_from_env(default='radio://0/102/2M')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI3, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        # Set virtual mem effect effect
        cf.param.set_value('ring.effect', '13')

        # Get LED memory and write to it
        mem = cf.mem.get_mems(MemoryElement.TYPE_DRIVER_LED)
        if len(mem) > 0:
            mem[0].leds[0].set(r=0, g=100, b=0)
            mem[0].leds[3].set(r=0, g=0, b=100)
            mem[0].leds[6].set(r=100, g=0, b=0)
            mem[0].leds[9].set(r=100, g=100, b=100)
            mem[0].write_data(None)

        time.sleep(2)

#URI = uri_helper.uri_from_env(default='radio://0/100/2M')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI4, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        # Set virtual mem effect effect
        cf.param.set_value('ring.effect', '13')

        # Get LED memory and write to it
        mem = cf.mem.get_mems(MemoryElement.TYPE_DRIVER_LED)
        if len(mem) > 0:
            mem[0].leds[0].set(r=0, g=100, b=0)
            mem[0].leds[3].set(r=0, g=0, b=100)
            mem[0].leds[6].set(r=100, g=0, b=0)
            mem[0].leds[9].set(r=100, g=100, b=100)
            mem[0].write_data(None)

        time.sleep(2)


# ========================================================================
# begin here code to activate the swarm and make them fly sync
# ========================================================================

# Time for one step in second
STEP_TIME = 1

# Possible commands, all times are in seconds
Takeoff = namedtuple('Takeoff', ['height', 'time'])
Land = namedtuple('Land', ['time'])
Goto = namedtuple('Goto', ['x', 'y', 'z', 'time'])
RGB [0-255], Intensity [0.0-1.0] #commented out for the LED, comment this again if it causes errors
Ring = namedtuple('Ring', ['r', 'g', 'b', 'intensity', 'time'])
# Reserved for the control loop, do not use in sequence
Quit = namedtuple('Quit', [])

uris = [
    'radio://0/100/2M',  # cf_id 0, startup position [-0.5, -0.5]
    'radio://0/102/2M',  # cf_id 1, startup position [ 0, 0]
    'radio://0/104/2M',  # cf_id 2, startup position [0.5, 0.5]
    'radio://0/106/2M',  # cf_id 3, startup position [0, 0]
    # Add more URIs if you want more copters in the swarm
]

#this sequence will be execute by the functions later on
sequence = [
    # Step, CF_id,  action

    #take off altogether after 2 seconds delay time
    (0,    0,      Takeoff(0.5, 2)),
    (0,    1,      Takeoff(0.5, 2)),
    (0,    2,      Takeoff(0.5, 2)),
    (0,    3,      Takeoff(0.5, 2)),

    #at time sequence 2 and after 1s delay, go to x y z coordinates - even drones
    (2,    0,      Goto(-0.5,  -0.5,   0.5, 1)),
    (2,    2,      Goto(0.5,  0.5,   0.5, 1)),

    #at time sequence 3 and after 1s delay, go to x y z coordinates - odd drones
    (3,    1,      Goto(0,  0,   1, 1)),
    (3,    3,      Goto(0,  0,   1, 1)),

    #at time sequence 4 change color of odd and even drones alternately based on RGB values specified
    (4,    0,      Ring(255, 255, 255, 0.2, 0)),
    (4,    1,      Ring(255, 0, 0, 0.2, 0)),
    (4,    2,      Ring(255, 255, 255, 0.2, 0)),
    (4,    3,      Ring(255, 0, 0, 0.2, 0)),

   #at time sequence 5 and after 2s delay, go to x y z coordinates - even drones
    (5,    0,      Goto(0.5, -0.5, 0.5, 2)),
    (5,    2,      Goto(-0.5, 0.5, 0.5, 2)),

   #at time sequence 7 and after 2s delay, go to x y z coordinates - odd drones
    (7,    1,      Goto(0.5, 0.5, 0.5, 2)),
    (7,    3,      Goto(-0.5, -0.5, 0.5, 2)),

  #at time sequence 9 and after 2s delay, go to x y z coordinates - even drones
    (9,    0,      Goto(-0.5, 0.5, 0.5, 2)),
    (9,    2,      Goto(0.5, -0.5, 0.5, 2)),

   #at time sequence 11 and after 2s delay, go to x y z coordinates - odd drones
    (11,   0,      Goto(-0.5, -0.5, 0.5, 2)),
    (11,   2,      Goto(0.5, 0.5, 0.5, 2)),

   #at time sequence 13 land all drones at current position after 2 second delay
    (13,    0,      Land(2)),
    (13,    1,      Land(2)),
    (13,    2,      Land(2)),

   #at time sequence 15 remove LED right light confi after 5s delay
    (15,    0,      Ring(0, 0, 0, 0, 5)),
    (15,    1,      Ring(0, 0, 0, 0, 5)),
    (15,    2,      Ring(0, 0, 0, 0, 5)),
]


def activate_high_level_commander(scf):
    scf.cf.param.set_value('commander.enHighLevel', '1')


def activate_mellinger_controller(scf, use_mellinger):
    controller = 1
    if use_mellinger:
        controller = 2
    scf.cf.param.set_value('stabilizer.controller', str(controller))


def set_ring_color(cf, r, g, b, intensity, time):
    cf.param.set_value('ring.fadeTime', str(time))

    r *= intensity
    g *= intensity
    b *= intensity

    color = (int(r) << 16) | (int(g) << 8) | int(b)

    cf.param.set_value('ring.fadeColor', str(color))


def crazyflie_control(scf):
    cf = scf.cf
    control = controlQueues[uris.index(cf.link_uri)]

    activate_mellinger_controller(scf, False)

    commander = scf.cf.high_level_commander

    # Set fade to color effect and reset to Led-ring OFF
    set_ring_color(cf, 0, 0, 0, 0, 0)
    cf.param.set_value('ring.effect', '14')

    while True:
        command = control.get()
        if type(command) is Quit:
            return
        elif type(command) is Takeoff:
            commander.takeoff(command.height, command.time)
        elif type(command) is Land:
            commander.land(0.0, command.time)
        elif type(command) is Goto:
            commander.go_to(command.x, command.y, command.z, 0, command.time)
        elif type(command) is Ring:
            set_ring_color(cf, command.r, command.g, command.b,
                           command.intensity, command.time)
            pass
        else:
            print('Warning! unknown command {} for uri {}'.format(command,
                                                                  cf.uri))

def control_thread():
    pointer = 0
    step = 0
    stop = False

    while not stop:
        print('Step {}:'.format(step))
        while sequence[pointer][0] <= step:
            cf_id = sequence[pointer][1]
            command = sequence[pointer][2]

            print(' - Running: {} on {}'.format(command, cf_id))
            controlQueues[cf_id].put(command)
            pointer += 1

            if pointer >= len(sequence):
                print('Reaching the end of the sequence, stopping!')
                stop = True
                break

        step += 1
        time.sleep(STEP_TIME)

    for ctrl in controlQueues:
        ctrl.put(Quit())


if __name__ == '__main__':
    controlQueues = [Queue() for _ in range(len(uris))]

    cflib.crtp.init_drivers()
    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        swarm.parallel_safe(activate_high_level_commander)
        swarm.reset_estimators()

        print('Starting sequence!')

        threading.Thread(target=control_thread).start()

        swarm.parallel_safe(crazyflie_control)

        time.sleep(1)