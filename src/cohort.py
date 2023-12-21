# -*- coding: utf-8 -*-
"""

"""

# Define cohort for microsimulation
# Creates a csv of all patient and whether they are male (1) or female (0)
# Number of patients determined by N_POP in configs.py

import pandas as pd
import numpy as np
import configs as c 

patientArr = []
for i in range(c.N_POP):
    randVal = np.random.rand()
    if randVal < c.PERC_FEMALE:
        patientArr.append(0)
    else:
        patientArr.append(1)

# Convert list to numpy array
patientArr = np.array(patientArr)
# Convert to dataframe
patient_df = pd.DataFrame(patientArr, columns = ['sex'])

PATH = 'C:/Users/sophi/OneDrive - cumc.columbia.edu/STIMULATE/CEA'
# Write to csv
patient_df.to_csv(PATH+'/data/patients.csv')
