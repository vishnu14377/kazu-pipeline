# [PL] Earliest event of Prostate cancer, among adult males
Cohort Definition Id: 10645

Link to Editable Definition: https://epi.jnj.com/atlas/#/cohortdefinition/10645


## Cohort Definition Description
source: 5907;
hashTag: #ASSURE, #Indication, #ASSURE-Indication;
submitter: Rupa Makadia
logic: Earliest event of Prostate cancer restricting age greater than or equal to 18 and males; indexed on prostate cancer diagnosis; cohort exit is the end of continuous observation.

## Clinical Description
Prostate cancer is a cancer of the prostate gland, an organ of the male reproductive system located below the bladder and surrounding the urethra. It is the second most common malignancy in men and the fifth leading cause of death worldwide. Median age at diagnosis is approximately 67 years.

## Evaluation Summary
NA

## Human Readable Algorithm
### Cohort Entry Events

People enter the cohort when observing any of the following:

1. condition occurrences of 'Prostate cancer', who are male &gt;= 18 years old.

Limit cohort entry events to the earliest event per person.

### Cohort Exit

The person exits the cohort at the end of continuous observation.

### Cohort Eras

Remaining events will be combined into cohort eras if they are within 0 days of each other.



## Concept Sets

### Prostate cancer
#### Concept Set Logic
| conceptId|conceptName                 |vocabularyId |includeDescendants |isExcluded |includeMapped |
|---------:|:---------------------------|:------------|:------------------|:----------|:-------------|
|   4163261|Malignant tumor of prostate |SNOMED       |TRUE               |FALSE      |FALSE         |
#### Included Concepts
| conceptId|conceptName                                                                                       |vocabularyId |
|---------:|:-------------------------------------------------------------------------------------------------|:------------|
|  44502035|Acinar cell carcinoma of prostate gland                                                           |ICDO3        |
|  37311683|Acinar cell cystadenocarcinoma of prostate                                                        |SNOMED       |
|  36550033|Acinar cell cystadenocarcinoma of prostate gland                                                  |ICDO3        |
|   1553599|Adenocarcinoid tumor of prostate gland                                                            |ICDO3        |
|  36519743|Adenocarcinoma in tubulovillous adenoma of prostate gland                                         |ICDO3        |
|  36538788|Adenocarcinoma in villous adenoma of prostate gland                                               |ICDO3        |
|   4161028|Adenocarcinoma of prostate                                                                        |SNOMED       |
|  36673096|Adenocarcinoma of the prostate metastatic                                                         |MedDRA       |
|  36552560|Adenocarcinoma with apocrine metaplasia of prostate gland                                         |ICDO3        |
|  36520903|Adenocarcinoma with cartilaginous and osseous metaplasia of prostate gland                        |ICDO3        |
|  44500595|Adenocarcinoma with mixed subtypes of prostate gland                                              |ICDO3        |
|  44499820|Adenocarcinoma with neuroendocrine differentiation of prostate gland                              |ICDO3        |
|  36530505|Adenocarcinoma with spindle cell metaplasia of prostate gland                                     |ICDO3        |
|  36535056|Adenocarcinoma with squamous metaplasia of prostate gland                                         |ICDO3        |
|  36540664|Adenoid cystic carcinoma of prostate gland                                                        |ICDO3        |
|   1553105|Adenosarcoma of prostate gland                                                                    |ICDO3        |
|  44503558|Adenosquamous carcinoma of prostate gland                                                         |ICDO3        |
|  36517339|ALK positive large B-cell lymphoma of prostate gland                                              |ICDO3        |
|  36550817|Alveolar adenocarcinoma of prostate gland                                                         |ICDO3        |
|  44501366|Alveolar rhabdomyosarcoma of prostate gland                                                       |ICDO3        |
|  36566280|Angiomyosarcoma of prostate gland                                                                 |ICDO3        |
|  36554023|Basal cell adenocarcinoma of prostate gland                                                       |ICDO3        |
|  44500494|Basal cell carcinoma, NOS, of prostate gland                                                      |ICDO3        |
|  36528487|Basaloid carcinoma of prostate gland                                                              |ICDO3        |
|  36545982|B-cell chronic lymphocytic leukemia/small lymphocytic lymphoma of prostate gland                  |ICDO3        |
|  36531690|B lymphoblastic leukemia/lymphoma, NOS, of prostate gland                                         |ICDO3        |
|  36545389|B lymphoblastic leukemia/lymphoma with hyperdiploidy of prostate gland                            |ICDO3        |
|  36540790|B lymphoblastic leukemia/lymphoma with hypodiploidy (Hypodiploid ALL) of prostate gland           |ICDO3        |
|  36524219|B lymphoblastic leukemia/lymphoma with t(1;19)(q23;p13.3); E2A-PBX1 (TCF3-PBX1) of prostate gland |ICDO3        |
|  36521407|B lymphoblastic leukemia/lymphoma with t(12;21)(p13;q22); TEL-AML1 (ETV6-RUNX1) of prostate gland |ICDO3        |
|  36559400|B lymphoblastic leukemia/lymphoma with t(5;14)(q31;q32); IL3-IGH of prostate gland                |ICDO3        |
|  36535181|B lymphoblastic leukemia/lymphoma with t(9;22)(q34;q11.2); BCR-ABL1 of prostate gland             |ICDO3        |
|  36528448|B lymphoblastic leukemia/lymphoma with t(v;11q23); MLL rearranged of prostate gland               |ICDO3        |
|  36566722|Carcinoma, anaplastic, NOS, of prostate gland                                                     |ICDO3        |
|  44503133|Carcinoma, NOS, of prostate gland                                                                 |ICDO3        |
|   4116087|Carcinoma of prostate                                                                             |SNOMED       |
|  36673097|Carcinoma of the prostate metastatic                                                              |MedDRA       |
|  44499712|Carcinoma, undifferentiated, NOS, of prostate gland                                               |ICDO3        |
|  36559613|Carcinoma with osteoclast-like giant cells of prostate gland                                      |ICDO3        |
|  36548533|Carcinosarcoma, embryonal of prostate gland                                                       |ICDO3        |
|  36543006|Carcinosarcoma, NOS, of prostate gland                                                            |ICDO3        |
|  36559448|Chondrosarcoma, NOS, of prostate gland                                                            |ICDO3        |
|  36540985|Choriocarcinoma, NOS, of prostate gland                                                           |ICDO3        |
|  36560590|Clear cell adenocarcinoma, NOS, of prostate gland                                                 |ICDO3        |
|  36520216|Cloacogenic carcinoma of prostate gland                                                           |ICDO3        |
|  44500341|Combined small cell carcinoma of prostate gland                                                   |ICDO3        |
|  44503145|Cribriform carcinoma, NOS, of prostate gland                                                      |ICDO3        |
|  36565427|Desmoplastic small round cell tumor of prostate gland                                             |ICDO3        |
|  42512688|Diffuse large B-cell lymphoma, NOS, of prostate gland                                             |ICDO3        |
|  40488897|Diffuse non-Hodgkin's lymphoma of prostate                                                        |SNOMED       |
|  36564577|Duct carcinoma, desmoplastic type of prostate gland                                               |ICDO3        |
|  36529320|Ectomesenchymoma of prostate gland                                                                |ICDO3        |
|  44502350|Embryonal rhabdomyosarcoma, NOS, of prostate gland                                                |ICDO3        |
|  36559535|Encapsulated papillary carcinoma with invasion of prostate gland                                  |ICDO3        |
|   4082919|Endometrioid carcinoma of prostate                                                                |SNOMED       |
|  36555690|Epithelial-myoepithelial carcinoma of prostate gland                                              |ICDO3        |
|  36564340|Epithelioid leiomyosarcoma of prostate gland                                                      |ICDO3        |
|  36533342|Epithelioid sarcoma, NOS, of prostate gland                                                       |ICDO3        |
|  36538823|Epithelioma, malignant of prostate gland                                                          |ICDO3        |
|  42511841|Extra-adrenal paraganglioma, NOS, of prostate gland                                               |ICDO3        |
|  37395835|Familial prostate cancer                                                                          |SNOMED       |
|  36552989|Fascial fibrosarcoma of prostate gland                                                            |ICDO3        |
|  36564328|Fibroblastic reticular cell tumor of prostate gland                                               |ICDO3        |
|  36522370|Fibrosarcoma, NOS, of prostate gland                                                              |ICDO3        |
|  42512430|Follicular lymphoma, NOS, of prostate gland                                                       |ICDO3        |
|  40488901|Follicular non-Hodgkin's lymphoma of prostate                                                     |SNOMED       |
|  36529897|Giant cell and spindle cell carcinoma of prostate gland                                           |ICDO3        |
|  36535925|Giant cell carcinoma of prostate gland                                                            |ICDO3        |
|  44501968|Giant cell sarcoma of prostate gland                                                              |ICDO3        |
|  36545616|Glassy cell carcinoma of prostate gland                                                           |ICDO3        |
|  36547024|Hemangiosarcoma of prostate gland                                                                 |ICDO3        |
|  36543214|HHV8 positive diffuse large B-cell lymphoma of prostate gland                                     |ICDO3        |
|   4141960|Hormone refractory prostate cancer                                                                |SNOMED       |
|  36716186|Hormone sensitive prostate cancer                                                                 |SNOMED       |
|  36546114|Infantile fibrosarcoma of prostate gland                                                          |ICDO3        |
|  44499514|Infiltrating duct carcinoma, NOS, of prostate gland                                               |ICDO3        |
|  37311236|Infiltrating duct carcinoma of prostate                                                           |SNOMED       |
|  44503555|Intraductal papillary adenocarcinoma with invasion of prostate gland                              |ICDO3        |
|  36527764|Intravascular large B-cell lymphoma of prostate gland                                             |ICDO3        |
|  36521611|Langerhans cell histiocytosis, disseminated of prostate gland                                     |ICDO3        |
|  36554370|Large cell carcinoma, NOS, of prostate gland                                                      |ICDO3        |
|  36557451|Large cell carcinoma with rhabdoid phenotype of prostate gland                                    |ICDO3        |
|  44499864|Large cell neuroendocrine carcinoma of prostate gland                                             |ICDO3        |
|  36550323|Leiomyosarcoma, NOS, of prostate gland                                                            |ICDO3        |
|   4200890|Local recurrence of malignant tumor of prostate                                                   |SNOMED       |
|  36563396|Lymphoepithelial carcinoma of prostate gland                                                      |ICDO3        |
|  36522940|Malignant fibrous histiocytoma of prostate gland                                                  |ICDO3        |
|  44500910|Malignant lymphoma, non-Hodgkin, NOS, of prostate gland                                           |ICDO3        |
|  36563308|Malignant melanoma, NOS, of prostate gland                                                        |ICDO3        |
|  36536835|Malignant peripheral nerve sheath tumor, NOS, of prostate gland                                   |ICDO3        |
|  36564066|Malignant tumor, clear cell type of prostate gland                                                |ICDO3        |
|  36540099|Malignant tumor, giant cell type of prostate gland                                                |ICDO3        |
|   4283738|Malignant tumor involving prostate by direct extension from bladder                               |SNOMED       |
|   4163261|Malignant tumor of prostate                                                                       |SNOMED       |
|  36525551|Malignant tumor, spindle cell type of prostate gland                                              |ICDO3        |
|  36531255|Marginal zone B-cell lymphoma, NOS, of prostate gland                                             |ICDO3        |
|  36566340|Medullary carcinoma, NOS, of prostate gland                                                       |ICDO3        |
|  36556099|Metaplastic carcinoma, NOS, of prostate gland                                                     |ICDO3        |
|  42512655|Mixed acinar-ductal carcinoma of prostate gland                                                   |ICDO3        |
|  42512952|Mixed adenoneuroendocrine carcinoma of prostate gland                                             |ICDO3        |
|  44500734|Mixed cell adenocarcinoma of prostate gland                                                       |ICDO3        |
|  36525831|Mixed type rhabdomyosarcoma of prostate gland                                                     |ICDO3        |
|  44501350|Mucinous adenocarcinoma of prostate gland                                                         |ICDO3        |
|  44501528|Mucin-producing adenocarcinoma of prostate gland                                                  |ICDO3        |
|  36543289|Myeloid or lymphoid neoplasm with FGFR1 abnormalities of prostate gland                           |ICDO3        |
|  36543452|Myeloid or lymphoid neoplasm with PDGFRA rearrangement of prostate gland                          |ICDO3        |
|  36556846|Myeloproliferative neoplasm, unclassifiable of prostate gland                                     |ICDO3        |
|  36547882|Myoepithelial carcinoma of prostate gland                                                         |ICDO3        |
|  42512398|Myofibroblastic sarcoma of prostate gland                                                         |ICDO3        |
|  36539639|Myosarcoma of prostate gland                                                                      |ICDO3        |
|  36545805|Myxofibrosarcoma of prostate gland                                                                |ICDO3        |
|  36551235|Myxoid leiomyosarcoma of prostate gland                                                           |ICDO3        |
|  44502000|Neoplasm, malignant of prostate gland                                                             |ICDO3        |
|  36559668|Nephroblastoma, NOS, of prostate gland                                                            |ICDO3        |
|  36527397|Neuroblastoma, NOS, of prostate gland                                                             |ICDO3        |
|  37177729|Neuroendocrine cancer of the prostate metastatic                                                  |MedDRA       |
|  44501627|Neuroendocrine carcinoma, NOS, of prostate gland                                                  |ICDO3        |
|  36520178|Neuroendocrine tumor, NOS, of prostate gland                                                      |ICDO3        |
|  40486666|Non-Hodgkin's lymphoma of prostate                                                                |SNOMED       |
|   1553133|Non-small cell carcinoma of prostate gland                                                        |ICDO3        |
|  36551411|Oxyphilic adenocarcinoma of prostate gland                                                        |ICDO3        |
|  42512377|Paget disease, extramammary of prostate gland                                                     |ICDO3        |
|  44499641|Papillary adenocarcinoma, NOS, of prostate gland                                                  |ICDO3        |
|  36529044|Papillary carcinoma, NOS, of prostate gland                                                       |ICDO3        |
|  36567202|Papillary squamous cell carcinoma of prostate gland                                               |ICDO3        |
|  44499734|Papillary urothelial carcinoma of prostate gland                                                  |ICDO3        |
|   1553597|Paraganglioma, NOS, of prostate gland                                                             |ICDO3        |
|  36550674|Plasmablastic lymphoma of prostate gland                                                          |ICDO3        |
|  36533689|Pleomorphic carcinoma of prostate gland                                                           |ICDO3        |
|  36563529|Pleomorphic rhabdomyosarcoma, adult type of prostate gland                                        |ICDO3        |
|  36544659|Polygonal cell carcinoma of prostate gland                                                        |ICDO3        |
|  36518000|Precursor T-cell lymphoblastic leukemia of prostate gland                                         |ICDO3        |
|  37166518|Primary acinar cell cystadenocarcinoma of prostate                                                |SNOMED       |
|  37166523|Primary adenocarcinoma of prostate                                                                |SNOMED       |
|  37166255|Primary carcinoma of prostate                                                                     |SNOMED       |
|  37166525|Primary endometrioid carcinoma of prostate                                                        |SNOMED       |
|  37166521|Primary infiltrating duct carcinoma of prostate                                                   |SNOMED       |
|  37174104|Primary malignant hormone-refractory neoplasm of prostate                                         |SNOMED       |
|    200962|Primary malignant neoplasm of prostate                                                            |SNOMED       |
|  37166560|Primary small cell neuroendocrine carcinoma of prostate                                           |SNOMED       |
|  36617703|Prostate cancer metastatic                                                                        |MedDRA       |
|  36617705|Prostate cancer stage 0                                                                           |MedDRA       |
|  36617706|Prostate cancer stage I                                                                           |MedDRA       |
|  36617707|Prostate cancer stage II                                                                          |MedDRA       |
|  36617708|Prostate cancer stage III                                                                         |MedDRA       |
|  36617709|Prostate cancer stage IV                                                                          |MedDRA       |
|  37177733|Prostate sarcoma                                                                                  |MedDRA       |
|  36673099|Prostatic cancer metastatic                                                                       |MedDRA       |
|  36565415|Pseudosarcomatous carcinoma of prostate gland                                                     |ICDO3        |
|  36712762|Recurrent malignant neoplasm of prostate                                                          |SNOMED       |
|  36525240|Rhabdoid tumor, NOS, of prostate gland                                                            |ICDO3        |
|  36519105|Rhabdomyosarcoma, NOS, of prostate gland                                                          |ICDO3        |
|  36526468|Sarcoma, NOS, of prostate gland                                                                   |ICDO3        |
|  36519069|Schneiderian carcinoma of prostate gland                                                          |ICDO3        |
|  36550618|Scirrhous adenocarcinoma of prostate gland                                                        |ICDO3        |
|  42512260|Sebaceous carcinoma of prostate gland                                                             |ICDO3        |
|  36547431|Seminoma, NOS, of prostate gland                                                                  |ICDO3        |
|  44500459|Signet ring cell carcinoma of prostate gland                                                      |ICDO3        |
|  36552590|Small cell carcinoma, fusiform cell of prostate gland                                             |ICDO3        |
|  37163177|Small cell neuroendocrine carcinoma of prostate                                                   |SNOMED       |
|  36552151|Small cell sarcoma of prostate gland                                                              |ICDO3        |
|  36539709|Solid carcinoma, NOS, of prostate gland                                                           |ICDO3        |
|  36519333|Solitary fibrous tumor, malignant of prostate gland                                               |ICDO3        |
|  36524677|Spindle cell carcinoma, NOS, of prostate gland                                                    |ICDO3        |
|  36558122|Spindle cell rhabdomyosarcoma of prostate gland                                                   |ICDO3        |
|  36567912|Spindle cell sarcoma of prostate gland                                                            |ICDO3        |
|  44500716|Squamous cell carcinoma, adenoid of prostate gland                                                |ICDO3        |
|  36534013|Squamous cell carcinoma, keratinizing, NOS, of prostate gland                                     |ICDO3        |
|  36531450|Squamous cell carcinoma, large cell, nonkeratinizing, NOS, of prostate gland                      |ICDO3        |
|  36532395|Squamous cell carcinoma, microinvasive of prostate gland                                          |ICDO3        |
|   4164017|Squamous cell carcinoma of prostate                                                               |SNOMED       |
|  36532454|Squamous cell carcinoma, small cell, nonkeratinizing of prostate gland                            |ICDO3        |
|  36543315|Squamous cell carcinoma, spindle cell of prostate gland                                           |ICDO3        |
|  36534105|Squamous cell carcinoma with horn formation of prostate gland                                     |ICDO3        |
|  36558501|Stromal sarcoma, NOS, of prostate gland                                                           |ICDO3        |
|  36517801|Superficial spreading adenocarcinoma of prostate gland                                            |ICDO3        |
|  36547390|Systemic EBV positive T-cell lymphoproliferative disease of childhood of prostate gland           |ICDO3        |
|  36544527|T-cell/histiocyte rich large B-cell lymphoma of prostate gland                                    |ICDO3        |
|  36540394|T-cell large granular lymphocytic leukemia of prostate gland                                      |ICDO3        |
|  36554563|Teratocarcinoma of prostate gland                                                                 |ICDO3        |
|  44501195|Transitional cell carcinoma, NOS, of prostate gland                                               |ICDO3        |
|  36554139|Tubular adenocarcinoma of prostate gland                                                          |ICDO3        |
|  36568174|Tumor cells, malignant of prostate gland                                                          |ICDO3        |
|  36531262|Undifferentiated sarcoma of prostate gland                                                        |ICDO3        |
|  36543398|Urothelial carcinoma, micropapillary of prostate gland                                            |ICDO3        |
|  36534262|Urothelial carcinoma, sarcomatoid of prostate gland                                               |ICDO3        |
|  36553778|Verrucous carcinoma, NOS, of prostate gland                                                       |ICDO3        |
|  36543338|Villous adenocarcinoma of prostate gland                                                          |ICDO3        |
|  36544648|Yolk sac tumor, NOS, of prostate gland                                                            |ICDO3        |
