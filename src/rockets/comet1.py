from rocketpy import Rocket, Fluid, LiquidMotor, CylindricalTank, MassFlowRateBasedTank, MassBasedTank
from math import exp

# Define constants
rocket_radius = 0.152 / 2 #m
rocket_length = 2.9 #m
nose_length = 0.5 #m

# Initialise rocket
comet = Rocket(
    radius=rocket_radius, #m
    mass=16.82, #kg (mass without motor and engine mass (7.6kg))
    inertia=(11.73, 0.08, 11.73), #kg*m^2 ???
    power_off_drag="src/data/comet1/comet1v5 drag curve2.csv", #path to csv file
    power_on_drag="src/data/comet1/comet1v5 drag curve2.csv", #path to same csv file
    center_of_mass_without_motor=1.4, #m
    coordinate_system_orientation="nose_to_tail"
)

# Add motor
## Define fluids (taken from encyclopedia.airliquide.com for N20 and N2, google for IPA - please change)
oxidizer_liq = Fluid(name="N2O_l", density=1230)
oxidizer_gas = Fluid(name="N2O_g", density=881.5) # Calculated using mass/volume from excel

fuel_liq = Fluid(name="IPA_l", density=785.1)
fuel_gas = Fluid(name="IPA_g", density=2.67)

nitrogen_liq = Fluid(name="N2_l", density=806.11)
nitrogen_gas = Fluid(name="N2_g", density=343.6) # Calculated using mass/volume from excel

## Define tanks (Taking these from "Combined Calcs.xlsx")

### Define oxidizer tank
oxidizer_tank_shape = CylindricalTank(radius = 0.127/2, height = 0.582)
#print(oxidizer_tank_shape.total_volume)

oxidizer_tank = MassFlowRateBasedTank(
    name="oxidizer tank",
    geometry=oxidizer_tank_shape,
    flux_time=8,
    initial_liquid_mass=0.01,
    initial_gas_mass=5.336,
    liquid_mass_flow_rate_in=0,
    liquid_mass_flow_rate_out=0,
    gas_mass_flow_rate_in=0,
    gas_mass_flow_rate_out=0.667,
    liquid=oxidizer_liq,
    gas=oxidizer_gas,
)

### Define fuel tank
fuel_tank_shape = CylindricalTank(radius = 0.127/2, height = 0.158)
fuel_tank = MassFlowRateBasedTank(
    name="fuel tank",
    geometry=fuel_tank_shape,
    flux_time=8,
    initial_liquid_mass=0.992,
    initial_gas_mass=0,
    liquid_mass_flow_rate_in=0,
    liquid_mass_flow_rate_out=0.124,
    gas_mass_flow_rate_in=0,
    gas_mass_flow_rate_out=0,
    liquid=fuel_liq,
    gas=fuel_gas,
)

### Define nitrogen tank (No clue what happens here)
nitrogen_tank_shape = CylindricalTank(radius = 0.111/2, height = 0.296) # Unsure if spherical caps are on top of current length or not
nitrogen_tank = MassFlowRateBasedTank(
    name="nitrogen tank",
    geometry=nitrogen_tank_shape,
    flux_time=8,
    initial_liquid_mass=0,
    initial_gas_mass=0.5,
    liquid_mass_flow_rate_in=0,
    liquid_mass_flow_rate_out=0,
    gas_mass_flow_rate_in=0,
    gas_mass_flow_rate_out=0,
    liquid=nitrogen_liq,
    gas=nitrogen_gas,
)

## Add tanks to motor
engine = LiquidMotor( # What's the engine's name?
    thrust_source="src/data/motors/SULRE_Comet1v11.eng",
    dry_mass=9.43, #kg (tanks plus engine mass)
    dry_inertia=(2.87, 0.02, 2.87), # kg*m^2, I_11, I_22, I_33
    nozzle_radius=49.28e-3, #m
    center_of_dry_mass_position=0.798, #m
    nozzle_position=0, #m
    burn_time=8,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

motor_length = 1.838 # m, distance from top of nitrogen tank to the end of the nozzle
engine_length = 0.311 # m, length of the engine
nitrogen_length = 0.296 # m, length of nitrogen tank
fuel_length = 0.158 # m, length of fuel tank
oxidizer_length = 0.582 # m, length of oxidizer tank
remaining_length = motor_length - (engine_length + nitrogen_length + fuel_length + oxidizer_length)
average_spacing = remaining_length / 3

engine.add_tank(tank=oxidizer_tank, position=engine_length + average_spacing + 0.5*oxidizer_length)
engine.add_tank(tank=fuel_tank, position=engine_length + 2*average_spacing + oxidizer_length + 0.5*fuel_length)
engine.add_tank(tank=nitrogen_tank, position=engine_length + 3*average_spacing + oxidizer_length + fuel_length + 0.5*nitrogen_length)

#engine.draw()
#engine.all_info()

## Add motor to rocket
comet.add_motor(engine, position=rocket_length)

# Add aerodynamic surfaces
nose_cone = comet.add_nose(
    length=nose_length, #m
    kind="von karman", #kind of nose cone
    position=0.0 #m
)

"""fin_set = comet.add_trapezoidal_fins(
    n=3, #number of fins
    root_chord=0.35, #m
    tip_chord=0.1, #m
    span=0.15, #m (distance from root to tip, presumably)
    position=2.55, #m (distance from nose to fin set)
    airfoil=("src/data/calisto/NACA0012-radians.csv","radians"), #path to airfoil file, same as calisto (for now)
    sweep_length=0.305 #m
)"""

fin_set = comet.add_trapezoidal_fins(
    n=4,
    root_chord=0.26, # Actually 0.252
    tip_chord=0.1, # Actually 0.05
    span=0.12,
    position=2.8, # Actually 2.641
    #airfoil=("src/data/calisto/NACA0012-radians.csv","radians"),
    sweep_length=0.17
)
    

tail = comet.add_tail(
    top_radius=rocket_radius, #m
    bottom_radius=0.099 / 2, #m
    length=0.201, #m
    position=rocket_length - 0.201 #m (distance from nose to tail minus its length)
)

# Add parachutes
main = comet.add_parachute(
    name="main",
    cd_s=10.27, # drag coefficient * reference area (96 inches diameter?)
    trigger=450, # ejection altitude in meters
    sampling_rate=105, # Hz
    lag=1.5, # time in seconds for chute to deploy after trigger
    noise=(0, 8.3, 0.5),
)


drogue = comet.add_parachute(
    name="drogue",
    cd_s=0.452, # drag coefficient * reference area (24 inches diameter?)
    trigger="apogee", # ejection at apogee
    sampling_rate=105, # Hz
    lag=2, # time in seconds for chute to deploy after trigger
    noise=(0, 8.3, 0.5),
)


# Draw rocket
#comet.draw()
comet.all_info()