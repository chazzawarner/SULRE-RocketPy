from rocketpy import Flight
import sys
sys.path.append('src/rockets/')
from calisto import calisto
sys.path.append('src/environments/')
from test_env import env

test_flight = Flight(
    rocket=calisto, environment=env, rail_length=5.2, inclination=85, heading=0
    )

test_flight.plots.trajectory_3d()
test_flight.plots.linear_kinematics_data()