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

    years = [year for year in model.methane_production_total.keys()]

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
    ax.set_ylim(bottom=-0.005)
    ax.set_ylabel(r'Tg of CH$_4$ per annum', fontsize=fontsize, fontname='Times New Roman')
    ax.set_xlabel(r'Year', fontsize=fontsize, fontname='Times New Roman')
    ax.tick_params(axis='both', labelsize=16)

    ax = axes[1]#[0]
    matrix_multiple = np.asarray([[arr for arr in model.plastic_in_ocean[key].values()]
                                  for key in model.plastic_in_ocean])

    labels = [label for label in model.plastic_in_ocean.keys()]

    sea = seaborn.tsplot(data=matrix_multiple.T,
                         time=years,
                         # value='plastic mass',
                         err_style='unit_traces',
                         condition=labels,
                         color=['#2f3fd6', '#e09a0f', '#3dd82f', '#de7bfc'],
                         legend=True,
                         # ci=[68, 95],
                         n_boot=300,
                         ax=ax)
    ax.legend(fontsize=20)
    ax.set_ylabel(r'Plastic weight (million of MT)',
                  fontsize=fontsize, fontname='Times New Roman')
    ax.set_xlabel(r'Year', fontsize=fontsize, fontname='Times New Roman')
    ax.set_ylim(bottom=-0.05)
    ax.tick_params(axis='both', labelsize=16)
    plt.tight_layout()
    fig.show()
    input('figure 1')
    fig, axes = plt.subplots(1, 2, figsize=(20, 12))
    # make time serie for annual methane production evolution
    ax = axes[0]

    matrix = np.asarray([arr for arr in model.methane_production_year.values()])

    sea = seaborn.tsplot(matrix.T, time=years,
                         legend=True,
                         # ci=[0, 100],
                         err_style=['unit_traces',
                                    #'ci_bars',
                         #           'ci_band'
                         ],
                         ci='sd',
                         color='#0b2d91',
                         err_palette=['yellow'],
                         n_boot=300,
                         estimator=np.mean,
                         ax=ax)
    # ax.set_title('Total methane production through plastic', fontsize=fontsize,
    #              fontname='Times New Roman')
    ax.set_ylabel(r'Tg of CH$_4$ per annum', fontsize=fontsize, fontname='Times New Roman')
    ax.set_xlabel(r'Year', fontsize=fontsize, fontname='Times New Roman')

    # sea = seaborn.kdeplot(matrix.T, model._final_values,
    #                       ax=ax, shade=True)
    # ax.set_title('Influence of plastic removed and the powder conversion to methane')
    # ax.set_xlabel('Percentage plastic in suspension')
    # ax.set_ylabel('Percentage of plastic removed from the ocean')

    ax = axes[1]

    labels, scores = zip(*sorted(model.features_score.items(), key=lambda x:x[1]))

    ax.bar(range(len(scores)), scores)
    ax.set_xticks(np.array(range(len(scores))) + 0.0)
    ax.set_xticklabels(labels,
                       rotation=90, fontsize=10
    )

    ax.set_title('feature score')
    plt.tight_layout()

    fig.show()

    input('figure 2')




if __name__ == "__main__":
    main()
