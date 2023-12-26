import os
import time
import pandas
import csv
import json
import threading
from itertools import groupby
# /assays = chEMBL data , chemical database
# /Prospect = TCP-DI dataset "focuses on data integration"
# /Wikidata = singers from the us wikidata formated
# /DeepMDataset (not seperated into unionable etc...) = Magellan Data  contains dataset pairs collected from real-world data and curated mainly for Entity Matching techniques
# /Miller2 This dataset consists of tables from Canada, USA and UK Open Data, provided to us by the authors of [8] for their dataset discovery techniques.


class MatcherResult:
    def __init__(self, matcher, problemName,path):
        self.path = path
        self.matcher = matcher
        self.problemName = problemName


matcher = [
            "comaInst", 
            "comaOpt", 
            "cupid", 
            "distributionBased",
            "jaccardLevenMatcher",
            "similarityFlooding"
           ]

base = 'C:/Users/dominic/Desktop/Bachelor/Traditional Matchers/results/'
results = 'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/AdnevPreProcessedData/'

threads = list()

def main():
    MatcherResults = []

    for subdir, dirs, files in os.walk(base):
        for file in files:
            print(file.split("_",1)[0])
            MatcherResults.append(MatcherResult(file.split("_",1)[0], file.split("_",1)[1],base+file))

    sortedMatcherResults = sorted(MatcherResults, key = lambda matchresult: matchresult.problemName)
    groupedMatcherResults = groupby(sortedMatcherResults, key= lambda matchresult: matchresult.problemName)
    
    for key,resultGroup in groupedMatcherResults:
        relevantResults = list(map(lambda x: MatcherResult(x.matcher, key, x.path), resultGroup))
        write_file(key,relevantResults)






def write_file(key,relevantResults):
    print("writing "+ key)
    with open(results+key,'w',newline='') as f:
        w = csv.writer(f)
        w.writerow(["","instance","candName","targName","conf","realConf"])

    for i in range(0, len(relevantResults),1):
        path = relevantResults[i].path
        matcher = relevantResults[i].matcher

        dataframe = pandas.read_csv(path)

        with open(results+key,'a',newline='') as f:
            w = csv.writer(f)
            dataframe.insert(0,'instance',range(0 + i*len(dataframe), 1 + i*len(dataframe) + len(dataframe)-1,True))
            dataframe.insert(1,'candName',str(i+1)+", "+matcher,True)
            for index,row in dataframe.iterrows():
                w.writerow(row)

if __name__ == '__main__':
    main()