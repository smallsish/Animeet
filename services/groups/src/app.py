from datetime import datetime
import socket
import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging


app = Flask(__name__)
if os.environ.get('db_conn'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('db_conn') + '/group'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = \
            'mysql+mysqlconnector://cs302:cs302@host.docker.internal:3306/group'
    
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = \
#             'mysql+mysqlconnector://cs302:cs302@localhost:3306/group'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Group(db.Model):
    __tablename__ = 'group'

    group_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    slots_left = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(64), nullable=False)

    def __init__(self, event_id, name, max_capacity, slots_left, description):
        self.event_id = event_id
        self.name = name
        self.max_capacity = max_capacity
        self.slots_left = slots_left
        self.description = description

    def to_dict(self):
        return {
            "group_id": self.group_id,
            "event_id": self.event_id,
            "name": self.name,
            "max_capacity": self.max_capacity,
            "slots_left": self.slots_left,
            "description": self.description
        }


class GroupUser(db.Model):
    __tablename__ = 'group_user'

    group_id = db.Column(
        db.Integer, db.ForeignKey('group.group_id'), primary_key=True
    )
    user_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(32), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)
    payment_status = db.Column(db.String(16), nullable=False)

    def __init__(self, group_id, user_id, role, date_joined, payment_status):
        self.group_id = group_id
        self.user_id = user_id
        self.role = role
        self.date_joined = date_joined
        self.payment_status = payment_status

    def to_dict(self):
        return {
            "group_id": self.group_id,
            "user_id": self.user_id,
            "role": self.role,
            "date_joined": self.date_joined,
            "payment_status": self.payment_status
        }


########################################## GET ##########################################
@app.route("/groups", methods=['GET'])
def get_all_groups():
    event_id = request.args.get('event_id', type=int)

    if event_id is not None:
        return get_groups_by_event(event_id)

    group_list = db.session.scalars(db.select(Group)).all()

    if group_list:
        return jsonify({
            "data": [group.to_dict() for group in group_list]
        }), 200
    else:
        return jsonify({
            "message": "There are no groups."
        }), 404

def get_groups_by_event(event_id):
    try:
        groups = db.session.scalars(
            db.select(Group).filter_by(event_id=event_id)
        ).all()

        if groups:
            return jsonify({
                "data": [group.to_dict() for group in groups]
            }), 200
        else:
            return jsonify({
                "message": f"No groups found for event_id {event_id}."
            }), 404

    except Exception as e:
        return jsonify({
            "message": "An error occurred fetching groups.",
            "error": str(e)
        }), 500


@app.route("/groups/<int:group_id>", methods=['GET'])
def find_group_by_id(group_id):
    group = db.session.scalar(
                db.select(Group).
                filter_by(group_id=group_id)
            )
    if group:
        return jsonify(
            {
                "data": group.to_dict()
            }
        ), 200
    return jsonify(
        {
            "message": "Group not found."
        }
    ), 404


@app.route("/groups/users", methods=['GET'])
def get_all_group_users():
    try:
        group_user_list = db.session.scalars(
            db.select(GroupUser)
        ).all()

        if len(group_user_list) != 0:
            return jsonify({
                "data": [
                    group_user.to_dict()
                    for group_user in group_user_list
                ]
            }), 200
        else:
            return jsonify({
                "message": "No group users found."
            }), 404

    except Exception as e:
        return jsonify({
            "message": "An error occurred fetching group users.",
            "error": str(e)
        }), 500


@app.route("/groups/<int:group_id>/users", methods=['GET'])
def get_all_users_in_group(group_id):
    try:
        group_users = db.session.scalars(
            db.select(GroupUser).filter_by(group_id=group_id)
        ).all()

        return jsonify({
            "data": [user.to_dict() for user in group_users]
        }), 200

    except Exception as e:
        return jsonify({
            "message": "An error occurred fetching users for this group.",
            "error": str(e)
        }), 500
        
        
