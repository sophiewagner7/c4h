# Separate 5-year (60 month) results into 13 months and 2-year results
# Ensures that we are following the same patients for the basecase and extended time horizon

import pandas as pd
import numpy as np
import configs as c

# Files to edit:
#   - bmi_perc_loss.xlsx
#   - bmi.xlsx
#   - costs.xlsx
#   - qalys.xlsx
#   - states_summ.xlsx

if c.MODE == 'basecase':
    for TIME in [12, 24]:  # months
        if TIME == 12:
            PATH = c.OUTPUT_PATHS['results_1yr']
        elif TIME == 24:
            PATH = c.OUTPUT_PATHS['results_2yr']
        else:
            print("ERROR: Wrong time horizon specified")
        STRATEGIES = ['No Intervention', 'C4H']
        DISCOUNT_ARRAY = np.array([1 /
                                   (1 + c.DISCOUNT_RATE) ** i
                                   for i in range(TIME)])

        if TIME == 12 or TIME == 24:
            # Average cost and qalys per patient, includes discounted
            cea_results = pd.DataFrame(0, index=STRATEGIES,
                                       columns=['Cost', 'QALY',
                                                'D_Cost', 'D_Qaly'])

            for strat in STRATEGIES:
                # Costs
                costs = pd.read_excel(PATH + 'costs.xlsx',
                                      sheet_name=strat)
                # Drop first column
                costs = costs.iloc[:, 1:]
                # Subset to specified number of months
                costs = costs.iloc[:, 0:TIME]

                # QALYs
                qalys = pd.read_excel(PATH + 'qalys.xlsx',
                                      sheet_name=strat)
                # Drop first column
                qalys = qalys.iloc[:, 1:]
                # Subset to specified number of months
                qalys = qalys.iloc[:, 0:TIME]

                # Convert dataframes to numpy arrays for costs and
                # qalys to discount them
                costsArr = costs.to_numpy()
                qalysArr = qalys.to_numpy()

                # Aggregate costs and qalys
                totalCosts = costs.sum(axis=1).values[0]
                totalQALYs = qalys.sum(axis=1).values[0]
                # Add to cea_results dataframe
                cea_results.loc[strat, :] = [
                    totalCosts / c.N_POP, totalQALYs / c.N_POP,
                    np.sum(costsArr * DISCOUNT_ARRAY) / c.N_POP,
                    np.sum(qalysArr * DISCOUNT_ARRAY) / c.N_POP]

            # Average costs and QALYs per patient
            cea_results.to_csv(PATH + 'results.csv')

        else:
            # Initialize dictionaries for each output
            bmi_loss_dict = {  # average bmi loss per patient
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_loss_lowerq_dict = {
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_loss_upperq_dict = {
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_loss_nh_dict = {  # average bmi loss per patient
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_loss_nh_lowerq_dict = {
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_loss_nh_upperq_dict = {
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_dict = {  # average bmi per patient,
                # including init bmi as month = 0
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_lowerq_dict = {
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_upperq_dict = {
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_z_loss_dict = {  # average bmi z-score loss per patient
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_z_loss_lowerq_dict = {
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_z_loss_upperq_dict = {
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_z_loss_nh_dict = {  # average bmi z-score loss per patient
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_z_loss_nh_lowerq_dict = {
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_z_loss_nh_upperq_dict = {
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_z_dict = {  # average bmi per patient,
                # including initial bmi as month = 0
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_z_lowerq_dict = {
                "NO_INTERVENTION": None,
                "C4H": None}
            bmi_z_upperq_dict = {
                "NO_INTERVENTION": None,
                "C4H": None}
            state_dict = {  # num patients in each state at each time point
                "NO_INTERVENTION": None,
                "C4H": None}
            costs_dict = {  # total cost for all patients
                "NO_INTERVENTION": None,
                "C4H": None}
            qalys_dict = {  # total qalys for all patients
                "NO_INTERVENTION": None,
                "C4H": None}

            # Average cost and qalys per patient, includes discounted
            cea_results = pd.DataFrame(0, index=STRATEGIES,
                                       columns=['Cost', 'QALY',
                                                'D_Cost', 'D_Qaly'])

            # Read files from 1-year results for each strategy
            for strat in STRATEGIES:
                # BMI percent loss
                bmi_perc_loss = pd.read_excel(PATH +
                                              'bmi_perc_loss_baseline.xlsx',
                                              sheet_name=strat)
                # Drop first column
                bmi_perc_loss = bmi_perc_loss.iloc[:, 1:]
                # Subset to specified number of months
                bmi_perc_loss = bmi_perc_loss.iloc[:, 0:TIME + 1]
                # Add to dictionary
                bmi_loss_dict[strat] = bmi_perc_loss.iloc[[0]]  # average
                bmi_loss_lowerq_dict[strat] = bmi_perc_loss.iloc[[1]]  # lowerq
                bmi_loss_upperq_dict[strat] = bmi_perc_loss.iloc[[2]]  # upperq

                # BMI percent loss from natural history
                bmi_nh_perc_loss = pd.read_excel(PATH +
                                                 'bmi_perc_loss_notx.xlsx',
                                                 sheet_name=strat)
                # Drop first column
                bmi_nh_perc_loss = bmi_nh_perc_loss.iloc[:, 1:]
                # Subset to specified number of months
                bmi_nh_perc_loss = bmi_nh_perc_loss.iloc[:, 0:TIME + 1]
                # Add to dictionary
                bmi_loss_nh_dict[strat] = bmi_nh_perc_loss.iloc[[0]]  # avg
                bmi_loss_nh_lowerq_dict[strat] = bmi_nh_perc_loss.iloc[[1]]
                bmi_loss_nh_upperq_dict[strat] = bmi_nh_perc_loss.iloc[[2]]

                # BMI
                bmi = pd.read_excel(PATH + 'bmi.xlsx',
                                    sheet_name=strat)
                # Drop first column
                bmi = bmi.iloc[:, 1:]
                # Subset to specified number of months
                bmi = bmi.iloc[:, 0:TIME + 1]
                # Add to dictionary
                bmi_dict[strat] = bmi.iloc[[0]]  # average
                bmi_lowerq_dict[strat] = bmi.iloc[[1]]  # lowerq
                bmi_upperq_dict[strat] = bmi.iloc[[2]]  # upperq

                # BMI Z
                # percent loss
                bmi_z_perc_loss = pd.read_excel(PATH + 'bmi_z_perc_loss_baseline.xlsx',
                                                sheet_name=strat)
                # Drop first column
                bmi_z_perc_loss = bmi_z_perc_loss.iloc[:, 1:]
                # Subset to specified number of months
                bmi_z_perc_loss = bmi_z_perc_loss.iloc[:, 0:TIME + 1]
                # Add to dictionary
                bmi_z_loss_dict[strat] = bmi_z_perc_loss.iloc[[0]]  # average
                # lowerq
                bmi_z_loss_lowerq_dict[strat] = bmi_z_perc_loss.iloc[[1]]
                # upperq
                bmi_z_loss_upperq_dict[strat] = bmi_z_perc_loss.iloc[[2]]

                # BMI percent loss from natural history
                bmi_z_nh_perc_loss = pd.read_excel(PATH + 'bmi_z_perc_loss_notx.xlsx',
                                                   sheet_name=strat)
                # Drop first column
                bmi_z_nh_perc_loss = bmi_z_nh_perc_loss.iloc[:, 1:]
                # Subset to specified number of months
                bmi_z_nh_perc_loss = bmi_z_nh_perc_loss.iloc[:, 0:TIME + 1]
                # Add to dictionary
                # average
                bmi_z_loss_nh_dict[strat] = bmi_z_nh_perc_loss.iloc[[0]]
                # lowerq
                bmi_z_loss_nh_lowerq_dict[strat] = bmi_z_nh_perc_loss.iloc[[1]]
                # upperq
                bmi_z_loss_nh_upperq_dict[strat] = bmi_z_nh_perc_loss.iloc[[2]]

                # BMI
                bmi_z = pd.read_excel(PATH + 'bmi_z.xlsx',
                                      sheet_name=strat)
                # Drop first column
                bmi_z = bmi_z.iloc[:, 1:]
                # Subset to specified number of months
                bmi_z = bmi_z.iloc[:, 0:TIME + 1]
                # Add to dictionary
                bmi_z_dict[strat] = bmi_z.iloc[[0]]  # average
                bmi_z_lowerq_dict[strat] = bmi_z.iloc[[1]]  # lowerq
                bmi_z_upperq_dict[strat] = bmi_z.iloc[[2]]  # upperq

                # Costs
                costs = pd.read_excel(PATH + 'costs.xlsx',
                                      sheet_name=strat)
                # Drop first column
                costs = costs.iloc[:, 1:]
                # Subset to specified number of months
                costs = costs.iloc[:, 0:TIME]
                # Add to dictinoary
                costs_dict[strat] = costs

                # QALYs
                qalys = pd.read_excel(PATH + 'qalys.xlsx',
                                      sheet_name=strat)
                # Drop first column
                qalys = qalys.iloc[:, 1:]
                # Subset to specified number of months
                qalys = qalys.iloc[:, 0:TIME]
                # Add to dictinoary
                qalys_dict[strat] = qalys

                # States
                states = pd.read_excel(PATH + 'states_summ.xlsx',
                                       sheet_name=strat)
                # Drop first column
                states = states.iloc[:, 1:]
                # Subset to specified number of months
                states = states.iloc[0:TIME, :]
                # Add to dictionary
                state_dict[strat] = states

                # Convert dataframes to numpy arrays for costs and qalys to
                # discount them
                costsArr = costs.to_numpy()
                qalysArr = qalys.to_numpy()

                # Aggregate costs and qalys
                totalCosts = costs.sum(axis=1).values[0]
                totalQALYs = qalys.sum(axis=1).values[0]
                # Add to cea_results dataframe
                cea_results.loc[strat, :] = [totalCosts / c.N_POP, totalQALYs / c.N_POP,
                                             np.sum(
                                                 costsArr * DISCOUNT_ARRAY) / c.N_POP,
                                             np.sum(qalysArr * DISCOUNT_ARRAY) / c.N_POP]

            # Write to output
            with pd.ExcelWriter(PATH + 'states_summ.xlsx') as writer:
                state_dict['NO_INTERVENTION'].to_excel(
                    writer, sheet_name='NO_INTERVENTION')
                state_dict['C4H'].to_excel(writer, sheet_name='C4H')

            with pd.ExcelWriter(PATH + 'costs.xlsx') as writer:
                costs_dict['NO_INTERVENTION'].to_excel(
                    writer, sheet_name='NO_INTERVENTION')
                costs_dict['C4H'].to_excel(writer, sheet_name='C4H')

            with pd.ExcelWriter(PATH + 'qalys.xlsx') as writer:
                qalys_dict['NO_INTERVENTION'].to_excel(
                    writer, sheet_name='NO_INTERVENTION')
                qalys_dict['C4H'].to_excel(writer, sheet_name='C4H')

            bmi_perc_loss_nh = pd.concat([bmi_loss_dict['NO_INTERVENTION'],
                                          bmi_loss_lowerq_dict['NO_INTERVENTION'],
                                          bmi_loss_upperq_dict['NO_INTERVENTION']], ignore_index=True)
            bmi_perc_loss_C4H = pd.concat([bmi_loss_dict['C4H'],
                                           bmi_loss_lowerq_dict['C4H'],
                                           bmi_loss_upperq_dict['C4H']], ignore_index=True)

            bmi_nh_perc_loss_nh = pd.concat([bmi_loss_nh_dict['NO_INTERVENTION'],
                                             bmi_loss_nh_lowerq_dict['NO_INTERVENTION'],
                                             bmi_loss_nh_upperq_dict['NO_INTERVENTION']], ignore_index=True)
            bmi_nh_perc_loss_C4H = pd.concat([bmi_loss_nh_dict['C4H'],
                                              bmi_loss_nh_lowerq_dict['C4H'],
                                              bmi_loss_nh_upperq_dict['C4H']], ignore_index=True)

            bmi_z_perc_loss_nh = pd.concat([bmi_z_loss_dict['NO_INTERVENTION'],
                                            bmi_z_loss_lowerq_dict['NO_INTERVENTION'],
                                            bmi_z_loss_upperq_dict['NO_INTERVENTION']], ignore_index=True)
            bmi_z_perc_loss_C4H = pd.concat([bmi_z_loss_dict['C4H'],
                                             bmi_z_loss_lowerq_dict['C4H'],
                                             bmi_z_loss_upperq_dict['C4H']], ignore_index=True)

            bmi_z_nh_perc_loss_nh = pd.concat([bmi_z_loss_nh_dict['NO_INTERVENTION'],
                                               bmi_z_loss_nh_lowerq_dict['NO_INTERVENTION'],
                                               bmi_z_loss_nh_upperq_dict['NO_INTERVENTION']], ignore_index=True)
            bmi_z_nh_perc_loss_C4H = pd.concat([bmi_z_loss_nh_dict['C4H'],
                                                bmi_z_loss_nh_lowerq_dict['C4H'],
                                                bmi_z_loss_nh_upperq_dict['C4H']], ignore_index=True)

            with pd.ExcelWriter(PATH + 'bmi_perc_loss_baseline.xlsx') as writer:
                bmi_perc_loss_nh.to_excel(writer, sheet_name='NO_INTERVENTION')
                bmi_perc_loss_C4H.to_excel(writer, sheet_name='C4H')

            with pd.ExcelWriter(PATH + 'bmi_perc_loss_notx.xlsx') as writer:
                bmi_nh_perc_loss_nh.to_excel(
                    writer, sheet_name='NO_INTERVENTION')
                bmi_nh_perc_loss_C4H.to_excel(writer, sheet_name='C4H')

            with pd.ExcelWriter(PATH + 'bmi_z_perc_loss_baseline.xlsx') as writer:
                bmi_z_perc_loss_nh.to_excel(
                    writer, sheet_name='NO_INTERVENTION')
                bmi_z_perc_loss_C4H.to_excel(writer, sheet_name='C4H')

            with pd.ExcelWriter(PATH + 'bmi_z_perc_loss_notx.xlsx') as writer:
                bmi_z_nh_perc_loss_nh.to_excel(
                    writer, sheet_name='NO_INTERVENTION')
                bmi_z_nh_perc_loss_C4H.to_excel(writer, sheet_name='C4H')

            bmi_nh = pd.concat([bmi_dict['NO_INTERVENTION'],
                                bmi_lowerq_dict['NO_INTERVENTION'],
                                bmi_upperq_dict['NO_INTERVENTION']],
                               ignore_index=True)
            bmi_C4H = pd.concat([bmi_dict['C4H'],
                                 bmi_lowerq_dict['C4H'],
                                 bmi_upperq_dict['C4H']], ignore_index=True)

            bmi_z_nh = pd.concat([bmi_z_dict['NO_INTERVENTION'],
                                  bmi_z_lowerq_dict['NO_INTERVENTION'],
                                  bmi_z_upperq_dict['NO_INTERVENTION']],
                                 ignore_index=True)
            bmi_z_C4H = pd.concat([bmi_dict['C4H'],
                                   bmi_z_lowerq_dict['C4H'],
                                   bmi_z_upperq_dict['C4H']],
                                  ignore_index=True)

            with pd.ExcelWriter(PATH + 'bmi.xlsx') as writer:
                bmi_nh.to_excel(writer, sheet_name='NO_INTERVENTION')
                bmi_C4H.to_excel(writer, sheet_name='C4H')

            with pd.ExcelWriter(PATH + 'bmi_z.xlsx') as writer:
                bmi_z_nh.to_excel(writer, sheet_name='NO_INTERVENTION')
                bmi_z_C4H.to_excel(writer, sheet_name='C4H')

            # Average costs and QALYs per patient
            cea_results.to_csv(PATH + 'results.csv')
