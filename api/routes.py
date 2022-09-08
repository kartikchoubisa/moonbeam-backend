from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from .models import Comment as CommentModel, Discussion as DiscussionModel
from .models import CommentSchema, DiscussionSchema
from .models import db
import logging

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

@api_blueprint.route('/')
def api_home():
    return 'API works'

class Discussion(Resource):
    def get(self, discussion_proposal_url):
        try:
            discussion = DiscussionModel.query.filter_by(proposal_url=discussion_proposal_url).first()
            if discussion is None:
                return jsonify({'message': 'Discussion not found'}), 404
            # get all comments for discussion
            comments = CommentModel.query.filter_by(discussion_proposal_url=discussion_proposal_url).all()
            comments_schema = CommentSchema(many=True)
            comments_data = comments_schema.dump(comments)
            discussion_schema = DiscussionSchema()
            discussion_data = discussion_schema.dump(discussion)
            discussion_data['comments'] = comments_data
            return jsonify({'discussion': discussion_data})
        except:
            return jsonify({'message': 'An error occurred'}), 500

    def post(self, discussion_proposal_url):
        try:
            discussion = DiscussionModel.query.filter_by(proposal_url=discussion_proposal_url).first()
            if discussion is None:
                return jsonify({'message': 'Discussion not found'}), 404
            # add comment to discussion
            content = request.json['content']
            author_address = request.json['author_address']
            comment = CommentModel(content=content, author_address=author_address, discussion_proposal_url=discussion_proposal_url)
            db.session.add(comment)
            db.session.commit()
            return jsonify({'message': 'Comment added'})
        except:
            return jsonify({'message': 'An error occurred'}), 500

class DiscussionsList(Resource):
    def get(self):
        discussions = DiscussionModel.query.all()
        discussion_schema = DiscussionSchema(many=True)
        output = discussion_schema.dump(discussions)
        return {'discussions': output}, 200

    def post(self):
        # creating a new discussion whenever a new proposal is added
        if not request.json:
            return jsonify({'message': 'No input data provided'}), 400

        proposal_url = request.json['proposal_url']

        # check if discussion already exists
        discussion = DiscussionModel.query.filter_by(proposal_url=proposal_url).first()
        if discussion is not None:
            return jsonify({'message': 'Discussion already exists'}), 400

        discussion = DiscussionModel(proposal_url=proposal_url)
        db.session.add(discussion)
        db.session.commit()
        return {'message': 'new discussion created'}, 201

api.add_resource(DiscussionsList, '/discussions')
api.add_resource(Discussion, '/discussions/<path:discussion_proposal_url>')


