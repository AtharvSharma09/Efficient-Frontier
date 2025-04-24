# Portfolio Optimization with Efficient Frontier
This project implements a portfolio optimization tool using the Efficient Frontier concept, designed to maximize returns for a given level of risk using historical stock data from the NIFTY 500 index.

## Overview
The script Efficient_Frontier.py downloads historical stock data, calculates daily returns, and optimizes portfolio weights to achieve the maximum return for a user-defined risk constraint. It uses the yfinance library for data retrieval and scipy.optimize for optimization.
Features

### Data Retrieval: Downloads historical stock prices for NIFTY 500 stocks from Yahoo Finance.

### Portfolio Optimization: Maximizes portfolio return for a user-specified maximum annualized risk.

### Custom Weights: Allows users to provide custom weights via a CSV file.

### Risk Calculation: Computes portfolio risk using the covariance matrix of daily returns.

### Output: Displays optimized investment weights for each stock as percentages.

## Prerequisites

Python 3.8+
Required Python packages:
numpy
pandas
yfinance
scipy



### Install dependencies using:
pip install numpy pandas yfinance scipy

Directory Structure
├── Data/
│   ├── ind_nifty500list.csv    # List of NIFTY 500 ticker symbols
│   ├── user_weights.csv        # User-defined portfolio weights
│   ├── yf_data.pkl             # Cached historical stock data
├── Efficient_Frontier.py       # Main script
└── README.md                   # This file

## Usage

Prepare Data:

Ensure ind_nifty500list.csv is in the Data/ directory with a column Symbol containing NIFTY 500 ticker symbols.
Optionally, provide user_weights.csv in the Data/ directory with columns Ticker and Weight for custom weights.


### Run the Script:
python Efficient_Frontier.py


### Input:

When prompted, enter the maximum annualized risk (e.g., 0.20 for 20%). If invalid, defaults to 0.20.


### Output:

The script outputs the optimized weights for each stock, sorted by percentage, indicating the amount to invest.



## Example
Enter maximum annualized risk (e.g., 0.20 for 20%): 0.20
Amount to invest in each stock:
RELIANCE.NS    15.23456789
TCS.NS         12.34567890
HDFCBANK.NS    10.12345678
...

## Notes

The script caches downloaded data in yf_data.pkl to avoid repeated downloads. Delete this file to refresh data.
Ensure the sum of weights in user_weights.csv does not exceed 1 to avoid errors.
The optimization assumes annualization by multiplying daily returns and covariance by 252 (trading days).
Stocks with missing data are dropped during preprocessing.

## Limitations

Relies on historical data, which may not predict future performance.
Assumes normal distribution of returns for risk calculations.
No transaction costs or taxes are considered in the optimization.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
Contributing
Contributions are welcome! Please open an issue or submit a pull request with improvements or bug fixes.
