from flask import Flask
from flask_restful import Api, Resource
from scraper import Scraper
app = Flask(__name__)
api = Api(app)

class AppRuntime(Resource):
    def get(self,name,resource):
        if resource == 'bio': 
            return Scraper(name).get_bio_info()
        elif resource == 'repos' or resource == 'repositories':
            return Scraper(name).get_repo_info()

api.add_resource(AppRuntime,'/gitscrap/<string:name>/<string:resource>/')

if __name__ == "__main__":
    app.run(debug=True)