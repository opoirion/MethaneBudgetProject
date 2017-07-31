from MethaneBudgetModel.config import PATH_THIS_FILE
from MethaneBudgetModel.config import PATH_PLASTIC_THROUGH_YEAR_DUMPED
from MethaneBudgetModel.config import PERC_PLASTIC_REMOVED
from MethaneBudgetModel.config import PERC_PELLET_REMOVED
from MethaneBudgetModel.config import PERC_FLAKE_REMOVED
from MethaneBudgetModel.config import PERC_POWDER_REMOVED
from MethaneBudgetModel.config import PERC_PLASTIC_SUSPENSION
from MethaneBudgetModel.config import PERC_PELLET_TRANSFORMED_TO_FLAKE
from MethaneBudgetModel.config import PERC_FLAKE_TRANSFORMED_TO_POWDER
from MethaneBudgetModel.config import PERC_PLASTIC_TRANSFORMED_TO_PELLET
from MethaneBudgetModel.config import PERC_PLASTIC_TRANSFORMED_TO_FLAKE
from MethaneBudgetModel.config import PERC_PLASTIC_TRANSFORMED_TO_POWDER
from MethaneBudgetModel.config import PERC_PELLET_TRANSFORMED_TO_FLAKE
from MethaneBudgetModel.config import PERC_PELLET_TRANSFORMED_TO_POWDER
from MethaneBudgetModel.config import PLASTIC_SCENARIO

from MethaneBudgetModel.config import PLASTIC_WEIGHT_CONSTANT

from MethaneBudgetModel.config import PLASTIC_TO_METHANE
from MethaneBudgetModel.config import AGED_PELLET_TO_METHANE
from MethaneBudgetModel.config import FLAKE_TO_METHANE
from MethaneBudgetModel.config import POWDER_TO_METHANE
from MethaneBudgetModel.config import CONSTANT
from MethaneBudgetModel.config import METHOD
from MethaneBudgetModel.config import N_IT
from MethaneBudgetModel.config import SEPARATOR

from collections import defaultdict

import numpy as np

from itertools import product

from copy import copy
from copy import deepcopy

from sys import stdout

from random import choice

from scipy.spatial.distance import correlation
from scipy.stats import kendalltau

from functools import reduce


def main():
    """ """
    plastic_model = PlasticModel()
    plastic_model.fit()

