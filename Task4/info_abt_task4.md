# Task 4
This was probably the hardest one, not because it was hard to come up with an algorithm, but rather debugging it. It took me quite a while before I could make the code relatively elegant and readable, it was a huge mess before that <br/>

In this task, borrowers were supposed to be divided into various buckets based on their FICO scores. I used a Dynamic Programming Approach to maximise the log liklihood of each bucket

After sorting the loaners based on their FICO scores, I added a prefix sum column to make it easy to calculate the number of defaulters in each bucket. 

The code divides all FICO scores into 2 ranges, 300-600 & 600-850, with both of these ranges being split into 5 buckets. For simplicity I kept the bucket widths divisible by 25, but this can easily be modified as per ones liking.
