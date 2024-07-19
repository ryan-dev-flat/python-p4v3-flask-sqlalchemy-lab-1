# server/app.py



from flask import Flask, make_response, g, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():

    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake is None:
        return jsonify({'message': f'Earthquake {id} not found.'}), 404
    else:
        return jsonify(earthquake.to_dict())

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_mag_greater_than(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({
        'count': len(earthquakes),
        'quakes': [quake.to_dict() for quake in earthquakes]
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)
