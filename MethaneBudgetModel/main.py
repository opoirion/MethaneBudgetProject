from MethaneBudgetModel.plastic_evol import PlasticModel
import seaborn
import numpy as np

import pylab as plt
import pandas as pd

from numpy import vstack
from numpy import hstack


def main():
    """ """
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))

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
                         color='#df67ab',
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
                         color='purple',
                         n_boot=100,
                         ax=ax)
    ax.set_title('Annual methane production through plastic')

    # make time serie for plastic particles in suspension
    ax = axes[1][0]
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


    # make time serie for plastic particles in suspension
    ax = axes[0][2]

    matrix_multiple = np.asarray([model.plastic_in_ocean[key].values()
                                  for key in model.plastic_in_ocean])


    matrix = np.asarray([model._params_var['plastic_removed'], model._params_var['plastic_susp']])

    sea = seaborn.kdeplot(matrix.T, model._final_values,
                          ax=ax, shade=True)
    ax.set_title('Influence of plastic removed and the powder conversion to methane')
    ax.set_xlabel('Percentage plastic in suspension')
    ax.set_ylabel('Percentage of plastic removed from the ocean')

    ax = axes[1][1]

    labels, scores = zip(*sorted(model.features_score.items(), key=lambda x:x[1]))

    ax.bar(range(len(scores)), scores)
    ax.set_xticks(np.array(range(len(scores))) + 0.0)
    ax.set_xticklabels(labels, rotation=60, fontsize=10)

    ax.set_title('feature score')
    plt.tight_layout()

    fig.show()

    raw_input('ok')




if __name__ == "__main__":
    main()
