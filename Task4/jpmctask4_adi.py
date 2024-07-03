import numpy as np
import pandas as pd
import math

df = pd.read_csv('Task 3 and 4_Loan_Data.csv')

df = df.sort_values(by='fico_score').reset_index(drop=True)
df['prefix'] = df['default'].cumsum()

# we will divide into 10 total buckets
# the first 5 buckets will be for fico scores ranging from 300-600, call these B5, B4, B3, B2, B1
# the second 5 buckets will be for fico scores ranging from 600-850, call these A5, A4, A3, A2, A1

def log_likelihood(b1, b2, b3, b4, ub):
    LL = 0
    boundaries = [b1, b2, b3, b4, ub]
    previous_idx = None

    for boundary in boundaries:
        filtered_df = df[df['fico_score'] > boundary]
        if filtered_df.empty:
            continue

        closest_value = filtered_df['fico_score'].min()
        idx = filtered_df[filtered_df['fico_score'] == closest_value].index[0]

        if previous_idx is not None and idx == previous_idx:
            continue

        if previous_idx is None:
            log_value = df.at[idx, 'prefix'] / (idx + 1)  # Adding 1 to avoid division by zero
            n = idx + 1
        else:
            interval = idx - previous_idx
            if interval == 0:
                continue
            log_value = df.at[idx, 'prefix'] / interval
            n = interval

        #print(f"Boundary: {boundary}, idx: {idx}, previous_idx: {previous_idx}, log_value: {log_value}, LL: {LL}")

        if 0 < log_value < 1:
            LL += df.at[idx, 'prefix'] * math.log(log_value) + ((n - df.at[idx, 'prefix']) * math.log(1 - log_value))
        else:
            LL += 0

        previous_idx = idx

    return LL

# we will make buckets multiples of 25

# 300-600 bucket
B = [300, 0, 0, 0, 0, 600]
A = [600, 0, 0, 0, 0, 850]

llb = -1e9
for a in range(325, 501, 25):
    for b in range(a + 25, 526, 25):
        for c in range(b + 25, 551, 25):
            for d in range(c + 25, 576, 25):
                temp = llb
                llb = log_likelihood(a, b, c, d, 600)
                if llb > temp:
                    B[1] = a
                    B[2] = b
                    B[3] = c
                    B[4] = d

lla = -1e9
for a in range(625, 751, 25):
    for b in range(a + 25, 776, 25):
        for c in range(b + 25, 801, 25):
            for d in range(c + 25, 826, 25):
                temp = lla
                lla = log_likelihood(a, b, c, d, 850)
                if lla > temp:
                    A[1] = a
                    A[2] = b
                    A[3] = c
                    A[4] = d

print(B)
print(A)
