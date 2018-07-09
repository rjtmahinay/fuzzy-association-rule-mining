# Results
The materials used to perform this comparison is a desktop with Intel Core i7 Processor and SSD.
<p align="center">
<img src="https://github.com/rjtmahinay/learning-of-high-dengue-incidence/blob/master/results/exec_memory.jpg">
</p>

**<p align="center">Fig 1. Execution Time and Memory Usage</p>**

In Fig 1, the execution time of FP-Growth Algorithm was significantly better than Apriori Algorithm when treated with P-value method. To compare the memory, we used a profiler to see its consumption for generation of frequent itemset and association rules.
<p align="center">
<img src="https://github.com/rjtmahinay/learning-of-high-dengue-incidence/blob/master/results/accuracy1.jpg">
</p>

**<p align="center">Fig 2. PPV, NPV and Specificity</p>**

In PPV and NPV, the result of signifance testing is FP-Growth is insignifanctly lower than Apriori using z-test for two proportions. The result for Specificity is the same so no significant difference.
<p align="center">
<img src="https://github.com/rjtmahinay/learning-of-high-dengue-incidence/blob/master/results/accuracy2.jpg">
</p>

**<p align="center">Fig 3. F1-score and Sensitivity</p>**

Using z-test for two proportions, there is no significant difference in Sensitivity. The F1-score was used to balance the Sensitivity and PPV of the algorithms obtaining the result in Fig 3.