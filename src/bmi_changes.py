

library(tidyverse)
PATH = 'C:/Users/sophi/OneDrive - cumc.columbia.edu/STIMULATE/CEA'

convert_wt_to_bmi <- function(init_weight, init_bmi, curr_weight) {
  bmi <- curr_weight / (init_weight/init_bmi)
  return(bmi)
}


##########################
# NO INTERVENTION
##########################
no_intervention <- read.csv(PATH+"/data/data_curves/")
colnames(placebo_ <- c("x","Curve1"))

# Plot points and best fit line
plot(no_intervention$x, no_intervention$Curve1, pch=16, col='red', cex=1.2)
abline(lm(no_intervention$Curve1 ~ no_intervention$x), col='blue', lty='dashed')

# Find regression model 
# y = 0.0048x - 2.787
# change in bmi = 0.034
summary(lm(no_intervention$Curve1 ~ no_intervention$x))$coefficients


line <- function(x) {
  return((0.0048*x) - 2.787)
}

placebo_init_weight = 101.1
placebo_init_bmi = 36
placebo_perc_weight_loss_13mo = line(56)
placebo_perc_weight_loss_2yr = line(104)
placebo_13mo_weight = placebo_init_weight + (placebo_init_weight * (placebo_perc_weight_loss_13mo/100))
placebo_2yr_weight = placebo_init_weight + (placebo_init_weight * (placebo_perc_weight_loss_2yr/100))

# BMI
mo13_bmi <- convert_wt_to_bmi(placebo_init_weight, placebo_init_bmi, placebo_13mo_weight)
yr2_bmi <- convert_wt_to_bmi(placebo_init_weight, placebo_init_bmi, placebo_2yr_weight)

# Get BMI % change from baseline
mo13_bmi_change <- (mo13_bmi - placebo_init_bmi)/placebo_init_bmi
yr2_bmi_change <- (yr2_bmi - placebo_init_bmi)/placebo_init_bmi

# Percent increase in bmi loss = 9.15%
lifestyle_perc_increase <- (mo13_bmi_change - yr2_bmi_change) / mo13_bmi_change
# Maintain same percent increase for adolescent trial

######################
# LIRAGLUTIDE
######################

# Read in data
lira <- read.csv("~/OneDrive - cumc.columbia.edu/adolescent_pharmacotherapy/repo/adolescent_pharmacotherapy/data/data_curves/liraglutide_2yr/astrup_lira_2yr_all.csv")
colnames(lira) <- c("x", "Curve1")

# Plot points and best fit line
plot(lira$x, lira$Curve1, pch=16, col='red', cex=1.2)
abline(lm(lira$Curve1 ~ lira$x), col='blue', lty='dashed')

# Find regression model 
# y = 0.034x - 13.431
# change in bmi = 0.034
summary(lm(lira$Curve1 ~ lira$x))$coefficients

line <- function(x) {
  return((0.034*x) - 13.431)
}

lira_init_weight = 97.6 # kg at randomization
lira_init_bmi = 34.8 # at randomization
lira_13mo_weight_change = line(56) # 13 months
lira_2yr_weight_change = line(104) # kg
lira_13mo_weight = lira_init_weight + lira_13mo_weight_change
lira_2yr_weight = lira_init_weight + lira_2yr_weight_change

# BMI
mo13_bmi <- convert_wt_to_bmi(lira_init_weight, lira_init_bmi, lira_13mo_weight)
yr2_bmi <- convert_wt_to_bmi(lira_init_weight, lira_init_bmi, lira_2yr_weight)

# Get BMI % change from baseline
mo13_bmi_change <- (mo13_bmi - lira_init_bmi)/lira_init_bmi
yr2_bmi_change <- (yr2_bmi - lira_init_bmi)/lira_init_bmi

# Percent increase in bmi loss = 14.2%
lira_perc_increase <- (mo13_bmi_change - yr2_bmi_change) / mo13_bmi_change
# Maintain same percent increase for adolescent trial

