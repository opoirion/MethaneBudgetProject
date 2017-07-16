"""
 __  ________ _____ _   _    _    _   _ _____   __  __  ___  ____  _____ _
|  \/  | ____|_   _| | | |  / \  | \ | | ____| |  \/  |/ _ \|  _ \| ____| |
| |\/| |  _|   | | | |_| | / _ \ |  \| |  _|   | |\/| | | | | | | |  _| | |
| |  | | |___  | | |  _  |/ ___ \| |\  | |___  | |  | | |_| | |_| | |___| |___
|_|  |_|_____| |_| |_| |_/_/   \_\_| \_|_____| |_|  |_|\___/|____/|_____|_____|

INPUT VARIABLE TO DEFINE HERE


"""

from numpy import linspace
from os.path import abspath

PATH_THIS_FILE = abspath(__file__)

# path to the csv file with year and mass of plastic dumped
PATH_PLASTIC_THROUGH_YEAR_DUMPED = PATH_THIS_FILE + '../data/plastic_dumped.csv'

# percentage of plastic in suspension
PERC_PASTIC_SUSPENSION = linspace(0.10, 0.50, 20)

# percentage of pastic in suspension disapearing each year
PERC_PASTIC_REMOVED = linspace(0.10, 0.50, 20)

# percentage of raw pastic in suspension transformed into pellet each year
PERC_PLASTIC_TRANSFORMED_TO_PELLET = linspace(0.10, 0.50, 20)

# percentage of pellet in suspension transformed into pellet each year
PERC_PELLET_TRANSFORMED_TO_FLAKE = linspace(0.10, 0.50, 20)

# percentage of pellet in suspension transformed into pellet each year
PERC_FLAKE_TRANSFORMED_TO_POWDER = linspace(0.10, 0.50, 20)
