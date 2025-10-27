from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db

class UserRole(Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.USER)
    full_name = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship("Post", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)
    votes = db.relationship("Vote", backref="user", lazy=True)
    reports = db.relationship("Report", backref="user", lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def is_moderator(self) -> bool:
        return self.role in [UserRole.MODERATOR, UserRole.ADMIN]

    def can_moderate(self) -> bool:
        return self.role in [UserRole.MODERATOR, UserRole.ADMIN]

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "role": self.role.value if self.role else UserRole.USER.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def to_profile_dict(self):
        """Return profile-specific data for API responses"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "role": self.role.value if self.role else UserRole.USER.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
