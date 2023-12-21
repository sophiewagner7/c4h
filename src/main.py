import pandas as pd
import numpy as np
import configs as c
import strategies
import microsim
from timeit import default_timer as timer
from datetime import timedelta
from datetime import datetime
# import sa
# import sema_cost
# import u_bmi_owsa as bmi

np.random.seed(965)

if c.TIME == 12:
    path = c.OUTPUT_PATHS['results_1yr']
elif c.TIME == 24:
    path = c.OUTPUT_PATHS['results_2yr']


def run_model():
    if c.TIME == 12:
        path = c.OUTPUT_PATHS['results_1yr']
    elif c.TIME == 24:
        path = c.OUTPUT_PATHS['results_2yr']
    else:
        path = 'C:/Users/sophi/OneDrive - cumc.columbia.edu/STIMULATE/CEA/output/'
    # Initialize data structures to hold average results for all strategies
    bmi_loss_no_tx_dict = {  # average bmi loss per patient
        "NO_INTERVENTION": np.zeros((3, c.TIME + 1)),
        "C4H": np.zeros((3, c.TIME + 1))}
    bmi_loss_baseline_dict = {  # average bmi loss per patient
        "NO_INTERVENTION": np.zeros((3, c.TIME + 1)),
        "C4H": np.zeros((3, c.TIME + 1))}
    bmi_dict = {  # average bmi per patient, including initial bmi as month = 0
        "NO_INTERVENTION": np.zeros((3, c.TIME + 1)),
        "C4H": np.zeros((3, c.TIME + 1))}
    bmi_z_loss_no_tx_dict = {  # average bmi loss per patient
        "NO_INTERVENTION": np.zeros((3, c.TIME + 1)),
        "C4H": np.zeros((3, c.TIME + 1))}
    bmi_z_loss_baseline_dict = {  # average bmi loss per patient
        "NO_INTERVENTION": np.zeros((3, c.TIME + 1)),
        "C4H": np.zeros((3, c.TIME + 1))}
    bmi_z_dict = {  # average bmi per patient, including init bmi as month = 0
        "NO_INTERVENTION": np.zeros((3, c.TIME + 1)),
        "C4H": np.zeros((3, c.TIME + 1))}
    state_dict = {  # number of patients in each state at each time point
        "NO_INTERVENTION": np.zeros((c.TIME, c.State.ALL)),
        "C4H": np.zeros((c.TIME, c.State.ALL))}
    costs_dict = {  # total cost for all patients
        "NO_INTERVENTION": np.zeros(c.TIME),
        "C4H": np.zeros(c.TIME)}
    qalys_dict = {  # total qalys for all patients
        "NO_INTERVENTION": np.zeros(c.TIME),
        "C4H": np.zeros(c.TIME)}
    if c.SAVE_PATIENTS:
        # patient alive status and bmi each month
        patient_dict = {"NO_INTERVENTION": np.zeros((c.N_POP, c.TIME + 4)),
                        "C4H": np.zeros((c.N_POP, c.TIME + 4))}

        # Run model for each strategy
        # Get parameters for each strategy
    for strat in strategies.ALL_STRATEGIES:
        if strat == "C4H":
            params = strategies.C4H()
            params.get_monthly_bmi_change()
        elif strat == "NO_INTERVENTION":
            params = strategies.NO_INTERVENTION()
            params.get_monthly_bmi_change()
        else:
            print("ERROR: Wrong strategy specified")

            # Run microsimulation
        print(f"RUNNING {strat}")
        m = microsim.Microsim(params)
        m.runMicrosim()
        # Record results
        bmi_loss_no_tx_dict[strat][0] = m.bmi_loss_notx_arr
        bmi_loss_baseline_dict[strat][0] = m.bmi_loss_baseline_arr
        bmi_loss_no_tx_dict[strat][1] = m.bmi_loss_notx_arr_lowerq
        bmi_loss_baseline_dict[strat][1] = m.bmi_loss_baseline_arr_lowerq
        bmi_loss_no_tx_dict[strat][2] = m.bmi_loss_notx_arr_upperq
        bmi_loss_baseline_dict[strat][2] = m.bmi_loss_baseline_arr_upperq
        bmi_dict[strat][0] = m.bmiArr
        bmi_dict[strat][1] = m.bmiArr_lowerq
        bmi_dict[strat][2] = m.bmiArr_upperq
        bmi_z_loss_no_tx_dict[strat][0] = m.bmi_z_loss_notx_arr
        bmi_z_loss_baseline_dict[strat][0] = m.bmi_z_loss_baseline_arr
        bmi_z_loss_no_tx_dict[strat][1] = m.bmi_z_loss_notx_arr_lowerq
        bmi_z_loss_baseline_dict[strat][1] = m.bmi_z_loss_baseline_arr_lowerq
        bmi_z_loss_no_tx_dict[strat][2] = m.bmi_z_loss_notx_arr_upperq
        bmi_z_loss_baseline_dict[strat][2] = m.bmi_z_loss_baseline_arr_upperq
        bmi_z_dict[strat][0] = m.bmizArr
        bmi_z_dict[strat][1] = m.bmizArr_lowerq
        bmi_z_dict[strat][2] = m.bmizArr_upperq
        state_dict[strat] = m.stateArr
        costs_dict[strat] = m.costArr
        qalys_dict[strat] = m.QOLArr / 12  # quality-adjusted life *years*
        if c.SAVE_PATIENTS:
            patient_dict[strat] = m.patientArr

    if c.PRINT:
        # Output results
        # Print state arrays as .npy files
        np.save(path + 'states_no_intervention.npy',
                state_dict['NO_INTERVENTION'])
        np.save(path + 'states_c4h.npy', state_dict['C4H'])

        # Create excel spreadsheets

        # BMI pts
        with pd.ExcelWriter(path + 'bmi_perc_loss_notx.xlsx') as writer:
            # Average BMI Loss
            pd.DataFrame(bmi_loss_no_tx_dict['NO_INTERVENTION']).to_excel(
                writer, sheet_name="No Intervention")
            pd.DataFrame(bmi_loss_no_tx_dict['C4H']).to_excel(
                writer, sheet_name="C4H")
        with pd.ExcelWriter(path + 'bmi_perc_loss_baseline.xlsx') as writer:
            # Average BMI Loss
            pd.DataFrame(bmi_loss_baseline_dict['NO_INTERVENTION']).to_excel(
                writer, sheet_name="No Intervention")
            pd.DataFrame(bmi_loss_baseline_dict['C4H']).to_excel(
                writer, sheet_name="C4H")
        with pd.ExcelWriter(path + 'bmi.xlsx') as writer:
            # Average BMI
            pd.DataFrame(bmi_dict['NO_INTERVENTION']).to_excel(
                writer, sheet_name="No Intervention")
            pd.DataFrame(bmi_dict['C4H']).to_excel(writer, sheet_name="C4H")
        # BMI Z
        with pd.ExcelWriter(path + 'bmi_z_perc_loss_notx.xlsx') as writer:
            # Average BMI Loss
            pd.DataFrame(bmi_z_loss_no_tx_dict['NO_INTERVENTION']).to_excel(
                writer, sheet_name="No Intervention")
            pd.DataFrame(bmi_z_loss_no_tx_dict['C4H']).to_excel(
                writer, sheet_name="C4H")
        with pd.ExcelWriter(path + 'bmi_perc_z_loss_baseline.xlsx') as writer:
            # Average BMI Loss
            pd.DataFrame(bmi_z_loss_baseline_dict['NO_INTERVENTION']).to_excel(
                writer, sheet_name="No Intervention")
            pd.DataFrame(bmi_z_loss_baseline_dict['C4H']).to_excel(
                writer, sheet_name="C4H")
        with pd.ExcelWriter(path + 'bmi_z.xlsx') as writer:
            # Average BMI
            pd.DataFrame(bmi_z_dict['NO_INTERVENTION']).to_excel(
                writer, sheet_name="No Intervention")
            pd.DataFrame(bmi_z_dict['C4H']).to_excel(writer, sheet_name="C4H")
        # Costs
        with pd.ExcelWriter(path + 'costs.xlsx') as writer:
            # Total Costs
            pd.DataFrame(costs_dict['NO_INTERVENTION']).T.to_excel(
                writer, sheet_name="No Intervention")
            pd.DataFrame(costs_dict['C4H']).T.to_excel(
                writer, sheet_name="C4H")
        # QALYs
        with pd.ExcelWriter(path + 'qalys.xlsx') as writer:
            # Total QALYs
            pd.DataFrame(qalys_dict['NO_INTERVENTION']).T.to_excel(
                writer, sheet_name="No Intervention")
            pd.DataFrame(qalys_dict['C4H']).T.to_excel(
                writer, sheet_name="C4H")

        if c.SAVE_PATIENTS:
            with pd.ExcelWriter(path + 'patients.xlsx') as writer:
                bmi_columns = ['bmi' + str(x) for x in range(-1, c.TIME)]
                pd.DataFrame(patient_dict['NO_INTERVENTION'], columns=['alive']
                             + bmi_columns).to_excel(
                                 writer,
                                 sheet_name="No intervention")
                pd.DataFrame(patient_dict['C4H'],
                             columns=['alive'] + bmi_columns).to_excel(
                                 writer,
                                 sheet_name="C4H")

        with pd.ExcelWriter(path + 'states_summ.xlsx') as writer:
            nh = pd.DataFrame(state_dict['NO_INTERVENTION'])
            nh.columns = c.state_names
            nh.to_excel(writer, sheet_name='No Intervention')

            c4h = pd.DataFrame(state_dict['C4H'])
            c4h.columns = c.state_names
            c4h.to_excel(writer, sheet_name='C4H')


