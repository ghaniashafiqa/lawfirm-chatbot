# backend/app/routes/auth.py

from flask import Blueprint, request, jsonify
from app.db import db
from app.models import Admin
from app.models import Session
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)

    # Basic validation
    username = data.get('username')
    email    = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        raise BadRequest("username, email, and password are all required")

    # Check for duplicates
    if Admin.query.filter_by(username=username).first():
        return jsonify(msg="Username already exists"), 400

    # Create and save
    admin = Admin(username=username, email=email)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()

    return jsonify(msg="Registered"), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        raise BadRequest("username and password are required")

    user = Admin.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify(msg="Bad credentials"), 401

    # Create token
    access_token = create_access_token(identity=str(user.id))

    # Create session
    session = Session(
        admin_id=user.id,
        ip=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        last_active=datetime.utcnow()
    )
    db.session.add(session)
    db.session.commit()

    return jsonify(access_token=access_token), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    # gets the user ID from the validated JWT
    user_id = get_jwt_identity()
    user = Admin.query.get(user_id)
    if not user:
        return jsonify(msg="User not found"), 404

    return jsonify(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        created_at=user.created_at.isoformat()
    ), 200

@auth_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    user_id = get_jwt_identity()
    sessions = Session.query.filter_by(admin_id=user_id).order_by(Session.last_active.desc()).all()

    return jsonify([
        {
            "id": s.id,
            "device": s.device or "Unknown Device",
            "location": s.location or "Unknown",
            "ip": s.ip,
            "user_agent": s.user_agent or "",
            "lastActive": s.last_active.isoformat(),
            "current": s.current
        } for s in sessions
    ]), 200

@auth_bp.route('/logout-session', methods=['POST'])
@jwt_required()
def logout_session():
    user_id = get_jwt_identity()
    data = request.get_json()
    session_id = data.get('session_id')

    if not session_id:
        return jsonify(msg="Session ID is required"), 400

    from app.models import Session
    session = Session.query.filter_by(id=session_id, admin_id=user_id).first()

    if not session:
        return jsonify(msg="Session not found"), 404

    session.current = False
    db.session.commit()

    return jsonify(msg="Session logged out"), 200


# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# from app.db import db
# from app.models import Admin

# auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# @auth_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     if Admin.query.filter_by(username=data['username']).first():
#         return jsonify(msg="Username exists"), 400
#     admin = Admin(username=data['username'], email=data['email'])
#     admin.set_password(data['password'])
#     db.session.add(admin); db.session.commit()
#     return jsonify(msg="Registered"), 201

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     user = Admin.query.filter_by(username=data['username']).first()
#     if not user or not user.check_password(data['password']):
#         return jsonify(msg="Bad credentials"), 401
#     token = create_access_token(identity=user.id)
#     return jsonify(access_token=token), 200

# @auth_bp.route('/me', methods=['GET'])
# @jwt_required()
# def me():
#     uid = get_jwt_identity()
#     user = Admin.query.get(uid)
#     return jsonify(id=user.id, username=user.username, role=user.role)
