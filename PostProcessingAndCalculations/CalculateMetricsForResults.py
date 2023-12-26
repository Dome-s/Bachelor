import os
import time
import pandas
import csv
import json
import threading
import argparse
from itertools import groupby
import MetricCalculation as mc
# /assays = chEMBL data , chemical database
# /Prospect = TCP-DI dataset "focuses on data integration"
# /Wikidata = singers from the us wikidata formated
# /DeepMDataset (not seperated into unionable etc...) = Magellan Data  contains dataset pairs collected from real-world data and curated mainly for Entity Matching techniques
# /Miller2 This dataset consists of tables from Canada, USA and UK Open Data, provided to us by the authors of [8] for their dataset discovery techniques.

results = 'C:/Users/dominic/Desktop/Bachelor/PostProcessingAndCalculations/combinedResults/'
Metricresults = 'C:/Users/dominic/Desktop/Bachelor/PostProcessingAndCalculations/CalculatedMetrics/'


S_l = 0  #elements in smaller schema
S_L = 0  # elements in larger schema
E = 0 # matches in ground truth
M = 0 # discovered Matches
R = 0 # number of correctly discovered Matches
class FileResultData:
    def __init__(self,File,Matcher, TruePositive, TrueNegative,FalsePositive,FalseNegative,S_l,S_L,E,M,R):
        self.File = File
        self.Matcher = Matcher
        self.TruePositive = TruePositive
        self.TrueNegative = TrueNegative
        self.FalsePositive = FalsePositive
        self.FalseNegative = FalseNegative
        self.S_l = S_l
        self.S_L = S_L
        self.E = E
        self.M = M
        self.R = R

class base:
     def __init__(self,TruePositive, TrueNegative,FalsePositive,FalseNegative):
        self.TruePositive = TruePositive
        self.TrueNegative = TrueNegative
        self.FalsePositive = FalsePositive
        self.FalseNegative = FalseNegative

fileResults = list()
baseData = dict()

def main():
    extractResultData(0)
    print("calculating Metrics")
    fileResults.sort(key= lambda elem: elem.File)
    with open(Metricresults+"CalculatedResultsIndividualThresholds.csv",'w',newline='') as f: 
        w = csv.writer(f)    
        w.writerow(['File','Matcher','Precision','Recall','F1','NUI','PME','HSR']) 
        for res in fileResults:
            precision = mc.precision(res.TruePositive,res.FalseNegative)
            recall = mc.recall(res.TruePositive,res.FalsePositive)
            f1 = mc.f1(res.TruePositive,res.FalseNegative,res.FalsePositive)
            nui = mc.nui(res.S_l,res.S_L,res.E,res.M,res.R)
            pme = mc.pme(res.S_l,res.S_L,res.E,res.M,res.R)
            hsr = mc.hsr(res.S_l,res.S_L,res.E,res.M,res.R)
            w.writerow([res.File,res.Matcher,float(precision),float(recall),float(f1),float(nui),float(pme),float(hsr)]) 
    print("finished Calculating Metrics")
            
                    


                
            

def evaluateRow(matcher,result,truth,threshold = 0):
    truePositive = result > threshold and truth > threshold 
    falsePositive = result > threshold and truth <= threshold
    trueNegative = result <= threshold and truth <= threshold 
    falseNegative = result <= threshold and truth > threshold 

    if(truePositive):
        baseData[matcher].TruePositive += 1
    if(falsePositive):
        baseData[matcher].FalsePositive += 1
    if(trueNegative):
        baseData[matcher].TrueNegative += 1
    if(falseNegative):
        baseData[matcher].FalseNegative += 1

def extractResultData(threshold):
    print("Extracting Data From Files")
    for subdir, dirs, files in os.walk(results):
        for file in files:
            baseData['ComaInstResult'] = base(0,0,0,0)
            baseData['ComaInstAdjusted'] = base(0,0,0,0)
            baseData['ComaOptResult'] = base(0,0,0,0)
            baseData['ComaOptAdjusted'] = base(0,0,0,0)
            baseData['CupidResult'] = base(0,0,0,0)
            baseData['CupidAdjusted'] = base(0,0,0,0)
            baseData['DistributionBasedResult'] = base(0,0,0,0)
            baseData['DistributionBasedAdjusted'] = base(0,0,0,0)
            baseData['JaccardLevenMatcherResult'] = base(0,0,0,0)
            baseData['JaccardLevenMatcherAdjusted'] = base(0,0,0,0)
            baseData['SimilarityFloodingResult'] = base(0,0,0,0)
            baseData['SimilarityFloodingAdjusted'] = base(0,0,0,0)
            baseData['SmatResult'] = base(0,0,0,0)

            currFile = pandas.read_csv(results+file)
            source =set()
            targ = set()

            for index,row in currFile.iterrows():
                truth = currFile.iat[index,15]
                evaluateRow('ComaInstResult',currFile.iat[index,2],truth,0)
                evaluateRow('ComaInstAdjusted',currFile.iat[index,3],truth,0)
                evaluateRow('ComaOptResult',currFile.iat[index,4],truth,0)
                evaluateRow('ComaOptAdjusted',currFile.iat[index,5],truth,0)
                evaluateRow('CupidResult',currFile.iat[index,6],truth,0.8)
                evaluateRow('CupidAdjusted',currFile.iat[index,7],truth,0.8)
                evaluateRow('DistributionBasedResult',currFile.iat[index,8],truth,0.8)
                evaluateRow('DistributionBasedAdjusted',currFile.iat[index,9],truth,0.8)
                evaluateRow('JaccardLevenMatcherResult',currFile.iat[index,10],truth,0.9)
                evaluateRow('JaccardLevenMatcherAdjusted',currFile.iat[index,11],truth,0.9)
                evaluateRow('SimilarityFloodingResult',currFile.iat[index,12],truth,0.07)
                evaluateRow('SimilarityFloodingAdjusted',currFile.iat[index,13],truth,0.07)
                evaluateRow('SmatResult',currFile.iat[index,14],truth,0)
                source.add(currFile.iat[index,0])
                targ.add(currFile.iat[index,1])
            for matcher in baseData:
                s_l = min(len(source),len(targ))
                s_L = max(len(source),len(targ))
                curr_E = baseData[matcher].TruePositive + baseData[matcher].FalseNegative
                curr_M = baseData[matcher].TruePositive + baseData[matcher].FalsePositive
                curr_R = baseData[matcher].TruePositive
                fileResults.append(FileResultData
                                   (file,matcher,baseData[matcher].TruePositive,baseData[matcher].TrueNegative,baseData[matcher].FalsePositive,baseData[matcher].FalseNegative,s_l,s_L,curr_E,curr_M,curr_R))
    print("Finished Extracting Data")

if __name__ == '__main__':
    main()