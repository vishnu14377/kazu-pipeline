# [PL] Earliest event of Crohns disease
Cohort Definition Id: 10616

Link to Editable Definition: https://epi.jnj.com/atlas/#/cohortdefinition/10616


## Cohort Definition Description
source: 5802;
hashTag: #ASSURE, #Indication, #ASSURE-Indication;
submitter: Joel Swerdel, Anna Sheehan
logic: Earliest occurrence of Crohns disease indexed on diagnosis date, for the first time in history; cohort exit is the end of continuous observation;

## Clinical Description
 Crohn’s disease (CD) is an idiopathic inflammatory bowel disease that can affect any portion of the intestinal tract with focal, asymmetric, transmural, and granulomatous inflammation[1-3]. Crohn’s disease is characterized by chronic inflammation that may extend through all layers of the intestinal wall, involving the mesentery and regional lymph nodes. Intestinal involvement is discontinuous; “skip areas” of apparently normal tissue separate severely involved segments. Reported incidence varies geographically, ranging from 0-20.02 cases per 100,000 py in North America and 0.3-12.7 cases per 100,000 in Europe. Reported prevalence is highest in Europe (322 cases per 100,000 persons in Germany) and North America (319 cases per 100,000 persons in Canada) [4]. Risk factors include smoking, diet, and genetic factors.

## Evaluation Summary
We developed a prevalent cohort definition for Crohns disease (CD) using a concept set of two concepts which incorporated all those found from the literature review and from the analysis of PHOEBE and orphan concepts in cohort diagnostics.  The algorithm retrieves subjects from all 11 databases tested. We developed a more specific cohort requiring a second diagnosis code for CD in the time period 31-365 days after index.  This cohort improves the specificity of the algorithm albeit at the expense of sensitivity as determined by PheValuator. The 31-365 day period was determined to improve specificity compared to a 1-30 day or 1-60 day post-index second code requirement.  The significant loss in sensitivity, however, precludes its use in ASSURE. 

## Human Readable Algorithm
### Cohort Entry Events

People enter the cohort when observing any of the following:

1. condition occurrence of 'Crohns disease' for the first time in the person's history.

Limit cohort entry events to the earliest event per person.

### Cohort Exit

The person exits the cohort at the end of continuous observation.

### Cohort Eras

Remaining events will be combined into cohort eras if they are within 0 days of each other.



## Concept Sets

