# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 12:26:55 2023

@author: sophi
"""

import pandas as pd
import numpy as np
import configs as c
import math
import common_functions as use


class Person:
    def __init__(self, id, gender, params):
        self.id = id
        self.params = params
        self.initialAgeInMonths = c.START_AGE*12
        self.gender = gender
        self.currAgeInMonths = c.START_AGE*12
        self.isAlive = True
        self.initialBMI = c.START_BMI
        self.initialBMI_z = c.START_BMI_Z
        self.BMI = np.zeros(c.TIME+1)
        self.BMI[0] = self.initialBMI
        self.BMI_z = np.zeros(c.TIME+1)
        self.BMI_z[0] = self.initialBMI_z
        self.initialQOL = params.u_init
        self.QOL = np.zeros(c.TIME+1)
        self.state = c.State.ALIVE
        self.month = 0
        self.cost = np.zeros(c.TIME)

    def calc_bmi_loss_from_notx(self):
        '''Compare BMI loss to natural history BMI for a single person
            Input is a numpy array of all weights for one patient at each
            time point. Outputs list of percent weight loss at each month
            for one patient
            '''
        # Get natural BMI gain
        natural_BMI = c.notx_bmiArr[0:c.TIME+1]
        # Calculate BMI loss
        perc_bmi_loss = (natural_BMI-self.BMI)/natural_BMI*100
        return perc_bmi_loss

    def calc_bmi_loss_from_baseline(self):
        '''Compare BMI loss to baseline for a single person
            Input is a numpy array of all weights at each time point
            Outputs list of perc weight loss at each month for one patient
            '''
        perc_bmi_loss = (self.initialBMI - self.BMI) / self.initialBMI * 100
        return perc_bmi_loss

    def calc_bmi_z_loss_from_notx(self):
        '''Compare BMI Z loss to natural history BMI Z for a single person
            Input is a numpy array of all weights for one patient at each
            ime point. Outputs list of percent weight loss at each month for
            one patient '''
        # Get natural BMI gain
        natural_BMI_z = c.notx_bmiArr_z[0:c.TIME+1]
        # Calculate BMI loss
        perc_bmi_z_loss = (natural_BMI_z-self.BMI_z)/natural_BMI_z*100
        return perc_bmi_z_loss

    def calc_bmi_z_loss_from_baseline(self):
        ''' Compare BMI Z-score loss to baseline for a single person
        Input is a numpy array of all BMI z=scores at each time point
        Outputs list of perc bmi z loss at each month for one patient
        '''
        perc_bmi_z_loss = (self.initialBMI_z - self.BMI_z) / \
            self.initialBMI_z * 100
        return perc_bmi_z_loss

    def checkMortality(self):
        # Life tables only go up to BMI 50
        if self.BMI[self.month] > 50:
            bmi = 50
        else:
            bmi = round(self.BMI[self.month])

        # Apply all-cause mortality and move to dead state
        # Once patient is dead, model should stop running for this person
        randVal = np.random.rand()

        if c.BMI_LIFE_TABLE:  # True = Alive
            if self.gender == 0:  # Male
                if randVal < c.p_acMort_month.loc[self.currAgeInMonths, bmi]:
                    self.isAlive = False
                    self.state = c.State.DEAD
                    self.QOL[self.month:] = 0  # no more new qalys
                    self.BMI[self.month+1:] = np.nan  # no more BMI

    def updateBMI(self):
        if self.month < self.params.spline1:
            bmichange = self.params.monthly_bmi_change_spline1
        elif self.month < self.params.spline2:
            bmichange = self.params.monthly_bmi_change_spline2
        else:  # after trial ends
            bmichange = c.MONTHLY_BMI_CHANGE_NH
        oldBMI = self.BMI[self.month]
        self.BMI[self.month + 1] = oldBMI + bmichange

    def updateBMI_Z(self):
        if self.month < self.params.spline1:
            bmichange_z = self.params.monthly_bmi_z_change_spline1
        elif self.month < self.params.spline2:
            bmichange_z = self.params.monthly_bmi_z_change_spline2
        else:  # after trial ends
            bmichange_z = c.MONTHLY_BMI_Z_CHANGE_NH
        oldBMI_z = self.BMI_z[self.month]
        self.BMI_z[self.month+1] = oldBMI_z + bmichange_z

    def updateCost(self):
        # No costs associated with no intervention
        # Initial costs for starting C4H = startup costs
        if self.params.strat != 'NO_INTERVENTION':
            if self.month == 0:
                self.cost[self.month] += self.params.c_initial
            if self.isAlive and self.month > 0:
                self.cost[self.month] += self.params.c_monthly

    def updateQOL(self):
        oldQOL = self.QOL[self.month]
        oldBMI_z = self.BMI_z[self.month]
        newBMI_z = self.BMI_z[self.month + 1]
        bmi_z_loss = oldBMI_z - newBMI_z  # positive val if z decreases
        self.QOL[self.month + 1] += oldQOL + \
            bmi_z_loss * self.params.u_bmi * 100

    def updateCounters(self):
        self.currAgeInMonths += 1
        self.month += 1

    def runPersonInstance(self):
        self.updateStates()
        if self.isAlive is False:
            # if patient is dead, model no longer runs for this patient
            return

    def updateStates(self):
        # Update mortality
        self.checkMortality()
        if self.isAlive is False:
            return
        self.updateBMI()
        self.updateBMI_Z()
        self.updateQOL()
        self.updateCost()
