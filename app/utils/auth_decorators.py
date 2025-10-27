from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required as flask_jwt_required, get_jwt_identity
from ..models.user import User, UserRole

def jwt_required(optional=False):
    """Enhanced JWT required decorator that also fetches user"""
    def decorator(f):
        @wraps(f)
        @flask_jwt_required(optional=optional)
        def decorated_function(*args, **kwargs):
            if optional and not get_jwt_identity():
                return f(*args, **kwargs)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Require admin role"""
    @wraps(f)
    @flask_jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user or not user.is_admin():
            return jsonify({"message": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

def moderator_required(f):
    """Require moderator or admin role"""
    @wraps(f)
    @flask_jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user or not user.can_moderate():
            return jsonify({"message": "Moderator access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Helper function to get current user from JWT"""
    user_id = get_jwt_identity()
    if user_id:
        return User.query.get(int(user_id))
    return None