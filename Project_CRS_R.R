library(dplyr)
library(lubridate)

data <- ScanRecords_2

# Mean and standard deviation for duration of all patients
mean_duration <- mean(data$Duration)
sd_duration <- sd(data$Duration)

# Mean and standard deviation for time of all patients
mean_time <- mean(data$Time)
sd_time <- sd(data$Time)

# Constructing normal distribution graph for the duration of type 1 patients
duration_1 <- subset(data$Duration, data$PatientType == "Type 1")
mean_duration_1 <- mean(duration_1)
sd_duration_1 <- sd(duration_1)
y <- dnorm(duration_1, mean_duration_1, sd_duration_1)
plot(duration_1,y)

# Mean and standard deviation for duration of type 2 patients
duration_2 <- subset(data$Duration, data$PatientType == "Type 2")
mean_duration_2 <- mean(duration_2)
sd_duration_2 <- sd(duration_2)

# Mean and standard deviation for time of type 1 patients
time_1 <- subset(data$Time, data$PatientType == "Type 1")
mean_time_1 <- mean(time_1)
sd_time_1 <- sd(time_1)

# Mean and standard deviation for time of type 2 patients
time_2 <- subset(data$Time, data$PatientType == "Type 2")
mean_time_2 <- mean(time_2)
sd_time_2 <- sd(time_2)

data %>%
  group_by(data$Date) %>%
  summarise(type1_sum = sum(data$PatientType == "Type 1"))

type1_per_day_data <- data %>%
  filter(PatientType == "Type 1") %>%
  group_by(Date) %>%
  summarise(type1_count = n())

mean_type1_day <- mean(type1_per_day_data$type1_count)
mean_type1_day

type2_per_day_data <- data %>%
  filter(PatientType == "Type 2") %>%
  group_by(Date) %>%
  summarise(type2_count = n())

mean_type2_day <- mean(type2_per_day_data$type2_count)
mean_type2_day

# Poisson distribution for the arrivals of the first group
max_type1_day <- max(type1_per_day_data$type1_count)

patient_counts_1 <- 0:max_type1_day  # Set the range of patient counts you want to consider
poisson_probabilities_1 <- dpois(patient_counts_1, lambda = mean_type1_day)

# Plot the Poisson distribution
plot(patient_counts_1, poisson_probabilities_1, type = "h",
     main = "Poisson Distribution of Type 1 Patients per Day",
     xlab = "Number of Type 1 Patients per Day",
     ylab = "Probability",
     ylim = c(0, max(poisson_probabilities_1) * 1.2))

# Random testing for the second group
# Poisson distribution for the arrivals of the second group, not sure if it is Poisson
max_type2_day <- max(type2_per_day_data$type2_count)

patient_counts_2 <- 0:max_type2_day  # Set the range of patient counts you want to consider
poisson_probabilities_2 <- dpois(patient_counts_2, lambda = mean_type2_day)

# Plot the Poisson distribution
plot(patient_counts_2, poisson_probabilities_2, type = "h",
     main = "Poisson Distribution of Type 2 Patients per Day",
     xlab = "Number of Type 2 Patients per Day",
     ylab = "Probability",
     ylim = c(0, max(poisson_probabilities_2) * 1.2))

z <- dnorm(patient_counts_2, mean(patient_counts_2), sd(patient_counts_2))
plot(patient_counts_2,z)


# Creating the empirical distribution function
duration_edf_2 <- ecdf(duration_2)

# Plotting the empirical distribution function
plot(duration_edf_2, main = "Empirical Distribution Function", xlab = "Data Values", ylab = "Cumulative Probability")

# From bootstrap lecture, currently not working
J <- sample.int(length(duration_2), size = length(duration_2), replace = TRUE)
duration_2.star <- duration_2[J] 

plot(duration_2.star, main = "Duration 2 star", xlab = "Data Values", ylab = "Cumulative Probability")

