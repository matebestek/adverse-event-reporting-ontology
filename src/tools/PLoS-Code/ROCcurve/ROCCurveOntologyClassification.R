

M <- read.csv(file="./ResultsOntologyClassification.csv", head=TRUE, sep=",")

pred<-M$OntologyClassification
#saves column "MelanieClassification" of "M" data.frame as vector named "pred"

ref <- M$GoldStandard
#saves column "VAERSManualClassification" of "M" data.frame as vector named "ref"

#note: to use the pROC library the score column needs to be ordered.

library(pROC)
#Type 'citation("pROC")' for a citation.

roc(ref,pred)

#output: Call:
#roc.default(response = ref, predictor = pred)

#Data: pred in 5795 controls (ref 0) < 237 cases (ref 1).
#Area under the curve: 0.7703


rocobj <- roc(ref,pred)

# gives us the CI of the AUC
ci(rocobj, of="auc")
#output : 95% CI: 0.7386-0.8019 (DeLong)



# gives us the best threshold using the chosen methods (here we want to use Youden and the closest euclidean distance from the top left point
bestCoords = coords(rocobj, x=c("best"), input=c("threshold", "specificity","sensitivity"), ret=c("threshold", "specificity", "sensitivity"),as.list=FALSE, drop=TRUE, best.method=c("youden", "closest.topleft"))
 
# output threshold specificity sensitivity 
#  0.5000000   0.9666954   0.5738397 
  
#gives us the CI at the specified threshold value
ciThres = ci.thresholds(ref, pred, boot.n=2000, conf.level=0.95, stratified=TRUE,thresholds=c(0.05000000))
 
#output: 95% CI (2000 stratified bootstrap replicates):
# thresholds sp.low sp.median sp.high se.low se.median se.high
#       0.05  0.962    0.9667   0.971 0.5105    0.5738  0.6371