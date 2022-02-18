from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .static.data import ref_documents

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    def init_db(db):
        '''Helper function to create the database tables and initiate default values.'''
        from .models import RefCompletion, TopicCompletion
        db.create_all()

        topics = ref_documents['TREC topic'].drop_duplicates().tolist()
        topic_ref = ref_documents.drop('PMID to be assessed', axis=1)
        topic_ref = topic_ref.drop_duplicates()
        list_topic_ref_dicts = topic_ref.to_dict(orient='tight')
        for topic in topics:
            statement = TopicCompletion(
                                topic_id = topic,
                                topic_complete = 0
                                )
            db.session.add(statement)

        for pair in list_topic_ref_dicts['data']:
            statement = RefCompletion(
                                topic_id = pair[0],      
                                ref_pmid = pair[1],
                                ref_complete = 0
                                )
            db.session.add(statement)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            print(error)


    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint)

    with app.app_context():
        init_db(db) # create all tables defined in models

        return app