import pytest
import flask_testing

from app import create_app
from api.models import db
from api.models import Discussion, Comment
from api.models import CommentSchema, DiscussionSchema

@pytest.fixture()
def app():
    app = create_app()
    # config is same

    yield app

    #cleanup
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def create_random_comment(num = 1):
    comment1 = Comment(content='I like this proposal', author_address='0x123', discussion_proposal_url = "https://distributed-proposal1")
    comment2 = Comment(content='meh', author_address='0x333', discussion_proposal_url = "https://distributed-proposal1")
    if num == 1:
        return comment1
    else:
        return [comment1, comment2]

def create_random_discussion(num = 1):
    discussion1 = Discussion(proposal_url = "https://distributed-proposal1")
    discussion2 = Discussion(proposal_url = "https://distributed-proposal2")
    if num == 1:
        return discussion1
    else:
        return [discussion1, discussion2]

def create_random_discussion_with_comments(num = 1):
    discussion1 = Discussion(proposal_url = "https://distributed-proposal1")
    comment1, comment2 = create_random_comment(2)
    discussion1.comments.append(comment1)
    discussion1.comments.append(comment2)

    discussion2 = Discussion(proposal_url = "https://distributed-proposal2")
    if num == 1:
        return discussion1
    else:
        return [discussion1, discussion2]

def test_comment_model(app):
    print("testing comment")

    comment = create_random_comment()
    with app.app_context():
        #add comment
        db.session.add(comment)
        db.session.commit()
        print(Comment.query.all())
        assert Comment.query.all() == [comment]

        # remove comment
        db.session.delete(comment)
        db.session.commit()
        assert Comment.query.all() == []

        print("successfully tested comment")

def test_discussion_model(app):
    print("testing discussion")

    with app.app_context():
        discussion = create_random_discussion_with_comments()
        db.session.add(discussion)
        db.session.commit()
        print(Discussion.query.all())
        assert Discussion.query.all() == [discussion]

        # remove discussion
        db.session.delete(discussion)
        db.session.commit()
        assert Discussion.query.all() == []
        assert Comment.query.all() == []

        print("successfully tested discussion")



def test_route_get_discussion(app, client):
    print('testing route get discussion')
    response = client.get('/api/discussions').get_json()
    print(response)
    assert response == {'discussions': []}

    with app.app_context():
        discussion = create_random_discussion_with_comments()
        db.session.add(discussion)
        db.session.commit()
        print(Discussion.query.all())
        response = client.get('/api/discussions').get_json()
        print(response)


        db.session.delete(discussion)
        db.session.commit()
        assert Discussion.query.all() == []

        print('successfully tested route get discussion')
