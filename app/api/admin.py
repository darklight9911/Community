from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models.user import User, UserRole
from ..utils.auth_decorators import admin_required, moderator_required, get_current_user

bp = Blueprint("admin", __name__)

@bp.get("/users")
@admin_required
def list_users():
    """Admin only: List all users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@bp.put("/users/<int:user_id>/role")
@admin_required
def update_user_role(user_id: int):
    """Admin only: Update user role"""
    data = request.get_json() or {}
    new_role = data.get("role")
    
    if new_role not in [role.value for role in UserRole]:
        return jsonify({"message": "Invalid role"}), 400
    
    user = User.query.get_or_404(user_id)
    
    # Prevent removing admin role from admin@gmail.com
    if user.email.lower() == "admin@gmail.com" and new_role != UserRole.ADMIN.value:
        return jsonify({"message": "Cannot change role of admin@gmail.com"}), 403
    
    user.role = UserRole(new_role)
    db.session.commit()
    
    return jsonify({"message": "Role updated successfully", "user": user.to_dict()}), 200

@bp.get("/stats")
@moderator_required
def get_stats():
    """Moderator/Admin: Get platform statistics"""
    from ..models.post import Post
    from ..models.comment import Comment
    from ..models.report import Report
    
    total_users = User.query.count()
    total_posts = Post.query.count()
    total_comments = Comment.query.count()
    total_reports = Report.query.count()
    
    role_counts = {}
    for role in UserRole:
        role_counts[role.value] = User.query.filter_by(role=role).count()
    
    return jsonify({
        "total_users": total_users,
        "total_posts": total_posts,
        "total_comments": total_comments,
        "total_reports": total_reports,
        "role_distribution": role_counts
    }), 200

@bp.get("/reports")
@moderator_required
def get_reports():
    """Moderator/Admin: Get all reports"""
    from ..models.report import Report
    
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return jsonify([report.to_dict() for report in reports]), 200