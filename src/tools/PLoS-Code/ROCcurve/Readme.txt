This folder contains the code to explore the statistics of the ROC curves.

- OntologyClassification.py
	This file takes in the VAERS Gold standard csv file as well as the output of the ontology classification csv file. 

- ResultsOntologyClassification.csv 
	This is the output of the classification as queried from the triplestore (queries are in SPARQLqueries.txt) Note that we retrieve only positive cases here. 

- ROCcurve.R
	This is the R code that allows to draw the ROC curve for the expanded MedDRA SMQ case. In this file you will find more comments as well as outputs expected

- ROCcurveOntologyClassifictaion.R
	Same as the above, but for the ontology classification case. This file as been kept separate to clearly show the outputs of the R functions.

- Sorted_R_VAERSMedDRATermsSMQContingencyCosineValues.csv
	The input for the file ROCcurve.R. As mentioned in the R file, we need to numerically sort the score values to apss as input to the roc function from pROC.

- SPARQLqueries.txt
	The SPARQL queries that were run against the triplestore. Their output was manually copied into the ResultsOntologyClassification.csv file.

	