# to get one user from the group-members list (eg. to get payment status from one user)
@app.route("/groups/<int:group_id>/users/<int:user_id>", methods=['GET'])
def get_one_user_in_group(group_id, user_id):
    user = db.session.scalar(
        db.select(GroupUser).filter_by(group_id=group_id, user_id=user_id)
    )

    if user:
        return jsonify(
            {
                "data": user.to_dict()
            }
        ), 200
       
    return jsonify(
        {
            "message": "User not found."
        }
    ), 404
    
    
# Get all groups that the user has joined
@app.route("/groups/users/<int:user_id>", methods=['GET'])
def get_all_groups_from_user(user_id):
    try:
        group_users = db.session.scalars(
            db.select(GroupUser).filter_by(user_id=user_id)
        ).all()

        groups = []
        for group in group_users:
            groups.append(db.session.scalar(
                db.select(Group).
                filter_by(group_id=group.group_id)
            ))
        
        return jsonify({
            "data": [group.to_dict() for group in groups]
        }), 200

    except Exception as e:
        return jsonify({
            "message": "An error occurred fetching groups for this user.",
            "error": str(e)
        }), 500
    
# Get payment status for that group-user entry
@app.route("/groups/<int:group_id>/users/<int:user_id>/payment-status", methods=['GET'])
def get_payment_status_in_group(group_id, user_id):
    try:
        
        # Fetch the GroupUser entry for the specific user and group
        user_group = db.session.scalar(
            db.select(GroupUser).filter_by(group_id=group_id, user_id=user_id)
        )

        if user_group:

            # Return just the payment_status
            return jsonify({
                "payment_status": user_group.payment_status
            }), 200
        else:
            return jsonify({
                "message": "User not found in this group."
            }), 404

    except Exception as e:
        return jsonify({
            "message": "An error occurred fetching payment status.",
            "error": str(e)
        }), 500
       

########################################## POST ##########################################
@app.route("/groups", methods=['POST'])
def new_group():
    try:
        data = request.get_json()

        # Check if the user is already part of any group in the given event
        user_id = data.get('user_id')
        event_id = data.get('event_id')

        existing_group_user = db.session.scalars(
            db.select(GroupUser).join(Group).filter(
                GroupUser.user_id == user_id,
                Group.event_id == event_id
            )
        ).first()

        if existing_group_user:
            return jsonify({
                "message": "User is already part of a group for this event."
            }), 400

        # Proceed to create the new group if user is not part of any group for the event
        group = Group(
            event_id=data['event_id'],
            name=data['name'],
            max_capacity=data['max_capacity'],
            slots_left=data['max_capacity'] - 1,
            description=data['description']
        )
        db.session.add(group)
        db.session.commit()

        # Insert creator into GROUP_USER.
        leader_id = data.get('user_id')
        group_user = GroupUser(
            group_id=group.group_id,
            user_id=leader_id,
            role='leader',
            date_joined=datetime.now(),
            payment_status='unpaid'
        )
        db.session.add(group_user)
        db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred creating the group.",
                "error": str(e)
            }
        ), 500

    return jsonify(
        {
            "data": group.to_dict(),
            "message": "Group has been created successfully."
        }
    ), 201


@app.route("/groups/<int:group_id>", methods=['POST'])
def join_group(group_id):
    try:
        data = request.get_json()
        
        # Insert member into GROUP_USER
        user_id = data.get('user_id')

        group = db.session.scalar(
            db.select(Group).filter_by(group_id=group_id)
        )

        if not group:
            return jsonify({
                "message": "Group not found."
            }), 404
        
        # Check if user is already in any other group for this event
        existing_event_group_user = db.session.scalar(
            db.select(GroupUser)
            .join(Group, Group.group_id == GroupUser.group_id)
            .filter(GroupUser.user_id == user_id, Group.event_id == group.event_id)
        )

        if existing_event_group_user:
            return jsonify({
                "message": "User is already a member of another group for this event."
            }), 400

        if group.slots_left <= 0:
            return jsonify({
                "message": "No slots available in this group."
            }), 400

        existing_user = db.session.scalar(
            db.select(GroupUser).filter_by(group_id=group_id, user_id=user_id)
        )
        if existing_user:
            return jsonify({
                "message": "User is already a member of this group."
            }), 400

        group_user = GroupUser(
            group_id=group.group_id,
            user_id=user_id,
            role='member',
            date_joined=datetime.now(),
            payment_status='unpaid'
        )
        db.session.add(group_user)

        # Update GROUP slots_left
        group.slots_left -= 1
        db.session.commit()
        
        # Get all group members to be returned
        group_users = db.session.scalars(
            db.select(GroupUser).filter_by(group_id=group.group_id)
        ).all()

    except Exception as e:
        return jsonify({
            "message": "An error occurred joining the group.",
            "error": str(e)
        }), 500

    return jsonify({
        "message": "Successfully joined the group.",
        "data": {
            "joined": group_user.date_joined,
            "group_id": group_user.group_id,
            "user_id": group_user.user_id,
            "role": group_user.role,
            "status": 'NEW',
            "members": [user.user_id for user in group_users]
        }
    }), 201


