from flask import Blueprint
import requests
from app import Post, db, EXTERNAL_API

utils = Blueprint("utils", __name__)


def search_all():
    posts = Post.query.all()
    posts_in_json = iter_posts(posts)

    if not posts_in_json:
        return {"error": "no posts"}, 404

    return {"posts": posts_in_json}, 200


def search_by_id(id):
    post = Post.query.get(id)

    if post is None:
        response = requests.get(f"{EXTERNAL_API}/posts/{id}")

        if response.status_code != 200:
            return {"error": "unexpected response"}, 500

        post_json = response.json()
        new_post = Post(id=post_json['id'], userId=post_json["userId"], title=post_json["title"],
                        body=post_json["body"])

        db.session.add(new_post)
        db.session.commit()

    else:
        post_json = {"id": post.id, "userId": post.userId, "title": post.title, "body": post.body}

    return {"posts": post_json}, 200


def search_by_user(userId):
    posts = Post.query.filter_by(userId=userId).all()
    posts_in_json = iter_posts(posts)

    if not posts_in_json:
        return {"error": f" user {userId} has not posted yet"}, 404

    return {"posts": posts_in_json}, 200


def search_by_both(id, userId):
    posts = Post.query.filter_by(id=id, userId=userId).all()
    posts_in_json = iter_posts(posts)

    if not posts_in_json:
        return {"error": f"no post with id {id} by user {userId}"}, 404

    return {"posts": posts_in_json}, 200


def iter_posts(posts):
    output = []

    for post in posts:
        post_data = {"id": post.id, "userId": post.userId, "title": post.title, "body": post.body}
        output.append(post_data)

    return output
