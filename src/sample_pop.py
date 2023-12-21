# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 15:00:18 2023

@author: sophi
"""

import csv
import numpy as np
from scipy.stats import norm

# Set random seed for reproducibility
np.random.seed(42)

# Population size
population_size = 100000

# Generate age using normal distribution
mean_age = 7.81
sd_age = 3.14
ages = np.random.normal(loc=mean_age, scale=sd_age, size=population_size)
ages = np.maximum(ages, 0)

# Generate gender based on specified proportions
gender = np.random.choice(['Male', 'Female'], size=population_size, p=[0.5303, 0.4697])

# Baseline mean and standard deviation of BMI z-score
mean_z_score = 1.91
sd_z_score = 0.56

# Generate random z-scores based on the normal distribution
z_scores = np.random.normal(loc=mean_z_score, scale=sd_z_score, size=population_size)

# Convert z-scores to percentiles using the cumulative distribution function (CDF)
percentiles = norm.cdf(z_scores) * 100

# Generate unique IDs for each individual
ids = np.arange(1, population_size + 1)

# Combine data into a list of tuples
sample_data = list(zip(ids, ages, gender, z_scores, percentiles))

# Specify the CSV file path
csv_file_path = 'sampled_cohort.csv'

# Write the data to the CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)

    # Write the header
    csv_writer.writerow(['ID', 'Age', 'Gender', 'BMI_Z', 'BMI_Percentile'])

    # Write the data
    csv_writer.writerows(sample_data)

print(f"Sampled cohort data has been saved to: {csv_file_path}")


