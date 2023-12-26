import os
import time
import pandas
import csv
import json
import threading
from itertools import groupby
import shutil
import random

# /assays = chEMBL data , chemical database
# /Prospect = TCP-DI dataset "focuses on data integration"
# /Wikidata = singers from the us wikidata formated
# /DeepMDataset (not seperated into unionable etc...) = Magellan Data  contains dataset pairs collected from real-world data and curated mainly for Entity Matching techniques
# /Miller2 This dataset consists of tables from Canada, USA and UK Open Data, provided to us by the authors of [8] for their dataset discovery techniques.



datasets = [
            "assays", 
            "miller2", 
            "musicians", #wikidata
            "prospect"
           ]

preProcessedData =  'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/AdnevPreProcessedData/'
trainingFile =  'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/ADnEVTrainingFile/trainingFile.csv'
testData =  'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/ADnEVMatchingTasksNotInTraining/'

threads = list()

def main():
    filelist = []


    seed= 12345
    percentageInTrain = 0.4
    datasetsOnlyForTrain = "prospect"

    for subdir, dirs, files in os.walk(preProcessedData):
        for file in files:
            if(datasetsOnlyForTrain in file):
                shutil.copyfile(subdir + file, testData + file)
            else:
                filelist.append(file)

    random.seed(seed)
    randomIndexes = random.sample(range(0,len(filelist)),round(len(filelist)*percentageInTrain))
    randomIndexes.sort()

    with open(trainingFile,'a',newline='') as f:
        w = csv.writer(f)
        w.writerow(["","instance","candName","targName","conf","realConf"])

    inst=0
    instanceNames = []
    instanceNumber = 0

    for i in range(0,len(filelist),1):
        if i in randomIndexes:
            inst,instanceNumber = write_file(trainingFile,filelist[i],inst,instanceNames,instanceNumber)
            instanceNames= []
            #file in trainingData
        else:
            shutil.copyfile(subdir + filelist[i], testData + filelist[i])
            #file in testdata




def write_file(filepath,element,inst,instanceNames,instanceNumber):
    print("writing "+element+" to trainingFile")
    with open(filepath,'a',newline='') as f:
        w = csv.writer(f)
        #w.writerow(["","instance","candName","targName","conf","realConf"])
        dataframe = pandas.read_csv(preProcessedData+element)
        
        for index,row in dataframe.iterrows():
            if(dataframe.iat[index,1] not in instanceNames):
                instanceNames.append(dataframe.iat[index,1])

            w.writerow([inst ,str(len(instanceNames)+ instanceNumber)+"," + dataframe.iat[index,1].split(', ')[1],dataframe.iat[index,2],dataframe.iat[index,3],dataframe.iat[index,4],dataframe.iat[index,5]])
            inst += 1
        instanceNumber += len(instanceNames)
    return inst,instanceNumber
if __name__ == '__main__':
    main()