if __name__ == '__main__':
    if c.MODE == 'basecase':
        print("RUNNING BASE CASE")
        print(f"TIME HORIZON = {c.TIME}")
        print(f"MICROSIM POPULATION: {c.N_POP}")
        start = timer()
        run_model()
        end = timer()
        print(f'total time: {timedelta(seconds=end-start)}')
"""
	elif c.MODE == 'owsa':
		print("RUNNING OWSA")
		print(f"TIME HORIZON = {c.TIME}")
		start = timer()
		sa.run_owsa()
		end = timer()
		print(f'total time: {timedelta(seconds=end-start)}')
	elif c.MODE == 'psa_params':
		sa.generate_psa_params()
	elif c.MODE == 'psa':
		print("RUNNING PSA")
		print(f"TIME HORIZON = {c.TIME}")
		print(f"{c.NUM_ITERATIONS} ITERATIONS FOR A COHORT OF {c.N_POP}")
		start = timer()
		sa.run_psa()
		end = timer()
		print(f'total time: {timedelta(seconds=end-start)}')
	elif c.MODE == 'owsa_bmi':
		print("RUNNING U_BMI OWSA")
		print(f"TIME HORIZON = {c.TIME}")
		start = timer()
		bmi.run_u_bmi_owsa()
		end = timer()
		print(f'total time: {timedelta(seconds=end-start)}')
"""
