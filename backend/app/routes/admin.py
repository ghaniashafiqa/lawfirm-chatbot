from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.db import db
from app.models import Admin

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("", methods=["GET"])
@jwt_required()
def list_admins():
    """List all admin users."""
    admins = Admin.query.all()
    return jsonify([
        { "id": a.id, "username": a.username, "email": a.email, "role": a.role, "created_at": a.created_at.isoformat() }
        for a in admins
    ])

@admin_bp.route("", methods=["POST"])
@jwt_required()
def create_admin():
    """Create a new admin user."""
    data = request.get_json(force=True)
    if Admin.query.filter_by(username=data["username"]).first():
        return jsonify(msg="Username exists"), 400
    a = Admin(username=data["username"], email=data["email"])
    a.set_password(data["password"])
    db.session.add(a)
    db.session.commit()
    return jsonify(msg="Admin created", id=a.id), 201

@admin_bp.route("/<int:admin_id>", methods=["PUT"])
@jwt_required()
def update_admin(admin_id):
    data = request.get_json(force=True)
    a = Admin.query.get_or_404(admin_id)
    a.username = data.get("username", a.username)
    a.email    = data.get("email",    a.email)
    if data.get("password"):
        a.set_password(data["password"])
    a.role     = data.get("role",     a.role)
    db.session.commit()
    return jsonify(msg="Admin updated")

@admin_bp.route("/<int:admin_id>", methods=["DELETE"])
@jwt_required()
def delete_admin(admin_id):
    a = Admin.query.get_or_404(admin_id)
    db.session.delete(a)
    db.session.commit()
    return jsonify(msg="Admin deleted")