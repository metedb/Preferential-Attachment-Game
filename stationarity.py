import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import kpss
from scipy.stats import chisquare, expon
from scipy.stats import kstest, expon, chi2, norm


def qq_plot_exponential(data):
    
    # Calculate the sample mean
    sample_mean = np.mean(data)

    # Generate a theoretical exponential distribution with the same mean
    theoretical = np.random.exponential(sample_mean, size=len(data))

    # Sort data and theoretical values
    data_sorted = np.sort(data)
    theoretical_sorted = np.sort(theoretical)

    # Generate QQ plot
    plt.figure(figsize=(10, 6))
    plt.plot(theoretical_sorted, data_sorted, 'o')
    min_value = np.floor(min(min(theoretical_sorted), min(data_sorted)))
    max_value = np.ceil(max(max(theoretical_sorted), max(data_sorted)))
    plt.plot([min_value, max_value], [min_value, max_value], 'r--')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Theoretical Quantiles')
    plt.ylabel('Sample Quantiles')
    plt.title('Q-Q Plot (Exponential Distribution)')
    plt.grid(True)
    plt.show()


from statsmodels.tsa.stattools import kpss

def analyze_excel_file_2(filename, column_name):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(filename)

    # Extract the column data based on the provided column name
    column_data = df[column_name]

    # Handle missing or invalid values (same as before)
    column_data = column_data.dropna()
    column_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    column_data = column_data.dropna()

    # Calculate the cumulative sum of the column data (same as before)
    cumulative_sum = column_data.cumsum()

    # Plot the graph (same as before)
    plt.plot(cumulative_sum, column_data)
    plt.xlabel("Cumulative Sum")
    plt.ylabel("Column Values")
    plt.title(f"Graph for {column_name}")
    plt.show()

    # Perform KPSS test for stationarity
    result = kpss(column_data)
    p_value = result[1]

    # Determine the stationarity based on the p-value
    if p_value < 0.05:
        stationarity = "Non-Stationary"
    else:
        stationarity = "Stationary"

        # Calculate class limits and frequencies
    k = 10  # Number of classes
    lambda_param = 1 / column_data.mean()
    probabilities = np.linspace(0, 1, k + 1)
    bin_edges = [0]
    
    observed_freq_vector = []
    expected_freq_vector = []
    lower_limits = []
    upper_limits = []

    # Now, we create bins based on these edges and count the number of observations in each bin
    for i in range(k - 1):
        lower_limit = bin_edges[i]
        bin_edges.append((-1 / lambda_param) * np.log(1 - (i + 1) * 0.1))
        upper_limit = bin_edges[i + 1]
        lower_limits.append(lower_limit)
        upper_limits.append(upper_limit)

        column_data_np = column_data.to_numpy()  # Convert to numpy array
        observed_freq = np.sum((column_data_np > lower_limit) & (column_data_np <= upper_limit))
        observed_freq_vector.append(observed_freq)

        expected_freq = len(column_data) / k
        expected_freq_vector.append(expected_freq)

    # Handle the last bin edge
    lower_limit = bin_edges[k - 1]
    upper_limit = float('inf')
    lower_limits.append(lower_limit)
    upper_limits.append(upper_limit)

    column_data_np = column_data.to_numpy()  # Convert to numpy array
    observed_freq = np.sum((column_data_np > lower_limit) & (column_data_np <= upper_limit))
    observed_freq_vector.append(observed_freq)

    expected_freq = len(column_data) / k
    expected_freq_vector.append(expected_freq)
        
    # Create the table
    table = pd.DataFrame({
        "Class Index": range(1, k + 1),
        "Lower Limit": lower_limits,
        "Upper Limit": upper_limits,
        "Observed Freq.": observed_freq_vector,
        "Expected Freq.": expected_freq_vector
    })

    # Perform chi-square test
    alpha = 0.05
    df = k - 2  # Degrees of freedom: k - 1 (number of classes) - 2 (estimated parameters)
    real_chi_squared_value = chi2.ppf(1 - alpha, df)
    chi_squared0 = np.sum(((table['Observed Freq.'] - table['Expected Freq.'])**2) / table['Expected Freq.'])

    autocorr_lag1 = column_data.autocorr(lag=1)
    autocorr_lag2 = column_data.autocorr(lag=2)
    autocorr_lag3 = column_data.autocorr(lag=3)

    print(table)
    qq_plot_exponential(column_data)
    print(real_chi_squared_value, chi_squared0, stationarity, "\n")
    print(autocorr_lag1, autocorr_lag2, autocorr_lag3)



    


analyze_excel_file_2("data_hw2.xlsx", "Group 13")




