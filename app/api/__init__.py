from flask import Blueprint

# Sub-blueprints will be registered here
api_bp = Blueprint("api", __name__)

from . import auth, posts, doubts, comments, votes, reports, admin, profile  # noqa: E402,F401

# Register child blueprints with prefixes
api_bp.register_blueprint(auth.bp, url_prefix="/auth")
api_bp.register_blueprint(posts.bp, url_prefix="/posts")
api_bp.register_blueprint(doubts.bp, url_prefix="/doubts")
api_bp.register_blueprint(comments.bp)
api_bp.register_blueprint(votes.bp)
api_bp.register_blueprint(reports.bp)
api_bp.register_blueprint(admin.bp, url_prefix="/admin")
api_bp.register_blueprint(profile.profile_bp)
