import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Evaluation
from . import db

views = Blueprint('views', __name__)

topics = pd.read_csv('data/output/test_adhoc2005narrative.tsv', sep='\t', header=0, names=['id', 'desc'], dtype='str')
topics = topics.dropna()
ref_documents = pd.read_csv('data/output/topic_reference_and_documents.tsv', sep='\t', header=0)
TREC_corpus = pd.read_csv('data/output/TREC_test_corpus.tsv', sep='\t', header=0)
TREC_corpus = TREC_corpus.set_index('PMID')
TREC_corpus['title'] = TREC_corpus['title'].astype('str')
TREC_corpus['abstract'] = TREC_corpus['abstract'].astype('str')


@views.route('/')
def home_page():
       return render_template('home_page.html') 

@views.route('/topics')
@login_required
def topic_overview():
        topics_overview = topics.set_index('id')
        topicsList = topics['id'].tolist()
        return render_template('topics_overview.html', topics=topics_overview, topicsList=topicsList, name=current_user.name)

@views.route('/<int:topic_id>')
@login_required
def topic(topic_id):
        topic_description = topics['desc'][topics['id']==str(topic_id)].reset_index(drop=True)
        topic_desc = topic_description[0]
        article_list = ref_documents['PMID reference document'][ref_documents['TREC topic'] == topic_id]
        article_list = list(set(article_list))
        # Check if article is in Trec Corpus and drop if not
        for article in article_list:
                if article not in list(set(TREC_corpus.index.values.tolist())):
                        article_list.remove(article)
        return render_template('topic.html', topic=topic_desc, topic_id = topic_id, article_list=article_list, TREC_corpus = TREC_corpus, name=current_user.name)


@views.route('/<int:topic_id>/<int:ref_pmid>', methods=['GET', 'POST'])
@login_required
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
         # check if there already is a evaluation score in the database:
        try:
                userEval = Evaluation.query.filter(
                                                Evaluation.topic_id == topic_id,
                                                Evaluation.ref_pmid == ref_pmid,
                                                Evaluation.user_id == current_user.id).all()
                evaluated_articles = []
                for evaluations in userEval:
                        evaluated_articles.append(evaluations.eval_pmid)
        except: 
                evaluated_articles = []
        return render_template(
                        'ref_article.html', 
                        topic=topic_desc, 
                        topic_id=topic_id, 
                        ref_pmid=ref_pmid, 
                        title=ref_title, 
                        abstract=ref_abstract, 
                        article_list=docList_chunked, 
                        evaluated_articles=evaluated_articles, 
                        TREC_corpus = TREC_corpus, 
                        name=current_user.name
                        )

@views.route('/<int:topic_id>/<int:ref_pmid>/<int:pmid>', methods=['GET', 'POST'])
@login_required
def assessment_article(pmid, ref_pmid, topic_id):
        topic_description = topics['desc'][topics['id']==str(topic_id)].reset_index(drop=True)
        topic_desc = topic_description[0]
        documents_to_asses = ref_documents['PMID to be assessed'][ref_documents['PMID reference document']==ref_pmid]
        docSet = set(documents_to_asses)
        article_list = list(docSet)
        for article in article_list:
                if article not in list(set(TREC_corpus.index.values.tolist())):
                        article_list.remove(article)
        n_articles = len(article_list)
        index_active = article_list.index(pmid)
        index_previous = index_active - 1
        index_next = index_active + 1
        percent_complete =round(((index_active+1)/n_articles)*100)
        article_title = TREC_corpus.at[pmid, 'title']
        article_abstract = TREC_corpus.at[pmid, 'abstract']
        # check if there already is a evaluation score in the database:
        try:
                userEval = Evaluation.query.filter(
                                                Evaluation.topic_id == topic_id,
                                                Evaluation.ref_pmid == ref_pmid,
                                                Evaluation.eval_pmid == pmid,
                                                Evaluation.user_id == current_user.id).first()
                eval_score = userEval.eval_score
        except: 
                eval_score = None
        if request.method == "POST":
                db.create_all()
                if eval_score == None:
                        eval_score = request.form.get('evaluation')
                        evaluation = Evaluation(
                                        topic_id=topic_id, 
                                        ref_pmid=ref_pmid, 
                                        eval_pmid=pmid, 
                                        eval_score=eval_score,
                                        user_id = current_user.id
                                        )
                        db.session.add(evaluation)
                else:
                        eval_score = request.form.get('evaluation')
                        userEval.eval_score = eval_score
                try:
                        db.session.commit()
                        return redirect(
                                url_for(
                                        "views.assessment_article", 
                                        topic_id=topic_id, 
                                        ref_pmid=ref_pmid, 
                                        pmid=article_list[index_next]
                                        ))
                except Exception as error:
                        db.session.rollback()
                        print(error)
                        pass


        return render_template(
                                "article.html", 
                                topic=topic_desc, 
                                topic_id=topic_id, 
                                title=article_title, 
                                abstract=article_abstract, 
                                pmid=pmid, 
                                ref_pmid=ref_pmid, 
                                article_list=article_list,
                                TREC_corpus = TREC_corpus, 
                                n_articles=n_articles, 
                                index_active=index_active, 
                                index_previous=index_previous, 
                                index_next=index_next, 
                                percent_complete=percent_complete, 
                                name=current_user.name,
                                eval_score=eval_score)




