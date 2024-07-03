# Task 3
In this task, given some info about loan borrowers, we were expected to predict their probability of default. <br/>

This was fairly simple as it required a simple logistic regression, which gave results with remarkable accuracy.

I've commented out the lines of code for the train test split, this code will take any input values and predict the expected loss <br/>

'y_pred_prob = model.predict_proba(X_test)[:, 1]' - This is the line of code that gives default probability (we denote a default on a loan as 1, otherwise 0)
