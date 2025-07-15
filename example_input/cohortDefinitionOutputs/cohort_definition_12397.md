# [PL] Earliest event of Psoriatic arthritis
Cohort Definition Id: 12397

Link to Editable Definition: https://epi.jnj.com/atlas/#/cohortdefinition/12397


## Cohort Definition Description
source: 5972;
hashTag: #ASSURE, #Indication, #ASSURE-Indication;
submitter: Joel Swerdel
logic: Earliest event of Psoriatic arthritis, indexed on the diagnosis of Psoriatic arthritis or diagnosis of Andropathy that co-occur with a diagnosis of Psoriasis within 60 days. Exit cohort at the end of continuous observation period.

## Clinical Description
Overview: Psoriatic Arthritis (PsA) ia a type of inflammatory autoimmune condition that can cause chronic pain in and around joints. If left untreated, PSA can lead to permanent joint damage and if untreated is disabling. Some patients with psoriasis develop psoriatic arthritis. Presentation: Psoriatic arthritis presents as painful, stiff, and swollen joints. Assessment: Symptoms of PsA include painful, stiff, and swollen joints, which may flare and subside. Joints may be swollen and tender, and fingernails may have be abnormal (e.g., pitting and flaking), in addition to tenderness of the soles of the feet. X-ray imaging may help to identify joint changes that are specific to PsA over other types of arthritis. Rheumatoid factor and joint fluid laboratory tests may help to rule out other types of conditions (rheumatoid arthritis and gout, respectively).  Plan: There is no cure for PsA. Treatment may include steroid injections, disease modifying antirheumatic drugs (DMARDs), biologic treatments, and newer oral medications (apremilast). Joint replacement surgery may also be an intervention. Prognosis: PsA may be mild to severe, is chronic, and joint damage that has occurred does not improve. Early diagnosis and intervention with treatment is important to limit progression of joint damage. If untreated, PsA will progress to disabling joint disease.

## Evaluation Summary
We developed a prevalent cohort definition for psoriatic arthritis (PsA) using a concept set of 3 concepts which incorporated all those found from the literature review and from the analysis of PHOEBE and orphan concepts in cohort diagnostics. The algorithm retrieves subjects from all 11 databases tested. We developed a more specific cohort requiring a second diagnosis code for PSA in the time period 31-365 days after index. This cohort improves the specificity of the algorithm albeit at the expense of sensitivity as determined by PheValuator. The significant loss in sensitivity, however, precludes its use in ASSURE. We also examined an algorithm where the specific codes for PsA were used. We found that this algorithm had similar PPV to the prevalent algorithm but significantly lower sensitivity. We determined that this algorithm did not have the performance characteristics necessary for ASSURE.

## Human Readable Algorithm
### Cohort Entry Events

People enter the cohort when observing any of the following:

1. condition occurrences of 'Psoriatic arthritis (exclude mutilans)'.

2. condition occurrences of 'Arthropathy'; having at least 1 condition occurrence of 'Psoriasis', starting between 60 days before and 60 days after 'Arthropathy' start date.

Limit cohort entry events to the earliest event per person.

### Cohort Exit

The person exits the cohort at the end of continuous observation.

### Cohort Eras

Remaining events will be combined into cohort eras if they are within 0 days of each other.



## Concept Sets

