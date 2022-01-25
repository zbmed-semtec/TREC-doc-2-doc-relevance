# Sample size estimation
To accurately estimate the sample size requirement for doc-2-doc relevance.

## Description
 
The goal is to calculate the sample size for relevant documents. The documents have been categorized into three classes:
+ Definitely relevant
+ Partially relevant
+ Non-relevant

This approach uses a web based calculator to calculate the sample size. The statistical measurement used is the Kappa coefficient. The method of choice was Hypothesis testing method. For a bettter estimation, we group the Definitely relevant and partially relevant articles in the same category. 

## Steps

1. Selecting a method of calculation: Hypothesis Testing
2. Selecting parameters.
   1. Minimum acceptable kappa was set to be 0.6 (based on the reference article)
   2. Expected kappa values were tested for 0.6.0.7,0.8 based on the levels of agreement. A value of 0.8 was selected denoting a strong agreement
   3. Proportion of outcome was set to be 0.5 (accounting for 50% of either category)
   4. Significance level was set to be  0.05 following a Two-tailed hypothesis test
   5. Power was set to be 80%
   6. Expected dropout rate was set as 10% to account for less number of non-relevant articles.
   



## Links

[Reference article] (https://doi.org/10.21315/eimj2018.10.3.8)

[Web based Calculator] (https://wnarifin.github.io/ssc/sskappa.html)