### Crohns disease
#### Concept Set Logic
| conceptId|conceptName                         |vocabularyId |includeDescendants |isExcluded |includeMapped |
|---------:|:-----------------------------------|:------------|:------------------|:----------|:-------------|
|  46269889|Complication due to Crohn's disease |SNOMED       |TRUE               |FALSE      |FALSE         |
|    201606|Crohn's disease                     |SNOMED       |TRUE               |FALSE      |FALSE         |
|   4340812|Perianal Crohn's disease            |SNOMED       |TRUE               |FALSE      |FALSE         |
#### Included Concepts
| conceptId|conceptName                                                                               |vocabularyId   |
|---------:|:-----------------------------------------------------------------------------------------|:--------------|
|  46269888|Abscess of intestine co-occurrent and due to Crohn's disease                              |SNOMED         |
|  46274073|Abscess of intestine co-occurrent and due to Crohn's disease of large intestine           |SNOMED         |
|  46269878|Abscess of intestine co-occurrent and due to Crohn's disease of small and large intestine |SNOMED         |
|  46269883|Abscess of intestine co-occurrent and due to Crohn's disease of small intestine           |SNOMED         |
|  36716986|Arthritis co-occurrent and due to Crohn's disease                                         |SNOMED         |
|  37162889|Colorectal Crohn disease                                                                  |SNOMED         |
|  46269889|Complication due to Crohn's disease                                                       |SNOMED         |
|  46269874|Complication due to Crohn's disease of large intestine                                    |SNOMED         |
|  46269879|Complication due to Crohn's disease of small and large intestines                         |SNOMED         |
|  46269884|Complication due to Crohn's disease of small intestine                                    |SNOMED         |
|  36715915|Crohn disease of anal canal                                                               |SNOMED         |
|  37116446|Crohn disease of appendix                                                                 |SNOMED         |
|  37172426|Crohn disease of colon in remission                                                       |SNOMED         |
|  37170088|Crohn disease of rectum in remission                                                      |SNOMED         |
|  37172546|Crohn disease of small intestine and large intestine in remission                         |SNOMED         |
|  37170274|Crohn disease of small intestine in remission                                             |SNOMED         |
|  42537666|Crohn disease of upper gastrointestinal tract                                             |SNOMED         |
|    201606|Crohn's disease                                                                           |SNOMED         |
|   4142544|Crohn's disease in remission                                                              |SNOMED         |
|   4177488|Crohn's disease of colon                                                                  |SNOMED         |
|   4210469|Crohn's disease of duodenum                                                               |SNOMED         |
|   4340114|Crohn's disease of esophagus                                                              |SNOMED         |
|  36716695|Crohn's disease of gastrointestinal anastomosis                                           |SNOMED         |
|   4122617|Crohn's disease of gingivae                                                               |SNOMED         |
|   4244235|Crohn's disease of ileum                                                                  |SNOMED         |
|   4246693|Crohn's disease of intestine                                                              |SNOMED         |
|   4239382|Crohn's disease of jejunum                                                                |SNOMED         |
|    194684|Crohn's disease of large bowel                                                            |SNOMED         |
|   4055884|Crohn's disease of oral soft tissues                                                      |SNOMED         |
|  37162884|Crohn's disease of parastomal skin                                                        |SNOMED         |
|   4299294|Crohn's disease of penis                                                                  |SNOMED         |
|   4323289|Crohn's disease of pyloric antrum                                                         |SNOMED         |
|   4266370|Crohn's disease of pylorus                                                                |SNOMED         |
|   4242392|Crohn's disease of rectum                                                                 |SNOMED         |
|   4292361|Crohn's disease of scrotum                                                                |SNOMED         |
|   4290835|Crohn's disease of skin                                                                   |SNOMED         |
|    195575|Crohn's disease of small and large intestines                                             |SNOMED         |
|    195585|Crohn's disease of small intestine                                                        |SNOMED         |
|  36686095|Crohn's disease of small intestine with stenosis                                          |SNOMED         |
|   4342643|Crohn's disease of stomach                                                                |SNOMED         |
|   4055020|Crohn's disease of terminal ileum                                                         |SNOMED         |
|   4297643|Crohn's disease of vulva                                                                  |SNOMED         |
|   4131542|Crohn's stricture of colon                                                                |SNOMED         |
|  37162851|Duodenal ulcer due to Crohn disease                                                       |SNOMED         |
|   1340297|Exacerbation of Crohn's disease                                                           |OMOP Extension |
|   4212991|Exacerbation of Crohn's disease of large intestine                                        |SNOMED         |
|   4212992|Exacerbation of Crohn's disease of small intestine                                        |SNOMED         |
|  37111373|Extraintestinal Crohn's                                                                   |SNOMED         |
|  46269880|Fistula of intestine due to Crohn's disease of small and large intestine                  |SNOMED         |
|  46269875|Fistula of large intestine due to Crohn's disease                                         |SNOMED         |
|  46269885|Fistula of small intestine due to Crohn's disease                                         |SNOMED         |
|  37162871|Gastric ulcer due to Crohn disease                                                        |SNOMED         |
|  37162865|Gastrointestinal anastomotic ulcer due to Crohn disease                                   |SNOMED         |
|   4264850|Gastrointestinal Crohn's disease                                                          |SNOMED         |
|  37162890|Ileojejunal Crohn disease                                                                 |SNOMED         |
|  46269890|Intestinal obstruction due to Crohn's disease                                             |SNOMED         |
|  46269876|Intestinal obstruction due to Crohn's disease of large intestine                          |SNOMED         |
|  46269881|Intestinal obstruction due to Crohn's disease of small and large intestine                |SNOMED         |
|  46269886|Intestinal obstruction due to Crohn's disease of small intestine                          |SNOMED         |
|   4253620|Iritis with Crohn's disease                                                               |SNOMED         |
|   4115377|Juvenile arthritis in Crohn disease                                                       |SNOMED         |
|   4297644|Metastatic Crohn's disease of skin                                                        |SNOMED         |
|   4340812|Perianal Crohn's disease                                                                  |SNOMED         |
|  37116713|Perianal fistula due to Crohn's disease                                                   |SNOMED         |
|  46269891|Rectal hemorrhage due to Crohn's disease                                                  |SNOMED         |
|  46269877|Rectal hemorrhage due to Crohn's disease of large intestine                               |SNOMED         |
|  46269882|Rectal hemorrhage due to Crohn's disease of small and large intestines                    |SNOMED         |
|  46269887|Rectal hemorrhage due to Crohn's disease of small intestine                               |SNOMED         |
