from enum import Enum
from ..extensions import db

class VoteType(Enum):
    UP = "up"
    DOWN = "down"

class Vote(db.Model):
    __tablename__ = "votes"
    __table_args__ = (
        db.UniqueConstraint("user_id", "post_id", name="uq_vote_user_post"),
        db.UniqueConstraint("user_id", "comment_id", name="uq_vote_user_comment"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True)
    vote_type = db.Column(db.Enum(VoteType), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "comment_id": self.comment_id,
            "vote_type": self.vote_type.value if self.vote_type else None,
        }
