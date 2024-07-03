import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load data
df = pd.read_csv('Task 3 and 4_Loan_Data.csv')

# Drop the 'customer_id' column if it exists
if 'customer_id' in df.columns:
    df = df.drop(columns=['customer_id'])

# Feature and target separation
X = df.drop(columns=['default'])
y = df['default']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

#model = LogisticRegression()
#model.fit(X_train, y_train)

# Evaluate the model
#y_pred = model.predict(X_test)
#y_pred_prob = model.predict_proba(X_test)[:, 1]
#print(classification_report(y_test, y_pred))

# Train the model on the entire dataset
model = LogisticRegression()
model.fit(X_scaled, y)


# Define the function to calculate expected loss
def calculate_expected_loss(income, years_employed, credit_lines_outstanding, loan_amt_outstanding,
                            total_debt_outstanding, fico_score):
    input_data = pd.DataFrame(
        [[income, years_employed, credit_lines_outstanding, loan_amt_outstanding, total_debt_outstanding, fico_score]],
        columns=['income', 'years_employed', 'credit_lines_outstanding', 'loan_amt_outstanding',
                 'total_debt_outstanding', 'fico_score'])

    # Ensure the order of columns matches the training set
    input_data = input_data[X.columns]

    input_data_scaled = scaler.transform(input_data)
    PD = model.predict_proba(input_data_scaled)[:, 1][0]
    LGD = 0.90  # Loss Given Default (1 - recovery rate)
    EAD = loan_amt_outstanding  # Exposure at Default
    expected_loss = PD * LGD * EAD
    return expected_loss


# Example usage
income = 42000
years_employed = 4
credit_lines_outstanding = 2
loan_amt_outstanding = 20000
total_debt_outstanding = 10000
fico_score = 700

estd_loss = calculate_expected_loss(income, years_employed, credit_lines_outstanding, loan_amt_outstanding,
                             total_debt_outstanding, fico_score)
print(f"Expected Loss: ${estd_loss:.2f}")
