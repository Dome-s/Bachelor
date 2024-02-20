# Repository Containing all the Data generated or used during the creation of Dominic Strempels Bachelor Thesis
## used repos
- https://github.com/shraga89/DSMA  
- https://github.com/JZCS2018/SMAT  
- https://github.com/delftdata/valentine  
- https://github.com/coreylynch/pyFM  
  
## also necessary to run SMAT are the following Glove Files which need to be added in a Glove folder to the [SMAT repo](https://github.com/Dome-s/Bachelor/tree/main/Repos/SMAT)  
- https://nlp.stanford.edu/projects/glove/

## Conda Environments for each repo can be found  [here](https://github.com/Dome-s/Bachelor/tree/main/Conda%20Environments)
- for ADnEV specifically pyFM found in the [pyFM repo](https://github.com/Dome-s/Bachelor/tree/main/Repos/pyFM) also needs to be installed

# Execution
## ADnEV 
- Trained Models can be found in the [Models](https://github.com/Dome-s/Bachelor/tree/main/Repos/DSMA/models) folder 
- to select an execution version within the mainLoader.py line 145-153 either the AnE.deep_adapt_and_evaluate() (this being the pre-trained model) or the  AnE.deep_adapt_and_evaluate_multi() (this being the multi model used in the thesis) can be commented in for usage results will be saved in either the resultsCRNN folder for the pre-trained model or the results folder for the multi model. Results are saved per dataset per matcher.
- the training file used needs to be defined in the config file
- the location for datasets to match is defined in the mainloader file in line 67
  
## SMAT
- some of the trained models and embeddings can be found in the state_dict folder or in the base repository folder these will be build and written for each execution
- a dataset can be defined in the train file in line 317+ though for this thesis the "test" part of the defined datasets is overwritten in line 413+ where a location for all the datasets to be matches is given
- so training and validation file will be used from the dataset given through the execution arguments but test dataset location is definedn in line 413
- the results are saved, location is defined in the train.py line 182

## Pipeline
### ADnEV
- results between steps can be found within this repo, but when trying to use the whole pipeline the following files need to be executed in order
- [import_PreProc_TMData.py](https://github.com/Dome-s/Bachelor/blob/main/Traditional%20Matchers/import_PreProc_TMData.py) . Traditional matchers are executed on valentine datasets located in a folder defined in line 44, results are saved to the results folder  
- [ADnEV PreProc.py](https://github.com/Dome-s/Bachelor/blob/main/ADnEV%20and%20SMAT%20PreProc/ADnEV%20PreProc.py) . uses Traditional matcher results (path defined in line 31) and formats them in an ADnEV understandable way results are saved to location defined in line 32
- [splitADnEVData.py](https://github.com/Dome-s/Bachelor/blob/main/ADnEV%20and%20SMAT%20PreProc/splitADnEVData.py) . splits ADnEV data into a trainingfile and copied the rest of the input files to a seperate location to clearly seperate training and test data paths defined in line 26-28
- After this step the location of the training file and the location of the test files can be given to ADnEV for execution
- the  [ConvertToFinalResults.py](https://github.com/Dome-s/Bachelor/blob/main/ADnEV%20and%20SMAT%20PreProc/ConvertToFinalResults.py) needs to be executed to combine ADnEV results with the TraditionalMatcher results.

### SMAT
- SMAT in this scenario needs to be executed after ADnEV as it uses some of the in between results to ensure consistency and save workload
- the [SMATSynonymGeneration.py](https://github.com/Dome-s/Bachelor/blob/main/ADnEV%20and%20SMAT%20PreProc/SMATSynonymGeneration.py) was used to gather all synanomys fields within the Valentine datasets to properly assign descriptions, the synonym files and descripions were combined into single files per dataset type in the [SynonymFiles](https://github.com/Dome-s/Bachelor/tree/main/ADnEV%20and%20SMAT%20PreProc/SMATPreProcessedData/SynonymFiles) folder
- with these present [SMATPreProcessing.py](https://github.com/Dome-s/Bachelor/blob/main/ADnEV%20and%20SMAT%20PreProc/SMATPreProcessing.py) can be executed creating a trainingfile and saving datasets to a folder, correctly formatted to be used by SMAT and descriptions added some paths to synonym files, adnev data and result target are defined in line 22-33
- This trainingfile and the formatted datasetfiles can now be used by SMAT

### post-processing
- the [combineResults.py](https://github.com/Dome-s/Bachelor/blob/main/PostProcessingAndCalculations/CombineResults.py) can now be executed to combine ADnEV+TM results with SMAT results
- [CalculateMetricsForResults.py](https://github.com/Dome-s/Bachelor/blob/main/PostProcessingAndCalculations/CalculateMetricsForResults.py) execution calculates the necessary metrics for all results in a specific folder and adds a line to a csv containing the dataset name a matcher and all the metrics calculated.
