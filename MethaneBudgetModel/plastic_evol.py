from MethaneBudgetModel.config import PATH_THIS_FILE
from MethaneBudgetModel.config import PATH_PLASTIC_THROUGH_YEAR_DUMPED
from MethaneBudgetModel.config import PERC_PASTIC_REMOVED
from MethaneBudgetModel.config import PERC_PASTIC_SUSPENSION
from MethaneBudgetModel.config import PERC_PELLET_TRANSFORMED_TO_FLAKE
from MethaneBudgetModel.config import PERC_FLAKE_TRANSFORMED_TO_POWDER
from MethaneBudgetModel.config import PERC_PLASTIC_TRANSFORMED_TO_PELLET

from collections import defaultdict


class PlasticModel():
    """ """
    def __init__(self):
        """ """
        self.dumped_plastic_per_year = defaultdict(float)

        self.methane_production = defaultdict(list)

        self.params = {
            'perc_flake': None,
            'perc_pellet': None,
            'perc_pastic': None,
            'plastic_removed': None,
            'plastic_susp': None,
            }

        self.params_list = {
            'perc_flake': PERC_FLAKE_TRANSFORMED_TO_POWDER,
            'perc_pellet': PERC_PELLET_TRANSFORMED_TO_FLAKE,
            'perc_pastic': PERC_PLASTIC_TRANSFORMED_TO_PELLET,
            'plastic_removed': PERC_PASTIC_REMOVED,
            'plastic_susp': PERC_PASTIC_SUSPENSION,
        }

        self._load_plastic_per_year()


    def _load_plastic_per_year(self, sep=';'):
        """ """
        with open(PATH_PLASTIC_THROUGH_YEAR_DUMPED) as f_data:
            f_data.readline()

            for line in f_data:
                line = line.strip(' \t\n' + sep).split(sep)
                year, mass = int(line[0]), float(line[-1])
                self.dumped_plastic_per_year[year] = mass

    def init_params(self):
        """ """
