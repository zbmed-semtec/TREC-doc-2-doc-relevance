  [![DOI](https://zenodo.org/badge/451905367.svg)](https://zenodo.org/badge/latestdoi/451905367)
  
# TREC-doc-2-doc-relevance
The code, data and docs at this repo aim at facilitating the creation of a doc-2-doc relevance assessment on PMIDs used in the TREC 2005 Genomics track. A doc-2-doc relevance assessment takes one document as reference and assess a second document regarding its relevance to the reference one. This doc-2-doc collection will be used to evaluate the doc-2-doc recommendations approaches that we are working on.

The TREC 2005 Genomics track corresponds to document-2-topic relevance assessment. Our assumption is that articles relevant to a topic will be more relevant to each other that those which are not relevant to the topic. This premise has been used before in previous approaches <REF>. With this TREC-doc-2-doc-relevance project, we want to double check this assumption by creating a doc-2-doc relevance assessment corpus based on TREC 2005 Genomics track.

The doc-2-doc relevance assessment is done as follows. Given a topic of research interest, a researcher has found an article they are interested in and want to explore the subject further. To do so, the researcher should select some other articles con continue their research. The researcher is presented with 20 documents that should be assessed. Only title and abstract are available to the researcher. The relevance assessment possible values are as follows:
- Definitely relevant to the reference article, meaning "Yes, the researcher wants to get a hold of the full-text as it is definitely relevant to their research"
- Partially relevant to the reference article, meaning "Looks promising but not sure yet. The researcher will keep the PMID just in case, as a maybe"
- Non-relevant to the reference articel, meaning "Not worth to give it a second look at all"

## Input data
We use the [TREC 2005 Genomics track data](https://trec.nist.gov/data/genomics/05/genomics.qrels.large.txt) as raw input data and do some pre-processing to obtain the reference documents and the ones to be assessed against them. The input data is a TSV file with a column of topic numbers, a column of zeros, a column of PMIDS and a column of relevance assessment against the topic (not against another document as we do here). The text corresponding to the topics are found in the [topics narrative file](https://trec.nist.gov/data/genomics/05/adhoc2005narrative.txt).

## Process
We first select some of the TREC topics for us to create a dataset for doc-2-doc relevance assessment. This dataset is used by annotators to enter their relevance assessment to we end up with a doc-2-doc relevance assessment corpus.

## Output data
Our final output is a doc-2-doc relevance assesment corpus corresonding to a TSV file with the following columns:
- Original TREC topic
- Reference PMID
- Assessed PMID
- Relevance assessment (2 definitely relevant, 1 partially relevant, 0 non-relevant)

# Citation
If you want to cite this repository please get the citation data for the corresponding release in [Zenodo](https://zenodo.org/record/7341391).

If you want to cite the data used in our doc-2-doc relevance assessment, you an find the corresponding [dataset in Zenodo](https://zenodo.org/record/7324822).
  
If you want to cite the data for the Fleiss Kappa analysis, it is also [available in Zenodo](https://zenodo.org/record/7338056).
  
The contribution to this repository has been as follows:
* Muhammad Talha is the main developer of this repository
* Lukas Geist and Tim Fellerhoff contributed to the extraction of titles and abstracts used in the corpus
* Rohitha Ravinder and Leyla Jael Castro contributed to the data pre-processing to obtain the assessment crorpus
* Olga Giraldo contributed to testing and validation of the interface
* Dietrich Rebholz-Schumann and Leyla Jael Castro conceptualized this work

