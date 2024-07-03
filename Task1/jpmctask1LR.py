import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import xgboost as xgb

df = pd.read_csv('Nat_Gas.csv', parse_dates=['Dates'])

# plt.scatter(df.Dates, df.Prices)
# plt.show()

# Interpolate missing daily prices
date_range = pd.date_range(start=df['Dates'].min(), end=df['Dates'].max(), freq='D')
df_full = df.set_index('Dates').reindex(date_range)
df_full['Prices'] = df_full['Prices'].interpolate()
df_full = df_full.reset_index().rename(columns={'index': 'Dates'})
df=df_full

# set index of the table to datetime column
df = df.set_index('Dates')
df.index=pd.to_datetime(df.index)


future_start_date = df.index.max() + pd.DateOffset(days=1)
future_end_date = future_start_date + pd.DateOffset(years=1) - pd.DateOffset(days=1)

future = pd.date_range(start=future_start_date, end=future_end_date, freq='D')

future_df = pd.DataFrame(index=future)
future_df['isFuture'] = True
df['isFuture'] = False
df_and_future = pd.concat([df, future_df])

#print(df_and_future)


Y_train=[]
X_train1=np.array([1,2,3]).reshape(-1,1)
X_train2=np.array([1,2,3,4]).reshape(-1,1)
model = LinearRegression()
# Get the last 4 years of data
for i, date in enumerate(future):
    Y_train.append([])
    if ((date-pd.DateOffset(years=4))>=pd.to_datetime('2020-10-31')):
        Y_train[i].append(df.loc[date - pd.DateOffset(years=4), 'Prices'])
    Y_train[i].append(df.loc[date-pd.DateOffset(years=3),'Prices'])
    Y_train[i].append(df.loc[date-pd.DateOffset(years=2), 'Prices'])
    Y_train[i].append(df.loc[date-pd.DateOffset(years=1), 'Prices'])

    if(len(Y_train[i])==3):
        model.fit(X_train1,Y_train[i])
        df_and_future.loc[date,'Prices'] = 4*model.coef_ +model.intercept_
    if (len(Y_train[i]) == 4):
        model.fit(X_train2, Y_train[i])
        df_and_future.loc[date,'Prices'] = 5*model.coef_ +model.intercept_





#print(df_and_future)


data_all = df_and_future.loc[df_and_future.index <= '09/30/2025']

fig, ax = plt.subplots(figsize=(15, 5))
data_all.plot(ax=ax, label='Training Set')
#plt.show()

#specific_date = pd.to_datetime(input())  # your specific date

#price_on_specific_date = df_and_future.loc[specific_date, 'Prices']
#print(price_on_specific_date)

def calculate_contract_value(injection_dates, withdrawal_dates, injection_rates, withdrawal_rates, max_storage, storage_costs, prices_df):
    # Initialize variables
    storage_volume = 0
    total_value = 0
    storage_cost_total = 0

    # Convert dates to datetime
    injection_dates = pd.to_datetime(injection_dates)
    withdrawal_dates = pd.to_datetime(withdrawal_dates)

    # Iterate over each day in the prices_df to simulate the storage and cash flow
    for date in prices_df.index:
        # Handle injection
        if date in injection_dates:
            idx = injection_dates.get_loc(date)
            injection_rate = injection_rates[idx]
            price_at_injection = prices_df.loc[date, 'Prices']
            volume_to_inject = min(injection_rate, max_storage - storage_volume)
            storage_volume += volume_to_inject
            total_value -= volume_to_inject * price_at_injection
            total_value -= injection_rate

        # Handle withdrawal
        if date in withdrawal_dates:
            idx = withdrawal_dates.get_loc(date)
            withdrawal_rate = withdrawal_rates[idx]
            price_at_withdrawal = prices_df.loc[date, 'Prices']
            volume_to_withdraw = min(withdrawal_rate, storage_volume)
            storage_volume -= volume_to_withdraw
            total_value += volume_to_withdraw * price_at_withdrawal
            total_value -= withdrawal_rate

        # Calculate daily storage costs
        daily_storage_cost = storage_costs * storage_volume
        storage_cost_total += daily_storage_cost

    # Subtract total storage costs from total value
    total_value -= storage_cost_total

    return total_value

prices_df = df_and_future
injection_dates = ['2024-06-01', '2024-07-01']
withdrawal_dates = ['2025-01-01', '2025-02-01']
injection_rates = [.1, .1]  # units per day
withdrawal_rates = [.1, .1]  # units per day
max_storage = 10  # maximum storage volume
storage_costs = 0.01  # cost per unit per day

contract_value = calculate_contract_value(injection_dates, withdrawal_dates, injection_rates, withdrawal_rates, max_storage, storage_costs, prices_df)
print(contract_value)