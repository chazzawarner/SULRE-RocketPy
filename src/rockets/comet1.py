from rocketpy import Rocket, Fluid, LiquidMotor, CylindricalTank, MassFlowRateBasedTank
from math import exp

# Define constants
radius = 0.16 / 2 #m
length = 3.07 - 0.05 #m (total length of rocket minus the overlap of the fins)
nose_length = 0.7 #m

# Initialise rocket
comet = Rocket(
    radius=radius, #m
    mass=30.9 - 7.6, #kg (mass without motor and engine mass (7.6kg))
    inertia=(1.5, 1.5, 0.1), #kg*m^2 ???
    power_off_drag="src/data/comet1/comet1v4 drag curve.csv", #path to csv file
    power_on_drag="src/data/comet1/comet1v4 drag curve.csv", #path to same csv file
    center_of_mass_without_motor=2.03, #m
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
nitrogen_tank_shape = CylindricalTank(radius = 0.111/2, height = 0.296)
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
    thrust_source="src/data/motors/SULRE_Comet1v10.eng",
    dry_mass=7.6,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=0.075,
    center_of_dry_mass_position=1.75,
    nozzle_position=0,
    burn_time=8,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)
engine.add_tank(tank=oxidizer_tank, position=1.0)
engine.add_tank(tank=fuel_tank, position=2.5)
engine.add_tank(tank=nitrogen_tank, position=3.5)

## Add motor to rocket
comet.add_motor(engine, position=2.78)

# Add aerodynamic surfaces
nose_cone = comet.add_nose(
    length=nose_length, #m
    kind="von karman", #kind of nose cone
    position=0.0 #m
)

fin_set = comet.add_trapezoidal_fins(
    n=4, #number of fins
    root_chord=0.35, #m
    tip_chord=0.1, #m
    span=0.15, #m (distance from root to tip, presumably)
    position=2.67, #m
    airfoil=("src/data/calisto/NACA0012-radians.csv","radians"), #path to airfoil file, same as calisto (for now)
    sweep_length=0.305 #m
)

tail = comet.add_tail(
    top_radius=radius, #m
    bottom_radius=0.1 / 2, #m
    length=0.15, #m
    position=length - 0.15 #m (distance from nose to tail minus its length)
)

# Draw rocket
comet.draw()