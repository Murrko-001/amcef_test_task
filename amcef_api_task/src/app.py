from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
import requests

app = Flask(__name__)
basedir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'data\data.db')
db = SQLAlchemy(app)

EXTERNAL_API = "https://jsonplaceholder.typicode.com"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    userId = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(50))
    body = db.Column(db.String(255))

    def __repr__(self):
        return f"post {self.id} by user {self.userId}\ntitle: {self.title}\nbody: {self.body}\n"


from utils import utils, search_all, search_by_id, search_by_user, search_by_both
app.register_blueprint(utils)


@app.route("/")
@app.route("/api")
def index():
    return "task v2"


@app.route("/api/posts", methods=["GET"])
def get_posts():
    args = request.args
    id = args.get("id", default=0, type=int)
    userId = args.get("userId", default=0, type=int)

    if id == 0 and userId == 0:
        return search_all()
    elif id != 0 and userId == 0:
        return search_by_id(id)
    elif id == 0 and userId != 0:
        return search_by_user(userId)
    else:
        return search_by_both(id, userId)


@app.route("/api/posts", methods=["POST"])
def add_post():
    try:
        request.json["id"], request.json["userId"]
    except KeyError:
        return {"error": "id or userId missing"}, 400

    response = requests.get(f"{EXTERNAL_API}/users/{request.json['userId']}")
    if not response.json():
        return {"error": f"user {request.json['userId']} does not exist"}, 404

    for i in Post.query.all():
        if i.id == request.json["id"]:
            return {"error": f"post with id {request.json['id']} already exists"}, 400

    try:
        post = Post(id=request.json["id"], userId=request.json["userId"], title=request.json["title"],
                    body=request.json["body"])
    except KeyError:
        post = Post(id=request.json["id"], userId=request.json["userId"], title="", body="")

    db.session.add(post)
    db.session.commit()
    return {"message": f"post with id {post.id} added"}, 200


@app.route("/api/posts", methods=["PUT"])
def update_post():
    id = request.json["id"]
    post = Post.query.get(id)

    if post is None:
        return {"error": f"post with id {id} could not be found"}, 404

    try:
        post.title = request.json["title"]
        post.body = request.json["body"]
    except KeyError:
        return {"error": "title or body missing"}, 400

    db.session.commit()
    return {"message": f"post with id {id} updated"}, 200


@app.route("/api/posts/<id>", methods=["DELETE"])
def delete_post(id):
    post = Post.query.get(id)
    if post is None:
        return {"error": f"no post with id {id}"}, 404

    db.session.delete(post)
    db.session.commit()
    return {"message": f"successfully removed post with id {id}"}, 200
