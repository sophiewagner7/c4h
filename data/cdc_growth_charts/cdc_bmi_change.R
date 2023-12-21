# regression line using CDC growth charts 


library(tidyverse)
library(readxl)

setwd("C:/Users/sophi/OneDrive - cumc.columbia.edu/STIMULATE/CEA/data/cdc_growth_charts/")

# Read files for BMI at 1-zscore, 2-score for girls and boys
girls_1z <- read_csv("BMI_girls_1z.csv")
girls_2z <- read_csv("BMI_girls_2z.csv")
boys_1z <- read_csv("BMI_boys_1z.csv")
boys_2z <- read_csv("BMI_boys_2z.csv")

girls_1z_cut <- girls_1z[(girls_1z$age >= 7.5 & girls_1z$age <= 10.5),]
girls_2z_cut <- girls_2z[(girls_2z$age >= 7.5 & girls_2z$age <= 10.5),]
boys_1z_cut <- boys_1z[(boys_1z$age >= 7.5 & boys_1z$age <= 10.5),]
boys_2z_cut <- boys_2z[(boys_2z$age >= 7.5 & boys_2z$age <= 10.5),]

## Girls 1z
plot(girls_1z_cut$age, girls_1z_cut$bmi, type="b", lty=1)
abline(lm(girls_1z_cut$age ~ girls_1z_cut$bmi))
summary(lm(girls_1z_cut$age ~ girls_1z_cut$bmi))$coefficients
# Slope = 1.220653

## Girls 2z
plot(girls_2z_cut$age, girls_2z_cut$bmi, type="b", lty=1)
abline(lm(girls_2z_cut$age ~ girls_2z_cut$bmi))
summary(lm(girls_2z_cut$age ~ girls_2z_cut$bmi))$coefficients
# Slope = 0.7103459 

## Boys 1z
plot(boys_1z_cut$age, boys_1z_cut$bmi, type="b", lty=1)
abline(lm(boys_1z_cut$age ~ boys_1z_cut$bmi))
summary(lm(boys_1z_cut$age ~ boys_1z_cut$bmi))$coefficients
# Slope = 1.40308 

## Boys 2z
plot(boys_2z_cut$age, boys_2z_cut$bmi, type="b", lty=1)
abline(lm(boys_2z_cut$age ~ boys_2z_cut$bmi))
summary(lm(boys_2z_cut$age ~ boys_2z_cut$bmi))$coefficients[2]
# Slope = 0.7631635

girls_1z_lm<-lm(age ~ bmi, data=girls_1z_cut)
predict(girls_1z_lm, newdata=data.frame(age=8, bmi=NA))


girls_2z_lm<-lm(girls_2z_cut$age ~ girls_2z_cut$bmi)
boys_1z_lm<-lm(boys_1z_cut$age ~ boys_1z_cut$bmi)
boys_2z_lm <- lm(boys_2z_cut$age ~ boys_2z_cut$bmi)


# Interpolate BMI values for z-score 1.81
z_target <- 1.81
slope_girls <- girls_1z_lm$coefficients[2] + ((girls_2z_lm$coefficients[2] -girls_1z_lm$coefficients[2]) * (z_target - 1)) / (2-1)
print(slope_girls)
slope_boys <- boys_1z_lm$coefficients[2] + ((boys_2z_lm$coefficients[2] - boys_1z_lm$coefficients[2]) * (z_target -1)) / (2-1)
print(slope_boys)                                                

# Average slope for boys and girls
p_girls <- 0.4697
p_boys <- 0.5303
(slope_boys * p_boys) + (slope_girls * p_girls)  # 0.8483724
0.84372 / 12 

# 0.07031 BMI increase each month for our NH arm


14.18181818 + (1.220653 * 8)


# Assuming you have models for z-scores 1 and 2: model_z1, model_z2

