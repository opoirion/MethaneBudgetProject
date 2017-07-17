from MethaneBudgetModel.plastic_evol import PlasticModel
import seaborn
import numpy as np

import pylab as plt
import pandas as pd

from numpy import vstack
from numpy import hstack


def main():
    """ """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    model = PlasticModel()
    model.fit()

    years = model.methane_production_total.keys()

    # make time serie for total methane production evolution
    ax = axes[0][0]

    matrix = np.asarray(model.methane_production_total.values())
    sea = seaborn.tsplot(matrix.T, time=years,
                         value='Methane production',
                         legend=True,
                         # ci=[68, 95],
                         err_style='unit_traces',
                         n_boot=100,
                         ax=ax)
    ax.set_title('Total methane production through plastic')

    # make time serie for annual methane production evolution
    ax = axes[0][1]

    matrix = np.asarray(model.methane_production_year.values())
    sea = seaborn.tsplot(matrix.T, time=years,
                         value='Methane production',
                         legend=True,
                         # ci=[68, 95],
                         err_style='unit_traces',
                         n_boot=100,
                         ax=ax)
    ax.set_title('Annual methane production through plastic')

    # make time serie for plastic particles in suspension
    ax = axes[1][0]

    frame = pd.DataFrame()
    matrix_multiple = np.asarray([model.plastic_in_ocean[key].values()
                                  for key in model.plastic_in_ocean])

    labels = model.plastic_in_ocean.keys()

    sea = seaborn.tsplot(data=matrix_multiple.T,
                         time=years,
                         value='plastic mass',
                         err_style='unit_traces',
                         condition=labels,
                         legend=True,
                         # ci=[68, 95],
                         n_boot=300,
                         ax=ax)
    ax.set_title('Annual methane production through plastic')

    fig.show()

    raw_input('ok')




if __name__ == "__main__":
    main()
