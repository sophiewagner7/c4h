
# Creates classes for each intervention
# Calculates monthly BMI loss

import pandas as pd
import numpy as np
import configs as c
import common_functions as use

ALL_STRATEGIES = ['NO_INTERVENTION', 'C4H']


def convert_bmiloss_to_bmi(start_fig, perc_bmi_loss):
    return start_fig - (start_fig * (perc_bmi_loss))


def get_monthly_bmi_change(start_bmi, end_bmi, start_month, end_month):
    return (end_bmi - start_bmi) / (end_month - start_month)

################
# BASE CASE
################


class NO_INTERVENTION:
    def __init__(self):
        self.strat = 'NO_INTERVENTION'
        # Costs
        # Assume no institutional costs for no intervention
        self.c_initial = 0
        self.c_monthly = 0
        # Utilities
        self.u_init = c.MODEL_INPUTS.loc['u_init', 'Value']
        # per 0.01 unit decrease in bmi z-score
        self.u_bmi = c.MODEL_INPUTS.loc['u_bmi_z_loss', 'Value']
        # BMI Change
        self.spline1 = 12
        self.spline2 = 24
        # 0.0591 calibrated, base case
        self.bmi_perc_loss_spline1 = c.MODEL_INPUTS.loc[
            'nh_bmichange_pt_perc_1yr_pop', 'Value'
        ]
        # 0.053, over year
        self.bmi_perc_loss_spline2 = c.MODEL_INPUTS.loc[
            'nh_bmichange_pt_perc_2yr_pop', 'Value'
        ]
        # 0 #maintain same z-score
        self.bmi_perc_z_loss_spline1 = c.MODEL_INPUTS.loc[
            'nh_bmichange_z_perc_1yr', 'Value'
        ]
        self.bmi_perc_z_loss_spline2 = c.MODEL_INPUTS.loc[
            'nh_bmichange_z_perc_2yr', 'Value'
        ]
        self.bmi_spline1 = None
        self.bmi_spline2 = None
        self.bmi_z_spline1 = None
        self.bmi_z_spline2 = None
        self.monthly_bmi_change_spline1 = None
        self.monthly_bmi_change_spline2 = None
        self.monthly_bmi_z_change_spline1 = None
        self.monthly_bmi_z_change_spline2 = None

    def get_monthly_bmi_change(self):
        # bmi pts
        self.bmi_spline1 = convert_bmiloss_to_bmi(
            c.START_BMI, self.bmi_perc_loss_spline1)
        self.bmi_spline2 = convert_bmiloss_to_bmi(
            c.START_BMI, self.bmi_perc_loss_spline2)
        self.monthly_bmi_change_spline1 = get_monthly_bmi_change(
            c.START_BMI, self.bmi_spline1, 0, self.spline1)
        self.monthly_bmi_change_spline2 = get_monthly_bmi_change(
            c.START_BMI, self.bmi_spline2, self.spline1+1, self.spline2)
        # bmi z
        self.bmi_z_spline1 = convert_bmiloss_to_bmi(
            c.START_BMI_Z, self.bmi_perc_z_loss_spline1)
        self.bmi_z_spline2 = convert_bmiloss_to_bmi(
            c.START_BMI_Z, self.bmi_perc_z_loss_spline2)
        self.monthly_bmi_z_change_spline1 = get_monthly_bmi_change(
            c.START_BMI_Z, self.bmi_z_spline1, 0, self.spline1)
        self.monthly_bmi_z_change_spline2 = get_monthly_bmi_change(
            c.START_BMI_Z, self.bmi_z_spline2, self.spline1+1, self.spline2)


