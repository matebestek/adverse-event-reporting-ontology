import csv
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as pl
from sklearn.metrics import roc_curve, auc
import math


#we load the gold standard from the FDA
dictGoldStandard = {}
with open('/Users/mcourtot/Desktop/VAERS/VAERSCosine/ReproduceBotsisBrightonResults/VAERSGoldStandardCSV.csv','rU') as fp:
    reader = csv.reader(fp)
    for row in reader:
        dictGoldStandard[int(row[0])] = row[1]


#we load the ontology classification
#this file contains only posiitve cases, so we set the outcome to '1'
dictOntologyClassification = {}
with open('/Users/mcourtot/Desktop/SVN/melanie/docs/phd/Results/VAERSOntologyClassificationResults.csv','rU') as fp:
    reader = csv.reader(fp)
    for row in reader:
        dictOntologyClassification[int(row[0])] = '1'


def buildVectorsTruePred(dictGoldStandard, dictOntologyClassification):
    #initialize y_pred, y_true
    y_true = []
    y_pred = []
    with open('ResultsOntologyClassification.csv', 'wb') as csvfile:
        resultswriter = csv.writer(csvfile,delimiter=',')
        resultswriter.writerow(['VAERSID','GoldStandard','OntologyClassification'])
    #Now we need to build y_true and y-pred for different threshold values
    # for each VAERS_ID, we will get the true outcome form the dictGoldStandard, then the predicted outcome from the dictCosineValues (if dictCosineValues[VAERS_ID]> threshold, then add 1 to y_pred. Else add 0)


        for VAERSID in dictGoldStandard:
            #print VAERSID, 'corresponds to', dictGoldStandard[VAERSID] # should give 377955 corresponds to 0, 377958 corresponds to 1
            y_true.append(int(dictGoldStandard[VAERSID]))
            if VAERSID in dictOntologyClassification:
                y_pred.append(1) #if present in the positive file, add 1
                resultswriter.writerow([VAERSID,int(dictGoldStandard[VAERSID]),1])
            else:
                y_pred.append(0) # if not present in the positive file, add 0
                resultswriter.writerow([VAERSID,int(dictGoldStandard[VAERSID]),0])
    return y_true,y_pred
        


y_true, y_pred = buildVectorsTruePred(dictGoldStandard, dictOntologyClassification)
print len(y_true) #should give 6032 as we have 6032 records
print len(y_pred) #should give 6032 as we have 6032 records


#print y_pred

##     #get the f-measure
#print "f1score: ", metrics.f1_score(y_true, y_pred)
cfm = confusion_matrix(y_true, y_pred)
print cfm
##     #print cfm[1,1]
tpr = float(cfm[1,1])/float(237)
##     #print tpr
fpr = float(cfm[0,1])/float(5795)

print "tpr: ", tpr
print "fpr: ", fpr



print "false positive: ", cfm[0,1]
print "true negative: ", cfm[0,0]
print "false negative: ", cfm[1,0]
print "true positive: ", cfm[1,1]


fpr, tpr, thresholds =  metrics.roc_curve(y_true,y_pred, pos_label=1)

roc_auc = auc(fpr, tpr)
print("Area under the ROC curve : %f" % roc_auc)
