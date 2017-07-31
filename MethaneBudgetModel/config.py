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
PATH_PLASTIC_THROUGH_YEAR_DUMPED = PATH_THIS_FILE + '/../data/plastic_production_new_v2.csv'
SEPARATOR = ','


#################### ALGORITHM ###########################################
METHOD = 'MONTECARLO' # 'EXACT' or 'MONTECARLO'
N_IT = 300
##########################################################################

#################### CONSTANT ############################################
CONSTANT = 1.0e-09 * 365 * 16 / 1e12
LINSPACE_DOTS = 20
METHANE_MASS = 16
PLASTIC_WEIGHT_CONSTANT = 1e12
##########################################################################

#################### VARIABLE ############################################
# column of the plastic file used
PLASTIC_SCENARIO = 1 # max
##### YEARLY AVERAGE
# original: PLASTIC_TO_METHANE = 0.01 Not based on real values
# true raw plastic production value = 4.101 std 0.23
PLASTIC_TO_METHANE = linspace(4.101 - 0.23, 4.101 + 0.23, LINSPACE_DOTS)
# New pellet: 4.44
# NEW_PELLET_TO_METHANE = linspace(3.0, 6.0, LINSPACE_DOTS)
# original: PELLET_TO_METHANE = 0.08 std 0.02
# Aged pellet: 9.03
AGED_PELLET_TO_METHANE = linspace(0.31 - 0.04, 0.31 + 0.04, LINSPACE_DOTS)
# original: FLAKE_TO_METHANE = 2.22 std 1.0
# new value 123.35 (yearly average)
FLAKE_TO_METHANE = linspace(2.22 - 1.05, 2.22 + 1.05, LINSPACE_DOTS)
# original: POWDER_TO_METHANE = 54.95 std 4.06
# new value 3053.16
POWDER_TO_METHANE = linspace(54.95 - 4.06, 54.95 + 4.06, LINSPACE_DOTS)

# percentage of plastic income entering in suspension (i.e. perc of LDPE)
PERC_PLASTIC_SUSPENSION = linspace(0.80, 0.90, LINSPACE_DOTS)

# percentage of plastic in suspension disapearing each year
PERC_PLASTIC_REMOVED = linspace(0.10, 0.20, LINSPACE_DOTS)

# percentage of pellet in suspension disapearing each year
PERC_PELLET_REMOVED = linspace(0.10, 0.20, LINSPACE_DOTS)

# percentage of flake in suspension disapearing each year
PERC_FLAKE_REMOVED = linspace(0.05, 0.10, LINSPACE_DOTS)

# percentage of powder in suspension disapearing each year
PERC_POWDER_REMOVED = linspace(0.05, 0.10, LINSPACE_DOTS)

# percentage of raw plastic in suspension transformed into pellet each year
PERC_PLASTIC_TRANSFORMED_TO_PELLET = linspace(0.10, 0.40, LINSPACE_DOTS)

# percentage of raw plastic in suspension transformed into pellet each year
PERC_PLASTIC_TRANSFORMED_TO_FLAKE = linspace(0.05, 0.1, LINSPACE_DOTS)

# percentage of raw plastic in suspension transformed into powder each year
PERC_PLASTIC_TRANSFORMED_TO_POWDER = linspace(0.01, 0.05, LINSPACE_DOTS)

# percentage of pellet in suspension transformed into flake each year
PERC_PELLET_TRANSFORMED_TO_FLAKE = linspace(0.10, 0.20, LINSPACE_DOTS)

# percentage of pellet in suspension transformed into powder each year
PERC_PELLET_TRANSFORMED_TO_POWDER = linspace(0.20, 0.30, LINSPACE_DOTS)

# percentage of flake in suspension transformed into powder each year
PERC_FLAKE_TRANSFORMED_TO_POWDER = linspace(0.30, 0.40, LINSPACE_DOTS)
#############################################################################