class C4H:
    def __init__(self):
        self.strat = 'C4H'
        # Costs
        # per person costs
        self.c_initial = c.MODEL_INPUTS.loc['c_init', 'Value']/c.N_POP
        # per person costs
        self.c_monthly = c.MODEL_INPUTS.loc['c_cont', 'Value']/c.N_POP
        # Utilities
        self.u_init = c.MODEL_INPUTS.loc['u_init', 'Value']
        self.u_bmi = c.MODEL_INPUTS.loc['u_bmi_z_loss', 'Value']
        # BMI Change
        self.spline1 = 12  # 1yr
        self.spline2 = 24  # 2yr
        # calibrated
        self.bmi_perc_loss_spline1 = c.MODEL_INPUTS.loc[
            'epc_bmichange_pt_perc_1yr_pop', 'Value']
        self.bmi_perc_loss_spline2 = c.MODEL_INPUTS.loc[
            'epc_bmichange_pt_perc_2yr_pop', 'Value']
        self.bmi_perc_z_loss_spline1 = c.MODEL_INPUTS.loc[
            'epc_bmichange_z_perc_1yr', 'Value']
        self.bmi_perc_z_loss_spline2 = c.MODEL_INPUTS.loc[
            'epc_bmichange_z_perc_2yr', 'Value']
        self.bmi_spline1 = None
        self.bmi_spline2 = None
        self.bmi_z_spline1 = None
        self.bmi_z_spline2 = None
        self.monthly_bmi_change_spline1 = None
        self.monthly_bmi_change_spline2 = None
        self.monthly_bmi_z_change_spline1 = None
        self.monthly_bmi_z_change_spline2 = None

    def get_monthly_bmi_change(self):
        # bmi pts
        self.bmi_spline1 = convert_bmiloss_to_bmi(
            c.START_BMI, self.bmi_perc_loss_spline1)
        self.bmi_spline2 = convert_bmiloss_to_bmi(
            c.START_BMI, self.bmi_perc_loss_spline2)
        self.monthly_bmi_change_spline1 = get_monthly_bmi_change(
            c.START_BMI, self.bmi_spline1, 0, self.spline1)
        self.monthly_bmi_change_spline2 = get_monthly_bmi_change(
            c.START_BMI, self.bmi_spline2, self.spline1+1, self.spline2)
        # bmi z
        self.bmi_z_spline1 = convert_bmiloss_to_bmi(
            c.START_BMI_Z, self.bmi_perc_z_loss_spline1)
        self.bmi_z_spline2 = convert_bmiloss_to_bmi(
            c.START_BMI_Z, self.bmi_perc_z_loss_spline2)
        self.monthly_bmi_z_change_spline1 = get_monthly_bmi_change(
            c.START_BMI_Z, self.bmi_z_spline1, 0, self.spline1)
        self.monthly_bmi_z_change_spline2 = get_monthly_bmi_change(
            c.START_BMI_Z, self.bmi_z_spline2, self.spline1+1, self.spline2)


