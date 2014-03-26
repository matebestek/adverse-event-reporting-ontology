import csv
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as pl
from sklearn.metrics import roc_curve, auc
import math


def confusion_table(cfm, label):
    """Returns a confusion table in the following format:
    [[true positives, false negatives],
    [false positives, true negatives]]
    for the given label index in the confusion matrix.
    """
    predicted = cfm[label]
    actual = [cfm[i][label] for i in range(len(cfm))]
    true_pos = predicted[label]
    false_pos = sum(actual) - true_pos
    false_neg = sum(predicted) - true_pos
    total = sum([sum(i) for i in cfm])
    true_neg = total - true_pos - false_pos - false_neg
 
    return [[true_pos, false_neg],
              [false_pos, true_neg]]

#we load the cosine values in a dict of the form dict[VAERS_ID] = cosineValue
dictCosineValues = {}
with open('./VAERSMedDRATermsSMQContingencyCosineValues.csv','rU') as fp:
    reader = csv.reader(fp)
    for row in reader:
        dictCosineValues[int(row[0])] = row[1]


#we can access each cosineValue by its dict[key], i.e., the corresponding VAERS_ID
#print dictCosineValues[368075]     #should give 0.173731547


#we load the gold standard from the FDA
dictGoldStandard = {}
with open('./VAERSGoldStandardCSV.csv','rU') as fp:
    reader = csv.reader(fp)
    for row in reader:
        dictGoldStandard[int(row[0])] = row[1]

#we can access each standard outcome by it's dict[key], i.e., the corresponding VAERS_ID
#print dictGoldStandard[368075]     # should give 0
#print dictGoldStandard[375607]     # should give 1

def buildVectorsTruePred(dictGoldStandard, dictCosineValues, threshold):
#Now we need to build y_true and y-pred for different threshold values
# for each VAERS_ID, we will get the true outcome form the dictGoldStandard, then the predicted outcome from the dictCosineValues (if dictCosineValues[VAERS_ID]> threshold, then add 1 to y_pred. Else add 0)

    #initialize y_pred, y_true
    y_true = []
    y_pred = []


    for VAERSID in dictGoldStandard:
        #print VAERSID, 'corresponds to', dictGoldStandard[VAERSID] # should give 377955 corresponds to 0, 377958 corresponds to 1
        y_true.append(int(dictGoldStandard[VAERSID]))
        if VAERSID in dictCosineValues:
            predCosineValue = float(dictCosineValues[VAERSID])
            if predCosineValue > threshold:
                y_pred.append(1) #if above the threshold, add 1 to y_pred
            else:
                y_pred.append(0) # if under the threshold, the add 0 to y-pred
        else: #VAERS_ID is not in dictCosineValues (there was no relevant Brighton term on that report)
            y_pred.append(0)

    return y_true,y_pred



#choose a threshold
#threshold = 0.3
## tpr_list = []
## fpr_list = []
## #for cosine values between 0 and 1, increment threshold by 0.01 and compute f-measure for each
## for threshold in [float(j) / 100 for j in range(0, 100, 1)]:
##     y_true, y_pred = buildVectorsTruePred(dictGoldStandard, dictCosineValues, threshold)
##     #print len(y_true) #should give 6032 as we have 6032 records
##     #print len(y_pred) #should give 6032 as we have 6032 records
##     #get the f-measure
##     #print threshold,", ", metrics.f1_score(y_true, y_pred)
##     cfm = confusion_matrix(y_true, y_pred)
##     #print cfm[1,1]
##     tpr = float(cfm[1,1])/float(237)
##     #print tpr
##     fpr = float(cfm[0,1])/float(5795)
##     tpr_list.append(tpr)
##     fpr_list.append(fpr)

#print tpr_list
#pl.plot(fpr_list,tpr_list)
#pl.show()


#initialize y_pred, y_true
y_true = []
y_pred = []


for VAERSID in dictGoldStandard:
    #print VAERSID, 'corresponds to', dictGoldStandard[VAERSID] # should give 377955 corresponds to 0, 377958 corresponds to 1
    y_true.append(int(dictGoldStandard[VAERSID]))
    if VAERSID in dictCosineValues:
        ###print (dictCosineValues[VAERSID])
        predCosineValue = float(dictCosineValues[VAERSID])
        y_pred.append(predCosineValue)
    else: #VAERS_ID is not in dictCosineValues (there was no relevant Brighton term on that report)
        y_pred.append(0)

###print y_true


#for value in y_pred:
#    print value

## # Compute best threshold
## roc_array = []

fpr, tpr, thresholds =  metrics.roc_curve(y_true,y_pred, pos_label=1)


## for i in range(0, len(thresholds)):
##     roc_cutoff = math.sqrt((1-tpr[i])**2+(fpr[i]**2))
##     print "threshold: ", thresholds[i], ",cutoff: ", roc_cutoff,  ",fpr: ", fpr[i], ",tpr: ", tpr[i]



    
roc_auc = auc(fpr, tpr)
print("Area under the ROC curve : %f" % roc_auc)




#Plot ROC curve
pl.clf()
fig = pl.figure()
fig.patch.set_facecolor('white')

pl.plot(fpr, tpr, label='ROC curve (area = %0.3f)' % roc_auc, )
pl.plot([0, 1], [0, 1], 'k--')
pl.xlim([0.0, 1.0])
pl.ylim([0.0, 1.0])
pl.xlabel('1-Specificity (FPR)')
pl.ylabel('Sensitivity (TPR)')
#pl.title('Receiver operating characteristic MedDRA SMQ + contingency tables terms')
pl.legend(loc="lower right")
pl.grid(True)
pl.show()

#fig.savefig('ROCcurve.png', facecolor=fig.get_facecolor(), edgecolor='none')



#best cutoff
threshold = 0.059528811
y_true_best, y_pred_best = buildVectorsTruePred(dictGoldStandard, dictCosineValues, threshold)

print classification_report(y_true_best, y_pred_best)

print "precision: ", metrics.precision_score(y_true_best, y_pred_best)
print "recall: ", metrics.recall_score(y_true_best, y_pred_best)
cfm = confusion_matrix(y_true_best, y_pred_best)



print "false positive: ", cfm[0,1]
print "true negative: ", cfm[0,0]
print "false negative: ", cfm[1,0]
print "true positive: ", cfm[1,1]

## #print cfm
## #print confusion_table(cfm,0)


## #pl.matshow(cfm)
## #pl.title('Confusion matrix')
## #pl.colorbar()
## #pl.ylabel('True label')
## #pl.xlabel('Predicted label')
## #pl.show()
