# -*- coding: utf-8 -*-
"""
Created by Sophie Wagner (sophie.wagn@gmail.com) on 8/8/2023
Utilizing code from Francesca Lim

Set parameter for the analysis of Connect4Health program implementation
"""

import pandas as pd
import numpy as np
import common_functions as use

###############################################################################
### MODEL SETTINGS ###

MODE = "basecase"  # type of model run ("base", "owsa", "psa", "calibrate")
N_POP = 500  # Population size, base case is 2494 (size of BMC)
N_SIMS = 1000  # Number of simulations (set to 1 for OWSA), base case is 1000
TIME = 24  # months, 24 for base
WTP_THRESHOLDS = range(0, 250001, 10000)
DISCOUNT_RATE = 0.03/12
DISCOUNT_ARRAY = np.array([1 / (1 + DISCOUNT_RATE) ** i for i in range(TIME)])
PRINT = True  # Determines whether to save outputs
SAVE_PATIENTS = False  # Determines whether to save each patient trajector
BMI_LIFE_TABLE = False  # What does this mean?

# Multiprocessing settings
N_PROCESSES = 1  # set to 1 for owsa
BLOCK_SIZE = 100

PATH = 'C:/Users/sophi/OneDrive - cumc.columbia.edu/STIMULATE/CEA'

# Input paths
INPUT_PATHS = {'female_mort': PATH+'/data/life_tables/mortality_female_adolescent.csv',
               'male_mort': PATH+'/data/life_tables/mortality_male_adolescent.csv',
               'model_inputs': PATH+'/data/model_inputs.xlsx',
               'patients': PATH+'/data/patients.csv',
               'program_costs': PATH+'/data/costs/program_costs.xlsx'}

# Output paths
OUTPUT_PATHS = {'results_1yr': PATH+'/output/results_1yr/',  # base case
                'results_2yr': PATH+'/output/results_2yr/',
                'pop_stats': PATH+'/output/pop_stats.csv',
                'weight_loss': PATH+'/output/weight_loss.xlsx',
                'bmi': PATH+'/output/bmi.xlsx',
                'costs': PATH+'/output/costs.xlsx',
                'qalys': PATH+'/output/qalys.xlsx',
                'cea': PATH+'/output/cea.xlsx',
                'cea_summary': PATH+'/output/cea_summary.xlsx',
                'states_summ': PATH+'/output/states_summ.xlsx',
                'accept_curve': PATH+'/output/accept_curve_data.xlsx',
                'BMI_curves': PATH+'/output/BMI.png',
                'cost_qaly_curves': PATH+'/output/cost_qaly.png',
                'cost_breakdown': PATH+'/output/cost_breakdown.xlsx'}


# Strategies: C4H program, no treatment
STRATEGIES = ['NO_INTERVENTION', 'C4H']


###############################################################################

class State:
    ALIVE = 0
    DEAD = 1
    ALL = 2


class Gender:
    MALE = 0
    FEMALE = 1


#state_names = ['HEALTHY_BMI', 'OVERWEIGHT', 'OBESE1', 'OBESE2', 'OBESE3', 'DEAD']
state_names = ['ALIVE', 'DEAD']

#cost_cats = {'Starting':0, 'Continuing':1}

# Load model inputs
MODEL_INPUTS = pd.read_excel(
    INPUT_PATHS['model_inputs'], sheet_name='inputs', index_col=0)

# Load program costs
PROGRAM_COSTS = pd.read_excel(
    INPUT_PATHS['program_costs'], sheet_name='Sheet1', index_col=0)

# Load cohort settings
COHORT_SETTINGS = pd.read_excel(
    INPUT_PATHS['model_inputs'], sheet_name='cohort_settings', index_col=0)

# Cohort settings
START_AGE = COHORT_SETTINGS.loc['start_age', 'Value']
# calculated using starting z's, cdc charts
START_BMI_G = COHORT_SETTINGS.loc['start_bmi_g', 'Value']
START_BMI_B = COHORT_SETTINGS.loc['start_bmi_b', 'Value']
START_BMI = COHORT_SETTINGS.loc['start_bmi_pop', 'Value']  # avg val
PERC_FEMALE = COHORT_SETTINGS.loc['perc_female', 'Value']
START_BMI_Z = COHORT_SETTINGS.loc['start_bmi_z', 'Value']  # same for whole pop

