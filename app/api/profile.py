from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from ..models.user import User
from ..extensions import db

profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")


@profile_bp.route("/", methods=["GET"])
@jwt_required()
def get_profile():
    """Get current user's profile information"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({
            "success": True,
            "profile": user.to_profile_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@profile_bp.route("/", methods=["PUT"])
@jwt_required()
def update_profile():
    """Update current user's profile information"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        data = request.get_json()
        
        # Update profile fields
        if "full_name" in data:
            user.full_name = data["full_name"].strip() if data["full_name"] else None
            
        if "bio" in data:
            user.bio = data["bio"].strip() if data["bio"] else None
            
        if "avatar_url" in data:
            user.avatar_url = data["avatar_url"].strip() if data["avatar_url"] else None
        
        # Update username if provided and not taken
        if "username" in data:
            new_username = data["username"].strip()
            if new_username != user.username:
                existing_user = User.query.filter_by(username=new_username).first()
                if existing_user:
                    return jsonify({"error": "Username already taken"}), 400
                user.username = new_username
        
        # Update email if provided and not taken
        if "email" in data:
            new_email = data["email"].strip().lower()
            if new_email != user.email:
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user:
                    return jsonify({"error": "Email already taken"}), 400
                user.email = new_email
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully",
            "profile": user.to_profile_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@profile_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    """Change current user's password"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        data = request.get_json()
        
        if not data.get("current_password") or not data.get("new_password"):
            return jsonify({"error": "Current password and new password are required"}), 400
        
        # Verify current password
        if not user.check_password(data["current_password"]):
            return jsonify({"error": "Current password is incorrect"}), 400
        
        # Validate new password
        new_password = data["new_password"]
        if len(new_password) < 6:
            return jsonify({"error": "New password must be at least 6 characters long"}), 400
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Password changed successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@profile_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_account():
    """Delete current user's account (soft delete by setting active=False would be better in production)"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        data = request.get_json()
        
        if not data.get("password"):
            return jsonify({"error": "Password required to delete account"}), 400
        
        # Verify password
        if not user.check_password(data["password"]):
            return jsonify({"error": "Incorrect password"}), 400
        
        # In production, you might want to soft delete instead
        # For now, we'll just return a message (actual deletion is dangerous)
        return jsonify({
            "success": True,
            "message": "Account deletion would be processed (not implemented for safety)"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500