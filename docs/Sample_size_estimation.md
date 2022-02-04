# Sample size estimation
To accurately estimate the sample size requirement for doc-2-doc relevance.

## Description
 
The goal is to calculate the sample size for relevant documents. The documents have been categorized into three classes:
+ Definitely relevant
+ Partially relevant
+ Non-relevant

This approach uses a [web based calculator](https://wnarifin.github.io/ssc/sskappa.html) to calculate the sample size . The statistical measurement used is the Kappa coefficient. The method of choice is the Hypothesis testing method. For a better estimation, we group the Definitely relevant and Partially relevant articles in the same category. 

## Steps

1. Selecting a method of calculation: Hypothesis Testing
2. Selecting parameters:
   1. Minimum acceptable Kappa was set to be 0.6 (based on the [reference article](https://doi.org/10.21315/eimj2018.10.3.8)).
   2. Expected Kappa values were tested for 0.6, 0.7, 0.8 based on the levels of agreement. A value of 0.8 was selected denoting a strong agreement.
   3. Proportion of outcome was set to be 0.5 (accounting for 50% of either category, in our case, Definitely relevant and Partially relevant).
   4. Significance level was set to be  0.05 following a Two-tailed hypothesis test.
   5. Power was set to be 80% to account for the standard error based on the [conventional level of power](http://www.stat.columbia.edu/~gelman/stuff_for_blog/chap20.pdf).
   6. Expected dropout rate was set as 10% to account for less number of possible dropouts and invalid cases (in our case, articles being Non-Relevant).
3. Resulting parameters:
   1. Sample size (n) : The evaluable sample size of the articles.
   2. Sample size (n<sub>drop</sub>) : Total number of articles that should be assessed in order to obtain n evaluable articles.





