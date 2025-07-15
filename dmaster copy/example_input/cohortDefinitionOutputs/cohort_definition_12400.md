# [PL] Earliest event of Atrial Fibrillation
Cohort Definition Id: 12400

Link to Editable Definition: https://epi.jnj.com/atlas/#/cohortdefinition/12400


## Cohort Definition Description
source: 10410;
hashTag: #ASSURE, #Indication, #ASSURE-Indication, #CVM
submitter: Nathan Hall
logic: Earliest occurrence of Atrial fibrillation (AF) indexed on occurrence of AF condition for the 1st time in one's history.  Cohort exit is the end of continuous observation.

## Clinical Description
Atrial fibrillation (AF) is the most common cardiac arrhythmia, characterized by rapid and irregular beating of the atrial chambers of the heart.  If not treated properly, patients with AF may have 5-fold increased risk of stroke compared to those without AF.  There are many possible causes of AF, and valvular heart diseases could be one of the causes.  Non-valvular AF (NVAF) refers to a type of AF that isn’t caused by heart value problems.

## Evaluation Summary
We developed an incident cohort definition for AF using a concept set of 1 concept which incorporated all those found from the literature review, the analysis of PHOEBE, and orphan concepts in cohort diagnostics. The algorithm retrieves subjects from 11 databases tested. We also developed a more specific cohort requiring at least one additional diagnosis code for AF within 1 year of the index date, given the possibility of the single-code incident cohort including some rule-out diagnoses relating to other arrhythmias. Using the more specific cohort only slightly improves the specificity and PPV of the algorithm albeit at the expense of sensitivity as determined by PheValuator. It should be noted that there is a drastic reduction in sensitivity (16-53%) when using the more specific cohort. Furthermore, the very high sensitivity values while maintaining relatively high PPV and specificity using the single-code incident cohort outperform several of the more specific AF definitions in the literature review, which supports its use even further. In the end, the indication phenotype team considered the single-code incident cohort definition using one AF diagnosis code to have sufficient performance for the ASSURE platform

## Human Readable Algorithm
### Cohort Entry Events

People enter the cohort when observing any of the following:

1. condition occurrence of '[ASSURE] Atrial fibrillation' for the first time in the person's history.

Limit cohort entry events to the earliest event per person.

### Cohort Exit

The person exits the cohort at the end of continuous observation.

### Cohort Eras

Remaining events will be combined into cohort eras if they are within 0 days of each other.



## Concept Sets

### [ASSURE] Atrial fibrillation
#### Concept Set Logic
| conceptId|conceptName         |vocabularyId |includeDescendants |isExcluded |includeMapped |
|---------:|:-------------------|:------------|:------------------|:----------|:-------------|
|    313217|Atrial fibrillation |SNOMED       |TRUE               |FALSE      |FALSE         |
#### Included Concepts
| conceptId|conceptName                                                    |vocabularyId   |
|---------:|:--------------------------------------------------------------|:--------------|
|    313217|Atrial fibrillation                                            |SNOMED         |
|  37171038|Atrial fibrillation due to heart valve disorder                |SNOMED         |
|  44782442|Atrial fibrillation with rapid ventricular response            |SNOMED         |
|   4141360|Chronic atrial fibrillation                                    |SNOMED         |
|   4117112|Controlled atrial fibrillation                                 |SNOMED         |
|   1340258|Exacerbation of atrial fibrillation                            |OMOP Extension |
|  37395821|Familial atrial fibrillation                                   |SNOMED         |
|   4119601|Lone atrial fibrillation                                       |SNOMED         |
|  45768480|Longstanding persistent atrial fibrillation                    |SNOMED         |
|   4119602|Non-rheumatic atrial fibrillation                              |SNOMED         |
|   4154290|Paroxysmal atrial fibrillation                                 |SNOMED         |
|  37172212|Paroxysmal atrial fibrillation due to heart valve disorder     |SNOMED         |
|    605092|Paroxysmal atrial fibrillation with rapid ventricular response |SNOMED         |
|   4232691|Permanent atrial fibrillation                                  |SNOMED         |
|  37170582|Permanent atrial fibrillation due to heart valve disorder      |SNOMED         |
|   4232697|Persistent atrial fibrillation                                 |SNOMED         |
|  37172244|Persistent atrial fibrillation due to heart valve disorder     |SNOMED         |
|  42539346|Preexcited atrial fibrillation                                 |SNOMED         |
|   4199501|Rapid atrial fibrillation                                      |SNOMED         |
