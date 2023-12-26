import os
import time
import pandas
import csv

testData =  'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/ADnEVMatchingTasksNotInTraining/'
ADnEVResults = 'C:/Users/dominic/Desktop/Bachelor/Repos/DSMA/results'
FinalResults = 'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/ADnEVFinalResults/'

matcher = [
            "comaInst", 
            "comaOpt", 
            "cupid", 
            "distributionBased",
            "jaccardLevenMatcher",
            "similarityFlooding"
           ]

for subdir, dirs, files in os.walk(testData):
        for file in files:
            dataFile = pandas.read_csv(subdir+file)
            comaInst = pandas.read_csv(ADnEVResults+'/'+file+'/1 comaInst')
            comaOpt = pandas.read_csv(ADnEVResults+'/'+file+'/2 comaOpt')
            cupid = pandas.read_csv(ADnEVResults+'/'+file+'/3 cupid')
            distributionBased = pandas.read_csv(ADnEVResults+'/'+file+'/4 distributionBased')
            jaccardLevenMatcher = pandas.read_csv(ADnEVResults+'/'+file+'/5 jaccardLevenMatcher')
            similarityFlooding = pandas.read_csv(ADnEVResults+'/'+file+'/6 similarityFlooding')

            with open(FinalResults+file,'w',newline='') as f:
                w = csv.writer(f)
                #w.writerow(["","instance","candName","targName","conf","realConf"])
                w.writerow(["sourceName","targName","ComaInstResult","ComaInstAdjusted","ComaOpt","ComaOptAdjusted","CupidResult","CupidAdjusted","DistributionBasedResult","DistributionBasedAdjusted","JaccardLevenMatcherResult","JaccardLevenMatcherAdjusted","SimilarityFloodingResult","SimilarityFloodingAdjusted","groundtruth"])
                for index,row in comaInst.iterrows():
                    sourceName = dataFile.iat[index,2]
                    targName = dataFile.iat[index,3]
                    groundTruth = dataFile.iat[index,5]

                    ComaInstResult = dataFile.iat[index,4]
                    ComaOptResult = dataFile.iat[len(comaInst)+index,4]
                    CupidResult = dataFile.iat[2*len(comaInst)+index,4]
                    distributionBasedResult = dataFile.iat[3*len(comaInst)+index,4]
                    jaccardLevenMatcherResult = dataFile.iat[4*len(comaInst)+index,4]
                    similarityFloodingResult = dataFile.iat[5*len(comaInst)+index,4]
                    
                    ComaInstAdjusted = str(comaInst.iat[index,1]).replace("[","").replace(".]",".0")
                    ComaOptAdjusted = str(comaOpt.iat[index,1]).replace("[","").replace(".]",".0")
                    CupidAdjusted = str(cupid.iat[index,1]).replace("[","").replace(".]",".0")
                    distributionBasedAdjusted = str(distributionBased.iat[index,1]).replace("[","").replace(".]",".0")
                    jaccardLevenMatcherAdjusted= str(jaccardLevenMatcher.iat[index,1]).replace("[","").replace(".]",".0")
                    similarityFloodingAdjusted = str(similarityFlooding.iat[index,1]).replace("[","").replace(".]",".0")

                    w.writerow([sourceName,targName,ComaInstResult,ComaInstAdjusted,ComaOptResult,ComaOptAdjusted,CupidResult,CupidAdjusted,distributionBasedResult,distributionBasedAdjusted,jaccardLevenMatcherResult,jaccardLevenMatcherAdjusted,similarityFloodingResult,similarityFloodingAdjusted,groundTruth])
