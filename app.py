from flask import Flask
from api.routes import api_blueprint
from api.models import db
import logging


def create_app():

    logging.basicConfig(level=logging.INFO)
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'mysecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    config = 'development'


    app.register_blueprint(api_blueprint, url_prefix='/api')

    db.init_app(app)
    from api.models import Comment
    with app.app_context():
        db.create_all()

    if config == 'production':
        ...

    elif config == 'testing':
        ...

    elif config == 'development':
        # TODO: Add development config
        ...


        # testing db
        # with app.app_context():
        #     logging.info("testing comment")
        #
        #     comment = Comment(content='Hello World')
        #     db.session.add(comment)
        #     db.session.commit()
        #     print(Comment.query.all())
        #
        #     db.session.delete(comment)
        #     db.session.commit()
        #     assert Comment.query.all() == []
        #
        #     logging.info("testing comment done")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
