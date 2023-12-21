# Calibration code to determine the % BMI from no treatment BMI for each strategy
# Assumes that when a patient discontinues treatment it takes them 31 months to returnt to their "no treatment" BMI
# Target: match ITT values reported in the trials
import pandas as pd
import numpy as np
import configs as c
import common_functions as use
import strategies
import microsim

# options: LIFESTYLE_THERAPY, LIRAGLUTIDE, MID_QSYMIA, TOP_QSYMIA, SEMAGLUTIDE
RUN_STRATEGY = 'LIFESTYLE_THERAPY'

# if RUN_STRATEGY == 'SEMAGLUTIDE':
#     END_MONTH = 16 # end of follow-up for clinical trial
# else:
#     END_MONTH = 13

# Set simulated annealing parameters
sim_anneal_params = {
    'starting_T': 1.0,
    'final_T': 0.1, # 0.01
    'cooling_rate': 0.6, # 0.9
    'iterations': 20} # 100

# Target data: ITT values for each study for 13/16 months and 2 years
if RUN_STRATEGY == 'TOP_QSYMIA':
    ITT_values = np.array([7.11, 7.76])
    ITT_months = np.array([13, 25])
elif RUN_STRATEGY == 'MID_QSYMIA':
    ITT_values = np.array([4.78, 5.7])
    ITT_months = np.array([13, 25])
elif RUN_STRATEGY == 'LIRAGLUTIDE':
    ITT_values = np.array([4.29, 3.15])
    ITT_months = np.array([13, 25])
elif RUN_STRATEGY == 'SEMAGLUTIDE':
    ITT_values = np.array([16.1, 16.42])
    ITT_months = np.array([16, 24])
elif RUN_STRATEGY == 'LIFESTYLE_THERAPY':
    ITT_values = np.array([-0.35])
    ITT_months = np.array([13])

# Goodness-of-fit functions
def gof(obs, exp):
    # chi-squared
    # inputs: numpy arrays of observed and expected values
    chi = ((obs-exp)**2)
    chi_sq = sum(chi)
    return chi_sq.sum()

# Functions for running simulated annealing algorithm
def select_new_params(step, old_param):
    '''Selects new param within range old_param +/- step%
       step: proportion to change param (between 0 and 1), does not depend on temperature
       old_param: old parameter
       Outputs a new parameter'''
    new_param = np.random.uniform(old_param - old_param * step, old_param + old_param * step)
    return new_param

# Function to generate bmi loss parameters
def generate_bmi_loss(old_spline1, old_spline2):
    if RUN_STRATEGY == 'TOP_QSYMIA':
        new_spline1 = select_new_params(0.10, old_spline1)
        new_spline2 = select_new_params(0.10, old_spline2)
        return new_spline1, new_spline2
    elif RUN_STRATEGY == 'MID_QSYMIA':
        new_spline1 = select_new_params(0.10, old_spline1)
        new_spline2 = select_new_params(0.10, old_spline2)
        return new_spline1, new_spline2
    elif RUN_STRATEGY == 'SEMAGLUTIDE':
        new_spline1 = select_new_params(0.10, old_spline1)
        new_spline2 = select_new_params(0.10, old_spline2)
        return new_spline1, new_spline2
    elif RUN_STRATEGY == 'LIRAGLUTIDE':
        new_spline1 = select_new_params(0.10, old_spline1)
        new_spline2 = select_new_params(0.10, old_spline2)
        return new_spline1, new_spline2
    elif RUN_STRATEGY == 'LIFESTYLE_THERAPY':
        new_spline1 = select_new_params(0.05, old_spline1)
        return new_spline1

def acceptance_prob(old_gof, new_gof, T):
    if new_gof < old_gof:
        return 1
    else:
        return np.exp((old_gof - new_gof) / T)

