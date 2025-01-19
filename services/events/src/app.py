import os
import socket

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)

if os.environ.get('db_conn'):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
            os.environ.get('db_conn') + '/event'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+mysqlconnector://root:root@host.docker.internal:3306/event'
    
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = \
#         'mysql+mysqlconnector://root:root@localhost:3306/event'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                            'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)


class Event(db.Model):
    __tablename__ = 'event'

    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(64), nullable=False)
    venue = db.Column(db.String(64), nullable=False)
    entry_fee = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    slots_left = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(64), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_dict(self):
        dto = {
            "event_id": self.event_id,
            "entry_fee": self.entry_fee,
            "capacity": self.capacity,
            "slots_left": self.slots_left,
            "event_name": self.event_name,
            "venue": self.venue,
            "description": self.description,
            "time": self.time
        }

        return dto


@app.route("/health")
def health_check():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    return jsonify(
            {
                "message": "Service is healthy.",
                "service:": "events",
                "ip_address": local_ip
            }
    ), 200


@app.route("/events")
def get_all():
    event_list = db.session.scalars(
                   db.select(Event)
                ).all()
    if len(event_list) != 0:
        return jsonify(
            {
                "data": {
                    "events": [event.to_dict() for event in event_list]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "There are no events."
        }
    ), 404


@app.route("/events/<int:event_id>")
def find_by_id(event_id):
    event = db.session.scalar(
              db.select(Event).
              filter_by(event_id=event_id)
           )
    if event:
        return jsonify(
            {
                "data": event.to_dict()
            }
        ), 200
    return jsonify(
        {
            "message": "Event not found."
        }
    ), 404


@app.route("/events", methods=['POST'])
def new_event():
    try:
        event_name = request.json.get('event_name')
        venue = request.json.get('venue')
        entry_fee = request.json.get('entry_fee')
        capacity = request.json.get('capacity')
        slots_left = request.json.get('slots_left')
        description = request.json.get('description')
        time = request.json.get('time')
        event = Event(event_name=event_name,
                      venue=venue,
                      entry_fee=entry_fee,
                      capacity=capacity,
                      slots_left=slots_left,
                      description=description,
                      time=time)

        db.session.add(event)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred creating the event.",
                "error": str(e)
            }
        ), 500

    return jsonify(
        {
            "data": event.to_dict()
        }
    ), 201


@app.route("/events/<int:event_id>", methods=['PATCH'])
def update_event(event_id):
    event = db.session.scalar(
              db.select(Event).
              with_for_update(of=Event).
              filter_by(event_id=event_id)
           )
    if event is None:
        return jsonify(
            {
                "data": {
                    "event_id": event_id
                },
                "message": "Event not found."
            }
        ), 404
    data = request.get_json()

    if 'reserve' in data.keys():
        if len(data.keys()) != 1:
            return jsonify(
                {
                    "message": "An error occurred updating the event.",
                    "error": "The 'reserve' key " +
                             "cannot be provided with any others."
                }
            ), 500
        if event.slots_left - data['reserve'] >= 0:
            event.slots_left = event.slots_left - data['reserve']
            try:
                db.session.commit()
            except Exception as e:
                return jsonify(
                    {
                        "message": "An error occurred updating the event.",
                        "error": str(e)
                    }
                ), 500
            return jsonify(
                {
                    "data": event.to_dict()
                }
            ), 200
        else:
            return jsonify(
                {
                    "message": "An error occurred updating the event.",
                    "error": "Not enough slots in event."
                }
            ), 500

    # If not a reserve slot update
    if 'event_name' in data.keys():
        event.event_name = data['event_name']
    if 'venue' in data.keys():
        event.venue = data['venue']
    if 'entry_fee' in data.keys():
        event.entry_fee = data['entry_fee']
    if 'time' in data.keys():
        event.time = data['time']
    if 'description' in data.keys():
        event.description = data['description']
    if 'slots_left' in data.keys():
        event.slots_left = data['slots_left']
    if 'capacity' in data.keys():
        event.capacity = data['capacity']
    try:
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred updating the event.",
                "error": str(e)
            }
        ), 500
    return jsonify(
        {
            "data": event.to_dict()
        }
    )


@app.route("/events/<int:event_id>", methods=['DELETE'])
def delete_event(event_id):
    event = db.session.scalar(
              db.select(Event).
              filter_by(event_id=event_id)
           )
    if event is not None:
        try:
            db.session.delete(event)
            db.session.commit()
        except Exception as e:
            return jsonify(
                {
                    "message": "An error occurred deleting the event.",
                    "error": str(e)
                }
            ), 500
        return jsonify(
            {
                "data": {
                    "event_id": event_id
                }
            }
        ), 200
    return jsonify(
        {
            "data": {
                "event_id": event_id
            },
            "message": "Event not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
