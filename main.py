from flask import Flask
from Requests import courses_request
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
API = Api(app)

# Fall 2022 Term Code
term = "1229"

courses_put_args = reqparse.RequestParser()
courses_put_args.add_argument('subject_1', type=str, required=True, help="No subject provided")
courses_put_args.add_argument('catalog_number_1', type=str, required=True, help="No catalog number provided")
courses_put_args.add_argument('subject_2', type=str)
courses_put_args.add_argument('catalog_number_2', type=str)
courses_put_args.add_argument('subject_3', type=str)
courses_put_args.add_argument('catalog_number_3', type=str)
courses_put_args.add_argument('subject_4', type=str)
courses_put_args.add_argument('catalog_number_4', type=str)
courses_put_args.add_argument('subject_5', type=str)
courses_put_args.add_argument('catalog_number_5', type=str)
courses_put_args.add_argument('subject_6', type=str)
courses_put_args.add_argument('catalog_number_6', type=str)
courses_put_args.add_argument('subject_7', type=str)
courses_put_args.add_argument('catalog_number_7', type=str)


class Courses(Resource):
    def put(self):
        args = courses_put_args.parse_args()
        return courses_request(term, args['subject_1'], args['catalog_number_1'])

API.add_resource(Courses, '/courses')

if __name__ == '__main__':
    app.run(debug=True)