### Psoriatic arthritis (exclude mutilans)
#### Concept Set Logic
| conceptId|conceptName         |vocabularyId |includeDescendants |isExcluded |includeMapped |
|---------:|:-------------------|:------------|:------------------|:----------|:-------------|
|  40319772|Psoriatic arthritis |SNOMED       |TRUE               |FALSE      |FALSE         |
|   4025831|Arthritis mutilans  |SNOMED       |FALSE              |TRUE       |FALSE         |
#### Included Concepts
| conceptId|conceptName                                                       |vocabularyId   |
|---------:|:-----------------------------------------------------------------|:--------------|
|   1340448|Exacerbation of psoriatic arthritis                               |OMOP Extension |
|   4132495|Iritis with psoriatic arthritis                                   |SNOMED         |
|   4079733|Juvenile psoriatic arthritis                                      |SNOMED         |
|   4079734|Juvenile psoriatic arthritis with psoriasis                       |SNOMED         |
|  37160379|Oligoarticular psoriatic arthritis                                |SNOMED         |
|  37160369|Polyarticular psoriatic arthritis                                 |SNOMED         |
|   1340520|Progression of psoriatic arthritis                                |OMOP Extension |
|   1076201|PsAPASH syndrome                                                  |SNOMED         |
|  40319772|Psoriatic arthritis                                               |SNOMED         |
|   4083682|Psoriatic arthritis with distal interphalangeal joint involvement |SNOMED         |
|   4064048|Psoriatic arthritis with spine involvement                        |SNOMED         |
|   4035742|Psoriatic dactylitis                                              |SNOMED         |
### Psoriasis
#### Concept Set Logic
| conceptId|conceptName |vocabularyId |includeDescendants |isExcluded |includeMapped |
|---------:|:-----------|:------------|:------------------|:----------|:-------------|
|    140168|Psoriasis   |SNOMED       |TRUE               |FALSE      |FALSE         |
#### Included Concepts
| conceptId|conceptName                                                          |vocabularyId   |
|---------:|:--------------------------------------------------------------------|:--------------|
|   4222163|Acrodermatitis continua of Hallopeau                                 |SNOMED         |
|   4033202|Acropustulosis of infancy                                            |SNOMED         |
|   4270746|Actively extending plaque psoriasis                                  |SNOMED         |
|  45773387|Acute generalized exanthematous pustulosis                           |SNOMED         |
|   4299285|Acute generalized pustular flare of preexisting plaque psoriasis     |SNOMED         |
|   4297497|Acute generalized pustular psoriasis de novo                         |SNOMED         |
|   4299281|Acute guttate psoriasis                                              |SNOMED         |
|   4270745|Chronic guttate pattern psoriasis                                    |SNOMED         |
|   4292222|Chronic large plaque psoriasis                                       |SNOMED         |
|   4270744|Chronic small plaque psoriasis                                       |SNOMED         |
|   4299280|Chronic stable plaque psoriasis                                      |SNOMED         |
|   4033785|Circinate and annular pustular psoriasis                             |SNOMED         |
|  37205061|Deficiency of interleukin 36 receptor antagonist                     |SNOMED         |
|   4292228|Drug-exacerbated psoriasis                                           |SNOMED         |
|  37165229|Drug-induced palmoplantar pustular psoriasis                         |SNOMED         |
|   4292230|Early onset psoriasis type 1                                         |SNOMED         |
|   4031648|Eczematized psoriasis                                                |SNOMED         |
|   4307927|Erythrodermic psoriasis                                              |SNOMED         |
|   1340447|Exacerbation of psoriasis                                            |OMOP Extension |
|   1245071|Exacerbation of psoriasis                                            |SNOMED         |
|   4299287|Familial psoriasis                                                   |SNOMED         |
|   4297499|Familial psoriasis with affected first degree relative               |SNOMED         |
|   4270752|Familial psoriasis without affected first degree relative            |SNOMED         |
|   4031645|Flexural psoriasis                                                   |SNOMED         |
|  37165154|Follicular psoriasis                                                 |SNOMED         |
|   4292223|Generalized psoriasis                                                |SNOMED         |
|   4031142|Generalized pustular psoriasis                                       |SNOMED         |
|   4103079|Generalized pustular psoriasis, exanthematous type                   |SNOMED         |
|   4080941|Generalized pustular psoriasis of pregnancy                          |SNOMED         |
|   4270747|Guttate flare of psoriasis with preexisting plaques                  |SNOMED         |
|   4284492|Guttate psoriasis                                                    |SNOMED         |
|   4292225|Hypertrophic palmar psoriasis                                        |SNOMED         |
|   4292226|Hypertrophic palmoplantar psoriasis                                  |SNOMED         |
|   4031143|Infantile pustular psoriasis                                         |SNOMED         |
|   4079734|Juvenile psoriatic arthritis with psoriasis                          |SNOMED         |
|   4033784|Juvenile pustular psoriasis                                          |SNOMED         |
|   4031651|Köbner psoriasis                                                     |SNOMED         |
|   4033783|Lapiere type of psoriasis                                            |SNOMED         |
|   4270751|Late onset psoriasis type 2                                          |SNOMED         |
|   4217927|Localized pustular psoriasis                                         |SNOMED         |
|   4270748|Non-pustular psoriasis of hands                                      |SNOMED         |
|   4292227|Non-pustular psoriasis of hands and feet                             |SNOMED         |
|   4299286|Onset of psoriasis in adolescence (10-20 years)                      |SNOMED         |
|   4297498|Onset of psoriasis in childhood (1-10 years)                         |SNOMED         |
|   4270750|Onset of psoriasis in early adulthood (20-40 years)                  |SNOMED         |
|   4270749|Onset of psoriasis in infancy (<1 year)                              |SNOMED         |
|   4292224|Photoaggravated psoriasis                                            |SNOMED         |
|   4063431|Plaque psoriasis                                                     |SNOMED         |
|  37165457|Plaque psoriasis with pustules                                       |SNOMED         |
|    140168|Psoriasis                                                            |SNOMED         |
|   4066830|Psoriasis annularis                                                  |SNOMED         |
|   4063430|Psoriasis circinata                                                  |SNOMED         |
|   4066485|Psoriasis diffusa                                                    |SNOMED         |
|    605345|Psoriasis exacerbated by human immunodeficiency virus infection      |SNOMED         |
|   4066486|Psoriasis geographica                                                |SNOMED         |
|   4066487|Psoriasis gyrata                                                     |SNOMED         |
|   4066831|Psoriasis inveterata                                                 |SNOMED         |
|  36715780|Psoriasis of anogenital region                                       |SNOMED         |
|   4297496|Psoriasis of face                                                    |SNOMED         |
|   4031649|Psoriasis of nail                                                    |SNOMED         |
|   4299282|Psoriasis of penis                                                   |SNOMED         |
|   4299283|Psoriasis of perianal skin                                           |SNOMED         |
|   4031141|Psoriasis of scalp                                                   |SNOMED         |
|   4299284|Psoriasis of scalp margin                                            |SNOMED         |
|   4223485|Psoriasis of vulva                                                   |SNOMED         |
|   4063433|Psoriasis palmaris                                                   |SNOMED         |
|   4064049|Psoriasis plantaris                                                  |SNOMED         |
|   4066832|Psoriasis punctata                                                   |SNOMED         |
|   4066488|Psoriasis universalis                                                |SNOMED         |
|   4307925|Psoriasis vulgaris                                                   |SNOMED         |
|   4031647|Psoriasis with eczema                                                |SNOMED         |
|   4031140|Psoriatic nail dystrophy                                             |SNOMED         |
|   4031650|Psoriatic nail pitting                                               |SNOMED         |
|   4080939|Psoriatic onycholysis                                                |SNOMED         |
|   4063434|Pustular psoriasis                                                   |SNOMED         |
|  37205057|Pustular psoriasis of palm of hand                                   |SNOMED         |
|   4100184|Pustular psoriasis of palms and soles                                |SNOMED         |
|  37205056|Pustular psoriasis of sole of foot                                   |SNOMED         |
|   4063432|Rupioid psoriasis                                                    |SNOMED         |
|   4093619|Seborrheic psoriasis                                                 |SNOMED         |
|   4031646|Unstable psoriasis                                                   |SNOMED         |
|  36714528|X-linked intellectual disability with seizure and psoriasis syndrome |SNOMED         |
### Arthropathy
#### Concept Set Logic
| conceptId|conceptName            |vocabularyId |includeDescendants |isExcluded |includeMapped |
|---------:|:----------------------|:------------|:------------------|:----------|:-------------|
|     80809|Rheumatoid arthritis   |SNOMED       |TRUE               |FALSE      |FALSE         |
|     81097|Felty's syndrome       |SNOMED       |TRUE               |FALSE      |FALSE         |
|     75897|Polyarthropathy        |SNOMED       |TRUE               |FALSE      |FALSE         |
|     79903|Effusion of joint      |SNOMED       |TRUE               |FALSE      |FALSE         |
|   4153359|Arthritis of spine     |SNOMED       |TRUE               |FALSE      |FALSE         |
|    437082|Ankylosing spondylitis |SNOMED       |TRUE               |FALSE      |FALSE         |
#### Included Concepts
| conceptId|conceptName                                                                                            |vocabularyId   |
|---------:|:------------------------------------------------------------------------------------------------------|:--------------|
|   4034672|Acute infective polyarthritis                                                                          |SNOMED         |
|   4117888|Acute joint effusion                                                                                   |SNOMED         |
|   4179092|Acute polyarthritis                                                                                    |SNOMED         |
|  42535150|Acute polyarticular juvenile idiopathic arthritis                                                      |SNOMED         |
|   4289292|Adult osteochondritis of spine                                                                         |SNOMED         |
|     80804|Allergic arthritis of multiple sites                                                                   |SNOMED         |
|   4323203|Allergic arthritis of spine                                                                            |SNOMED         |
|   4117713|Ankle joint effusion                                                                                   |SNOMED         |
|    437082|Ankylosing spondylitis                                                                                 |SNOMED         |
|  37203959|Ankylosing spondylitis co-occurrent with anterior uveitis                                              |SNOMED         |
|   4035741|Ankylosing spondylitis with multisystem involvement                                                    |SNOMED         |
|   4035614|Ankylosing spondylitis with organ / system involvement                                                 |SNOMED         |
|  37160399|Anti-citrullinated protein antibody positive erosive rheumatoid arthritis                              |SNOMED         |
|    762720|Arthritis due to alkaptonuria                                                                          |SNOMED         |
|  37109064|Arthritis of facet joint of cervical spine                                                             |SNOMED         |
|  37109063|Arthritis of facet joint of lumbar spine                                                               |SNOMED         |
|  37309677|Arthritis of facet joint of thoracic spine                                                             |SNOMED         |
|   1076699|Arthritis of intervertebral joint due to and following immunization                                    |SNOMED         |
|  37170948|Arthritis of joint of spine due to inflammatory bowel disease                                          |SNOMED         |
|   1246675|Arthritis of joint structure of spine caused by Streptococcus                                          |SNOMED         |
|  36714940|Arthritis of lumbosacral spine                                                                         |SNOMED         |
|   4153359|Arthritis of spine                                                                                     |SNOMED         |
|   4033630|Arthritis of temporomandibular joint as part of polyarthritis                                          |SNOMED         |
|   4176931|Arthropathy in Behcet's syndrome of the spine                                                          |SNOMED         |
|   4322887|Arthropathy of multiple joints associated with a neurological disorder                                 |SNOMED         |
|  36716984|Arthropathy of spinal facet joint co-occurrent and due to effusion                                     |SNOMED         |
|   4184046|Atelosteogenesis                                                                                       |SNOMED         |
|  37110773|Atelosteogenesis type 1                                                                                |SNOMED         |
|   4111311|Atelosteogenesis type 2                                                                                |SNOMED         |
|  37117239|Atelosteogenesis type 3                                                                                |SNOMED         |
|  37163922|Autoimmune interstitial lung disease, arthritis syndrome                                               |SNOMED         |
|  36716891|Axial spondyloarthritis                                                                                |SNOMED         |
|    607398|Axial spondyloarthritis with peripheral joint involvement                                              |SNOMED         |
|  46273196|Bacterial arthritis of atlantoaxial joint                                                              |SNOMED         |
|  46273622|Bacterial arthritis of facet joint of cervical spine                                                   |SNOMED         |
|  46273216|Bacterial arthritis of facet joint of lumbar spine                                                     |SNOMED         |
|  46273215|Bacterial arthritis of facet joint of thoracic spine                                                   |SNOMED         |
|    760722|Bacterial arthritis of vertebral column                                                                |SNOMED         |
|    607427|Bacterial spondyloarthritis                                                                            |SNOMED         |
|  36687050|Bilateral effusion of ankle joints                                                                     |SNOMED         |
|  36687052|Bilateral effusion of elbow joints                                                                     |SNOMED         |
|  37169288|Bilateral effusion of joint of feet                                                                    |SNOMED         |
|  37169290|Bilateral effusion of joint of hands                                                                   |SNOMED         |
|  37169289|Bilateral effusion of joint of shoulder regions                                                        |SNOMED         |
|  36686955|Bilateral effusion of joints of knees                                                                  |SNOMED         |
|   1245849|Bilateral intermittent effusion of joint of hips                                                       |SNOMED         |
|  37209321|Bilateral rheumatoid arthritis of feet                                                                 |SNOMED         |
|  37209323|Bilateral rheumatoid arthritis of hands                                                                |SNOMED         |
|  37209322|Bilateral rheumatoid arthritis of knees                                                                |SNOMED         |
|    608810|Bilateral seronegative rheumatoid arthritis of elbow joints                                            |SNOMED         |
|    608809|Bilateral seronegative rheumatoid arthritis of feet                                                    |SNOMED         |
|    608811|Bilateral seronegative rheumatoid arthritis of knees                                                   |SNOMED         |
|    608812|Bilateral seronegative rheumatoid arthritis of wrists                                                  |SNOMED         |
|    603301|Bilateral seropositive rheumatoid arthritis of ankle joints                                            |SNOMED         |
|    609024|Bilateral seropositive rheumatoid arthritis of feet                                                    |SNOMED         |
|    603300|Bilateral seropositive rheumatoid arthritis of hip joints                                              |SNOMED         |
|    603302|Bilateral seropositive rheumatoid arthritis of joint of elbows                                         |SNOMED         |
|    603299|Bilateral seropositive rheumatoid arthritis of knees                                                   |SNOMED         |
|    603298|Bilateral seropositive rheumatoid arthritis of shoulder regions                                        |SNOMED         |
|    608813|Bilateral seropositive rheumatoid arthritis of wrist joint regions                                     |SNOMED         |
|   4109057|Boomerang dysplasia                                                                                    |SNOMED         |
|  36674262|Camptodactyly, arthropathy, coxa-vara, pericarditis syndrome                                           |SNOMED         |
|   4300489|Cervical arthritis                                                                                     |SNOMED         |
|   4067539|Cervical discitis                                                                                      |SNOMED         |
|   4185030|Cervical facet joint effusion                                                                          |SNOMED         |
|   4245641|Chlamydial polyarthritis                                                                               |SNOMED         |
|  37204289|Chondrodysplasia with joint dislocations gPAPP type                                                    |SNOMED         |
|  46270449|Chronic gout of vertebra without tophus caused by drug                                                 |SNOMED         |
|  46270428|Chronic gout of vertebra without tophus due to renal impairment                                        |SNOMED         |
|   4172431|Chronic infective polyarthritis                                                                        |SNOMED         |
|   4115995|Chronic joint effusion                                                                                 |SNOMED         |
|  46270448|Chronic tophaceous gout of vertebra caused by drug                                                     |SNOMED         |
|  46273508|Chronic tophaceous gout of vertebra due to renal impairment                                            |SNOMED         |
|  37110891|CHST3-related skeletal dysplasia                                                                       |SNOMED         |
|   4126944|Circinate balanitis co-occurrent with reactive arthritis triad                                         |SNOMED         |
|   4221664|Circinate vulvovaginitis co-occurrent with reactive arthritis triad                                    |SNOMED         |
|     80806|Climacteric arthritis of multiple sites                                                                |SNOMED         |
|   4179506|Climacteric arthritis of spine                                                                         |SNOMED         |
|   4000061|Clutton's joints                                                                                       |SNOMED         |
|     75617|Degenerative joint disease involving multiple joints                                                   |SNOMED         |
|   4025957|Degenerative polyarthritis                                                                             |SNOMED         |
|   4113729|Desbuquois syndrome                                                                                    |SNOMED         |
|    607413|Destructive spondylopathy                                                                              |SNOMED         |
|   4046205|Discitis                                                                                               |SNOMED         |
|   4035612|Early onset polyarticular juvenile chronic arthritis                                                   |SNOMED         |
|   4117880|Effusion of acromioclavicular joint                                                                    |SNOMED         |
|  37209349|Effusion of bilateral hip joints                                                                       |SNOMED         |
|   1245619|Effusion of bilateral radiocarpal joints                                                               |SNOMED         |
|   4115352|Effusion of distal interphalangeal joint of finger                                                     |SNOMED         |
|   4117882|Effusion of distal radioulnar joint                                                                    |SNOMED         |
|   4117886|Effusion of first metatarsophalangeal joint                                                            |SNOMED         |
|   4117887|Effusion of interphalangeal joint of toe                                                               |SNOMED         |
|     79903|Effusion of joint                                                                                      |SNOMED         |
|     78834|Effusion of joint of hand                                                                              |SNOMED         |
|  36684498|Effusion of joint of left ankle                                                                        |SNOMED         |
|  36684499|Effusion of joint of left elbow                                                                        |SNOMED         |
|  37170940|Effusion of joint of left foot                                                                         |SNOMED         |
|  37207775|Effusion of joint of left hand                                                                         |SNOMED         |
|  36684500|Effusion of joint of left hip                                                                          |SNOMED         |
|  36684501|Effusion of joint of left knee                                                                         |SNOMED         |
|  36684502|Effusion of joint of left shoulder region                                                              |SNOMED         |
|   1244940|Effusion of joint of left wrist region                                                                 |SNOMED         |
|     73851|Effusion of joint of multiple sites                                                                    |SNOMED         |
|   4247710|Effusion of joint of pelvic region                                                                     |SNOMED         |
|  36684503|Effusion of joint of right ankle                                                                       |SNOMED         |
|  36684504|Effusion of joint of right elbow                                                                       |SNOMED         |
|  37170942|Effusion of joint of right foot                                                                        |SNOMED         |
|  37207777|Effusion of joint of right hand                                                                        |SNOMED         |
|  36684505|Effusion of joint of right hip                                                                         |SNOMED         |
|    762253|Effusion of joint of right knee                                                                        |SNOMED         |
|  36684506|Effusion of joint of right shoulder region                                                             |SNOMED         |
|   1244939|Effusion of joint of right wrist region                                                                |SNOMED         |
|     72407|Effusion of joint of shoulder region                                                                   |SNOMED         |
|   1244938|Effusion of joint of wrist region                                                                      |SNOMED         |
|   1244942|Effusion of left radiocarpal joint                                                                     |SNOMED         |
|   4115994|Effusion of lesser metatarsophalangeal joint                                                           |SNOMED         |
|   4115351|Effusion of metacarpophalangeal joint                                                                  |SNOMED         |
|   4117711|Effusion of proximal interphalangeal joint of finger                                                   |SNOMED         |
|   1245226|Effusion of radiocarpal joint                                                                          |SNOMED         |
|   1244941|Effusion of right radiocarpal joint                                                                    |SNOMED         |
|   4117884|Effusion of sacroiliac joint                                                                           |SNOMED         |
|   4117742|Effusion of sternoclavicular joint                                                                     |SNOMED         |
|   4115992|Effusion of subtalar joint                                                                             |SNOMED         |
|   4115993|Effusion of talonavicular joint                                                                        |SNOMED         |
|   4117885|Effusion of tibiofibular joint                                                                         |SNOMED         |
|   4117881|Elbow joint effusion                                                                                   |SNOMED         |
|   1340249|Exacerbation of ankylosing spondylitis                                                                 |OMOP Extension |
|   1340322|Exacerbation of effusion of joint                                                                      |OMOP Extension |
|   1340460|Exacerbation of rheumatoid arthritis                                                                   |OMOP Extension |
|     81097|Felty's syndrome                                                                                       |SNOMED         |
|  37160417|Felty syndrome with seronegative erosive rheumatoid arthritis                                          |SNOMED         |
|  37160421|Felty syndrome with seronegative rheumatoid arthritis                                                  |SNOMED         |
|   4266181|Fibroblastic rheumatism                                                                                |SNOMED         |
|   4179142|Finger joint effusion                                                                                  |SNOMED         |
|   4114444|Flare of rheumatoid arthritis                                                                          |SNOMED         |
|   4185029|Foot joint effusion                                                                                    |SNOMED         |
|  35624445|Ganglion of multiple joints                                                                            |SNOMED         |
|  46270460|Gout of vertebra caused by drug                                                                        |SNOMED         |
|  46273541|Gout of vertebra due to renal impairment                                                               |SNOMED         |
|   4117712|Hip joint effusion                                                                                     |SNOMED         |
|   4184052|Hydrarthrosis of yaws                                                                                  |SNOMED         |
|   4195770|Idiopathic polyarthritis                                                                               |SNOMED         |
|  37162067|Immune dysregulation, inflammatory bowel disease, arthritis, recurrent infection, lymphopenia syndrome |SNOMED         |
|   4067312|Infection of intervertebral disc - pyogenic                                                            |SNOMED         |
|   1246668|Infective arthritis of joint of vertebral column                                                       |SNOMED         |
|   4120327|Infective discitis                                                                                     |SNOMED         |
|   4266078|Infective polyarthritis                                                                                |SNOMED         |
|  42534954|Infective polyarthritis caused by bacteria                                                             |SNOMED         |
|    607400|Inflammation of intervertebral disc caused by fungus                                                   |SNOMED         |
|     74125|Inflammatory polyarthropathy                                                                           |SNOMED         |
|  46273949|Intermittent effusion of joint                                                                         |SNOMED         |
|   1246055|Intermittent effusion of joint of ankle                                                                |SNOMED         |
|   1245846|Intermittent effusion of joint of bilateral ankles                                                     |SNOMED         |
|   1245847|Intermittent effusion of joint of bilateral elbows                                                     |SNOMED         |
|   1245845|Intermittent effusion of joint of bilateral knees                                                      |SNOMED         |
|   1245848|Intermittent effusion of joint of bilateral shoulder regions                                           |SNOMED         |
|   1246056|Intermittent effusion of joint of elbow                                                                |SNOMED         |
|   1245850|Intermittent effusion of joint of left ankle                                                           |SNOMED         |
|   1246127|Intermittent effusion of joint of left elbow                                                           |SNOMED         |
|   1246129|Intermittent effusion of joint of left shoulder region                                                 |SNOMED         |
|   1245851|Intermittent effusion of joint of right ankle                                                          |SNOMED         |
|   1246130|Intermittent effusion of joint of right elbow                                                          |SNOMED         |
|   1246132|Intermittent effusion of joint of right shoulder region                                                |SNOMED         |
|   1246058|Intermittent effusion of joint of shoulder region                                                      |SNOMED         |
|   1246057|Intermittent hydrarthrosis of hip                                                                      |SNOMED         |
|   1246128|Intermittent hydrarthrosis of left hip                                                                 |SNOMED         |
|  37310663|Intermittent hydrarthrosis of left knee                                                                |SNOMED         |
|   1246131|Intermittent hydrarthrosis of right hip                                                                |SNOMED         |
|  37310662|Intermittent hydrarthrosis of right knee                                                               |SNOMED         |
|    607144|Isolated nailfold rheumatoid vasculitis                                                                |SNOMED         |
|     77072|Joint effusion of ankle AND/OR foot                                                                    |SNOMED         |
|   4083681|Juvenile ankylosing spondylitis                                                                        |SNOMED         |
|   4035429|Juvenile reactive arthritis triad                                                                      |SNOMED         |
|   4132810|Juvenile seronegative polyarthritis                                                                    |SNOMED         |
|   4132809|Juvenile seropositive polyarthritis                                                                    |SNOMED         |
|   4079735|Juvenile spondyloarthropathy                                                                           |SNOMED         |
|   4115991|Knee joint effusion                                                                                    |SNOMED         |
|   4094282|Large effusion in suprapatellar pouch                                                                  |SNOMED         |
|  35622774|Larsen-like osseous dysplasia, short stature syndrome                                                  |SNOMED         |
|  35622345|Larsen-like syndrome B3GAT3 type                                                                       |SNOMED         |
|   4272804|Larsen syndrome                                                                                        |SNOMED         |
|  36009832|Laryngeal rheumatoid arthritis                                                                         |MedDRA         |
|   4083558|Late onset polyarticular juvenile chronic arthritis                                                    |SNOMED         |
|    601030|Left ankle seropositive rheumatoid arthritis                                                           |SNOMED         |
|    601031|Left elbow seropositive rheumatoid arthritis                                                           |SNOMED         |
|    605414|Left foot seropositive rheumatoid arthritis                                                            |SNOMED         |
|    601040|Left hip joint seronegative rheumatoid arthritis                                                       |SNOMED         |
|    601042|Left shoulder region seronegative rheumatoid arthritis                                                 |SNOMED         |
|    601043|Left wrist region seronegative rheumatoid arthritis                                                    |SNOMED         |
|    601034|Left wrist region seropositive rheumatoid arthritis                                                    |SNOMED         |
|  36714264|Lethal Larsen-like syndrome                                                                            |SNOMED         |
|   4224167|Lipoid dermatoarthritis                                                                                |SNOMED         |
|     75898|Loose joint body in multiple joints                                                                    |SNOMED         |
|  44783242|Lumbar arthritis                                                                                       |SNOMED         |
|   4067311|Lumbar discitis                                                                                        |SNOMED         |
|   4184087|Lumbar facet joint effusion                                                                            |SNOMED         |
|   4179143|Metatarsophalangeal joint effusion                                                                     |SNOMED         |
|   4009504|Migratory polyarthritis                                                                                |SNOMED         |
|   4095200|Moderate effusion in knee                                                                              |SNOMED         |
|   4109180|Multiple dislocations with dysplasia                                                                   |SNOMED         |
|   4066600|Multiple-level thoracic spondylosis without myelopathy                                                 |SNOMED         |
|  37160367|Mycobacterial discitis                                                                                 |SNOMED         |
|  37169795|Mycobacterial spondyloarthritis                                                                        |SNOMED         |
|   4223486|Nail dystrophy co-occurrent with reactive arthritis triad                                              |SNOMED         |
|   4067532|Neuropathic spondylopathy                                                                              |SNOMED         |
|  37017494|Non-radiographic axial spondyloarthritis                                                               |SNOMED         |
|   1077466|Non-radiographic axial spondyloarthritis of cervical region                                            |SNOMED         |
|   1077336|Non-radiographic axial spondyloarthritis of lumbar and sacral regions                                  |SNOMED         |
|   1077506|Non-radiographic axial spondyloarthritis of lumbar region                                              |SNOMED         |
|   1077446|Non-radiographic axial spondyloarthritis of thoracic and lumbar regions                                |SNOMED         |
|  44811664|Nonspecific polyarthritis                                                                              |SNOMED         |
|   4122761|Oral lesion co-occurrent with reactive arthritis triad                                                 |SNOMED         |
|   4147779|Osteoarthritis of multiple joints                                                                      |SNOMED         |
|     76194|Osteoarthrosis involving multiple sites but not designated as generalized                              |SNOMED         |
|     81945|Palindromic rheumatism of multiple sites                                                               |SNOMED         |
|   1076200|PASS syndrome                                                                                          |SNOMED         |
|     73289|Pathological dislocation of multiple joints                                                            |SNOMED         |
|   4067196|Pneumococcal arthritis and polyarthritis                                                               |SNOMED         |
|   4265764|Polyarthritis associated with another disorder                                                         |SNOMED         |
|    765773|Polyarthritis associated with hemochromatosis                                                          |SNOMED         |
|   4254769|Polyarthritis caused by Erysipelothrix rhusiopathiae                                                   |SNOMED         |
|     75897|Polyarthropathy                                                                                        |SNOMED         |
|   4198076|Polyarthropathy associated with another disorder                                                       |SNOMED         |
|    603008|Polyarticular acute gout caused by lead                                                                |SNOMED         |
|    603005|Polyarticular acute primary gout                                                                       |SNOMED         |
|    603006|Polyarticular chronic gout caused by lead                                                              |SNOMED         |
|    607387|Polyarticular chronic primary gouty arthritis                                                          |SNOMED         |
|  42535177|Polyarticular juvenile idiopathic arthritis                                                            |SNOMED         |
|  37160369|Polyarticular psoriatic arthritis                                                                      |SNOMED         |
|    618647|Polyarticular viral arthritis                                                                          |SNOMED         |
|   4173925|Post-infective polyarthritis                                                                           |SNOMED         |
|  46270474|Primary chronic gout without tophus of vertebra                                                        |SNOMED         |
|   1340523|Progression of rheumatoid arthritis                                                                    |OMOP Extension |
|   4113605|Pseudodiastrophic dysplasia                                                                            |SNOMED         |
|   4064048|Psoriatic arthritis with spine involvement                                                             |SNOMED         |
|     73838|Pyogenic arthritis of multiple sites                                                                   |SNOMED         |
|    761945|Pyogenic bacterial polyarthritis                                                                       |SNOMED         |
|  37171002|Pyogenic infection of cervical intervertebral disc                                                     |SNOMED         |
|  37171003|Pyogenic infection of cervicothoracic intervertebral disc                                              |SNOMED         |
|  37171005|Pyogenic infection of lumbar intervertebral disc                                                       |SNOMED         |
|  37171006|Pyogenic infection of lumbosacral intervertebral disc                                                  |SNOMED         |
|  37171007|Pyogenic infection of sacrococcygeal intervertebral disc                                               |SNOMED         |
|  37171008|Pyogenic infection of thoracic intervertebral disc                                                     |SNOMED         |
|  37171009|Pyogenic infection of thoracolumbar intervertebral disc                                                |SNOMED         |
|  37395567|Reactive arthritis co-occurrent and due to nonspecific urethritis                                      |SNOMED         |
|   4066958|Reactive arthritis of joint of multiple sites due to and following dysentery                           |SNOMED         |
|    765044|Reactive arthritis of spine                                                                            |SNOMED         |
|     78357|Reactive arthritis triad                                                                               |SNOMED         |
|  40483306|Remitting seronegative symmetrical synovitis with pitting edema                                        |SNOMED         |
|   4306357|Rheumatoid aortitis                                                                                    |SNOMED         |
|   4269880|Rheumatoid arteritis                                                                                   |SNOMED         |
|     80809|Rheumatoid arthritis                                                                                   |SNOMED         |
|   4117687|Rheumatoid arthritis - ankle and/or foot                                                               |SNOMED         |
|   4115161|Rheumatoid arthritis - hand joint                                                                      |SNOMED         |
|  37117421|Rheumatoid arthritis in remission                                                                      |SNOMED         |
|   4116149|Rheumatoid arthritis of acromioclavicular joint                                                        |SNOMED         |
|   4116445|Rheumatoid arthritis of ankle                                                                          |SNOMED         |
|  36687005|Rheumatoid arthritis of bilateral ankles                                                               |SNOMED         |
|  36687002|Rheumatoid arthritis of bilateral elbows                                                               |SNOMED         |
|   1245533|Rheumatoid arthritis of bilateral glenohumeral joints                                                  |SNOMED         |
|  36687003|Rheumatoid arthritis of bilateral hips                                                                 |SNOMED         |
|  36686999|Rheumatoid arthritis of bilateral temporomandibular joints                                             |SNOMED         |
|  36687006|Rheumatoid arthritis of bilateral wrists                                                               |SNOMED         |
|   4116439|Rheumatoid arthritis of cervical spine                                                                 |SNOMED         |
|   4114440|Rheumatoid arthritis of distal interphalangeal joint of finger                                         |SNOMED         |
|   4115050|Rheumatoid arthritis of distal radioulnar joint                                                        |SNOMED         |
|   4116440|Rheumatoid arthritis of elbow                                                                          |SNOMED         |
|   4114441|Rheumatoid arthritis of first metatarsophalangeal joint                                                |SNOMED         |
|   4179378|Rheumatoid arthritis of foot                                                                           |SNOMED         |
|   4116150|Rheumatoid arthritis of hip                                                                            |SNOMED         |
|   4114442|Rheumatoid arthritis of interphalangeal joint of toe                                                   |SNOMED         |
|  36683391|Rheumatoid arthritis of joint of spine                                                                 |SNOMED         |
|   4116151|Rheumatoid arthritis of knee                                                                           |SNOMED         |
|  36685017|Rheumatoid arthritis of left ankle                                                                     |SNOMED         |
|  36685018|Rheumatoid arthritis of left elbow                                                                     |SNOMED         |
|  36685019|Rheumatoid arthritis of left foot                                                                      |SNOMED         |
|  42534834|Rheumatoid arthritis of left hand                                                                      |SNOMED         |
|  42534835|Rheumatoid arthritis of left hip                                                                       |SNOMED         |
|  37108590|Rheumatoid arthritis of left knee                                                                      |SNOMED         |
|  35609009|Rheumatoid arthritis of left shoulder                                                                  |SNOMED         |
|  36687001|Rheumatoid arthritis of left temporomandibular joint                                                   |SNOMED         |
|  36685020|Rheumatoid arthritis of left wrist                                                                     |SNOMED         |
|   4116153|Rheumatoid arthritis of lesser metatarsophalangeal joint                                               |SNOMED         |
|   4116442|Rheumatoid arthritis of metacarpophalangeal joint                                                      |SNOMED         |
|   4117686|Rheumatoid arthritis of multiple joints                                                                |SNOMED         |
|   4116443|Rheumatoid arthritis of proximal interphalangeal joint of finger                                       |SNOMED         |
|  36685021|Rheumatoid arthritis of right ankle                                                                    |SNOMED         |
|  36685022|Rheumatoid arthritis of right elbow                                                                    |SNOMED         |
|  36685023|Rheumatoid arthritis of right foot                                                                     |SNOMED         |
|  42534836|Rheumatoid arthritis of right hand                                                                     |SNOMED         |
|  42534837|Rheumatoid arthritis of right hip                                                                      |SNOMED         |
|  37108591|Rheumatoid arthritis of right knee                                                                     |SNOMED         |
|  35609010|Rheumatoid arthritis of right shoulder                                                                 |SNOMED         |
|  36687000|Rheumatoid arthritis of right temporomandibular joint                                                  |SNOMED         |
|  36685024|Rheumatoid arthritis of right wrist                                                                    |SNOMED         |
|   4116444|Rheumatoid arthritis of sacroiliac joint                                                               |SNOMED         |
|   4114439|Rheumatoid arthritis of shoulder                                                                       |SNOMED         |
|   4116148|Rheumatoid arthritis of sternoclavicular joint                                                         |SNOMED         |
|   4116446|Rheumatoid arthritis of subtalar joint                                                                 |SNOMED         |
|   4116152|Rheumatoid arthritis of talonavicular joint                                                            |SNOMED         |
|   4179536|Rheumatoid arthritis of temporomandibular joint                                                        |SNOMED         |
|   4115051|Rheumatoid arthritis of tibiofibular joint                                                             |SNOMED         |
|   4116441|Rheumatoid arthritis of wrist                                                                          |SNOMED         |
|   2107560|Rheumatoid arthritis (RA) disease activity, high (RA)                                                  |CPT4           |
|   2107558|Rheumatoid arthritis (RA) disease activity, low (RA)                                                   |CPT4           |
|   2107559|Rheumatoid arthritis (RA) disease activity, moderate (RA)                                              |CPT4           |
|  42539550|Rheumatoid arthritis with erosion of joint                                                             |SNOMED         |
|   4297651|Rheumatoid arthritis with nailfold and finger-pulp infarcts                                            |SNOMED         |
|   4162539|Rheumatoid arthritis with pneumoconiosis                                                               |SNOMED         |
|  37160562|Rheumatoid arthritis with rheumatoid lung disease                                                      |SNOMED         |
|  35327341|Rheumatoid bursitis                                                                                    |MedDRA         |
|   4103516|Rheumatoid carditis                                                                                    |SNOMED         |
|   4300202|Rheumatoid episcleritis                                                                                |SNOMED         |
|  37160390|Rheumatoid factor and anti-citrullinated protein antibody positive erosive rheumatoid arthritis        |SNOMED         |
|  37160384|Rheumatoid factor and anti-citrullinated protein antibody positive rheumatoid arthritis                |SNOMED         |
|    608043|Rheumatoid factor negative and anti-citrullinated protein antibody negative juvenile polyarthritis     |SNOMED         |
|    608044|Rheumatoid factor negative and anti-citrullinated protein antibody positive juvenile polyarthritis     |SNOMED         |
|    608042|Rheumatoid factor positive and anti-citrullinated protein antibody negative juvenile polyarthritis     |SNOMED         |
|    608041|Rheumatoid factor positive and anti-citrullinated protein antibody positive juvenile polyarthritis     |SNOMED         |
|   4347065|Rheumatoid necrotizing vasculitis                                                                      |SNOMED         |
|   4299308|Rheumatoid neutrophilic dermatitis                                                                     |SNOMED         |
|   4030424|Rheumatoid osteoperiostitis                                                                            |SNOMED         |
|   4296152|Rheumatoid pericarditis                                                                                |SNOMED         |
|   4243509|Rheumatoid scleritis                                                                                   |SNOMED         |
|   4271003|Rheumatoid vasculitis                                                                                  |SNOMED         |
|    601035|Right ankle seropositive rheumatoid arthritis                                                          |SNOMED         |
|    601036|Right elbow seropositive rheumatoid arthritis                                                          |SNOMED         |
|    605413|Right foot seropositive rheumatoid arthritis                                                           |SNOMED         |
|    601045|Right hip joint seronegative rheumatoid arthritis                                                      |SNOMED         |
|    601047|Right shoulder region seronegative rheumatoid arthritis                                                |SNOMED         |
|    601048|Right wrist region seronegative rheumatoid arthritis                                                   |SNOMED         |
|    601038|Right wrist region seropositive rheumatoid arthritis                                                   |SNOMED         |
|   4180469|Sacral arthritis                                                                                       |SNOMED         |
|  37150958|Sacrococcygeal discitis                                                                                |SNOMED         |
|  40479848|Seronegative arthritis of joint of spine                                                               |SNOMED         |
|  37160376|Seronegative erosive rheumatoid arthritis                                                              |SNOMED         |
|   4083556|Seronegative rheumatoid arthritis                                                                      |SNOMED         |
|    603308|Seronegative rheumatoid arthritis in remission                                                         |SNOMED         |
|  37209328|Seronegative rheumatoid arthritis of bilateral hands                                                   |SNOMED         |
|   1245542|Seronegative rheumatoid arthritis of bilateral hip joints                                              |SNOMED         |
|   1076884|Seronegative rheumatoid arthritis of elbow joint                                                       |SNOMED         |
|   1245541|Seronegative rheumatoid arthritis of joint of bilateral shoulder regions                               |SNOMED         |
|    601039|Seronegative rheumatoid arthritis of joint of left ankle                                               |SNOMED         |
|    601044|Seronegative rheumatoid arthritis of joint of right ankle                                              |SNOMED         |
|   1244750|Seronegative rheumatoid arthritis of joint of shoulder region                                          |SNOMED         |
|   1076984|Seronegative rheumatoid arthritis of left elbow joint                                                  |SNOMED         |
|  37207808|Seronegative rheumatoid arthritis of left hand                                                         |SNOMED         |
|    601041|Seronegative rheumatoid arthritis of left knee joint                                                   |SNOMED         |
|  37207809|Seronegative rheumatoid arthritis of multiple joints                                                   |SNOMED         |
|   1076985|Seronegative rheumatoid arthritis of right elbow joint                                                 |SNOMED         |
|  37207810|Seronegative rheumatoid arthritis of right hand                                                        |SNOMED         |
|    601046|Seronegative rheumatoid arthritis of right knee joint                                                  |SNOMED         |
|   4147418|Seropositive erosive rheumatoid arthritis                                                              |SNOMED         |
|   4035611|Seropositive rheumatoid arthritis                                                                      |SNOMED         |
|    603309|Seropositive rheumatoid arthritis in remission                                                         |SNOMED         |
|  37209329|Seropositive rheumatoid arthritis of bilateral hands                                                   |SNOMED         |
|    601033|Seropositive rheumatoid arthritis of joint of left shoulder region                                     |SNOMED         |
|    601037|Seropositive rheumatoid arthritis of joint of right shoulder region                                    |SNOMED         |
|    601032|Seropositive rheumatoid arthritis of left hand                                                         |SNOMED         |
|  37207804|Seropositive rheumatoid arthritis of left hip                                                          |SNOMED         |
|  37207805|Seropositive rheumatoid arthritis of left knee                                                         |SNOMED         |
|  37108714|Seropositive rheumatoid arthritis of multiple joints                                                   |SNOMED         |
|    609061|Seropositive rheumatoid arthritis of right hand                                                        |SNOMED         |
|  37207806|Seropositive rheumatoid arthritis of right hip                                                         |SNOMED         |
|  37207807|Seropositive rheumatoid arthritis of right knee                                                        |SNOMED         |
|  36684998|Seropositive rheumatoid arthritis of shoulder joint                                                    |SNOMED         |
|  37163586|Severe myopia, generalized joint laxity, short stature syndrome                                        |SNOMED         |
|   4066957|Sexually acquired reactive arthritis of multiple sites                                                 |SNOMED         |
|   4066599|Single-level thoracic spondylosis without myelopathy                                                   |SNOMED         |
|   4184086|Spinal effusion                                                                                        |SNOMED         |
|    607428|Spondyloarthritis caused by fungus                                                                     |SNOMED         |
|   3655820|Spondyloarthritis caused by parasite                                                                   |SNOMED         |
|  37168829|Spondyloepimetaphyseal dysplasia with joint laxity, EXOC6B type                                        |SNOMED         |
|  35624206|Spondyloepimetaphyseal dysplasia with multiple dislocations                                            |SNOMED         |
|  37164084|Spondyloepiphyseal dysplasia Stanescu type                                                             |SNOMED         |
|  45765457|Spondyloepiphyseal dysplasia with congenital joint dislocations                                        |SNOMED         |
|    764930|Spondylosis due to another disorder                                                                    |SNOMED         |
|   4084271|Spontaneous joint effusion                                                                             |SNOMED         |
|   4066952|Staphylococcal arthritis and polyarthritis                                                             |SNOMED         |
|   1076990|Staphylococcal arthritis of intervertebral joint                                                       |SNOMED         |
|  37162796|Steel syndrome                                                                                         |SNOMED         |
|   4243832|Subacute infective polyarthritis                                                                       |SNOMED         |
|    607145|Systemic rheumatoid vasculitis                                                                         |SNOMED         |
|   4184084|Temporomandibular joint effusion                                                                       |SNOMED         |
|   4304035|Thoracic arthritis                                                                                     |SNOMED         |
|   4068628|Thoracic discitis                                                                                      |SNOMED         |
|   4181891|Thoracic facet joint effusion                                                                          |SNOMED         |
|     74130|Thoracic spondylosis without myelopathy                                                                |SNOMED         |
|   4184085|Thumb joint effusion                                                                                   |SNOMED         |
|   4095199|Trace effusion in knee                                                                                 |SNOMED         |
|     74724|Transient arthropathy of multiple sites                                                                |SNOMED         |
|     72991|Traumatic arthropathy of multiple sites                                                                |SNOMED         |
|   4085547|Traumatic effusion of joint of elbow                                                                   |SNOMED         |
|   4085548|Traumatic effusion of joint of knee                                                                    |SNOMED         |
|   4136691|Traumatic joint effusion                                                                               |SNOMED         |
|   4067528|Two-level thoracic spondylosis without myelopathy                                                      |SNOMED         |
|   4218311|Undifferentiated inflammatory polyarthritis                                                            |SNOMED         |
|   4311391|Uveitis-rheumatoid arthritis syndrome                                                                  |SNOMED         |
|  37160412|Viral discitis                                                                                         |SNOMED         |
|  37160396|Viral spondyloarthritis                                                                                |SNOMED         |
