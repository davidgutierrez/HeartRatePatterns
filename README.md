# HeartRatePatterns
This work focuses on predictive mortality analysis, through the identification of patterns in heart beats of patients in the intensive care unit (ICU).

As a data source, MIMIC III is used, where the patient information is found in the ICU, these data are transformed into graphs, later the possible patterns of beats are located between all the patients, through the frequent graph mining, reduce these patterns using Non-Negative Matrix Factorization (MFN) and group the patients by their characteristics. In the end, using logistic regression identifies the probability that each of these groups of patients have to die. 

For more info see the [Wiki](https://github.com/davidgutierrez/HeartRatePatterns/wiki)
