# Connect4Health
Connect4Health pediatric obesity lifestyle intervention CEA

## Define patient population
In the configs.py file, set the START_AGE, START_BMI, and PERC_FEMALE of your patient population. Determine how large you want your cohort size to be using the N_POP parameter.
Alternatively, you can adjust the patient population within the model_inputs.xlsx sheet.

Once your starting patient parameters are established, run the cohort.py file which outputs a csv in the data folder of length N_POP where each row is one unique patient in the cohort. A value of 1 in the sex column indicates that the patient is male and a value of 0 indicates the patient is female. The proportion of male and female patients is dependent on the value set in PERC_FEMALE in the configs.py file.

## Run base case
To run the base case version of the model, set MODE = 'basecase' in the configs.py file and set PRINT = True in order to save the model outputs. Set TIME = 60 which will run the model for 5 years. Set N_PROCESSES to the number of cores you want to use.

Ensure that you have an output folder with 3 subfolders: 1yr, 2yr, 5yr. Run the main.py file. All model output files will initially be placed in the 7yr file.

After the base case model has finished running, run the separate_results.py file to break up the 7 year results into 13 months, 2 years, and 5 years. These results are then output to their corresponding folders. Run the post-processing.py file. This will generate the cost-effectiveness results for each time horizon. In the terminal, it will print the time horizon and whether or not any strategies are strictly or extendedly dominated. Two cost-effectiveness files are output for each time horizon. The file all_cea.xlsx will show the discounted costs, discounted qalys, and icer for all strategies. If an icer cell is empty, it means the strategy is either strictly or extendedly dominated. The file frontier_cea.xlsx only shows the strategies that are on the efficiency frontier. 