# Function to calculate BMI using linear interpolation
bmi_interpolation <- function(model_z1, model_z2, age_target, z_target) {
  bmi_z1 <- predict(model_z1, newdata = data.frame(age = age_target))
  bmi_z2 <- predict(model_z2, newdata = data.frame(age = age_target))
  
  bmi_target <- bmi_z1 + (bmi_z2 - bmi_z1) * (z_target - 1) / (2 - 1)
  
  return(bmi_target)
}

predict(girls_1z_lm, newdata=data.frame(age=8))

# Example usage:
age_target <- 8
z_target <- 1.77

# Replace model_z1 and model_z2 with your actual models
# For example, if you have linear models: model_z1 <- lm(BMI ~ age, data = your_data_z1)
#                                            model_z2 <- lm(BMI ~ age, data = your_data_z2)

estimated_bmi <- bmi_interpolation(girls_1z_lm, girls_2z_lm, age_target, z_target)

# Print the estimated BMI
print(estimated_bmi)


############## G 1z
your_data <- data.frame(
  age = c( 7.4975, 7.9848, 8.5178, 9.0051, 9.5228, 10.0102),
  bmi = c(17.8203, 18.1937, 18.5671, 18.9693, 19.4289, 
          19.831)
)

# Fit a linear model
linear_model <- lm(bmi ~ age, data = your_data)

# Predict BMI at age 8
new_data <- data.frame(age = 8)
predicted_bmi <- predict(linear_model, newdata = new_data)

# Print the predicted BMI at age 8
print(predicted_bmi) #18.19547


########### G 2z
# Create a data frame from the provided data
your_data <- data.frame(
  age = c(7.4856, 7.9883, 8.5063, 8.9939, 9.4966, 10.0147),
  bmi = c(22.8213, 23.4818, 24.1136, 24.889, 25.5782, 26.2961)
)

# Fit a linear model
linear_model <- lm(bmi ~ age, data = your_data)

# Predict BMI at age 8
new_data <- data.frame(age = 8)
predicted_bmi <- predict(linear_model, newdata = new_data)

# Print the predicted BMI at age 8
print(predicted_bmi) # 23.49555


############### B 1z
# Create a data frame from the provided data
your_data <- data.frame(
  age = c(7.0084, 7.4955, 7.9674, 8.4849, 9.4896, 9.9768, 10.5096),
  bmi = c(17.3607, 17.6192, 17.8778, 18.1363, 18.8831, 19.2852, 19.6874)
)

# Fit a linear model
linear_model <- lm(bmi ~ age, data = your_data)

# Predict BMI at age 8
new_data <- data.frame(age = 8)
predicted_bmi <- predict(linear_model, newdata = new_data)

# Print the predicted BMI at age 8
print(predicted_bmi) #17.93534


############### B 2z

# Create a data frame from the provided data
your_data <- data.frame(
  age = c(7.0254, 7.5127, 7.9848, 8.4873, 9.0051, 9.4924, 10.0102, 10.5279),
  bmi = c(21.8106, 22.3846, 22.9872, 23.6186, 24.3361, 24.9962, 25.6276, 26.3163)
)

# Fit a linear model
linear_model <- lm(bmi ~ age, data = your_data)

# Predict BMI at age 8
new_data <- data.frame(age = 8)
predicted_bmi <- predict(linear_model, newdata = new_data)

# Print the predicted BMI at age 8
print(predicted_bmi) #23.02995

bmi_g_1z<-18.19547
bmi_g_2z<-23.49555
bmi_b_1z<-17.93534
bmi_b_2z<-23.02995

start_b <- bmi_b_1z + ((bmi_b_2z - bmi_b_1z) * (z_target -1)) / (2-1)
print(start_b) #21.85819
start_g <- bmi_g_1z + ((bmi_g_2z - bmi_g_1z) * (z_target -1)) / (2-1)
print(start_g) #22.27653

start_bmi<-p_boys*start_b + p_girls*start_g

print(start_bmi) #22.05468
