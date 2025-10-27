from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc
from ..extensions import db
from ..models.post import Post, PostType
from ..models.user import User

bp = Blueprint("posts", __name__)

@bp.get("/")
@jwt_required(optional=True)
def list_posts():
    posts = Post.query.filter_by(post_type=PostType.POST).order_by(desc(Post.created_at)).all()
    return jsonify([p.to_dict() for p in posts]), 200

@bp.post("/")
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    title = data.get("title")
    content = data.get("content")
    if not title or not content:
        return jsonify({"message": "title and content are required"}), 400
    post = Post(user_id=int(user_id), title=title, content=content, post_type=PostType.POST)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

@bp.get("/<int:post_id>")
@jwt_required(optional=True)
def get_post(post_id: int):
    post = Post.query.get_or_404(post_id)
    if post.post_type != PostType.POST:
        return jsonify({"message": "Not a post"}), 404
    return jsonify(post.to_dict()), 200

@bp.put("/<int:post_id>")
@jwt_required()
def update_post(post_id: int):
    user_id = int(get_jwt_identity())
    post = Post.query.get_or_404(post_id)
    if post.user_id != user_id:
        return jsonify({"message": "Forbidden"}), 403
    data = request.get_json() or {}
    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    db.session.commit()
    return jsonify(post.to_dict()), 200

@bp.delete("/<int:post_id>")
@jwt_required()
def delete_post(post_id: int):
    user_id = int(get_jwt_identity())
    post = Post.query.get_or_404(post_id)
    if post.user_id != user_id:
        return jsonify({"message": "Forbidden"}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200