class PlasticModel():
    """ """
    def __init__(self):
        """ """
        self.method = METHOD
        self.n_it = N_IT

        self.dumped_plastic_per_year = defaultdict(float)

        self.methane_production_year = defaultdict(list)
        self.methane_production_total = defaultdict(list)
        self._params_var = defaultdict(list)
        self._final_values = []
        self.features_score = {}

        self._methane_total = 0.0
        self._param_changed = None
        self._next_params_gen = None
        self._next_year_gen = None

        self.current_year = None
        self.incoming_plastic = None

        self.plastic_to_methane = PLASTIC_TO_METHANE
        self.aged_pellet_to_methane = AGED_PELLET_TO_METHANE
        self.flake_to_methane = FLAKE_TO_METHANE
        self.powder_to_methane = POWDER_TO_METHANE
        self.constant = CONSTANT
        self.plastic_weight_constant = PLASTIC_WEIGHT_CONSTANT
        self.plastic_scenario = PLASTIC_SCENARIO

        self.plastic = {
            'raw': 0.0,
            'pellet': 0.0,
            'flake':0.0,
            'powder':0.0,
        }

        self.plastic_in_ocean = {key:defaultdict(list) for key in self.plastic}

        self.params = {
            'perc_flake_powder': None,
            'perc_pellet_flake': None,
            'perc_pellet_powder': None,
            'perc_plastic_pellet': None,
            'perc_plastic_flake': None,
            'perc_plastic_powder': None,
            'plastic_removed': None,
            'flake_removed': None,
            'pellet_removed': None,
            'powder_removed': None,
            'plastic_susp': None,
            'plastic_to_methane': None,
            'aged_pellet_to_methane': None,
            'flake_to_methane': None,
            'powder_to_methane': None,
            'plastic_scenario': None,
            }

        self._load_plastic_per_year()

        self.params_list = {
            'perc_flake_powder': PERC_FLAKE_TRANSFORMED_TO_POWDER,
            'perc_pellet_flake': PERC_PELLET_TRANSFORMED_TO_FLAKE,
            'perc_pellet_powder': PERC_PELLET_TRANSFORMED_TO_POWDER,
            'perc_plastic_pellet': PERC_PLASTIC_TRANSFORMED_TO_PELLET,
            'perc_plastic_flake': PERC_PLASTIC_TRANSFORMED_TO_FLAKE,
            'perc_plastic_powder': PERC_PLASTIC_TRANSFORMED_TO_POWDER,
            'plastic_removed': PERC_PLASTIC_REMOVED,
            'flake_removed': PERC_FLAKE_REMOVED,
            'pellet_removed': PERC_PELLET_REMOVED,
            'powder_removed': PERC_POWDER_REMOVED,
            'plastic_susp': PERC_PLASTIC_SUSPENSION,
            'plastic_to_methane': PLASTIC_TO_METHANE,
            'aged_pellet_to_methane': AGED_PELLET_TO_METHANE,
            'flake_to_methane': FLAKE_TO_METHANE,
            'powder_to_methane': POWDER_TO_METHANE,
            'plastic_scenario': np.arange(self.params['plastic_scenario'])
        }

        if self.method == 'EXACT':
            self._nb_experiments = self._compute_nb_experiments()
            self.n_it = self._nb_experiments

        else:
            self._nb_experiments = self.n_it

    def _compute_nb_experiments(self):
        """ """
        return reduce(lambda x, y: x * y, map(len, self.params_list.values()))

    def _load_plastic_per_year(self, sep=SEPARATOR):
        """ """
        with open(PATH_PLASTIC_THROUGH_YEAR_DUMPED) as f_data:
            line = f_data.readline()

            for line in f_data:
                line = line.strip(' \t\n' + sep).split(sep)
                year, mass = int(line[0]), list(map(float, line[1:]))

                if self.plastic_scenario is not None:
                    mass = [mass[self.plastic_scenario]]

                self.dumped_plastic_per_year[year] = mass

            self.params['plastic_scenario'] = len(mass)

    def next_params(self):
        """ """
        if not self._next_params_gen:
            if self.method == 'EXACT':
                self._next_params_gen = self._next_params_exact()
            elif self.method == 'MONTECARLO':
                self._next_params_gen = self._next_params_montecarlo()

        return next(self._next_params_gen)

    def next_year(self, init=False):
        """ """
        if init:

            self._next_year_gen = None

        if not self._next_year_gen:
            self._next_year_gen = iter(sorted(self.dumped_plastic_per_year.keys()))

        return next(self._next_year_gen)

    def _next_params_exact(self):
        """ """
        zipped_lists = []

        for param in self.params_list:
            zipped_lists.append(([(param, value) for value in self.params_list[param]]))

        for combination in product(*zipped_lists):

            # determine the parameter changed
            old_params = copy(self.params)
            param_changed = None
            nb_param_changed = 0
            # attribute the valuexs
            for key, value in combination:
                self.params[key] = value

                if self.params[key] != old_params[key]:
                    param_changed = key
                    nb_param_changed += 1

            if nb_param_changed == 1:
                self._param_changed = param_changed

            yield param_changed

    def _next_params_montecarlo(self):
        """ """
        zipped_lists = []

        for it in range(self.n_it):

            for param in self.params_list:
                value = choice(self.params_list[param])

                self.params[param] = value

            yield True

    def init(self):
        """ """
        self.plastic = {
            'raw': 0.0,
            'pellet': 0.0,
            'flake':0.0,
            'powder':0.0,
        }

        self._methane_total = 0.0
        self.current_year = self.next_year(init=True)
        scenario = self.params['plastic_scenario']
        self.incoming_plastic = self.dumped_plastic_per_year[self.current_year][scenario]

    def increment_one_year(self):
        """ """
        methane_prod = defaultdict(list)
        scenario = self.params['plastic_scenario']

        self.plastic['powder'] = self.plastic['powder'] * (1.0 - self.params['powder_removed']) + \
                                 self.plastic['raw'] * self.params['perc_plastic_powder'] + \
                                 self.plastic['pellet'] * self.params['perc_pellet_powder'] +\
                                 self.plastic['flake'] * self.params['perc_flake_powder']

        self.plastic['flake'] = self.plastic['flake'] * (1.0 - self.params['flake_removed']) + \
                                 self.plastic['raw'] * self.params['perc_plastic_flake'] + \
                                 self.plastic['pellet'] * self.params['perc_pellet_flake'] - \
                                 self.plastic['flake'] * self.params['perc_flake_powder']

        self.plastic['pellet'] = self.plastic['pellet'] * (1.0 - self.params['pellet_removed']) + \
                                 self.plastic['raw'] * self.params['perc_plastic_pellet'] - \
                                 self.plastic['pellet'] * self.params['perc_pellet_flake'] - \
                                 self.plastic['pellet'] * self.params['perc_pellet_powder']

        self.plastic['raw'] = self.plastic['raw'] * (1.0 - self.params['plastic_removed']) -\
                              self.plastic['raw'] * self.params['perc_plastic_pellet'] - \
                              self.plastic['raw'] * self.params['perc_plastic_flake'] - \
                              self.plastic['raw'] * self.params['perc_plastic_powder'] + \
                              self.incoming_plastic * self.params['plastic_susp']

        methane_prod['raw'].append(self.plastic['raw'] * self.params['plastic_to_methane'])
        methane_prod['pellet'].append(self.plastic['pellet'] * self.params['aged_pellet_to_methane'])
        methane_prod['flake'].append(self.plastic['flake'] * self.params['flake_to_methane'])
        methane_prod['powder'].append(self.plastic['powder'] * self.params['powder_to_methane'])

        self._increment_methane_prod(methane_prod)
        self._increment_plastic_in_ocean()

        self.current_year = self.next_year()
        self.incoming_plastic = self.dumped_plastic_per_year[self.current_year][scenario]

    def _increment_plastic_in_ocean(self):
        """ """
        for plastic in self.plastic:
            self.plastic_in_ocean[plastic][self.current_year].append(
                self.plastic[plastic] / self.plastic_weight_constant
            )

    def _increment_methane_prod(self, methane_prod):
        """ """
        methane_prod_values = []

        for methane in product(*methane_prod.values()):
            methane_prod_values.append(reduce(lambda x, y: x + y, methane))

        methane_mean = np.mean(methane_prod_values) * self.constant

        self.methane_production_year[self.current_year].append(methane_mean)
        self._methane_total += methane_mean

        self.methane_production_total[self.current_year].append(self._methane_total)

    def iterate(self):
        """ """
        while True:
            try:
                self.increment_one_year()
            except StopIteration:
                break

    def fit(self):
        """ """
        i = 0

        while True:
            try:
                self.next_params()

            except StopIteration:
                break

            self.init()
            self.iterate()

            for param in self.params:
                self._params_var[param].append(self.params[param])

            self._final_values.append(self._methane_total)

            i += 1

            stdout.write('\r{0} / {1} conf done...'.format(i, self._nb_experiments))
            stdout.flush()

        self._rank_features()

        print('\n')

    def _rank_features(self):
        """ """
        for feature in self._params_var:
            score, pvalue = kendalltau(self._params_var[feature],
                                        self._final_values)
            if np.isnan(pvalue):
                continue

            self.features_score[feature] = score

            print('score: {0}, p-value: {1} for:{2}'.format(score, pvalue, feature))


if __name__ == "__main__":
    main()