# Simulated annealing algorithm
def anneal():
    print("STRATEGY:", RUN_STRATEGY)

    # Initial BMI loss parameters
    if RUN_STRATEGY == 'LIFESTYLE_THERAPY':
        params = strategies.LIFESTYLE_THERAPY()
        params.get_monthly_bmi_change()
        final_bmi_loss_baseline = np.zeros(1) # time points for ITT BMI loss 
    elif RUN_STRATEGY == 'LIRAGLUTIDE':
        params = strategies.LIRAGLUTIDE()
        params.get_monthly_bmi_change()
        final_bmi_loss_baseline = np.zeros(2) # time points for ITT BMI loss 
    elif RUN_STRATEGY == 'MID_QSYMIA':
        params = strategies.MID_QSYMIA()
        params.get_monthly_bmi_change()
        final_bmi_loss_baseline = np.zeros(2) # time points for ITT BMI loss 
    elif RUN_STRATEGY == 'TOP_QSYMIA':
        params = strategies.TOP_QSYMIA()
        params.get_monthly_bmi_change()
        final_bmi_loss_baseline = np.zeros(2) # time points for ITT BMI loss 
    elif RUN_STRATEGY == 'SEMAGLUTIDE':
        params = strategies.SEMAGLUTIDE()
        params.get_monthly_bmi_change()
        final_bmi_loss_baseline = np.zeros(2) # time points for ITT BMI loss 

    # Run microsimulation
    m = microsim.Microsim(params)
    m.runMicrosim()
    # Get initial solutions
    if RUN_STRATEGY == 'LIFESTYLE_THERAPY':
        final_bmi_loss_baseline[0] = m.bmi_loss_baseline_arr[ITT_months[0]]
    else:
        final_bmi_loss_baseline[0] = m.bmi_loss_baseline_arr[ITT_months[0]]
        final_bmi_loss_baseline[1] = m.bmi_loss_baseline_arr[ITT_months[1]]
    print(final_bmi_loss_baseline)
    
    # Calculate gof
    old_gof = gof(final_bmi_loss_baseline, ITT_values) * 1000
    print("Initial_gof:", old_gof)

    # Starting temperature
    T = sim_anneal_params['starting_T']
    # Start temperature loop
    # Annealing schedule
    while T > sim_anneal_params['final_T']:
        print("Temperture:", T)
        # Sampling at T
        for i in range(sim_anneal_params['iterations']):
            print("Iteration:", i)
            # Find new values for bmi loss for each strategy
            if RUN_STRATEGY == 'LIFESTYLE_THERAPY':
                newspline1 = generate_bmi_loss(params.bmi_perc_loss_spline1, 0)
            else:
                newspline1, newspline2 = generate_bmi_loss(params.bmi_perc_loss_spline1, params.bmi_perc_loss_spline2)
            # Generate new instance of strategy class
            if RUN_STRATEGY == "LIFESTYLE_THERAPY":
                new_params = strategies.LIFESTYLE_THERAPY()
                new_params.bmi_perc_loss_spline1 = newspline1
                new_params.get_monthly_bmi_change()
            elif RUN_STRATEGY == 'LIRAGLUTIDE':
                new_params = strategies.LIRAGLUTIDE()
                new_params.bmi_perc_loss_spline1 = newspline1
                new_params.bmi_perc_loss_spline2 = newspline2
                new_params.get_monthly_bmi_change()
            elif RUN_STRATEGY == 'TOP_QSYMIA':
                new_params = strategies.TOP_QSYMIA()
                new_params.bmi_perc_loss_spline1 = newspline1
                new_params.bmi_perc_loss_spline2 = newspline2
                new_params.get_monthly_bmi_change()
            elif RUN_STRATEGY == 'MID_QSYMIA':
                new_params = strategies.MID_QSYMIA()
                new_params.bmi_perc_loss_spline1 = newspline1
                new_params.bmi_perc_loss_spline2 = newspline2
                new_params.get_monthly_bmi_change()
            elif RUN_STRATEGY == 'SEMAGLUTIDE':
                new_params = strategies.SEMAGLUTIDE()
                new_params.bmi_perc_loss_spline1 = newspline1
                new_params.bmi_perc_loss_spline2 = newspline2
                new_params.get_monthly_bmi_change()
            else:
                print("ERROR")

            # Get new outputs
            if RUN_STRATEGY == 'LIFESTYLE_THERAPY':
                new_bmi_loss_baseline = np.zeros(1)
            else:
                new_bmi_loss_baseline = np.zeros(2)
            m = microsim.Microsim(new_params)
            m.runMicrosim()
            if RUN_STRATEGY == 'LIFESTYLE_THERAPY':
                new_bmi_loss_baseline[0] = m.bmi_loss_baseline_arr[ITT_months[0]]
            else:
                new_bmi_loss_baseline[0] = m.bmi_loss_baseline_arr[ITT_months[0]]
                new_bmi_loss_baseline[1] = m.bmi_loss_baseline_arr[ITT_months[1]]

            # Calculate new gof
            new_gof = gof(new_bmi_loss_baseline, ITT_values) * 1000
            ap = acceptance_prob(old_gof, new_gof, T)

            # Decide if the new solution is accepted
            if np.random.uniform() < ap:
                params = new_params
                old_gof = new_gof
                print("New parameters:", T, i, new_gof)
                print("New BMI loss values:", new_bmi_loss_baseline)
                
        T = T * sim_anneal_params['cooling_rate']
    
    if RUN_STRATEGY == 'LIFESTYLE_THERAPY':
        return params.bmi_perc_loss_spline1
    else:
        return params.bmi_perc_loss_spline1, params.bmi_perc_loss_spline2





