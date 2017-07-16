from MethaneBudgetModel.plastic_evol import PlasticModel
import seaborn
import numpy as np


def main():
    """ """
    model = PlasticModel()
    model.fit()

    years = model.methane_production_total.keys()
    matrix = model.methane_production_total.values()

    import ipdb;ipdb.set_trace()




if __name__ == "__main__":
    main()
