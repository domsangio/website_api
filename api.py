from flask import Flask, jsonify, request
from flask_cors import CORS

import urllib.parse as urlparse

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
print(client)

app = Flask(__name__)
CORS(app)

db = client.backend

@app.route('/projects/list', methods=['GET', 'PUT', 'DELETE', 'POST'])
def project_list():
    if request.method == 'GET':
        project_list = db.project_list
        results = []
        project_name = request.args['project_name']

        # project_list is the collection in the database
        # results will be the result thats going to be returned
        # project_name is a query param

        if (project_name == 'all'):
            for query in project_list.find():
                # print(query) # prints the query thats current
                results.append({
                        'project_name': query['project_name'], 
                        'project_description': query['project_description'],
                        'branch': query['branch'],
                        'difficulty': query['difficulty'],
                        'coolness': query['coolness']
                                })
        else:
            for query in project_list.find({"project_name":project_name}):
                results.append({
                        'project_name': query['project_name'], 
                        'project_description': query['project_description'],
                        'branch': query['branch'],
                        'difficulty': query['difficulty'],
                        'coolness': query['coolness']
                                })

        return jsonify({'result': results})
    elif request.method == 'PUT':
        project_list = db.project_list
        data = request.get_json()

        project_name = data['project_name']
        project_description = data['project_description']
        branch = data['branch']
        difficulty = data['difficulty']
        coolness = data['coolness']

        project_id = project_list.insert(
            {
                'project_name': project_name,
                'project_description': project_description,
                'branch': branch,
                'difficulty': difficulty,
                'coolness': coolness
            })

        new_project = project_list.find_one({'_id': project_id})

        output = {
            'project_name' : new_project['project_name'],
            'project_description' : new_project['project_description'],
            'branch' : new_project['branch'],
            'difficulty' : new_project['difficulty'],
            'coolness' : new_project['coolness']
        }
        return jsonify({'result' : output})
    elif (request.method == 'POST'):
        project_list = db.project_list

        project_name = request.json['project_name']
        project_description = request.json['project_description']
        branch = request.json['branch']
        difficulty = request.json['difficulty']
        coolness = request.json['coolness']

        project_list.update_one({ "project_name" : project_name }, 
                                { '$set' : 
                                    { 
                                        'project_description' : project_description,
                                        'branch' : branch,
                                        'difficulty' : difficulty,
                                        'coolness' : coolness
                                    }
                                })
        return project_list.find({ 'project_name' : project_name})
    elif (request.method == 'DELETE'):
        project_list = db.project_list

        project_name = request.json['project_name']
        print("\n\n")
        print(project_name)
        project_list.delete_many({ 'project_name' : project_name})

        return True
    else:
        return 'error'
        
if __name__ == '__main__':
    app.run(debug=True)