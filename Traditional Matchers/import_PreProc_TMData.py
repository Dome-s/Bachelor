import os
import pandas as pd
from valentine import valentine_match, valentine_metrics
from valentine.algorithms import *
import csv
import json
import time

# /assays = chEMBL data , chemical database
# /Prospect = TCP-DI dataset "focuses on data integration"
# /Wikidata = singers from the us wikidata formated
# /DeepMDataset (not seperated into unionable etc...) = Magellan Data  contains dataset pairs collected from real-world data and curated mainly for Entity Matching techniques
# /Miller2 This dataset consists of tables from Canada, USA and UK Open Data, provided to us by the authors of [8] for their dataset discovery techniques.


assays_union = '/assays/Unionable/' 
assays_viewunion = '/assays/View-Unionable/'

miller2_union = '/miller2/Unionable/'
miller2_viewunion = '/miller2/View -Unionable/'

prospect_union = '/prospect/Unionable/'
prospect_viewunion = '/prospect/View-Unionable/'

wikidata_union = '/Wikidata/Musicians/Musicians_unionable/'
wikidata_viewunion = '/wikidata/Musicians/Musicians_viewunion/'

covidData = '/CovidData/'

options = [
            assays_union, 
            #assays_viewunion, 
            #miller2_union, 
            #miller2_viewunion,
            #prospect_union, 
            #prospect_viewunion, 
            #wikidata_union, 
            #wikidata_viewunion
           ]

base = 'C:/Users/dominic/Desktop/Bachelor/Traditional Matchers/Data/Valentine-datasets/Valentine-datasets'

def main():
    for option in options:
        thread_task(option)

def thread_task(option):
    paths = []
    mappingpaths = []

    for subdir, dirs, files in os.walk(base+option):
        for file in files:
            if(file.endswith(".csv")):
                filepath = subdir + os.sep + file
                paths.append(filepath)
            if(file.endswith("mapping.json")):
                filepath = subdir + os.sep + file
                mappingpaths.append(filepath)

    for i in range(0, len(paths), 2):
        d1_path = paths[i]
        d2_path = paths[i+1]
        mappingfile = open(mappingpaths[int(i/2)])
        mapping = json.load(mappingfile)

        df1 = pd.read_csv(d1_path)
        df2 = pd.read_csv(d2_path)

        filename = d1_path.split("\\")[len(d1_path.split("\\"))-1]
        filename = filename.replace("source","")
        t = time.time()
        #print("matching cupid")
        cupid_matches = None #valentine_match(df1, df2,  Cupid(th_accept=0))
        #print("matched cupid in "+str(time.time() - t))
        t = time.time()
        #print("matching distributionBased")
        distributionBased_matches = None # valentine_match(df1, df2, DistributionBased(threshold1=0,threshold2=0))  
        #print("matched distributionBased in "+str(time.time() - t))
        t = time.time()
        #print("matching similarityFlooding")
        similarityFlooding_matches = None #valentine_match(df1, df2, SimilarityFlooding()) 
        #print("matched similarityFlooding in "+str(time.time() - t))
        t = time.time()
        #print("matching jaccard")
        jaccard_matches = None #valentine_match(df1, df2,  JaccardLevenMatcher(threshold_leven=0,process_num=16))
        #print("matched jaccard in "+str(time.time() - t))
        t = time.time()
        #print("matching ComaOpt")
        comaOpt_matches = valentine_match(df1, df2, Coma(max_n=1, java_xmx="24g"))
        #print("matched ComaOpt in "+str(time.time() - t))
        t = time.time()
        #print("matching comaInst")
        comaInst_matches = None # valentine_match(df1, df2, Coma(java_xmx="24g",use_instances=True))
        #print("matched comaInst in "+str(time.time() - t))
        write_to_files(cupid_matches, distributionBased_matches,similarityFlooding_matches,jaccard_matches,comaOpt_matches,comaInst_matches,filename, df1 ,df2, mapping)
    return


def write_to_files(cupid_matches, distributionBased_matches,similarityFlooding_matches,jaccard_matches,comaOpt_matches,comaInst_matches,fileName, df1, df2, mapping):
    #write_file("cupid",cupid_matches,fileName,df1,df2,mapping)
    #write_file("jaccardLevenMatcher",jaccard_matches,fileName,df1,df2,mapping)
    #write_file("distributionBased",distributionBased_matches,fileName,df1,df2,mapping)
    #write_file("similarityFlooding",similarityFlooding_matches,fileName,df1,df2,mapping)
    write_file("comaOpt",comaOpt_matches,fileName,df1,df2,mapping)
    #write_file("comaInst",comaInst_matches,fileName,df1,df2,mapping)



def write_file(matcher, dict, fileName,df1,df2,mapping):
    with open("ComaInst_results/"+matcher+"_"+fileName, 'w',newline='') as f:
        w = csv.writer(f)
        w.writerow(["source","target","conf","realConf"])
        matches = mapping["matches"]

        for c1 in df1.columns:
            for c2 in df2.columns:
                matchInt = 0
                for match in matches:
                    if(match["source_column"] == c1 and match["target_column"] == c2):
                        matchInt = 1
                if((('table_1',c1),('table_2',c2)) in dict.keys()):
                    w.writerow([c1,c2,dict[(('table_1',c1),('table_2',c2))],matchInt])
                else:
                    w.writerow([c1,c2,0,matchInt])

if __name__ == '__main__':
    main()