# Load patients
PATIENTS = pd.read_csv(INPUT_PATHS['patients'], index_col=0)
# Subset based on N_POP
PATIENTS = PATIENTS.iloc[0:N_POP]
PATIENTS.reset_index(drop=True, inplace=True)

if BMI_LIFE_TABLE:
    # Load mortality data
    # Indexed by age and BMI
    # Source: Wang et al, 2013. Derivation of background mortality by
    # smoking and obesity in cancer simulation models.
    acm_y_female = pd.read_csv(
        INPUT_PATHS['female_mort'], header=0, index_col=0)
    acm_y_male = pd.read_csv(INPUT_PATHS['male_mort'], header=0, index_col=0)

    def calculate_monthly_acm(yearly_acm):
        # Converts annual life table to monthly life table
        age_min = 8*12
        age_max = 10*12
        bmi_min = 17
        bmi_max = 50
        # Initialize dataframe
        pDie_monthly = pd.DataFrame(index=range(
            age_min, age_max+1), columns=range(bmi_min, bmi_max+1))

        for bmi in list(yearly_acm.columns.values):
            # Temporary list of monthly probs for each age given BMI
            temp = list()
            for age in list(yearly_acm.index.values):
                prob_month = use.prob_to_prob(yearly_acm.loc[age, bmi], 12)
                temp.append(prob_month)

            # Interpolate temp list to get probs at every month
            # Start, stop, step; age in months
            x0 = range(age_min, age_max+1, 12)
            # Points you want the inperpolated value,
            # known x points, known y values
            monthly_probs = np.interp(range(age_min, age_max+1), x0, temp)

            # Insert monthly probs into the new data DataFrame
            pDie_monthly.loc[:, int(bmi)] = monthly_probs
        return pDie_monthly

    # Calculate monthly probabilities of death
    p_acm_m_female = calculate_monthly_acm(acm_y_female)
    p_acm_m_male = calculate_monthly_acm(acm_y_male)

elif BMI_LIFE_TABLE is False:
    p_acm_m = pd.read_excel(
        PATH+'/data/life_tables/cdc_acmort_male_2017.xlsx', index_col=0)
    p_acm_f = pd.read_excel(
        PATH+'/data/life_tables/cdc_acmort_female_2017.xlsx', index_col=0)

# Array of natural BMI by age in months
MONTHLY_BMI_CHANGE_NH_G = 1.349884/12
MONTHLY_BMI_CHANGE_NH_B = 1.279539/12
MONTHLY_BMI_CHANGE_NH = ((0.47*1.349884) + (0.53*1.279439)) / 12
MONTHLY_BMI_Z_CHANGE_NH = 0
# Contains initial starting month 0 before treatment
notx_bmiArr_g = np.array([START_BMI_G])
notx_bmiArr_b = np.array([START_BMI_B])
notx_bmiArr = np.array([START_BMI])
notx_bmiArr_z = np.array([START_BMI_Z])
for month in range(TIME):  # 12 MONTHS
    prevBMI = notx_bmiArr[-1]
    prevBMI_G = notx_bmiArr_g[-1]
    prevBMI_B = notx_bmiArr_b[-1]
    prevBMI_Z = notx_bmiArr_z[-1]
    notx_bmiArr = np.append(notx_bmiArr, prevBMI + MONTHLY_BMI_CHANGE_NH)
    notx_bmiArr_g = np.append(
        notx_bmiArr_g, prevBMI_G + MONTHLY_BMI_CHANGE_NH_G)
    notx_bmiArr_b = np.append(
        notx_bmiArr_b, prevBMI_B + MONTHLY_BMI_CHANGE_NH_B)
    notx_bmiArr_z = np.append(
        notx_bmiArr_z, prevBMI_Z + MONTHLY_BMI_Z_CHANGE_NH)
# Write out to dataframe
notx_df = pd.DataFrame({
    'BMI': notx_bmiArr,
    'BMI_G': notx_bmiArr_g,
    'BMI_B': notx_bmiArr_b,
    'BMI_Z': notx_bmiArr_z
})

# Save the DataFrame to an Excel file
notx_df.to_excel(PATH+'/output/notx_BMI_1y.xlsx', index=False)
