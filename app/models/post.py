from datetime import datetime
from enum import Enum
from ..extensions import db

class PostType(Enum):
    POST = "post"
    DOUBT = "doubt"

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.Enum(PostType), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship("Comment", backref="post", lazy=True, cascade="all, delete-orphan")
    votes = db.relationship("Vote", backref="post", lazy=True, cascade="all, delete-orphan")
    reports = db.relationship("Report", backref="post", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content,
            "post_type": self.post_type.value if self.post_type else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
