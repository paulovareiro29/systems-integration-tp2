import sys

from flask import Flask, jsonify, request

from entities import Team

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

# set of all teams
# !TODO: replace by database access
teams = [
]

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/teams/', methods=['GET'])
def get_teams():
    return jsonify([team.__dict__ for team in teams])


@app.route('/api/teams/', methods=['POST'])
def create_team():
    data = request.get_json()
    team = Team(name=data['name'])
    teams.append(team)
    return jsonify(team.__dict__), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
