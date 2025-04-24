from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import scipy.optimize as so


# Load the ticker symbols
nifty_500 = pd.read_csv('Data/ind_nifty500list.csv')
tickers = [f"{symbol}.NS" for symbol in nifty_500['Symbol']]

# Download or load historical data
start_date = '2020-01-01'
end_date = datetime.now().strftime('%Y-%m-%d')
data_path = "Data/yf_data.pkl"

try:
    data = pd.read_pickle(data_path)
except FileNotFoundError:
    data = yf.download(tickers, start=start_date, end=end_date)
    data.to_pickle(data_path)
    print("Data downloaded and saved.")

# Convert to DataFrame and clean
df = pd.DataFrame(data)
df = df.dropna(axis=1)

# Extract closing prices
close_price = df['Close']

# Calculate daily returns
daily_returns = close_price.pct_change().dropna()

weights_df = pd.DataFrame({"Ticker": tickers, "Weight": 0.00})
user_weights = pd.read_csv("Data/user_weights.csv")
user_weights = user_weights[user_weights['Ticker'].isin(daily_returns.columns)]

weights = user_weights.set_index('Ticker').reindex(daily_returns.columns)['Weight'].fillna(0)
expected_returns = pd.DataFrame(daily_returns * weights)

if sum(user_weights['Weight']) > 1:
    print("Weight should not 1")
else:
    pass

# Risk calculation
cov_matrix = daily_returns.cov() * 252
variance = np.dot(weights.T, np.dot(cov_matrix, weights))
risk = np.sqrt(variance)

# === Maximum Return with User-Defined Risk Constraint ===

# User input for max risk
try:
    max_risk = float(input("Enter maximum annualized risk (e.g., 0.20 for 20%): "))
except ValueError:
    print("Invalid input. Using default risk = 0.20")
    max_risk = 0.20

# Prepare for optimization
mean_returns = daily_returns.mean() * 252
num_assets = len(daily_returns.columns)

# Objective function
def negative_portfolio_return(w, mean_returns):
    return -np.dot(w, mean_returns)

# Constraints
constraints = [
    {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
    {'type': 'ineq', 'fun': lambda w: max_risk - np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))}
]

# Optimization setup
init_guess = num_assets * [1. / num_assets]
bounds = tuple((0, 1) for _ in range(num_assets))

# Run optimizer
opt_result_max_ret_risk = so.minimize(negative_portfolio_return, init_guess,
                                      args=(mean_returns,),
                                      method='SLSQP', bounds=bounds,
                                      constraints=constraints)
# Display result
max_ret_risk_weights = pd.Series(opt_result_max_ret_risk.x, index=daily_returns.columns)
max_ret_risk_weights = max_ret_risk_weights * 100  # scale to percentage
max_ret_risk_weights = max_ret_risk_weights.round(10)
max_ret_risk_weights = max_ret_risk_weights[max_ret_risk_weights > 0]

print("Amount to invest in each stock:")
print(max_ret_risk_weights.sort_values(ascending=False))

