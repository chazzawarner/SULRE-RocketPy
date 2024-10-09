from rocketpy import EnvironmentAnalysis, Environment
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import json

# Basic environmental analysis of Euroc launch site in Portugal (from RocketPy docs examples)
## Mean profiles already exists so shouldn't need to run this again!
"""env_analysis = EnvironmentAnalysis(
    start_date=datetime(2002, 10, 6),  # (Year, Month, Day)
    end_date=datetime(2021, 10, 23),  # (Year, Month, Day)
    start_hour=4,
    end_hour=20,
    latitude=39.3897,
    longitude=-8.28896388889,
    surface_data_file="src/data/climate/EuroC_single_level_reanalysis_2002_2021.nc",
    pressure_level_data_file="src/data/climate/EuroC_pressure_levels_reanalysis_2001-2021.nc",
    timezone="Europe/Lisbon",
    unit_system="metric",
)

env_analysis.export_mean_profiles("src/data/climate/EuroC_mean_profiles_2002_2021")

env_analysis.info()"""

# Defining the EuroC environment for sims using the mean profiles of historical data (from above)
with open('src/data/climate/EuroC_mean_profiles_2002_2021.json', 'r') as f:
    env_mean_profiles = json.load(f)
    
print(env_mean_profiles.keys())

# Setting up the environment class using the mean profiles file
flight_time = 12 # pm in Portugal timezone, must be between 4 and up to but not including 20
flight_date = datetime(2021, 10, 10, flight_time) # (Year, Month, Day, Hour), must be between 2002 and 2021 inclusive and between October 6th and October 23rd inclusive
latitude = env_mean_profiles['latitude'] # Standard Portugual EuroC launch site
longitude = env_mean_profiles['longitude']
timezone = env_mean_profiles['timezone'] # Europe/Lisbon
elevation = env_mean_profiles['elevation'] # ~110m (above sea level)

env = Environment(
    date=flight_date,
    latitude=latitude,
    longitude=longitude,
    elevation=elevation,
    timezone=timezone,
)

# Setting the atmospheric model to the custom atmosphere from the mean profiles
pressure = None # Altitude vs pressure is "not bijective", shelving for now, using standard

temperature = env_mean_profiles['atmospheric_model_temperature_profile'][str(flight_time)]
temperature = np.array(temperature)
temperature[:, 1] = temperature[:, 1] + 273.15 # Convert to Kelvin (from Celsius

wind_u = env_mean_profiles['atmospheric_model_wind_velocity_x_profile'][str(flight_time)] # I've made the assumption that the x and y profiles are the u and v components of the wind - maybe they're not but that's a problem for future me
wind_v = env_mean_profiles['atmospheric_model_wind_velocity_y_profile'][str(flight_time)]

env.set_atmospheric_model(
    type="custom_atmosphere",
    pressure=pressure,
    temperature=temperature,
    wind_u=wind_u,
    wind_v=wind_v,
)

#env.info()