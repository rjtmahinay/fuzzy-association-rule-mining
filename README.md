# Learning of High Dengue Incidence with Clustering and FP-Growth Algorithm using WHO Historical Data

*This is an accepted paper at the 3rd IEEE International Conference on Agents (ICA 2018)*

## Abstract
This paper applies FP-Growth algorithm in mining fuzzy association rules for a prediction system of dengue. The system mines its rules through input of historic predictor variables for dengue. The rules will be used to build a rule-based classifier to predict the dengue incidence for the next month for the years 2001-2006 in the Philippines. The FP-Growth Algorithm was compared to Apriori Algorithm by Sensitivity, Specificity, PPV, NPV, execution time and memory usage. The results showed that FP-Growth Algorithm is significantly better in execution time, numerically better in memory and comparable in Sensitivity, Specificity PPV and NPV to Apriori Algorithm.

## Instructions
1. CREATE Tables (FFSD_TestData2, FFSD_TrainingData2,PPSD_TrainingData2,PPSD_TestData2)
   edit tablename in code below
   ```
    CREATE TABLE [dbo].TABLENAME(
        [region] [varchar](1000) NOT NULL,
        [month_no] [varchar](1000) NOT NULL,
        [popdensity] [varchar](1000) NOT NULL,
        [ssta] [varchar](1000) NOT NULL,
        [soi] [varchar](1000) NOT NULL,
        [typhoon_distance] [varchar](1000) NOT NULL,
        [typhoon_wind] [varchar](1000) NOT NULL,
        [rainfall] [varchar](1000) NOT NULL,
        [poverty] [varchar](1000) NOT NULL,
        [ndvi] [varchar](1000) NOT NULL,
        [evi] [varchar](1000) NOT NULL,
        [daily_temp] [varchar](1000) NOT NULL,
        [nightly_temp] [varchar](1000) NOT NULL,
        [polstab] [varchar](1000) NOT NULL,
        [dengue] [varchar](1000) NOT NULL,
        [dengue_next] [varchar](1000) NOT NULL
    ) ON [PRIMARY] 
    GO
	```
2. Import CSV Files<br />
Right click database ThesisSampleDB 
-> Tasks -> Import Data -> Source = Flat File Source
-> SQL Server Client 11.0 or 10.0 for destination  -> Map to table PPSD_TrainingData

3. Create Table FP_Rules and Apriori_Rules2
    ```
    CREATE TABLE [dbo].[FP_Rules](
	    [Antecedent] [varchar](1000) NOT NULL,
	    [Consequent] [varchar](1000) NOT NULL,
	    [Confidence] [float] NOT NULL,
	    [Num_Antecedent] [int] NULL
    ) ON [PRIMARY]
    GO
    ```
    ```
    CREATE TABLE [dbo].[Apriori_Rules2](
	    [Antecedent] [varchar](1000) NOT NULL,
	    [Consequent] [varchar](1000) NOT NULL,
	    [Confidence] [float] NOT NULL,
	    [Num_Antecedent] [int] NULL,
	    [Lift] [float] NOT NULL
    ) ON [PRIMARY]
    ```
## Authors
*  [**Reynaldo John Tristan Mahinay Jr.**](https://github.com/rjtmahinay)
* **Franz Stewart Dizon**
* [**Stephen Kyle Farinas**](https://github.com/kfpyzi)
* **Harry Pardo**
* **Cecil Jose Delfinado (Advisor)**

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

