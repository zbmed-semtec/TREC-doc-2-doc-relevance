import pandas as pd

topics = pd.read_csv(
    "app/static/data/test_adhoc2005narrative.tsv",
    sep="\t",
    header=0,
    names=["id", "desc"],
    dtype="str",
)
ref_documents = pd.read_csv(
    "app/static/data/topic_reference_and_documents.tsv", sep="\t", header=0
)
TREC_corpus = pd.read_csv("app/static/data/TREC_test_corpus.tsv", sep="\t", header=0)
ref_documents = ref_documents[
    ref_documents["PMID to be assessed"].isin(TREC_corpus["PMID"])
]  # Drop all articles where we dont have a title or article
TREC_corpus = TREC_corpus.set_index("PMID")
TREC_corpus["title"] = TREC_corpus["title"].astype("str")
TREC_corpus["abstract"] = TREC_corpus["abstract"].astype("str")
