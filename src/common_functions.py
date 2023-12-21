
import configs as c
import pandas as pd
import numpy as np
import sys
sys.path.append(
    'C:/Users/sophi/OneDrive - cumc.columbia.edu/STIMULATE/CEA/src')


def rate_to_prob(rate, time):
    # Converts rate into a probability
    prob = 1 - np.exp(-abs(rate) * time)
    return prob


def prob_to_rate(prob, time):
    # Converts probability to rate
    rate = -(np.log(1 - prob)) / time
    return rate


def annual_prob_to_monthly_prob(yearly_prob):
    # Converts annual probability to monthly probability
    return 1 - (1 - yearly_prob) ** (1/12)


def prob_to_prob(prob, from_cycle_length):
    return(1 - (1 - prob)**(1/from_cycle_length))


def beta_params(mean, sd):
    if mean == 0 and sd == 0:
        return 0, 0
    else:
        alpha = ((mean**2)*(1-mean)/(sd**2)-mean)
        beta = ((1-mean)*((1-mean)*mean)/(sd**2)-1)
        return alpha, beta


def random_beta(mean, sd):
    if mean == 0 and sd == 0:
        return 0
    else:
        a, b = beta_params(mean, sd)
        return np.random.beta(a, b)


def gamma_params(mean, sd):
    # Output: theta (scale) and kappa (shape)
    if mean > 0:
        theta = sd**2 / mean
        kappa = mean / theta
    else:
        print('Mean must be positive.')
    return kappa, theta


def random_gamma(mean, sd):
    k, t = gamma_params(mean, sd)
    return np.random.gamma(k, t)


def efficiency_frontier(data, cols):
    # Input: data = dataframe with cost and effectiveness columns;
    # cols = names of cost and effectiveness columns
    # Output: dataframe with icers column added

    # Sort from smallest -> largest values
    icers = data.sort_values(by=cols)

    num_rows = len(icers)
    row = 0

    # Eliminate dominated strategies (lower qalys; higher costs)
    while row < num_rows - 1:  # look through each strategy/row
        # If next most expensive strategy has lower QALYs that current
        # strategy, remove this strategy
        if (icers.loc[icers.index[row+1], cols[1]] <
                icers.loc[icers.index[row], cols[1]]):
            if c.MODE == "basecase":
                print(f"{icers.index[row+1]} is strictly dominated")
            icers = icers.drop(icers.index[row+1])
            num_rows = len(icers)  # reset strategy counters
            row = 0
        else:
            row += 1
    # Initiate icers column
    icers.loc[:, 'icer'] = 0

    # Calculate icers and eliminate weakly dominated strategies
    if len(icers) != 1:
        num_rows = len(icers)
        row = 1  # skip reference row
        while row < num_rows:
            # Calculate icers: based on previous strategy/row
            # Differences in costs / Differences in QALYs
            icers.loc[icers.index[row], 'icer'] = (
                (icers.loc[icers.index[row], cols[0]] -
                 icers.loc[icers.index[row - 1], cols[0]]) /
                (icers.loc[icers.index[row], cols[1]] -
                 icers.loc[icers.index[row - 1], cols[1]])
            )
            # If icer is less than previous strategy/row's icer, we drop the
            # previous strategy/row
            if (icers.loc[icers.index[row], 'icer'] <
                    icers.loc[icers.index[row - 1], 'icer']):
                if c.MODE == "basecase":
                    print(f"{icers.index[row - 1]} is extendedly dominated")
                icers = icers.drop(icers.index[row - 1])
                num_rows = len(icers)
                row -= 1
            else:
                row += 1
    # all strategies
    data = data.reset_index(drop=True).merge(icers, how='left')
    return data, icers


def accept_curve(winner_per_threshold):
    '''Used to export Excel spreadsheet of probability of accepting a
        strategy at each WTP threshold'''
    # Initialize data frame
    for_plot = pd.DataFrame()
    for i in range(len(winner_per_threshold)):
        for strat in ['NO_INTERVENTION', 'C4H']:
            for_plot = for_plot.append(pd.DataFrame({
                'WTP': [winner_per_threshold.index[i]],
                'value': [winner_per_threshold.iloc[i,
                          :].tolist().count(strat) /
                          c.NUM_ITERATIONS],
                'Strategy': [strat]}))
    return for_plot
