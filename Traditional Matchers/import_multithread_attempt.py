import os
import pandas as pd
from valentine import valentine_match, valentine_metrics
from valentine.algorithms import *
import time
import csv
import json
import threading
# /assays = chEMBL data , chemical database
# /Prospect = TCP-DI dataset "focuses on data integration"
# /Wikidata = singers from the us wikidata formated
# /DeepMDataset (not seperated into unionable etc...) = Magellan Data  contains dataset pairs collected from real-world data and curated mainly for Entity Matching techniques
# /Miller2 This dataset consists of tables from Canada, USA and UK Open Data, provided to us by the authors of [8] for their dataset discovery techniques.

batch_size = 4

assays_union = '/assays/Unionable/'
assays_viewunion = '/assays/View-Unionable/'

miller2_union = '/miller2/Unionable/'
miller2_viewunion = '/miller2/View -Unionable/'

prospect_union = '/prospect/Unionable/'
prospect_viewunion = '/prospect/View-Unionable/'

wikidata_union = '/Wikidata/Musicians/Musicians_unionable/'
wikidata_viewunion = '/wikidata/Musicians/Musicians_viewunion/'

options = [
            #assays_union, 
            #assays_viewunion, 
            #miller2_union, 
            miller2_viewunion,
            #prospect_union, 
            #prospect_viewunion, 
            #wikidata_union, 
            #wikidata_viewunion 
           ]

base = 'C:/Users/dominic/Desktop/Bachelor/Traditional Matchers/Data/Valentine-datasets/Valentine-datasets'

threads = list()

def main():
    for option in options:
        start_Matching(option)

def start_Matching(option):
    paths = []
    mappingpaths = []

    for subdir, dirs, files in os.walk(base+option):
        for file in files:
            if(file.endswith(".csv") and ("0_70" in file)):
                filepath = subdir + os.sep + file
                paths.append(filepath)
            if(file.endswith("mapping.json") and ("0_70" in file)):
                filepath = subdir + os.sep + file
                mappingpaths.append(filepath)

    for i in range(0, len(paths), 2):
        t = threading.Thread(target=thread_task,args=(paths,mappingpaths,i))
        threads.append(t)
        t.start()
        if(i>0 and i % (batch_size*2) == 0):
            for tr in threads:
                tr.join()
        

    for tr in threads:
        tr.join()
    print("all threads done")


def thread_task(paths,mappingpaths,i):
    print("starting thread "+str(i/2))
    d1_path = paths[i]
    d2_path = paths[i+1]
    mappingfile = open(mappingpaths[int(i/2)])
    mapping = json.load(mappingfile)

    df1 = pd.read_csv(d1_path)
    df2 = pd.read_csv(d2_path)

    filename = d1_path.split("\\")[len(d1_path.split("\\"))-1]
    filename = filename.replace("source","")

    t = time.time()
    #print("matching comaOpt")
    comaOpt_matches = None # valentine_match(df1, df2, Coma(max_n=0,java_xmx="4096m"))
    #print("matching comaInst")
    comaInst_matches =valentine_match(df1, df2, Coma(strategy="COMA_OPT_INST"))
    print("matched ComaInst in "+str(time.time()- t))

    write_to_files(comaOpt_matches,comaInst_matches,filename, df1 ,df2, mapping)
    return
    

 

def write_to_files(comaOpt,comaInst, fileName, df1, df2, mapping):
    #write_file("comaOpt",comaOpt,fileName,df1,df2,mapping)
    write_file("comaInst",comaInst,fileName,df1,df2,mapping)



def write_file(matcher, dict, fileName,df1,df2,mapping):
    with open("results/"+matcher+"_"+fileName, 'w',newline='') as f:
        w = csv.writer(f)
        w.writerow(["source","target","conf","realConf"])
        matches = mapping["matches"]
        print(dict.keys())
        for c1 in df1.columns:
            for c2 in df2.columns:
                matchInt = 0
                for match in matches:
                    if(match["source_column"] == c1 and match["target_column"] == c2):
                        matchInt = 1

                #print((('table_1',c1),('table_2',c2)) in dict.keys())
                if((('table_1',c1),('table_2',c2)) in dict.keys()):
                    w.writerow([c1,c2,dict[(('table_1',c1),('table_2',c2))],matchInt])
                else:
                    w.writerow([c1,c2,0,matchInt])

if __name__ == '__main__':
    main()
