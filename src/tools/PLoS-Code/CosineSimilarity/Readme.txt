This folder contains code allowing to reproduce the results obtained by Botsis et al., and described in the paper "Application of information retrieval approaches to case classification in the vaccine adverse event reporting system.", Drug Saf. 2013 Jul;36(7):573-82. doi: 10.1007/s40264-013-0064-4.
It also allows to use the same code to compute the ROC curve for the proposed expanded SMQ query.


We export the Brighton terms from the database, and use the python script

python cosine.py > results.txt

in python_code. 
The script will read in the values from VAERSMedDRATermsSMQCosineValues.csv and for each VAERS ID will collect the corresponding MedDRA labels from the database. You can create a local database by loading the included VAERSDATA.sql file. Note that the script assumes you are running MySQL, and the table is contained in a database named "H1N1Classification". You should also load the table4.sql file, which contains the mapping between the MedDRA terms and the Brighton terms.

Those parameters can be updated in the script at the line 74:
	listMedDRANames =  getMedDRANamesforeachEventID("H1N1Classification", "VAERSDATA", VAERSID)
The script will output the file "results.txt" which is the corresponding list of all cosine values.


Same script can be adapted to reproduce results using the Brighton terms: you will need use VAERSBrightonTermsTotal.csv as input and modify the script.

This folder contains:

1) Code
- cosine.py
	This scripts computes the cosine similarity values
- computeROC.py
	Reads the result of the cosine computation and compute the ROC curve. As is, it will take the VAERSMedDRATermsSMQContingencyCosineValues.csv as input (i.e., the cosine values for our expanded query), and build the ROC curve. It will also display FPR, TPR etc for the best threshold value (identified as threshold = 0.059528811 in the file ROCcutoff.txt. 
- utils.py
	Helper functions, such as database connection



2) Files
- VAERSGoldStandardCSV.csv
	The reference classification as manually curated by the FDA
- VAERSBrightonTermsCosineValues.csv
	The computed cosine values when comparing vectors build based on the Brighton guidelines and aligning it with the Brighton terms from each report (Brighton terms are obtained after applying the MedDRA to Brighton mapping)	
- VAERSMedDRATermsSMQCosineValues.csv
	The computed cosine values when comparing vectors build based on the MedDRA SMQ and aligning it with the MedDRA terms from each report
- VAERSBrightonTermsTotal.csv
	The exported Brighton terms from the database
- VAERSMedDRATermsSMQContingencyCosineValues.csv
	The computed cosine values for the expanded MedDRA query (SMQ + terms from the contingency tables)
- ROCcutoff.txt
	The values thereshold, cutoff, fpr and tpr for each poin of the ROC curve.The best cutoff is the shortest Euclidean distance between the top left corner of the ROC curve and each point on the curve, conputed as square root of ((1-sensitivity)^2+(1-specificity)^2)