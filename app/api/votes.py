from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db, redis_client
from ..models.vote import Vote, VoteType
from ..models.post import Post
from ..models.comment import Comment
from ..services.redis_service import update_vote_count

bp = Blueprint("votes", __name__)

@bp.post("/posts/<int:post_id>/vote")
@jwt_required()
def vote_post(post_id: int):
    return _vote("post", post_id)

@bp.post("/comments/<int:comment_id>/vote")
@jwt_required()
def vote_comment(comment_id: int):
    return _vote("comment", comment_id)

def _vote(item_type: str, item_id: int):
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    vote_type_str = data.get("vote_type")  # 'up' or 'down'
    if vote_type_str not in ("up", "down"):
        return jsonify({"message": "vote_type must be 'up' or 'down'"}), 400

    # Ensure item exists
    if item_type == "post":
        obj = Post.query.get_or_404(item_id)
    else:
        obj = Comment.query.get_or_404(item_id)

    # Find existing vote
    vote = Vote.query.filter_by(user_id=user_id,
                                post_id=item_id if item_type == "post" else None,
                                comment_id=item_id if item_type == "comment" else None).first()

    new_type = VoteType.UP if vote_type_str == "up" else VoteType.DOWN

    delta = 0
    if vote:
        if vote.vote_type != new_type:
            # update
            delta = 2 if new_type == VoteType.UP else -2  # switching from down->up or up->down
            vote.vote_type = new_type
        else:
            # unvote (toggle off)
            delta = -1 if new_type == VoteType.UP else 1
            db.session.delete(vote)
            vote = None
    else:
        # new vote
        delta = 1 if new_type == VoteType.UP else -1
        vote = Vote(user_id=user_id,
                    post_id=item_id if item_type == "post" else None,
                    comment_id=item_id if item_type == "comment" else None,
                    vote_type=new_type)
        db.session.add(vote)

    db.session.commit()

    # Update Redis counter atomically
    update_vote_count(item_type, item_id, delta)

    return jsonify({"message": "ok", "delta": delta}), 200
