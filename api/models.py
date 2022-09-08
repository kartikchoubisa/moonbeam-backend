from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Discussion(db.Model):
    __tablename__ = 'discussion'
    proposal_url = db.Column(db.String(100), primary_key=True)
    comments = db.relationship('Comment', backref='discussion', cascade='all, delete', lazy=True)

    def __repr__(self):
        return f"Discussion('{self.proposal_url=}', '{self.comments=}')"

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    author_address = db.Column(db.String(100), nullable=False)
    discussion_proposal_url = db.Column(db.Integer, db.ForeignKey('discussion.proposal_url'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.content=}', '{self.author_address=}, '{self.discussion_proposal_url=}')"

class DiscussionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Discussion
        # include_relationships = True

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        # include_fk = True
    # discussion = ma.Nested(DiscussionSchema)
