# this code was derived from https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/swarm/swarmSequence.py 
"""
Code for hovering crazyflies. 

The layout of the positions:
    x2      x1      x0

y3  10              4

            ^ Y
            |
y2  9       6       3
            |
            +------> X

y1  8       5       2



y0  7               1

"""
import time

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm

# Change uris and sequences according to your setup
URI1 = 'radio://0/102/2M'
URI2 = 'radio://0/104/2M'
#URI3 = 'radio://0/106/2M'
#URI4 = 'radio://0/106/2M'

# Magic Lab swarm channels can be found in this script https://github.com/IDCHerzliya/personal-swarms/blob/bc0bb27759ca780b2abc79ea94e0a4634f721e0c/scripts/00_drone%20radio%20channels.md 

z0 = 0.5
z = 1.0

x0 = 0.0
x1 = 2.0
x2 = 0.0

y0 = 0
y1 = 2.0
y2 = 0
y3 = 0

#    x   y   z  time
sequence1 = [
    (x0, y0, z0, 5.0),
    (x0, y0, z, 10.0),
    (x1, y0, z, 5.0),
    (x1, y0, z0, 5.0),
]


# i will be preserving all 10 sequences. just replace the variables below with the sequence you want to test. the next stage would be to play around with the values of these sequence for testing purposes

seq_args = {
    URI1: [sequence1],
    URI2: [sequence1],
  #  URI3: [sequence1],
   #URI4: [sequence2],
    #URI5: [sequence5],
    #URI6: [sequence6],
    #URI7: [sequence7],
    #URI8: [sequence8],
    #URI9: [sequence9],
    #URI10: [sequence10],
}

# List of URIs, comment the one you do not want to fly
uris = {
    URI1,
    URI2,
  #  URI3,
  #  URI4,
 #   URI5,
 #   URI6,
 #   URI7,
 #   URI8,
 #   URI9,
 #   URI10
}


def wait_for_param_download(scf):
    while not scf.cf.param.is_updated:
        time.sleep(1.0)
    print('Parameters downloaded for', scf.cf.link_uri)


def take_off(cf, position):
    take_off_time = 1.0
    sleep_time = 0.1
    steps = int(take_off_time / sleep_time)
    vz = position[2] / take_off_time

    print(vz)

    for i in range(steps):
        cf.commander.send_velocity_world_setpoint(0, 0, vz, 0)
        time.sleep(sleep_time)


def land(cf, position):
    landing_time = 1.0
    sleep_time = 0.1
    steps = int(landing_time / sleep_time)
    vz = -position[2] / landing_time

    print(vz)

    for _ in range(steps):
        cf.commander.send_velocity_world_setpoint(0, 0, vz, 0)
        time.sleep(sleep_time)

    cf.commander.send_stop_setpoint()
    # Make sure that the last packet leaves before the link is closed
    # since the message queue is not flushed before closing
    time.sleep(0.1)


def run_sequence(scf, sequence):
    try:
        cf = scf.cf

        take_off(cf, sequence[0])
        for position in sequence:
            print('Setting position {}'.format(position))
            end_time = time.time() + position[3]
            while time.time() < end_time:
                cf.commander.send_position_setpoint(position[0],
                                                    position[1],
                                                    position[2], 0)
                time.sleep(0.1)
        land(cf, sequence[-1])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    cflib.crtp.init_drivers()

    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        # If the copters are started in their correct positions this is
        # probably not needed. The Kalman filter will have time to converge
        # any way since it takes a while to start them all up and connect. We
        # keep the code here to illustrate how to do it.
        # swarm.reset_estimators()

        # The current values of all parameters are downloaded as a part of the
        # connections sequence. Since we have 10 copters this is clogging up
        # communication and we have to wait for it to finish before we start
        # flying.
        print('Waiting for parameters to be downloaded...')
        swarm.parallel(wait_for_param_download)

        swarm.parallel(run_sequence, args_dict=seq_args)