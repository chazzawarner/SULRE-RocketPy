from rocketpy import Flight
import sys
sys.path.append('src/rockets/')
from comet1 import comet # Import comet1 instead of calisto
sys.path.append('src/environments/')
from test_env import env

test_flight = Flight(
    rocket=comet, environment=env, rail_length=12, inclination=85, heading=0
    )

#test_flight.plots.trajectory_3d()
test_flight.plots.linear_kinematics_data()
