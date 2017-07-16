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
from os.path import split as pathsplit

PATH_THIS_FILE = pathsplit(abspath(__file__))[0]

# path to the csv file with year and mass of plastic dumped
PATH_PLASTIC_THROUGH_YEAR_DUMPED = PATH_THIS_FILE + '/../data/plastic_production2.csv'


#################### CONSTANT ############################################
PERC_PLASTIC_LDPE = 0.7
PELLET_TO_METHANE = 0.08 * 365
PELLET_TO_METHANE_STD = 0.02
FLAKE_TO_METHANE = 2.22 * 365
FLAKE_TO_METHANE_STD = 1.0
POWDER_TO_METHANE = 54.95 * 365
POWDER_TO_METHANE_STD = 4.06
##########################################################################

#################### VARIABLE ############################################
# percentage of plastic in suspension
PERC_PLASTIC_SUSPENSION = linspace(0.10, 0.50, 2)

# percentage of plastic in suspension disapearing each year
PERC_PLASTIC_REMOVED = linspace(0.10, 0.50, 2)

# percentage of pellet in suspension disapearing each year
PERC_PELLET_REMOVED = linspace(0.10, 0.50, 2)

# percentage of flake in suspension disapearing each year
PERC_FLAKE_REMOVED = linspace(0.10, 0.50, 2)

# percentage of powder in suspension disapearing each year
PERC_POWDER_REMOVED = linspace(0.10, 0.50, 2)

# percentage of raw plastic in suspension transformed into pellet each year
PERC_PLASTIC_TRANSFORMED_TO_PELLET = linspace(0.10, 0.50, 2)

# percentage of raw plastic in suspension transformed into pellet each year
PERC_PLASTIC_TRANSFORMED_TO_FLAKE = linspace(0.10, 0.50, 2)

# percentage of raw plastic in suspension transformed into pellet each year
PERC_PLASTIC_TRANSFORMED_TO_POWDER = linspace(0.10, 0.50, 2)

# percentage of pellet in suspension transformed into pellet each year
PERC_PELLET_TRANSFORMED_TO_FLAKE = linspace(0.10, 0.50, 2)

# percentage of pellet in suspension transformed into pellet each year
PERC_PELLET_TRANSFORMED_TO_POWDER = linspace(0.10, 0.50, 2)

# percentage of pellet in suspension transformed into pellet each year
PERC_FLAKE_TRANSFORMED_TO_POWDER = linspace(0.10, 0.50, 2)
#############################################################################
