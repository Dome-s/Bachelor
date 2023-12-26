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

class SynonymsDisc:
    def __init__(self, synonyms, disc1,disc2):
        self.synonyms = synonyms
        self.disc1 = disc1
        self.disc2 = disc2


ADnEVData = 'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/ADnEVMatchingTasksNotInTraining/'
ADnEVTrain = 'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/ADnEVTrainingFile/trainingFile.csv'

SMATData = 'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/SMATPreProcessedData/SMATMatchingTasksNotInTraining/'
SMATTrain = 'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/SMATPreProcessedData/SMATtrainingFile.csv'

assays_synonyms_and_disc  =  'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/SMATPreProcessedData/SynonymFiles/assays.csv'
miller2_synonyms_and_disc  =  'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/SMATPreProcessedData/SynonymFiles/miller2.csv'
prospect_synonyms_and_disc  =  'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/SMATPreProcessedData/SynonymFiles/prospect.csv'
wikidata_synonyms_and_disc  =  'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/SMATPreProcessedData/SynonymFiles/wikidata.csv'

threads = list()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fileType', default='none', type=str, help = 'type of files to generate train for single training file data for all the input files')
    opt = parser.parse_args()

    SynonymsDiscs = list()
    SynonymsDiscs = loadSynonyms(assays_synonyms_and_disc,SynonymsDiscs)
    SynonymsDiscs = loadSynonyms(miller2_synonyms_and_disc,SynonymsDiscs)
    SynonymsDiscs = loadSynonyms(prospect_synonyms_and_disc,SynonymsDiscs)
    SynonymsDiscs = loadSynonyms(wikidata_synonyms_and_disc,SynonymsDiscs)

    adnevTrainFile = pandas.read_csv(ADnEVTrain)
    count = 0
    max = 0
    elementsWithNoDisc = list()


    if(opt.fileType != 'none' and opt.fileType == 'train'):
        max = len(adnevTrainFile) / 6
        with open(SMATTrain,'w',newline='') as f:
            w = csv.writer(f)
            w.writerow(["source","target","des1","des2","label"])
            for index,row in adnevTrainFile.iterrows():
                #adnevTrainFile.iat[index,1] instance
                #adnevTrainFile.iat[index,2] source
                #adnevTrainFile.iat[index,3] target
                #adnevTrainFile.iat[index,4] conf
                #adnevTrainFile.iat[index,5] realconf
                if("comaInst" in adnevTrainFile.iat[index,1]):
                    disc1 = ""
                    disc2 = ""
                    source = adnevTrainFile.iat[index,2]
                    target = adnevTrainFile.iat[index,3]
                    for elements in SynonymsDiscs:
                        if(source in elements.synonyms and target not in elements.synonyms):
                            #no match
                            disc1 = elements.disc1
                        if(source not in elements.synonyms and target in elements.synonyms):
                            #no match
                            disc2 = elements.disc2
                        if(source in elements.synonyms and target in elements.synonyms):
                            disc1 = elements.disc1
                            disc2 = elements.disc2    
                        if(disc1 != "" and disc2 != ""):
                            break
                    w.writerow([adnevTrainFile.iat[index,2],adnevTrainFile.iat[index,3],disc1,disc2,adnevTrainFile.iat[index,5]])
                    count +=1
                    donePerc= count / (max*0.01)
                    print((count , max,str(donePerc)), end="\r", flush=True)

    if(opt.fileType != 'none' and opt.fileType == 'data'):
        for subdir, dirs, files in os.walk(ADnEVData):
            for file in files:
                adnevResultFile = pandas.read_csv(ADnEVData+file)
                max = len(files)
                with open(SMATData+file,'w',newline='') as f:
                    w = csv.writer(f)
                    w.writerow(["source","target","des1","des2","label"])

                    for index,row in adnevResultFile.iterrows():
                        if("comaInst" in adnevResultFile.iat[index,1]):
                            disc1 = ""
                            disc2 = ""
                            source = adnevResultFile.iat[index,2]
                            target = adnevResultFile.iat[index,3]
                            truth = 0
                            
                            for elements in SynonymsDiscs:
                                if(source in elements.synonyms and target not in elements.synonyms):
                                    #no match
                                    disc1 = elements.disc1
                                if(source not in elements.synonyms and target in elements.synonyms):
                                    #no match
                                    disc2 = elements.disc2
                                if(source in elements.synonyms and target in elements.synonyms):
                                    disc1 = elements.disc1
                                    disc2 = elements.disc2    
                                    truth = 1
                                if(disc1 != "" and disc2 != ""):
                                    break
                            if(disc1 == ""):
                                elementsWithNoDisc.append(source)
                            if(disc2 == ""):
                                elementsWithNoDisc.append(target)
                            w.writerow([source,target,disc1,disc2,truth])
                    
                filecsv = pandas.read_csv(SMATData+file)
                filecsv.to_excel(SMATData+file.split('.')[0]+'.xlsx' , index=False)

                count +=1
                donePerc= count / (max*0.01)
                print((count , max,str(donePerc)), end="\r", flush=True)

        unique_items = list(dict.fromkeys(elementsWithNoDisc))
        print(unique_items)
            
def loadSynonyms(file,SynonymsDiscs):
    with open(file) as f:
        reader_obj = csv.reader(f)
        for row in reader_obj: 
            syns = list()
            for i in range(0,len(row)-2,1):
                syns.append(row[i])
            SynonymsDiscs.append(SynonymsDisc(syns,row[-2],row[-1]))
    return SynonymsDiscs


if __name__ == '__main__':
    main()