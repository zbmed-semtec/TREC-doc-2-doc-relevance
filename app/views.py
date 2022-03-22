from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from .models import Evaluation, RefCompletion, TopicCompletion
from . import db
from .static.data.data import TREC_corpus, topics, ref_documents

views = Blueprint("views", __name__)


@views.route("/")
def home_page():
    return render_template("home_page.html")


@views.route("/topics")
@login_required
def topic_overview():
    topics_overview = topics.set_index("id")
    topicsList = topics["id"].tolist()
    # Check which topics are evaluated completely
    topicCompl = TopicCompletion.query.filter(
        TopicCompletion.topic_complete == 1, TopicCompletion.user_id == current_user.id
    ).all()
    completed_topics = [topics.topic_id for topics in topicCompl]

    return render_template(
        "topics_overview.html",
        topics=topics_overview,
        topicsList=topicsList,
        completed_topics=completed_topics,
        name=current_user.name,
    )


@views.route("/<int:topic_id>")
@login_required
def topic(topic_id):
    topic_description = topics["desc"][topics["id"] == str(topic_id)].reset_index(
        drop=True
    )
    topic_desc = topic_description[0]
    article_list = ref_documents["PMID reference document"][
        ref_documents["TREC topic"] == topic_id
    ]
    article_list = list(set(article_list))
    # Check which reference articles are evaluated completely
    refCompl = RefCompletion.query.filter(
        RefCompletion.ref_complete == 1, RefCompletion.user_id == current_user.id
    ).all()
    completed_refArticles = [ref_article.ref_pmid for ref_article in refCompl]

    if set(article_list).issubset(completed_refArticles):
        # Check which topics are evaluated completely
        topicCompl = TopicCompletion.query.filter(
            TopicCompletion.topic_complete == 1, TopicCompletion.user_id == current_user.id
        ).all()
        completed_topics = [topics.topic_id for topics in topicCompl]

        # Check if topic is already in the database. Add if not found
        if topic_id not in completed_topics:
            addTopicCompletion = TopicCompletion(
                topic_id=topic_id, user_id=current_user.id, topic_complete=1
            )
            db.session.add(addTopicCompletion)
            try:
                db.session.commit()
            except Exception as error:
                db.session.rollback()
                print(error)
                pass
    return render_template(
        "topic.html",
        topic=topic_desc,
        topic_id=topic_id,
        article_list=article_list,
        TREC_corpus=TREC_corpus,
        name=current_user.name,
        completed_refArticles=completed_refArticles,
    )


@views.route("/<int:topic_id>/<int:ref_pmid>", methods=["GET", "POST"])
@login_required
def ref_article(ref_pmid, topic_id):
    topic_description = topics["desc"][topics["id"] == str(topic_id)].reset_index(
        drop=True
    )
    topic_desc = topic_description[0]
    ref_article_list = list(
        set(
            ref_documents["PMID to be assessed"][
                ref_documents["PMID reference document"] == ref_pmid
            ]
        )
    )
    ref_title = TREC_corpus.at[ref_pmid, "title"]
    ref_abstract = TREC_corpus.at[ref_pmid, "abstract"]
    refList_chunked = [
        ref_article_list[i : i + 3] for i in range(0, len(ref_article_list), 3)
    ]
    # check if there already is a evaluation score in the database:
    try:
        userEval = Evaluation.query.filter(
            Evaluation.topic_id == topic_id,
            Evaluation.ref_pmid == ref_pmid,
            Evaluation.user_id == current_user.id,
        ).all()
        evaluated_articles = []
        for evaluations in userEval:
            evaluated_articles.append(evaluations.eval_pmid)
    except:
        evaluated_articles = []
    return render_template(
        "ref_article.html",
        topic=topic_desc,
        topic_id=topic_id,
        ref_pmid=ref_pmid,
        title=ref_title,
        abstract=ref_abstract,
        article_list=refList_chunked,
        evaluated_articles=evaluated_articles,
        TREC_corpus=TREC_corpus,
        name=current_user.name,
    )


@views.route("/<int:topic_id>/<int:ref_pmid>/<int:pmid>", methods=["GET", "POST"])
@login_required
def assessment_article(pmid, ref_pmid, topic_id):
    topic_description = topics["desc"][topics["id"] == str(topic_id)].reset_index(
        drop=True
    )
    topic_desc = topic_description[0]
    article_list = list(
        set(
            ref_documents["PMID to be assessed"][
                ref_documents["PMID reference document"] == ref_pmid
            ]
        )
    )
    index_active = article_list.index(pmid)
    article_title = TREC_corpus.at[pmid, "title"]
    article_abstract = TREC_corpus.at[pmid, "abstract"]
    # check how many articles were already evaluated:
    try:
        userEval = Evaluation.query.filter(
            Evaluation.topic_id == topic_id,
            Evaluation.ref_pmid == ref_pmid,
            Evaluation.user_id == current_user.id,
        ).all()
        evaluated_articles = []
        for evaluations in userEval:
            evaluated_articles.append(evaluations.eval_pmid)
    except:
        evaluated_articles = []
    # check if there already is a evaluation score for pmid in the database:
    try:
        userEval = Evaluation.query.filter(
            Evaluation.topic_id == topic_id,
            Evaluation.ref_pmid == ref_pmid,
            Evaluation.eval_pmid == pmid,
            Evaluation.user_id == current_user.id,
        ).first_or_404()
        eval_score = userEval.eval_score
    except:
        eval_score = None

    @views.before_request
    def checkRemaining():
        remaining_articles = [
            pmid for pmid in article_list if pmid not in evaluated_articles
        ]
        return remaining_articles

    percent_complete = round((len(evaluated_articles) / len(article_list) * 100))
    remaining_articles = checkRemaining()
    if request.method == "POST":
        if (eval_score == None) & (pmid not in evaluated_articles):
            eval_score = request.form.get("evaluation")
            evaluation = Evaluation(
                topic_id=topic_id,
                ref_pmid=ref_pmid,
                eval_pmid=pmid,
                eval_score=eval_score,
                user_id=current_user.id,
            )
            db.session.add(evaluation)
        else:
            eval_score = request.form.get("evaluation")
            userEval.eval_score = eval_score
        try:
            db.session.commit()
            try:
                remaining_articles.remove(pmid)
            except:
                pass
            if len(remaining_articles) > 0:
                print(remaining_articles)
                next_pmid = remaining_articles[0]
                return redirect(
                    url_for(
                        "views.assessment_article",
                        topic_id=topic_id,
                        ref_pmid=ref_pmid,
                        pmid=next_pmid,
                    )
                )
            else:
                addRefCompletion = RefCompletion(
                    topic_id=topic_id,
                    ref_pmid=ref_pmid,
                    user_id=current_user.id,
                    ref_complete=1,
                )
                db.session.add(addRefCompletion)

                try:
                    db.session.commit()
                except Exception as error:
                    db.session.rollback()
                    print(error)
                    pass

                return redirect(
                    url_for("views.ref_article", topic_id=topic_id, ref_pmid=ref_pmid)
                )
        except Exception as error:
            db.session.rollback()
            print(error)

    return render_template(
        "article.html",
        topic=topic_desc,
        topic_id=topic_id,
        title=article_title,
        abstract=article_abstract,
        pmid=pmid,
        ref_pmid=ref_pmid,
        article_list=article_list,
        evaluated_articles=evaluated_articles,
        remaining_articles=remaining_articles,
        TREC_corpus=TREC_corpus,
        index_active=index_active,
        percent_complete=percent_complete,
        name=current_user.name,
        eval_score=eval_score,
    )
