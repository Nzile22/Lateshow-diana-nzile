from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance  
import os

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

 
    db.init_app(app)
    migrate = Migrate(app, db)

    return app

app = create_app()

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([{'id': e.id, 'date': e.date, 'number': e.number} for e in episodes])

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if episode:
        return jsonify({
            'id': episode.id,
            'date': episode.date,
            'number': episode.number,
            'appearances': [{'id': a.id, 'guest_id': a.guest_id, 'rating': a.rating, 
                             'guest': {'id': a.guest.id, 'name': a.guest.name, 'occupation': a.guest.occupation}} 
                            for a in episode.appearances]
        })
    return jsonify({"error": "Episode not found"}), 404

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([{'id': g.id, 'name': g.name, 'occupation': g.occupation} for g in guests])

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    try:
        appearance = Appearance(rating=data['rating'], episode_id=data['episode_id'], guest_id=data['guest_id'])
        db.session.add(appearance)
        db.session.commit()
        return jsonify({
            'id': appearance.id,
            'rating': appearance.rating,
            'guest_id': appearance.guest_id,
            'episode_id': appearance.episode_id,
            'episode': {'id': appearance.episode.id, 'date': appearance.episode.date, 'number': appearance.episode.number},
            'guest': {'id': appearance.guest.id, 'name': appearance.guest.name, 'occupation': appearance.guest.occupation}
        }), 201
    except Exception as e:
        return jsonify({"errors": ["validation errors"]}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
