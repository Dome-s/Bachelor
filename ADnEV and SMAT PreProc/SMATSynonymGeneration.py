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
class Synonym:
    def __init__(self, source, target):
        self.source = source
        self.target = target

assayNames = ["assay_id","doc_id","description","assay_type","assay_test_type","assay_category","assay_organism","assay_tax_id","assay_strain","assay_tissue","assay_cell_type","assay_subcellular_fraction","tid","relationship_type","confidence_score","curated_by","src_id","src_assay_id","chembl_id","cell_id","bao_format","tissue_id","variant_id"]
millerNames = ["Fiscal year","Project number","Status","Maximum CIDA contribution (project-level)","Branch ID","Branch name","Division ID","Division name","Section ID","Section name","Regional program (marker)","Fund centre ID","Fund centre name","Untied amount(Project-level budget)","FSTC percent","IRTC percent","CFLI (marker)","CIDA business delivery model (old)","Programming process (new)","Bilateral aid (international marker)","PBA type","Enviromental sustainability (marker)","Climate change adaptation (marker)","Climate change mitigation (marker)","Desertification (marker)","Participatory development and good governance","Trade development (marker)","Biodiversity (marker)","Urban issues (marker)","Children issues (marker)","Youth issues (marker)","Indigenous issues (marker)","Disability issues (marker)","ICT as a tool for development (marker)","Knowledge for development (marker)","Gender equality (marker)","Organisation ID","Organisation name","Organisation type","Organisation class","Organisation sub-class","Continent ID","Continent name","Project Browser country ID","CountryRegion ID","CountryRegion name","CountryRegion percent","Sector ID","Sector name","Sector percent","Amount spent"]
musicianNames = ["musician","musicianLabel","genderLabel","birthDate","cityLabel","familyNameLabel","givenNameLabel","fatherLabel","motherLabel","partner","numberOfChildren","genreLabel","websiteLabel","residenceLabel","ethnicityLabel","religionLabel","activityStart","twitterNameLabel","geniusNameLabel","recordLabelLabel"]
prospectNames = ["AgencyID","LastName","FirstName","MiddleInitial","Gender","AddressLine1","AddressLine2","PostalCode","City","State","Country","Phone","Income","NumberCars","NumberChildren","MaritalStatus","Age","CreditRating","OwnOrRentFlag","Employer","NumberCreditCards","NetWorth"]


base = 'C:/Users/dominic/Desktop/Bachelor/Traditional Matchers/results/'
results = 'C:/Users/dominic/Desktop/Bachelor/ADnEV and SMAT PreProc/SMATPreProcessedData/'

names = list()
matches = list()
synonymSets = list()

def main():
    for subdir, dirs, files in os.walk(base):
        for file in files:
            if("comaInst" in file and "prospect" in file):
                dataframe = pandas.read_csv(subdir+file)
                for index,row in dataframe.iterrows():
                    if(dataframe.iat[index,3] == 1):
                        matches.append(Synonym(dataframe.iat[index,0],dataframe.iat[index,1]))
                    #print(dataframe.iat[index,0]) #source
                    #print(dataframe.iat[index,1]) #target
                    #print(dataframe.iat[index,3]) #groundTruth    
                          
    for i in range(0,len(prospectNames),1):
        matchList = list()
        matchList.append(prospectNames[i])
        for j in range(0,len(matches),1):
            if(prospectNames[i] == matches[j].source):
                matchList.append(matches[j].target)

        unique_items = list(dict.fromkeys(matchList))
        sortedItems = sorted(unique_items, key=lambda item: (-len(item), item))

        if(sortedItems not in synonymSets):
            synonymSets.append(sortedItems)

    with open(results+"prospect.csv",'w',newline='') as f:
        w = csv.writer(f)
        for i in synonymSets:
            w.writerow(i)


if __name__ == '__main__':
    main()




