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