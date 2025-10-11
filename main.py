from flask import Flask, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(
    __name__,
    static_folder="static",
    static_url_path=""
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)

@app.route("/")
@limiter.exempt
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/create", methods=["POST"])
@limiter.limit("10/day")
def create_comment():
    data = request.get_json()
    new_comment = Comment(
        name=data["name"], #type: ignore
        comment=data["comment"], #type: ignore
        date=data["date"] #type: ignore
    )
    db.session.add(new_comment)
    db.session.commit()
    return {"message": "comment added!"}, 201

@app.route("/api/comments", methods=["GET"])
@limiter.limit("8/minute")
def get_comments():
    comments = Comment.query.all()
    return [{"id": c.id, "name": c.name, "comment": c.comment, "date": c.date} for c in comments]

with app.app_context():
    db.create_all()
