# Creation of a dataset to judge doc-2-doc relevance assessment

## Input data
We use the [TREC 2005 Genomics track data](https://trec.nist.gov/data/genomics/05/genomics.qrels.large.txt) as raw input data and do some pre-processing to obtain the reference documents and the ones to be assessed against them. The input data is a TSV file with a column of topic numbers, a column of zeros, a column of PMIDS and a column of relevance assessment against the topic (not against another document as we do here). The text corresponding to the topics are found in the [topics narrative file](https://trec.nist.gov/data/genomics/05/adhoc2005narrative.txt).
- [Local copy of the TREC 2005 Genomics track data](../data/input/genomics.qrels.large.txt)
- [Local copy of topics narrative](../data/input/adhoc2005narrative.txt)

## Pre-process
For agreement and evaluation purposes, we do not need to assess every document in the collection. We are also more interested in relevant (either definitely or partially relevant) so we are focusing on those rather than the non-relevant ones which we used more as a control element (i.e., we expect non-relavant doc-2-topic documents to be also non-relevant to other documents in the same topic). We have therefore selected TREC 2005 Genomics track topics with definitely relevant doc-2-topic documents between 10 and 60, using a third of the definitely relevant doc-2-topic documents as candidates for reference documents. Steps are as follows:
- For each TREC topic, get the total numbers of non, partial and definitely doc-2-topic relevant documents
- Keep only those topics with definitely doc-2-topic relevant documents between 10 and 60
- Estimate the number of reference candidates as a third of the number of definitely doc-2-topic relevant documents

In the following table we show the selected TREC topics for our doc-2-doc relevanc assessment task. also available as a TSV file.
- [TSV file with selected TREC topics for our doc-2-doc relevanc assessment task](../data/input/selected_trec_topics.tsv)

|	Topic	|	Non	|	Partial	|	Def	|	Reference candidates	|
|	:---:	|	:---:	|	:---:	|	:---:	|	:---:	|
|	100	|	630	|	52	|	22	|	7	|
|	106	|	1061	|	125	|	44	|	14	|
|	116	|	1179	|	28	|	58	|	19	|
|	118	|	905	|	12	|	20	|	6	|
|	119	|	528	|	19	|	42	|	14	|
|	121	|	380	|	25	|	17	|	5	|
|	122	|	815	|	37	|	19	|	6	|
|	128	|	880	|	53	|	21	|	7	|
|	129	|	949	|	22	|	16	|	5	|
|	137	|	1078	|	39	|	12	|	4	|
|	139	|	345	|	20	|	15	|	5	|
|	140	|	366	|	15	|	14	|	4	|
|	141	|	439	|	47	|	34	|	11	|

## Creation of a dataset ready for doc-2-doc relevance assessment
Here we describe at a high level the steps required to create a dataset that will be later used by annotators to do the doc-2-doc relevance assessments using the reference documents.
- For each [selected TREC topic](../data/input/selected_trec_topics.tsv), randomly select the reference documents, i.e., PMIDs, from those marked as "definitely relevant (2)" in the [TREC assessment list](../data/input/genomics.qrels.large.txt). Keep the TREC topic number so you end up with a two-column TSV file, first column for TREC topic, second column for reference PMID. Let's call this file topic_reference_pmid.tsv
- For each reference PMID from the previous step, from the same TREC topic, randomly select 20 documents for which the relevance against the reference document will be assessed. To select those 20 documents, first randomly select 6 to 9 TREC PMIDs marked as "definitely relevant (2)" and then 6 to 9 "partially relevant (1)". Randomly select as many "non-relevant (0)" to complete the 20 documents. You will end up with a TSV file with 3 columns, first column for the TREC topic, second column for the PMID reference document, and third column for a PMID to be assessed. Let's call this file topic_reference_and_documents.tsv
- Order the topic_reference_and_documents.tsv file by the first column, then the second and then the third. Save the order dataset using the same number.

## PMID data
For the user interface, we will need title and abstract for all reference and to-be-assessed documents. We have already obtained that information from Medline and have them available as a TSV file with columns PMID, title and abstract.

## Relevance assessment user interface
Here we describe at a high level the user interface used by annotators to produce the relevance assessment using as input the topic_reference_and_documents.tsv file
- Each annotator will be given a login and password details that will be kept encrypted. At this point, we do not need something too elaborated so features such as recovering and changing the password are nice to have but not a must.
- We need the relevance assessmente to be roughly coordinated across different annotators so we will present them with the relevance assessment tasks in the order of the file. Once an annotator enters the interface, the system presents a relevance assesment task for one reference PMID only
  - The reference PMID is the first one in the file that has not been yet done/fully processed
  - The information presented to the researcher includes the TREC topic narrative as a context, the reference PMID together with title and abstract, and a list of the to-be-assessed documents including their PMID, title, abstract and a text box to enter the relevance (2, 1, or 0)
  - The annotator should be able to save the entered relevance assements at any time
  - The relevance assessments should not be modified once they have entered but we will allowed edition in case of mistyping
  - Once all of the to-be-assessed documents for the displayed reference document have been assessed (all of the assessment text box have a value), the annotator will mark the task as done/fully processed for that reference document. The system will record the reference document as done/fully processed
  - The system will present the next not done/fully processed reference document to the annotator
