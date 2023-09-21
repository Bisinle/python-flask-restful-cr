#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "newsletter": "it's a beautiful 108 out   in Austin today"
        }
        return make_response(response_dict,200)
    
api.add_resource(Home, '/')

class Newsletters(Resource):
    def get(self):
        newsletter_dict_list = [nletter.to_dict() for nletter in Newsletter.query.all()]
        return make_response(newsletter_dict_list,200)

    def post(self):
        newsletter = Newsletter(
                title = request.form['title'],
                body=request.form['body']              
        )
        db.session.add(newsletter)
        db.session.commit()

        newsletter_dict = newsletter.to_dict()

        return make_response( newsletter_dict,201)
    
    
api.add_resource(Newsletters, '/newsletters')



class Newsletter_by_id(Resource):

    def get(self,id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        newsletter_dict = newsletter.to_dict()

        return make_response(newsletter_dict,200)


api.add_resource(Newsletter_by_id,'/newsletter/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
