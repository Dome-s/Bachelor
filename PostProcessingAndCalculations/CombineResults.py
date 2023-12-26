import os
import time
import pandas
import csv
import json
import threading
import argparse
from itertools import groupby
# /assays = chEMBL data , chemical database
# /Prospect = TCP-DI dataset "focuses on data integration"
# /Wikidata = singers from the us wikidata formated
# /DeepMDataset (not seperated into unionable etc...) = Magellan Data  contains dataset pairs collected from real-world data and curated mainly for Entity Matching techniques
# /Miller2 This dataset consists of tables from Canada, USA and UK Open Data, provided to us by the authors of [8] for their dataset discovery techniques.

ADnEVResultFiles= 'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/ADnEVFinalResults/'
SMATResultFiles = 'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/SMATFinalResults/'
results = 'C:/Users/dominic/Desktop/Bachelor/PostProcessingAndCalculations/combinedResults/'


adnevResults = list()
smatResults = list()

def main():
    for subdir, dirs, files in os.walk(ADnEVResultFiles):
        adnevResults = files
    
    for subdir, dirs, files in os.walk(SMATResultFiles):
        smatResults = files

    for smatElem in smatResults:
        for adnevElem in adnevResults:
            if(smatElem == adnevElem):
                print("merging " + smatElem+ " from Smat with " +adnevElem+ " From ADnEV")
                ares = pandas.read_csv(ADnEVResultFiles+adnevElem)
                sres = pandas.read_csv(SMATResultFiles+smatElem, header=None)
                with open(results+smatElem,'w',newline='') as f:
                    w = csv.writer(f)
                    w.writerow(["sourceName","targName","ComaInstResult","ComaInstAdjusted","ComaOptResult","ComaOptAdjusted","CupidResult","CupidAdjusted","DistributionBasedResult","DistributionBasedAdjusted","JaccardLevenMatcherResult","JaccardLevenMatcherAdjusted","SimilarityFloodingResult","SimilarityFloodingAdjusted","SmatResult","groundtruth"])
                    for index,row in ares.iterrows():
                        #sourceName,targName,ComaInstResult,ComaInstAdjusted,ComaOpt,ComaOptAdjusted,CupidResult,CupidAdjusted,DistributionBasedResult,DistributionBasedAdjusted,JaccardLevenMatcherResult,JaccardLevenMatcherAdjusted,SimilarityFloodingResult,SimilarityFloodingAdjusted,groundtruth
                        w.writerow([ares.iat[index,0],ares.iat[index,1],ares.iat[index,2],ares.iat[index,3],ares.iat[index,4],ares.iat[index,5],ares.iat[index,6],ares.iat[index,7],ares.iat[index,8],ares.iat[index,9],ares.iat[index,10],ares.iat[index,11],ares.iat[index,12],ares.iat[index,13],sres.iloc[index,0],ares.iat[index,14]])

                        


if __name__ == '__main__':
    main()