######################
# MID-DOSE QSYMIA
######################
# Read in data
midq <- read.csv("~/OneDrive - cumc.columbia.edu/adolescent_pharmacotherapy/repo/adolescent_pharmacotherapy/data/data_curves/qsymia_2yr/middose_all.csv")
colnames(midq) <- c("x", "Curve1")

# Plot points and best fit line
plot(midq$x, midq$Curve1, pch=16, col='red', cex=1.2)
abline(lm(midq$Curve1 ~ midq$x), col='blue', lty='dashed')

# Find regression model 
# y = 0.018x - 11.292
# change in bmi = 0.034
summary(lm(midq$Curve1 ~ midq$x))$coefficients

line <- function(x) {
  return((0.018*x) - 11.292)
}

mid_qsymia_init_weight = 102.2
mid_qsymia_init_bmi = 36.1
mid_qsymia_perc_weight_loss_13mo = line(56)/100
mid_qsymia_perc_weight_loss_2yr = line(104)/100
mid_qsymia_13mo_weight = mid_qsymia_init_weight + (mid_qsymia_init_weight * mid_qsymia_perc_weight_loss_13mo)
mid_qsymia_2yr_weight = mid_qsymia_init_weight + (mid_qsymia_init_weight * mid_qsymia_perc_weight_loss_2yr)

# BMI
mo13_bmi <- convert_wt_to_bmi(mid_qsymia_init_weight, mid_qsymia_init_bmi, mid_qsymia_13mo_weight)
yr2_bmi <- convert_wt_to_bmi(mid_qsymia_init_weight, mid_qsymia_init_bmi, mid_qsymia_2yr_weight)

# Get BMI % change from baseline
mo13_bmi_change <- (mo13_bmi - mid_qsymia_init_bmi)/mid_qsymia_init_bmi
yr2_bmi_change <- (yr2_bmi - mid_qsymia_init_bmi)/mid_qsymia_init_bmi

# Percent increase in bmi loss = 8.4%
mid_qsymia_perc_increase <- (mo13_bmi_change - yr2_bmi_change) / mo13_bmi_change
# Maintain same percent increase for adolescent trial

######################
# TOP-DOSE QSYMIA
######################

# Read in data
topq <- read.csv("~/OneDrive - cumc.columbia.edu/adolescent_pharmacotherapy/repo/adolescent_pharmacotherapy/data/data_curves/qsymia_2yr/topdose_all.csv")
colnames(topq) <- c("x", "Curve1")

# Plot points and best fit line
plot(topq$x, topq$Curve1, pch=16, col='red', cex=1.2)
abline(lm(topq$Curve1 ~ topq$x), col='blue', lty='dashed')

# Find regression model 
# y = 0.034x - 14.617
# change in bmi = 0.034
summary(lm(topq$Curve1 ~ topq$x))$coefficients

line <- function(x) {
  return((0.034*x) - 14.617)
}

top_qsymia_init_weight = 101.9
top_qsymia_init_bmi = 36.2
top_qsymia_perc_weight_loss_13mo = line(56)/100
top_qsymia_perc_weight_loss_2yr = line(104)/100
top_qsymia_13mo_weight = top_qsymia_init_weight + (top_qsymia_init_weight * top_qsymia_perc_weight_loss_13mo)
top_qsymia_2yr_weight = top_qsymia_init_weight + (top_qsymia_init_weight * top_qsymia_perc_weight_loss_2yr)

# BMI
mo13_bmi <- convert_wt_to_bmi(top_qsymia_init_weight, top_qsymia_init_bmi, top_qsymia_13mo_weight)
yr2_bmi <- convert_wt_to_bmi(top_qsymia_init_weight, top_qsymia_init_bmi, top_qsymia_2yr_weight)

# Get BMI % change from baseline
mo13_bmi_change <- (mo13_bmi - top_qsymia_init_bmi)/top_qsymia_init_bmi
yr2_bmi_change <- (yr2_bmi - top_qsymia_init_bmi)/top_qsymia_init_bmi

# Percent increase in bmi loss = 12.8%
top_qsymia_perc_increase <- (mo13_bmi_change - yr2_bmi_change) / mo13_bmi_change
# Maintain same percent increase for adolescent trial