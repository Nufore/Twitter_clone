from flask import Flask, render_template, request
from database import Base, engine, session
from models import User
import os

root_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

template_folder = os.path.join(root_dir, "templates")
static_directory = os.path.join(root_dir, "static")

app = Flask(__name__, template_folder=template_folder, static_folder=static_directory)


@app.before_request
def before_request_func():
    Base.metadata.create_all(engine)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tweets")
def get_tweets():
    data = {
        "result": True,
        "tweets": [
            {
                "id": 1,
                "content": "test tweet",
                "attachments": [],
                "author": {
                    "id": 1,
                    "name": "test author"
                },
                "likes": [
                    {
                        "user_id": 2,
                        "name": "test_user"
                    }
                ],
            },
        ]
    }
    return data


@app.route("/api/users/me")
def get_users_me():
    api_key = request.headers.get("Api-Key")
    user_me = session.query(User).filter(User.api_key == api_key).one_or_none()
    data = {
        "result": True,
        "user": {
            "id": user_me.id,
            "name": user_me.name,
            "followers": [
                {
                    "id": 2,
                    "name": "test user 2"
                },
                {
                    "id": 3,
                    "name": "test user 3"
                },
            ],
            "following": [
                {
                    "id": 3,
                    "name": "test user 3"
                },
            ]
        }
    }
    return data


@app.route("/api/users/<int:user_id>/follow", methods=["POST"])
def follow_user(user_id: int):
    api_key = request.headers.get("Api-Key")
    user_me = session.query(User).filter(User.api_key == api_key).one_or_none()

    user_to_follow = session.query(User).filter(User.id == user_id).one_or_none()

    user_me.follow(user_to_follow)
    session.commit()
    return {"result": True}


if __name__ == "__main__":
    app.run(debug=True, port=8000)
