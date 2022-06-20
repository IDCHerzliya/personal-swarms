
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

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm

# Change uris according to your setup
#URI0 = 'radio://0/100/2M'
URI1 = 'radio://0/102/2M'
URI2 = 'radio://0/104/2M'
URI3 = 'radio://0/106/2M'

# d: diameter of circle
# z: altitude
params0 = {'d': 0.5, 'z': 1.0}
params1 = {'d': 0.5, 'z': 1.0}
params2 = {'d': 0.0, 'z': 1.5} 
params2 = {'d': 0.5, 'z': 1.0}
params3 = {'d': 0.5, 'z': 1.0}


uris = {
 #   URI0,
    URI1,
    URI2,
    URI3,
   # URI4,
}

params = {
  #  URI0: [params0],
     URI1: [params1],
     URI2: [params2],
     URI3: [params3],
 #   URI4: [params1],
}


def poshold(cf, t, z):
    steps = t * 1

    for r in range(steps):
        cf.commander.send_hover_setpoint(0, 0, 0, z)
        time.sleep(0.1)


def run_sequence(scf, params):
    cf = scf.cf

    # Number of setpoints sent per second
    fs = 3 #changed from 5
    fsi = 1.0 / fs

    # Compensation for unknown error :-(
    comp = 1.5

    # Base altitude in meters
    base = 0.5

    d = params['d']
    z = params['z']

    poshold(cf, 5, base) #changed from 2

    ramp = fs * 2
    for r in range(ramp):
        cf.commander.send_hover_setpoint(0, 0, 0, base + r * (z - base) / ramp)
        time.sleep(fsi)

    poshold(cf, 5, z)

    for _ in range(2):
        # The time for one revolution
        circle_time = 8

        steps = circle_time * fs
        for _ in range(steps):
            cf.commander.send_hover_setpoint(d * comp * math.pi / circle_time,
                                             0, 360.0 / circle_time, z)
            time.sleep(fsi)

    poshold(cf, 5, z)

    for r in range(ramp):
        cf.commander.send_hover_setpoint(0, 0, 0,
                                         base + (ramp - r) * (z - base) / ramp)
        time.sleep(fsi)

    poshold(cf, 3, base)

    cf.commander.send_stop_setpoint()


if __name__ == '__main__':
    cflib.crtp.init_drivers()

    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        swarm.reset_estimators()
        swarm.parallel(run_sequence, args_dict=params)