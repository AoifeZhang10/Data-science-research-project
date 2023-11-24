import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import nbinom, norm

# Replace with your actual file path and column name
file_path = 'data/Result_processed_SNP_result y.xlsx'
column_name = 'generation year'

# Read the Excel file
df = pd.read_excel(file_path)

# Calculate mean and standard deviation
mean_value = df[column_name].mean()
standard_deviation = df[column_name].std()  # Sample standard deviation by default
print(mean_value)
print(standard_deviation)

# Assuming df, r, and p are already defined
# Calculate the parameters r and p for the negative binomial distribution
r = (mean_value ** 2) / (standard_deviation ** 2 - mean_value)
p = r / (r + mean_value)

# Generate a sequence of x values
x_values = np.arange(0, 500)

# Calculate CDF values
cdf_values = nbinom.cdf(x_values, r, p)

# Calculate PMF values
pmf_values = nbinom.pmf(x_values, r, p)

# Find the minimum x value where CDF is greater than 0.99
x_max = x_values[np.argmax(cdf_values > 0.99)]

# Find the peak value of PMF
peak_x = x_values[np.argmax(pmf_values)]
peak_y = np.max(pmf_values)

# Create PMF plot
plt.figure(figsize=(10, 6))
plt.plot(x_values, pmf_values, color='blue', label='PMF')
plt.scatter(peak_x, peak_y, color='red', s=30, label='Peak')
plt.title('Probability Mass Function Value')
plt.xlabel('Number of Year')
plt.ylabel('PMF Value')
plt.legend()
plt.grid()
plt.show()

# Create CDF plot
plt.figure(figsize=(10, 6))
plt.plot(x_values, cdf_values, color='red', label='CDF')
plt.axvline(x=x_max, color='black', linestyle='--', label=f'CDF > 0.99 at x={x_max}')
plt.title('Cumulative Distribution Function Value')
plt.xlabel('Number of Year')
plt.ylabel('CDF Value')
plt.legend()
plt.grid()
plt.show()

# Create a normal distribution with a mean of the mid-point between your min and max values and a standard deviation.
min_val = 1840
max_val = 1960
mean = (max_val + min_val) / 2
std = (max_val - min_val) / 4  # Assuming you want 95% within 4 standard deviations

# Function to get the probability from the negative binomial distribution
def get_probability_from_negbin(value, r, p):
    return nbinom.pmf(value, r, p)

# Function to get y_value from x_value for a normal distribution
def get_y_value_from_normal_distribution(x_value, mean, std):
    return norm.pdf(x_value, mean, std)

# print(get_probability_from_negbin(200,r,p))
#
Time_values = []
inside_p_values = []

for generation in range(1840-x_max, 1930):
    inside_p = 0
    for data_point in range(1840, 1930):
        generation_c = data_point - generation
        if generation_c > 0:

            p_c = get_probability_from_negbin(generation_c, r, p)
            inside_p += get_y_value_from_normal_distribution(data_point, mean, std) * p_c
    Time_values.append(generation)
    inside_p_values.append(inside_p)

# Find the peaks
peaks_x = []
peaks_y = []
for i in range(1, len(inside_p_values) - 1):
    if inside_p_values[i] > inside_p_values[i-1] and inside_p_values[i] > inside_p_values[i+1]:
        peaks_x.append(Time_values[i])
        peaks_y.append(inside_p_values[i])


# Plotting
plt.figure(figsize=(12, 8))
plt.plot(Time_values, inside_p_values, color='blue', label='Probability Over Time')
plt.scatter(peaks_x, peaks_y, color='red', zorder=5, label=f'Peak year x={peaks_x}')  # Zorder ensures the points are on top of the line
plt.xlabel('Year')
plt.ylabel('Probability')
plt.legend()
plt.grid(True)
plt.show()

plt.savefig("result.png")

# number_imported = [260, 1636, 6620, 13144, 34064, 107006, 30960]
# year_list = [1620, 1640, 1660, 1680, 1700, 1720, 1740]
number_imported = [260, 1636, 6620, 13144, 34064, 107006, 30960, 100686, 41418, 82578, 1501, 303]
year_list = [1620,1640,1660,1680,1700,1720,1740,1760,1780,1800,1820,1840]
# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot inside_p_values over Time_values on the primary y-axis
ax1.plot(Time_values, inside_p_values, 'g-', label='Probability Over Time')
ax1.set_xlabel('Year')
ax1.set_ylabel('Probability', color='g')
ax1.tick_params('y', colors='g')

# Create a secondary y-axis for number_imported
ax2 = ax1.twinx()
ax2.plot(year_list, number_imported, 'b-', label='Number of Imported Slave)')
ax2.set_ylabel('Number Imported', color='b')
ax2.tick_params('y', colors='b')

# Draw red vertical lines and year labels
for i, year in enumerate(year_list):
    ax2.vlines(x=year, ymin=0, ymax=number_imported[i], color='red', linestyle='--')
    ax2.text(year, 0, str(year), color='red', ha='center', va='top', rotation=45)

# Adding legends
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.show()