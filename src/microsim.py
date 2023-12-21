# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 17:47:04 2023

@author: sophi
"""
import pandas as pd
import numpy as np
import configs as c
import person
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# Set output paths
if c.TIME == 12:
    path = c.OUTPUT_PATHS['results_1yr']
elif c.TIME == 24:
    path = c.OUTPUT_PATHS['results_2yr']

# Define Microsim class to run microsim


class Microsim:
    def __init__(self, params):
        self.params = params
        self.n = c.N_POP
        self.time = c.TIME
        self.probFemale = c.PERC_FEMALE
        # mean bmi loss for all patients
        self.bmi_loss_notx_arr = np.zeros(self.time + 1)
        self.bmi_loss_baseline_arr = np.zeros(
            self.time + 1)  # mean bmi loss for all patients
        self.bmi_loss_notx_arr_lowerq = np.zeros(self.time + 1)
        self.bmi_loss_notx_arr_upperq = np.zeros(self.time + 1)
        self.bmi_loss_baseline_arr_lowerq = np.zeros(self.time + 1)
        self.bmi_loss_baseline_arr_upperq = np.zeros(self.time + 1)
        self.bmiArr = np.zeros(self.time + 1)  # mean bmi for all patients
        self.bmiArr_lowerq = np.zeros(self.time + 1)
        self.bmiArr_upperq = np.zeros(self.time + 1)
        self.bmi_z_loss_notx_arr = np.zeros(
            self.time + 1)  # mean bmi loss for all patients
        self.bmi_z_loss_baseline_arr = np.zeros(
            self.time + 1)  # mean bmi loss for all patients
        self.bmi_z_loss_notx_arr_lowerq = np.zeros(self.time + 1)
        self.bmi_z_loss_notx_arr_upperq = np.zeros(self.time + 1)
        self.bmi_z_loss_baseline_arr_lowerq = np.zeros(self.time + 1)
        self.bmi_z_loss_baseline_arr_upperq = np.zeros(self.time + 1)
        self.bmizArr = np.zeros(self.time + 1)  # mean bmi for all patients
        self.bmizArr_lowerq = np.zeros(self.time + 1)
        self.bmizArr_upperq = np.zeros(self.time + 1)
        self.QOLArr = np.zeros(self.time)  # sum of QOL for all patients
        self.totalQOL = 0  # total sum of QOL for all patients
        self.costArr = np.zeros(self.time)  # sum of costs for the program
        # number of patients in each state
        self.stateArr = np.zeros((self.time, c.State.ALL))
        self.state_df = 0  # initialize and update later, dataframe for stateArr
        self.startAge = c.START_AGE
        self.timeHorizon = c.TIME
        if c.SAVE_PATIENTS == True:
            self.patientArr = np.zeros((c.N_POP, c.TIME + 4))

    # Initialize Population
    def initPopulation(self):
        '''Outputs list of unique patients from the Patient class'''
        population = []
        for index, row in c.PATIENTS.iterrows():
            if row['sex'] == 0:  # female
                # create Person object with gender Female, append to population list
                population.append(person.Person(
                    index, c.Gender.FEMALE, self.params))
            else:  # male
                population.append(person.Person(
                    index, c.Gender.MALE, self.params))

        if len(population) != c.N_POP:
            print("Generated population size:", len(population))
            raise ValueError(
                "Issue in initPopulation() function, wrong number of patients")

        return population

    # Run person for full time horizon
    def runPerson(self, p):
        '''Runs a person for the full time horizon
           Input is a Person class object
           Outputs state array, bmi, quality of life, cost'''
        # Initialize state matrix
        states_p = np.zeros((c.TIME, c.State.ALL))
        while p.month < self.time:
            p.runPersonInstance()  # runs for one month

            if p.isAlive is False:  # patient is dead
                # Fill all remaining time points with dead state
                # Fill in BMI and QOL
                fillmonths = (c.TIME + 1) - len(p.BMI)
                for i in range(fillmonths):
                    p.QOL = np.append(p.QOL, 0)
                    p.BMI = np.append(p.BMI, np.nan)
                    p.BMI_z = np.append(p.BMI_z, np.nan)
                states_p[p.month:, c.State.DEAD] += 1
                break  # stops running of this patient

            # Update state matrix
            states_p[p.month, p.state] += 1

            # This is run here so results are incremented
            # before p.month is incremented
            p.updateCounters()

        if c.SAVE_PATIENTS:
            outputs = [states_p, p.calc_bmi_loss_from_notx(),
                       p.calc_bmi_loss_from_baseline(),
                       p.calc_bmi_z_loss_from_notx(),
                       p.calc_bmi_z_loss_from_baseline(),
                       p.BMI, p.BMI_z, p.QOL[1:], p.cost,
                       np.concatenate((p.isAlive, p.BMI, p.BMI_z), axis=None)]
        else:
            outputs = [states_p, p.calc_bmi_loss_from_notx(),
                       p.calc_bmi_loss_from_baseline(),
                       p.calc_bmi_z_loss_from_notx(),
                       p.calc_bmi_z_loss_from_baseline(),
                       p.BMI, p.BMI_z, p.QOL[1:], p.cost]
        return outputs

    def processResults(self, results):
        # Results from each individual patient
        temp_bmi_loss_notx = np.zeros((c.N_POP, c.TIME + 1))
        temp_bmi_loss_baseline = np.zeros((c.N_POP, c.TIME + 1))
        temp_bmi = np.zeros((c.N_POP, c.TIME + 1))
        temp_bmi_z_loss_notx = np.zeros((c.N_POP, c.TIME + 1))
        temp_bmi_z_loss_baseline = np.zeros((c.N_POP, c.TIME + 1))
        temp_bmi_z = np.zeros((c.N_POP, c.TIME + 1))
        # Combine like results for each patient
        for i in range(len(results)):
            self.stateArr += results[i][0]
            temp_bmi_loss_notx[i, :] += results[i][1]
            temp_bmi_loss_baseline[i, :] += results[i][2]
            temp_bmi[i, :] += results[i][5]
            temp_bmi_z_loss_notx[i, :] += results[i][3]
            temp_bmi_z_loss_baseline[i, :] += results[i][4]
            temp_bmi_z[i, :] += results[i][6]
            self.QOLArr += results[i][7]
            self.costArr += results[i][8]
            if c.SAVE_PATIENTS:
                self.patientArr[i, :] = results[i][9]
        # Get mean bmi loss, bmi values for each month
        self.bmi_loss_notx_arr = np.nanmean(temp_bmi_loss_notx, axis=0)
        self.bmi_loss_baseline_arr = np.nanmean(temp_bmi_loss_baseline, axis=0)
        self.bmiArr = np.nanmean(temp_bmi, axis=0)
        self.bmi_z_loss_notx_arr = np.nanmean(temp_bmi_z_loss_notx, axis=0)
        self.bmi_z_loss_baseline_arr = np.nanmean(
            temp_bmi_z_loss_baseline, axis=0)
        self.bmizArr = np.nanmean(temp_bmi_z, axis=0)
        # Get lowerq and upperq for bmi loss, bmi values for each month
        self.bmi_loss_notx_arr_lowerq = np.nanquantile(
            temp_bmi_loss_notx, 0.025, axis=0)
        self.bmi_loss_notx_arr_upperq = np.nanquantile(
            temp_bmi_loss_notx, 0.975, axis=0)
        self.bmi_loss_baseline_arr_lowerq = np.nanquantile(
            temp_bmi_loss_baseline, 0.025, axis=0)
        self.bmi_loss_baseline_arr_upperq = np.nanquantile(
            temp_bmi_loss_baseline, 0.975, axis=0)
        self.bmiArr_lowerq = np.nanquantile(temp_bmi, 0.025, axis=0)
        self.bmiArr_upperq = np.nanquantile(temp_bmi, 0.975, axis=0)
        self.bmi_z_loss_notx_arr_lowerq = np.nanquantile(
            temp_bmi_z_loss_notx, 0.025, axis=0)
        self.bmi_z_loss_notx_arr_upperq = np.nanquantile(
            temp_bmi_z_loss_notx, 0.975, axis=0)
        self.bmi_z_loss_baseline_arr_lowerq = np.nanquantile(
            temp_bmi_z_loss_baseline, 0.025, axis=0)
        self.bmi_z_loss_baseline_arr_upperq = np.nanquantile(
            temp_bmi_z_loss_baseline, 0.975, axis=0)
        self.bmizArr_lowerq = np.nanquantile(temp_bmi_z, 0.025, axis=0)
        self.bmizArr_upperq = np.nanquantile(temp_bmi_z, 0.975, axis=0)

        # Convert state array to dataframe for readability
        self.state_df = pd.DataFrame(
            data=self.stateArr, index=range(self.time), columns=c.state_names)
        self.totalQOL = self.QOLArr.sum() / 12  # quality-adjusted years
        self.totalCosts = self.costArr.sum()

    def runMicrosim(self):
        # Define population
        population = self.initPopulation()

        # Save gender ratio
        num_f = 0
        num_m = 0
        for patient in population:
            if patient.gender == 0:
                num_m += 1
            else:
                num_f += 1
        gender_ratio = {"Male": [num_m / c.N_POP],
                        "Female": [num_f / c.N_POP]}
        df = pd.DataFrame(gender_ratio)
        if c.PRINT and c.MODE == 'basecase':
            df.to_excel(path + "pop_stats.xlsx")

        # Loops through all patients in the population and calls runPerson
        pool = Pool(processes=c.N_PROCESSES)
        # list, each element is output of one patient
        results = pool.map(self.runPerson, population, c.BLOCK_SIZE)
        pool.close()
        pool.join()

        self.processResults(results)
