M <- read.csv(file="./Sorted_R_VAERSMedDRATermsSMQContingencyCosineValues.csv", head=TRUE, sep=",")

pred<-M$MelanieClassification
#saves column "MelanieClassification" of "M" data.frame as vector named "pred"

ref <- M$VAERSManualClassification
#saves column "VAERSManualClassification" of "M" data.frame as vector named "ref"

#note: to use the pROC library the score column needs to be ordered.

library(pROC)
#Type 'citation("pROC")' for a citation.

roc(ref,pred)




rocobj <- roc(ref,pred)

# gives us the CI of the AUC
aucCI <- ci(rocobj, of="auc")
#output : 95% CI: 0.9467-0.9695 (DeLong)



# gives us the best threshold using the chosen methods (here we want to use Youden and the closest euclidean distance from the top left point
bestCoord <- coords(rocobj, x=c("best"), input=c("threshold", "specificity","sensitivity"), ret=c("threshold", "specificity", "sensitivity"),as.list=FALSE, drop=TRUE, best.method=c("youden", "closest.topleft"))
 
#output:   threshold specificity sensitivity 
#		   0.0594979   0.8769629   0.9240506 
  
#gives us the CI at the specified threshold value
ciThres <- ci.thresholds(ref, pred, boot.n=2000, conf.level=0.95, stratified=TRUE,thresholds=c(0.0594979))
 
#output: 95% CI (2000 stratified bootstrap replicates):
# thresholds sp.low sp.median sp.high se.low se.median se.high
#  0.0594979 0.8685     0.877  0.8851 0.8861    0.9241  0.9536



#Can be used to draw the CI shape if desired.
#plot(x = roc(ref, pred, percent = TRUE, ci = TRUE, of = "se", sp = seq(0, 100, 5)), ci.type="shape")

#output:
#Call:
#roc.default(response = ref, predictor = pred, percent = TRUE,     ci = TRUE, of = "se", sp = seq(0, 100, 5))

#Data: pred in 5795 controls (ref 0) < 237 cases (ref 1).
#Area under the curve: 95.81%
#95% CI (2000 stratified bootstrap replicates):
#  sp se.low se.median se.high
#   0 100.00   100.000  100.00
#   5 100.00   100.000  100.00
#  10 100.00   100.000  100.00
#  15 100.00   100.000  100.00
#  20 100.00   100.000  100.00
#  25 100.00   100.000  100.00
#  30 100.00   100.000  100.00
#  35  98.73    99.580  100.00
#  40  97.89    99.160  100.00
#  45  97.89    99.160  100.00
#  50  97.46    98.730  100.00
#  55  97.05    98.730  100.00
#  60  97.05    98.730  100.00
#  65  96.20    97.890   99.58
#  70  96.20    97.890   99.58
#  75  94.94    97.050   99.16
#  80  91.56    94.940   97.47
# 85  90.30    93.670   96.62
#  90  83.54    88.190   92.41
#  95  72.57    78.060   83.97
# 100   2.11     4.641   10.13