########################################## DELETE ##########################################
@app.route("/groups/<int:group_id>", methods=['DELETE'])
def delete_group(group_id):
    group = db.session.scalar(
        db.select(Group).filter_by(group_id=group_id)
    )

    if group is not None:
        try:
            db.session.delete(group)
            db.session.commit()

        except Exception as e:
            return jsonify(
                {
                    "message": "An error occurred deleting the group" +
                               "and its associated users.",
                    "error": str(e)
                }
            ), 500

        return jsonify(
            {
                "data": {
                    "group_id": group_id
                }
            }
        ), 200

    return jsonify(
        {
            "message": "Group not found.",
            "data": {
                "group_id": group_id
            }
        }
    ), 404


@app.route("/groups/<int:group_id>/users/<int:user_id>", methods=['DELETE'])
def delete_user_from_group(group_id, user_id):
    group_user = db.session.scalar(
        db.select(GroupUser).filter_by(group_id=group_id, user_id=user_id)
    )

    if group_user is not None:
        try:
            db.session.delete(group_user)

            group = db.session.scalar(
                db.select(Group).filter_by(group_id=group_id)
            )
            if group:
                group.slots_left += 1

            db.session.commit()

            # Get all group members to be returned
            group_users = db.session.scalars(
                db.select(GroupUser).filter_by(group_id=group.group_id)
            ).all()

        except Exception as e:
            return jsonify(
                {
                    "message": "An error occurred deleting the user" +
                               "from the group.",
                    "error": str(e)
                }
            ), 500

        return jsonify(
            {
                "data": {
                    "group_id": group_id,
                    "user_id": user_id,
                    "members": [user.user_id for user in group_users]
                }
            }
        ), 200

    return jsonify(
        {
            "message": "User not found in the group.",
            "data": {
                "group_id": group_id,
                "user_id": user_id
            }
        }
    ), 404


########################################## PATCH ##########################################
@app.route("/groups/<int:group_id>/users/<int:user_id>", methods=['PATCH'])
def patch_group_user(group_id, user_id):
    group_user = db.session.scalar(
        db.select(GroupUser).filter_by(group_id=group_id, user_id=user_id)
    )

    if group_user is None:
        logger.error(f"User {user_id} not found in group {group_id}.")
        return jsonify({
            "message": "User not found in the group.",
            "data": {
                "group_id": group_id,
                "user_id": user_id
            }
        }), 404

    data = request.get_json()
    try:
        if "payment_status" in data:
            group_user.payment_status = data["payment_status"]
            logger.info(f"Updated payment status to {data['payment_status']} for user {user_id} in group {group_id}.")
        if "role" in data:
            group_user.role = data["role"]
            logger.info(f"Updated role to {data['role']} for user {user_id} in group {group_id}.")

        db.session.commit()
        
        logger.info(f"Successfully updated user {user_id} in group {group_id}.")
        return jsonify({
            "data": {
                "group_id": group_id,
                "user_id": user_id,
                "payment_status": group_user.payment_status,
                "role": group_user.role
            }
        }), 200

    except Exception as e:
        logger.error(f"Error updating group user {user_id} in group {group_id}: {e}")
        return jsonify({
            "message": "An error occurred while updating the group user.",
            "error": str(e)
        }), 500


@app.route("/health")
def health_check():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    return jsonify(
            {
                "message": "Service is healthy.",
                "service:": "groups",
                "ip_address": local_ip
            }
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
