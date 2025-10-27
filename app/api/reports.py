from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.report import Report
from ..models.post import Post
from ..models.comment import Comment

bp = Blueprint("reports", __name__)

@bp.post("/posts/<int:post_id>/report")
@jwt_required()
def report_post(post_id: int):
    user_id = int(get_jwt_identity())
    Post.query.get_or_404(post_id)
    data = request.get_json() or {}
    reason = data.get("reason")
    if not reason:
        return jsonify({"message": "reason is required"}), 400
    report = Report(user_id=user_id, post_id=post_id, reason=reason)
    db.session.add(report)
    db.session.commit()
    return jsonify(report.to_dict()), 201

@bp.post("/comments/<int:comment_id>/report")
@jwt_required()
def report_comment(comment_id: int):
    user_id = int(get_jwt_identity())
    Comment.query.get_or_404(comment_id)
    data = request.get_json() or {}
    reason = data.get("reason")
    if not reason:
        return jsonify({"message": "reason is required"}), 400
    report = Report(user_id=user_id, comment_id=comment_id, reason=reason)
    db.session.add(report)
    db.session.commit()
    return jsonify(report.to_dict()), 201
