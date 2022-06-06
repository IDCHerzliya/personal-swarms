"""
A script to fly 5 Crazyflies in formation. One stays in the center and the
other four fly around it in a circle. Mainly intended to be used with the
Flow deck.
The starting positions are vital and should be oriented like this

     >

^    +    v

     <

The distance from the center to the perimeter of the circle is around 0.5 m

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

# swarm related scripts
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
# begin here code to activate the swarm and make them do a circle
# ========================================================================


# d: diameter of circle
# z: altitude
params0 = {'d': 1.0, 'z': 0.3}
params1 = {'d': 1.0, 'z': 0.3}
#params2 = {'d': 0.0, 'z': 0.5} commented for now 
params3 = {'d': 1.0, 'z': 0.3}
params4 = {'d': 1.0, 'z': 0.3}


uris = {
    URI0,
    URI1,
    #URI2,
    URI3,
    URI4,
}

params = {
    URI0: [params0],
    URI1: [params1],
    #URI2: [params2],
    URI3: [params3],
    URI4: [params4],
}


def poshold(cf, t, z):
    steps = t * 10

    for r in range(steps):
        cf.commander.send_hover_setpoint(0, 0, 0, z)
        time.sleep(0.1)


def run_sequence(scf, params):
    cf = scf.cf

    # Number of setpoints sent per second
    fs = 4
    fsi = 1.0 / fs

    # Compensation for unknown error :-(
    comp = 1.3

    # Base altitude in meters
    base = 0.15

    d = params['d']
    z = params['z']

    poshold(cf, 2, base)

    ramp = fs * 2
    for r in range(ramp):
        cf.commander.send_hover_setpoint(0, 0, 0, base + r * (z - base) / ramp)
        time.sleep(fsi)

    poshold(cf, 2, z)

    for _ in range(2):
        # The time for one revolution
        circle_time = 8

        steps = circle_time * fs
        for _ in range(steps):
            cf.commander.send_hover_setpoint(d * comp * math.pi / circle_time,
                                             0, 360.0 / circle_time, z)
            time.sleep(fsi)

    poshold(cf, 2, z)

    for r in range(ramp):
        cf.commander.send_hover_setpoint(0, 0, 0,
                                         base + (ramp - r) * (z - base) / ramp)
        time.sleep(fsi)

    poshold(cf, 1, base)

    cf.commander.send_stop_setpoint()


if __name__ == '__main__':
    cflib.crtp.init_drivers()

    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        swarm.reset_estimators()
        swarm.parallel(run_sequence, args_dict=params)

        