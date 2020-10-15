from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# Stored in memory
users = [
    { "name"     : "John",
      "age"      : 42,
      "language" : "english"
    },
    { "name"     : "Joe",
      "age"      : 42,
      "language" : "english"
    },
    { "name"     : "Lucy",
      "age"      : 30,
      "language" : "english"
    }
]
# Optionally in file or db
# db can be for example SQL database

# Create or update user data
def add_user(name, age, language):
    user = {
        "name"     : name,
        "age"      : age,
        "language" : language
    }
    return user

class User(Resource):
    def get(self, name):
        # The get method is used to fetch a specific user

        # Blank user is checked by API
        #print "DEBUG(get): name is:", name

        for user in users:
            if (name == user["name"]):
                return user, 200 #Status OK
        return "User not found", 404 #Status Not Found

    def post(self, name):
        # The post method is used to create a new user

        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("language")
        args = parser.parse_args()

        for user in users:
            if (name == user["name"]):
                return "User with name {} already exists".format(name), 400 #Status code Bad Request

        user = add_user(name, args["age"], args["language"]);
        print "DEBUG(post): user is:", user

        users.append(user)
        return user, 201 #Status Created

    def put(self, name):
        # The put method is used to updte details of user,
        # or create a new one if it not existed yet

        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("language")
        args = parser.parse_args()

        for user in users:
            if (name == user["name"]):
                user["age"] = args["age"]
                user["language"] = args["language"]
                print "DEBUG(put): existing user is:", user
                return user, 200 #Status OK

        user = add_user(name, args["age"], args["language"]);
        print "DEBUG(put): user is:", user

        users.append(user)
        return user, 201 #Status Created

    def delete(self, name):
        # The delete method is used to delete user that is no longer relevant

        global users
        users = [user for user in users if user ["name"] != name]
        return "{} is deleted".format(name), 200 #Status OK

# Main route to API
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Current Users</h1>
<p>A prototype API for current users.</p>'''

# A route to return all of the available users in our class.
@app.route('/users/all', methods=['GET'])
def api_all():
    return jsonify(users)

# Specify a route to API
# <string:name> variable part of the route, accepts any name
api.add_resource(User, "/user/<string:name>")

# Run Flask application
app.run(debug=True)
