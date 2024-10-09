from rocketpy import Flight
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('src/rockets/')
from comet1 import comet # Import comet1 
#from calisto import calisto # Import calisto
sys.path.append('src/environments/')
from euroc_env import env



test_flight = Flight(
    rocket=comet, 
    environment=env, 
    rail_length=12, 
    inclination=85, 
    heading=0,
    verbose=True,
)

#test_flight.all_info()

ax = test_flight.ax.get_value(np.linspace(0, 180, 100))
ay = test_flight.ay.get_value(np.linspace(0, 180, 100))
az = test_flight.az.get_value(np.linspace(0, 180, 100))

acceleration = np.sqrt(ax**2 + ay**2 + az**2)

plt.plot(np.linspace(0, 180, 100), acceleration)
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s^2)")
plt.show()