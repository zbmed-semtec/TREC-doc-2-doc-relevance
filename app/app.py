import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

topics = pd.read_csv('../data/output/test_adhoc2005narrative.tsv', sep='\t', header=0, names=['id', 'desc'], dtype='str')
topics = topics.dropna()
ref_documents = pd.read_csv('../data/output/topic_reference_and_documents.tsv', sep='\t', header=0)
TREC_corpus = pd.read_csv('../data/output/TREC_test_corpus.tsv', sep='\t', header=0)
TREC_corpus = TREC_corpus.set_index('PMID')
TREC_corpus['title'] = TREC_corpus['title'].astype('str')
TREC_corpus['abstract'] = TREC_corpus['abstract'].astype('str')


@app.route('/')
@app.route('/topics')
def topic_overview():
        topics_overview = topics.set_index('id')
        topicsList = topics['id'].tolist()
        return render_template('topics_overview.html', topics=topics_overview, topicsList=topicsList)

@app.route('/<int:topic_id>')
def topic(topic_id):
        topic_description = topics['desc'][topics['id']==str(topic_id)].reset_index(drop=True)
        topic_desc = topic_description[0]
        article_list = ref_documents['PMID reference document'][ref_documents['TREC topic'] == topic_id]
        article_list = list(set(article_list))
        # Check if article is in Trec Corpus and drop if not
        for article in article_list:
                if article not in list(set(TREC_corpus.index.values.tolist())):
                        article_list.remove(article)
        return render_template('topic.html', topic=topic_desc, topic_id = topic_id, article_list=article_list, TREC_corpus = TREC_corpus)


@app.route('/<int:topic_id>/<int:ref_pmid>', methods=['GET', 'POST'])
def ref_article(ref_pmid, topic_id):
        topic_description = topics['desc'][topics['id']==str(topic_id)].reset_index(drop=True)
        topic_desc = topic_description[0]
        documents_to_asses = ref_documents['PMID to be assessed'][ref_documents['PMID reference document']==ref_pmid]
        docSet = set(documents_to_asses)
        docList = list(docSet)
        ref_title = TREC_corpus.at[ref_pmid, 'title']
        ref_abstract = TREC_corpus.at[ref_pmid, 'abstract']
        # Check if article is in Trec Corpus and drop if not
        for article in docList:
                if article not in list(set(TREC_corpus.index.values.tolist())):
                        docList.remove(article)
        docList_chunked = [docList[i:i + 4] for i in range(0, len(docList), 4)] 
        
        return render_template('ref_article.html', topic=topic_desc, topic_id=topic_id, ref_pmid=ref_pmid, title=ref_title, abstract=ref_abstract, article_list=docList_chunked, TREC_corpus = TREC_corpus)

@app.route('/<int:topic_id>/<int:ref_pmid>/<int:pmid>', methods=['GET', 'POST'])
def assessment_article(pmid, ref_pmid, topic_id):
        topic_description = topics['desc'][topics['id']==str(topic_id)].reset_index(drop=True)
        topic_desc = topic_description[0]
        documents_to_asses = ref_documents['PMID to be assessed'][ref_documents['PMID reference document']==ref_pmid]
        docSet = set(documents_to_asses)
        docList = list(docSet)
        for article in docList:
                if article not in list(set(TREC_corpus.index.values.tolist())):
                        docList.remove(article)
        n_articles = len(docList)
        index_active = docList.index(pmid)
        index_previous = index_active - 1
        index_next = index_active + 1
        percent_complete =round(((index_active+1)/n_articles)*100)
        article_title = TREC_corpus.at[pmid, 'title']
        article_abstract = TREC_corpus.at[pmid, 'abstract']
        return render_template("article.html", topic=topic_desc, topic_id=topic_id, title=article_title, abstract=article_abstract, pmid=pmid, ref_pmid=ref_pmid, article_list=docList, TREC_corpus = TREC_corpus, n_articles=n_articles, index_active=index_active, index_previous=index_previous, index_next=index_next, percent_complete=percent_complete)

@app.route("/login")
def login():
        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)



