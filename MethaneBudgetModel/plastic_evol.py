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

from MethaneBudgetModel.config import PERC_PLASTIC_LDPE
from MethaneBudgetModel.config import PELLET_TO_METHANE
from MethaneBudgetModel.config import PELLET_TO_METHANE_STD
from MethaneBudgetModel.config import FLAKE_TO_METHANE
from MethaneBudgetModel.config import FLAKE_TO_METHANE_STD
from MethaneBudgetModel.config import POWDER_TO_METHANE
from MethaneBudgetModel.config import POWDER_TO_METHANE_STD

from collections import defaultdict

import numpy as np

from itertools import product

from copy import copy
from copy import deepcopy

from sys import stdout


def main():
    """ """
    plastic_model = PlasticModel()
    plastic_model.fit()

    import ipdb;ipdb.set_trace()

class PlasticModel():
    """ """
    def __init__(self):
        """ """
        self.dumped_plastic_per_year = defaultdict(float)

        self.methane_production_year = defaultdict(list)
        self.methane_production_total = defaultdict(list)

        self._methane_total = np.array([0.0, 0.0, 0.0])
        self._param_changed = None
        self._next_params_gen = None
        self._next_year_gen = None
        self._params_var = defaultdict(list)

        self.current_year = None
        self.incoming_plastic = None
        self.perc_plastic_ldpe = PERC_PLASTIC_LDPE

        self.pellet_to_methane = PELLET_TO_METHANE
        self.pellet_to_methane_std = PELLET_TO_METHANE_STD
        self.flake_to_methane = FLAKE_TO_METHANE
        self.flake_to_methane_std = FLAKE_TO_METHANE_STD
        self.powder_to_methane = POWDER_TO_METHANE
        self.powder_to_methane_std = POWDER_TO_METHANE_STD

        self.plastic = {
            'raw': 0.0,
            'pellet': 0.0,
            'flake':0.0,
            'powder':0.0,
            'total': 0.0
        }

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
            }

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
        }

        self._load_plastic_per_year()
        self._nb_experiments = self._compute_nb_experiments()

    def _compute_nb_experiments(self):
        """ """
        return reduce(lambda x, y: x * y, map(len, self.params_list.values()))

    def _load_plastic_per_year(self, sep=';'):
        """ """
        with open(PATH_PLASTIC_THROUGH_YEAR_DUMPED) as f_data:
            line = f_data.readline()

            for line in f_data:
                line = line.strip(' \t\n' + sep).split(sep)
                year, mass = int(line[0]), float(line[-1])
                self.dumped_plastic_per_year[year] = mass

    def next_params(self):
        """ """
        if not self._next_params_gen:
            self._next_params_gen = self._next_params()

        return self._next_params_gen.next()

    def next_year(self, init=False):
        """ """
        if init:
            self._next_year_gen = None

        if not self._next_year_gen:
            self._next_year_gen = iter(sorted(self.dumped_plastic_per_year.keys()))

        return self._next_year_gen.next()

    def _next_params(self):
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

    def init(self):
        """ """
        self._methane_total = np.array([0.0, 0.0, 0.0])
        self.current_year = self.next_year(init=True)
        self.incoming_plastic = self.dumped_plastic_per_year[self.current_year]

    def increment_one_year(self):
        """ """
        methane_prod = defaultdict(list)

        self.plastic['raw'] = self.plastic['raw'] * (1.0 - self.params['plastic_removed']) + \
                              self.incoming_plastic * self.perc_plastic_ldpe

        self.plastic['pellet'] = self.plastic['pellet'] * (1.0 - self.params['pellet_removed']) + \
                                 self.plastic['raw'] * self.params['perc_plastic_pellet']

        self.plastic['flake'] = self.plastic['flake'] * (1.0 - self.params['flake_removed']) + \
                                 self.plastic['raw'] * self.params['perc_plastic_flake'] + \
                                 self.plastic['pellet'] * self.params['perc_pellet_flake']

        self.plastic['powder'] = self.plastic['powder'] * (1.0 - self.params['powder_removed']) + \
                                 self.plastic['raw'] * self.params['perc_plastic_powder'] + \
                                 self.plastic['pellet'] * self.params['perc_pellet_powder'] +\
                                 self.plastic['flake'] * self.params['perc_flake_powder']

        methane_prod['pellet'].append(self.plastic['pellet'] * self.pellet_to_methane)
        methane_prod['pellet'].append(self.plastic['pellet'] * self.pellet_to_methane -\
                                      self.pellet_to_methane_std)
        methane_prod['pellet'].append(self.plastic['pellet'] * self.pellet_to_methane +\
                                      self.pellet_to_methane_std)

        methane_prod['flake'].append(self.plastic['flake'] * self.flake_to_methane)
        methane_prod['flake'].append(self.plastic['flake'] * self.flake_to_methane -\
                                      self.flake_to_methane_std)
        methane_prod['flake'].append(self.plastic['flake'] * self.flake_to_methane +\
                                      self.flake_to_methane_std)

        methane_prod['powder'].append(self.plastic['powder'] * self.powder_to_methane)
        methane_prod['powder'].append(self.plastic['powder'] * self.powder_to_methane -\
                                      self.powder_to_methane_std)
        methane_prod['powder'].append(self.plastic['powder'] * self.powder_to_methane +\
                                      self.powder_to_methane_std)

        self._increment_methane_prod(methane_prod)

        self.current_year = self.next_year()
        self.incoming_plastic = self.dumped_plastic_per_year[self.current_year]

    def _increment_methane_prod(self, methane_prod):
        """ """
        methane_prod_values = []

        for methane in product(*methane_prod.values()):
            methane_prod_values.append(reduce(lambda x, y: x + y, methane))

        methane_mean = np.mean(methane_prod_values)
        methane_max = np.mean(methane_prod_values)
        methane_min = np.max(methane_prod_values)

        self.methane_production_year[self.current_year].append(methane_mean)
        self.methane_production_year[self.current_year].append(methane_min)
        self.methane_production_year[self.current_year].append(methane_max)

        self._methane_total += np.array([methane_min, methane_mean, methane_max])

        self.methane_production_total[self.current_year] += list(self._methane_total)

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

            if self._param_changed:
                self._params_var[self._param_changed].append(self._methane_total[1])

            i += 1

            stdout.write('\r{0} / {1} conf done...'.format(i, self._nb_experiments))
            stdout.flush()

        print('\n')


if __name__ == "__main__":
    main()