################
# OWSA
################
"""
class NO_INTERVENTION_OWSA:
    def __init__(self):
        self.strat = 'NO_INTERVENTION'
        # Costs
        ## Assume none
        self.c_initial=0;
        self.c_monthly=0;
        # Utilities`````````````````````````````````````````````````````````
        self.u_init = c.MODEL_INPUTS.loc['u_init', 'Value']
        self.u_bmi = c.MODEL_INPUTS.loc['u_bmi_z_loss', 'Value']
        # BMI Change
        self.spline1 = 12 
        self.spline2 = 24
        self.bmi_perc_loss_spline1 = c.MODEL_INPUTS.loc['nh_bmichange_pt_perc_1yr_pop', 'Value'] #0.0591 calibrated, base case
        self.bmi_perc_loss_spline2 = c.MODEL_INPUTS.locl['nh_bmichange_pt_perc_2yr_pop', 'Value'] #0.053, over year
        self.bmi_perc_z_loss_spline1 = c.MODEL_INPUTS.loc['nh_bmichange_z_perc_1yr', 'Value'] #0 #maintain same z-score
        self.bmi_perc_z_loss_spline2 = c.MODEL_INPUTS.loc['nh_bmichange_z_perc_2yr', 'Value']
        self.bmi_spline1 = None
        self.bmi_spline2 = None
        self.bmi_z_spline1 = None
        self.bmi_z_spline2 = None
        self.monthly_bmi_change_spline1 = None
        self.monthly_bmi_change_spline2 = None
        self.monthly_bmi_z_change_spline1 = None
        self.monthly_bmi_z_change_spline2 = None

    def get_monthly_bmi_change(self):
        self.bmi_spline1 = convert_bmiloss_to_bmi(c.START_BMI, self.bmi_perc_loss_spline1)
        self.bmi_spline2 = convert_bmiloss_to_bmi(c.START_BMI, self.bmi_perc_loss_spline2)
        self.monthly_bmi_change_spline1 = get_monthly_bmichange(c.START_BMI, self.bmi_spline1,
                                                                0, self.spline1)
        self.monthly_bmi_change_spline2 = get_monthly_bmichange(c.START_BMI, self.bmi_spline2,
                                                                self.spline1+1, self.spline2)
        ## bmi z
        self.bmi_z_spline1 = convert_bmi_z_loss_to_z(c.START_BMI_Z, self.bmi_perc_z_loss_spline1)
        self.bmi_z_spline2 = convert_bmiloss_to_bmi(c.START_BMI_Z, self.bmi_perc_z_loss_spline2)        
        self.monthly_bmi_z_change_spline1 = get_monthly_bmi_change(c.START_BMI_Z, self.bmi_z_spline1, 
                                                                   0, self.spline1)
        self.monthly_bmi_z_change_spline2 = get_monthly_bmi_change(c.START_BMI_Z, self.bmi_z_spline2, 
                                                                   self.spline1+1, self.spline2)

    def set_new_value(self, param, value_on, owsa_dict):
        # Change the value of one parameter
        # Set range of 5 values from the lower bound to the upper bound
        # owsa_dict contains the 5 values tested in the model
        elif param == "u_init":
            init_range = np.linspace(
                c.MODEL_INPUTS.loc['u_init', 'l_bound'], c.MODEL_INPUTS.loc['u_init', 'u_bound'], 5
            )
            self.u_init = init_range[value_on]
            owsa_dict["init_bmi"] = init_range
        elif param == "u_bmi":
            bmi_range = np.linspace(
                c.MODEL_INPUTS.loc['u_bmi_z_loss', 'l_bound'], c.MODEL_INPUTS.loc['u_bmi_loss', 'u_bound'], 5
            )
            self.u_bmi = bmi_range[value_on]
            owsa_dict["u_bmi"] = bmi_range
        elif param == "no_intervention_bmi":
            bmi_perc_loss_spline1_range = np.linspace(
                c.MODEL_INPUTS.loc['nh_bmichange_pt_perc_1yr_pop', 'l_bound'], 
                c.MODEL_INPUTS.loc['nh_bmichange_pt_perc_1yr_pop', 'u_bound'], 5
            )
            bmi_perc_loss_spline2_range = np.linspace(
                c.MODEL_INPUTS.loc['nh_bmichange_pt_perc_2yr_pop', 'l_bound'], 
                c.MODEL_INPUTS.loc['nh_bmichange_pt_perc_2yr_pop', 'u_bound'], 5
                )
            bmi_z_perc_loss_spline1_range = np.linspace(
                c.MODEL_INPUTS.loc['nh_bmichange_z_perc_1yr_pop', 'l_bound'], 
                c.MODEL_INPUTS.loc['nh_bmichange_z_perc_1yr_pop', 'u_bound'], 5
                )
            bmi_z_perc_loss_spline2_range = np.linspace(
                c.MODEL_INPUTS.loc['nh_bmichange_z_perc_2yr_pop', 'l_bound'], 
                c.MODEL_INPUTS.loc['nh_bmichange_z_perc_2yr_pop', 'u_bound'], 5
                )
            self.bmi_perc_loss_spline1 = bmi_perc_loss_spline1_range[value_on]
            self.get_monthly_bmi_change()
            # Add to dictionary
            owsa_dict['nh_bmi_loss_spline1'] = bmi_perc_loss_spline1_range
            owsa_dict['nh_bmi_loss_spline2'] = bmi_perc_loss_spline2_range
            owsa_dict['nh_bmi_z_loss_spline1'] = bmi_z_perc_loss_spline1_range
            owsa_dict['nh_bmi_z_loss_spline2'] = bmi_z_perc_loss_spline2_range

class C4H_OWSA():
    def __init__(self):
        self.strat = 'C4H'
        # Costs
        self.c_initial = c.MODEL_INPUTS.loc['c_init', 'Value']/c.N_POP
        self.c_monthly = c.MODEL_INPUTS.loc['c_cont', 'Value']/c.N_POP
        # Utilities
        self.u_init = c.MODEL_INPUTS.loc['u_init', 'Value']
        self.u_bmi = c.MODEL_INPUTS.loc['u_bmi_z_loss', 'Value']
        # BMI Change
        self.spline1 = 12 # 1yr
        self.spline2 = 24 # 2yr
        self.bmi_perc_loss_spline1 = c.MODEL_INPUTS.loc['epc_bmichange_pt_perc_1yr_pop', 'Value'] # calibrated
        self.bmi_perc_loss_spline2 = c.MODEL_INPUTS.loc['epc_bmichange_pt_perc_2yr_pop', 'Value']
        self.bmi_z_loss_spline1 = c.MODEL_INPUTS.loc['epc_bmichange_z_perc_1yr', 'Value']
        self.bmi_z_loss_spline2 = c.MODEL_INPUTS.loc['epc_bmichange_z_perc_2yr', 'Value']
        self.bmi_spline1 = None
        self.bmi_spline2 = None
        self.bmi_z_spline1 = None
        self.bmi_z_spline2 = None
        self.monthly_bmi_change_spline1 = None
        self.monthly_bmi_change_spline2 = None
        self.monthly_bmi_z_change_spline1 = None
        self.monthly_bmi_z_change_spline2 = None

    def get_monthly_bmi_change(self):
        ## bmi pts
        self.bmi_spline1 = convert_bmiloss_to_bmi(c.START_BMI, self.bmi_perc_loss_spline1)
        self.bmi_spline2 = convert_bmiloss_to_bmi(c.START_BMI, self.bmi_perc_loss_spline2)
        self.monthly_bmi_change_spline1 = get_monthly_bmichange(c.START_BMI, self.bmi_spline1,
                                                                0, self.spline1)
        self.monthly_bmi_change_spline2 = get_monthly_bmichange(c.START_BMI, self.bmi_spline2,
                                                                self.spline1+1, self.spline2)
        ## bmi z
        self.bmi_z_spline1 = convert_bmi_z_loss_to_z(c.START_BMI_Z, self.bmi_perc_z_loss_spline1)
        self.bmi_z_spline2 = convert_bmiloss_to_bmi(c.START_BMI_Z, self.bmi_perc_z_loss_spline2)        
        self.monthly_bmi_z_change_spline1 = get_monthly_bmi_change(c.START_BMI_Z, self.bmi_z_spline1, 
                                                                   0, self.spline1)
        self.monthly_bmi_z_change_spline2 = get_monthly_bmi_change(c.START_BMI_Z, self.bmi_z_spline2, 
                                                                   self.spline1+1, self.spline2)

    def set_new_value(self, param, value_on, owsa_dict):
        # Change the value of one parameter
        # Set range of 5 values from the lower bound to the upper bound
        # owsa_dict contains the 5 values tested in the model
        if param == "c_program"
            cost_initial_range = np.linspace(
                c.MODEL_INPUTS.loc['c_init', 'l_bound'], c.MODEL_INPUTS.loc['c_init', 'u_bound'], 5
            )
            cost_monthly_range = np.linspace(
                c.MODEL_INPUTS.loc['c_cont', 'l_bound'], c.MODEL_INPUTS.loc['c_cont', 'u_bound'], 5
            )
            self.cost_initial_epc = cost_initial_range[value_on]
            self.cost_monthly_epc = cost_monthly_range[value_on]
            # Add to value dictionary
            owsa_dict["c_init"] = cost_init_range
            owsa_dict["c_cont"] = cost_cont_range
        elif param == "u_init":
            init_range = np.linspace(
                c.MODEL_INPUTS.loc['u_init', 'l_bound'], c.MODEL_INPUTS.loc['u_init', 'u_bound'], 5
            )
            self.u_init = init_range[value_on]
            owsa_dict["bmi_init"] = init_range
        elif param == "u_bmi":
            bmi_range = np.linspace(
                c.MODEL_INPUTS.loc['u_bmi_loss', 'l_bound'], c.MODEL_INPUTS.loc['u_bmi_loss', 'u_bound'], 5
            )
            self.u_bmi = bmi_range[value_on]
            owsa_dict["u_bmi"] = bmi_range
        elif param == "epc_bmi":
            bmi_perc_loss_spline1_range = np.linspace(
                c.MODEL_INPUTS.loc['epc_bmichange_pt_perc_1yr_pop', 'l_bound'], 
                c.MODEL_INPUTS.loc['epc_bmichange_pt_perc_1yr_pop', 'u_bound'], 5
            )
            bmi_perc_loss_spline2_range = np.linspace(
                c.MODEL_INPUTS.loc['epc_bmichange_pt_perc_2yr_pop', 'l_bound'], 
                c.MODEL_INPUTS.loc['epc_bmichange_pt_perc_2yr_pop', 'u_bound'], 5
            )
            bmi_z_perc_loss_spline1_range = np.linspace(
            c.MODEL_INPUTS.loc['epc_bmichange_z_perc_1yr', 'l_bound'], 
            c.MODEL_INPUTS.loc['epc_bmichange_z_perc_1yr', 'u_bound'], 5
            )
            bmi_z_perc_loss_spline2_range = np.linspace(
            c.MODEL_INPUTS.loc['epc_bmichange_z_perc_2yr', 'l_bound'], 
            c.MODEL_INPUTS.loc['epc_bmichange_z_perc_2yr', 'u_bound'], 5
            )
            ## bmi pt
            self.bmi_perc_loss_spline1 = bmi_perc_loss_spline1_range[value_on]
            self.bmi_perc_loss_spline2 = bmi_perc_loss_spline2_range[value_on]
            self.get_monthly_bmi_change()
            # Add to dictionary
            owsa_dict['epc_bmi_loss_spline1'] = bmi_perc_loss_spline1_range
            owsa_dict['epc_bmi_loss_spline2'] = bmi_perc_loss_spline2_range
            ## bmi z
            self.bmi_z_perc_loss_spline1 = bmi_z_perc_loss_spline1_range[value_on]
            self.bmi_z_perc_loss_spline2 = bmi_z_perc_loss_spline2_range[value_on]
            self.get_monthly_bmi_change()
            ## Add to dictionary
            owsa_dict['epc_bmi_z_loss_spline1'] = bmi_z_perc_loss_spline1_range
            owsa_dict['epc_bmi_z_loss_spline2'] = bmi_z_perc_loss_spline2_range
"""
