In this folder you will find:

- ListMedDRATermsAndOutcome.csv
	A CSV file containing the outcome (positive or negative for Anaphylaxis) as identified by the manual curators @FDA, as well as the corresponding VAERS ID and the list of MedDRA terms associated with them
	
- runAllSymptoms.R
	A R script that take the ListMedDRATermsAndOutcome.csv spreadsheet as input, and build the contingency table for each MedDRA term. It outputs three measures: the chi-square value, the p-value and the odd-ratios value
	
- symptomsSignificance.csv
	The output of the R script. It is a CSV file with three columns corresponding to the three values chi-square value, the p-value and the odd-ratios value
	
	
	
	