from flask import Flask, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, unique=True, nullable=False)
    date = db.Column(db.String, nullable=False)

@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/api/create", methods=["POST"])
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
def get_comments():
    comments = Comment.query.all()
    return [{"id": c.id, "name": c.name, "comment": c.comment, "date": c.date} for c in comments]

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
