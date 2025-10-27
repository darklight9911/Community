from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.comment import Comment
from ..models.post import Post

bp = Blueprint("comments", __name__)

@bp.get("/posts/<int:post_id>/comments")
@jwt_required(optional=True)
def list_comments(post_id: int):
    Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()

    # Build tree
    by_id = {c.id: {**c.to_dict(), "children": []} for c in comments}
    roots = []
    for c in comments:
        node = by_id[c.id]
        if c.parent_id and c.parent_id in by_id:
            by_id[c.parent_id]["children"].append(node)
        else:
            roots.append(node)

    return jsonify(roots), 200

@bp.post("/posts/<int:post_id>/comments")
@jwt_required()
def create_comment(post_id: int):
    user_id = int(get_jwt_identity())
    Post.query.get_or_404(post_id)
    data = request.get_json() or {}
    content = data.get("content")
    parent_id = data.get("parent_id")
    if not content:
        return jsonify({"message": "content is required"}), 400
    if parent_id is not None:
        # Validate parent comment belongs to same post
        parent = Comment.query.get_or_404(int(parent_id))
        if parent.post_id != post_id:
            return jsonify({"message": "parent_id does not belong to this post"}), 400
    comment = Comment(user_id=user_id, post_id=post_id, parent_id=parent_id, content=content)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

@bp.put("/comments/<int:comment_id>")
@jwt_required()
def update_comment(comment_id: int):
    user_id = int(get_jwt_identity())
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != user_id:
        return jsonify({"message": "Forbidden"}), 403
    data = request.get_json() or {}
    comment.content = data.get("content", comment.content)
    db.session.commit()
    return jsonify(comment.to_dict()), 200

@bp.delete("/comments/<int:comment_id>")
@jwt_required()
def delete_comment(comment_id: int):
    user_id = int(get_jwt_identity())
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != user_id:
        return jsonify({"message": "Forbidden"}), 403
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200
