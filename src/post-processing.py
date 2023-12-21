import pandas as pd
import numpy as np
import configs as c
import common_functions as use
from tqdm import tqdm
import strategies

# Helper functions


def calculate_inmb(data):
    # input: dataframe with cost and effectiveness columns; names of cost and effectiveness columns
    # output: dataframe with nmb and inmb column added
    data = data.reindex(['NO_INTERVENTION', 'C4H'])
    data['NMB'] = (data['D_QALY'] * WTP) - data['D_Cost']
    vals = [np.nan,
            (data.loc['C4H', 'NMB'] - data.loc['NO_INTERVENTION', 'NMB'])]
    data['INMB'] = vals
    return data


# Post-processing for base case
if c.MODE == "basecase":
    WTP = 100000
    for time in [12, 24]:
        print("TIME HORIZON:", time)
        if time == 12:
            path = c.OUTPUT_PATHS['results_1yr']
            DISCOUNT_ARRAY = np.array(
                [1 / (1 + c.DISCOUNT_RATE) ** i for i in range(time)])
        elif time == 24:
            path = c.OUTPUT_PATHS['results_2yr']
            DISCOUNT_ARRAY = np.array(
                [1 / (1 + c.DISCOUNT_RATE) ** i for i in range(time)])

            nh_states = pd.read_excel(
                path + 'states_summ.xlsx', sheet_name='No Intervention')
            nh_states = nh_states.iloc[:, 1:]
            nh_states_12mo = nh_states.loc[12, 'ALIVE']
            #nh_states_24mo = lt_states.loc[15, 'ALIVE']

            c4h_states = pd.read_excel(
                path + 'states_summ.xlsx', sheet_name='C4H')
            c4h_states = c4h_states.iloc[:, 1:]
            c4h_states_12mo = c4h_states.loc[12, 'ALIVE']
            #lira_states_16mo = lira_states.loc[15, 'ALIVE']

        # Get CEA results
        # Load cost and qaly data
        costs = pd.concat(
            [pd.read_excel(path + 'costs.xlsx', sheet_name='No Intervention'),
             pd.read_excel(path + 'costs.xlsx', sheet_name='C4H')],
            axis=0, keys=['nh', 'c4h']
        )
        qalys = pd.concat(
            [pd.read_excel(path + 'qalys.xlsx', sheet_name='No Intervention'),
             pd.read_excel(path + 'qalys.xlsx', sheet_name='C4H')],
            axis=0, keys=['nh', 'c4h']
        )

        # Remove Unnamed column
        costs = costs.iloc[:, 1:]
        qalys = qalys.iloc[:, 1:]

        # Discount costs and qalys
        d_costs = costs * DISCOUNT_ARRAY
        d_qalys = qalys * DISCOUNT_ARRAY

        # Sum costs and qalys across time and divide by total population (to get average per person)
        sum_costs = costs.sum(axis=1) / c.N_POP
        sum_qalys = qalys.sum(axis=1) / c.N_POP
        sum_d_costs = d_costs.sum(axis=1) / c.N_POP
        sum_d_qalys = d_qalys.sum(axis=1) / c.N_POP

        # Combine cost and qaly data across all runs
        costs_qalys = pd.concat(
            [sum_costs, sum_d_costs, sum_qalys, sum_d_qalys], axis=1)
        costs_qalys = costs_qalys.reset_index()
        costs_qalys.columns = ['Strat', 'Run',
                               'Costs', 'Dis Costs', 'QALYs', 'Dis QALYs']
        # Remove second column
        costs_qalys = costs_qalys.drop(['Run'], axis=1)

        # Calculate incremental costs, incremental qalys, and ICER
        frontier_df = pd.DataFrame()
        cea_df = pd.DataFrame()
        # Calculate incremental costs and qalys in reference to no treatment
        temp = costs_qalys.copy()
        temp.index = temp['Strat'].values
        temp['Incr Costs'] = [
            np.nan,  # nh is reference
            (temp.loc['c4h', 'Dis Costs'] - temp.loc['nh', 'Dis Costs'])
        ]
        temp['Incr QALYs'] = [
            np.nan,  # nh is reference
            (temp.loc['c4h', 'Dis QALYs'] - temp.loc['nh', 'Dis QALYs'])
        ]
        # Calculate ICERs
        all, frontier = use.efficiency_frontier(
            temp, ['Dis Costs', 'Dis QALYs'])
        # Append to CEA data frame
        cea_df = cea_df.append(all)
        frontier_df = frontier_df.append(frontier)

        # Output CEA results
        cea_df.to_excel(path + 'all_cea.xlsx')
        frontier_df.to_excel(path + 'frontier_cea.xlsx')
