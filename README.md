# Learning of High Dengue Incidence with Clustering and FP-Growth Algorithm using WHO Historical Data

*This is an accepted paper at the 3rd IEEE International Conference on Agents (ICA 2018)*

## Abstract
This paper applies FP-Growth algorithm in mining fuzzy association rules for a prediction system of dengue. The system mines its rules through input of historic predictor variables for dengue. The rules will be used to build a rule-based classifier to predict the dengue incidence for the next month for the years 2001-2006 in the Philippines. The FP-Growth Algorithm was compared to Apriori Algorithm by Sensitivity, Specificity, PPV, NPV, execution time and memory usage. The results showed that FP-Growth Algorithm is significantly better in execution time, numerically better in memory and comparable in Sensitivity, Specificity PPV and NPV to Apriori Algorithm.

## Rule Mining Usage

The following default values were used in this research based on the data:

Support: 0.014 <br />
Confidence: 0.9

### Apriori Algorithm
Generate association rules
```
rules = Apriori.generate_itemsets_rules(data, support, confidence, lift)
```
Print association rules
```
print_result(rules)
```

### FP-Growth Algorithm
Generate association rules
```
rules = FPGrowth.generate_patterns_rules(data, support, confidence)
```
Print association rules
```
print_result(rules)
```

## Authors
*  [**Reynaldo John Tristan Mahinay Jr.**](https://github.com/rjtmahinay)
* **Franz Stewart Dizon**
* [**Stephen Kyle Farinas**](https://github.com/kfpyzi)
* **Harry Pardo**

## Results
The results are showed in this link - [Comparison Result](https://github.com/rjtmahinay/learning-of-high-dengue-incidence/tree/master/results)
## License

    Copyright (c) 2018 Reynaldo John Tristan Mahinay Jr., Franz Stewart Dizon, Stephen Kyle Farinas and Harry Pardo

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

