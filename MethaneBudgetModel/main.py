from MethaneBudgetModel.plastic_evol import PlasticModel
import seaborn
import numpy as np

from matplotlib import rc
#rc('text', usetex=True)

import pylab as plt
import pandas as pd

from numpy import vstack
from numpy import hstack


def main():
    """ """
    fig, axes = plt.subplots(1, 2, figsize=(20, 12))

    model = PlasticModel()
    model.fit()

    tot_methane = model._final_values
    mmin = min(tot_methane)
    mmax = max(tot_methane)
    mmean = np.mean(tot_methane)
    mstd = np.std(tot_methane)
    mmed = np.median(tot_methane)

    print('min: {0} max:{1} mean:{2} std:{3} med:{4}'.format(mmin, mmax, mmean, mstd, mmed))

    years = model.methane_production_total.keys()

    # make time serie for total methane production evolution
    ax = axes[0]#[0]

    seaborn.set(font_scale=1.25)
    fontsize = 17
    matrix = np.asarray([arr for arr in model.methane_production_total.values()])

    sea = seaborn.tsplot(matrix.T, time=years,
                         legend=True,
                         # ci=[0, 100],
                         err_style=['unit_traces',
                                    #'ci_bars',
                         #           'ci_band'
                         ],
                         ci='sd',
                         color='#0b2d91',
                         err_palette=['#959699'],
                         n_boot=300,
                         estimator=np.mean,
                         ax=ax)
    # ax.set_title('Total methane production through plastic', fontsize=fontsize,
    #              fontname='Times New Roman')
    ax.set_ylabel(r'Tg of CH$_4$ per annum', fontsize=fontsize, fontname='Times New Roman')
    ax.set_xlabel(r'Year', fontsize=fontsize, fontname='Times New Roman')

    # make time serie for annual methane production evolution
    # ax = axes[0][1]

    # matrix = np.asarray(model.methane_production_year.values())
    # sea = seaborn.tsplot(matrix.T, time=years,
    #                      value='Methane production',
    #                      legend=True,
    #                      # ci=[68, 95],
    #                      err_style='unit_traces',
    #                      color='purple',
    #                      n_boot=300,
    #                      ax=ax)
    # ax.set_title('Annual methane production through plastic')

    # make time serie for plastic particles in suspension
    ax = axes[1]#[0]
    matrix_multiple = np.asarray([[arr for arr in model.plastic_in_ocean[key].values()]
                                  for key in model.plastic_in_ocean])

    labels = model.plastic_in_ocean.keys()
    import ipdb;ipdb.set_trace()
    sea = seaborn.tsplot(data=matrix_multiple.T,
                         time=years,
                         # value='plastic mass',
                         err_style='unit_traces',
                         condition=labels,
                         legend=True,
                         # ci=[68, 95],
                         n_boot=300,
                         ax=ax)

    ax.set_ylabel(r'Plastic weight (million of MT)',
                  fontsize=fontsize, fontname='Times New Roman')
    ax.set_xlabel(r'Year', fontsize=fontsize, fontname='Times New Roman')

    # make time serie for plastic particles in suspension
    # ax = axes[0][2]

    # matrix_multiple = np.asarray([model.plastic_in_ocean[key].values()
    #                               for key in model.plastic_in_ocean])


    # matrix = np.asarray([model._params_var['plastic_removed'], model._params_var['plastic_susp']])

    # sea = seaborn.kdeplot(matrix.T, model._final_values,
    #                       ax=ax, shade=True)
    # ax.set_title('Influence of plastic removed and the powder conversion to methane')
    # ax.set_xlabel('Percentage plastic in suspension')
    # ax.set_ylabel('Percentage of plastic removed from the ocean')

    # ax = axes[0][1]

    # labels, scores = zip(*sorted(model.features_score.items(), key=lambda x:x[1]))

    # ax.bar(range(len(scores)), scores)
    # ax.set_xticks(np.array(range(len(scores))) + 0.0)
    # ax.set_xticklabels(labels,
    #                    rotation=60, fontsize=10
    # )

    # ax.set_title('feature score')
    plt.tight_layout()

    fig.show()

    raw_input('ok')




if __name__ == "__main__":
    main()
