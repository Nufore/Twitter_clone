from flask import Flask, render_template, request
from database import Base, engine, session
from models import User, Tweet, Like, Media
from werkzeug.utils import secure_filename
import os

root_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))


template_folder = os.path.join(root_dir, "templates")
static_directory = os.path.join(root_dir, "static")
UPLOAD_FOLDER = os.path.join(root_dir, "static/images")

app = Flask(__name__, template_folder=template_folder, static_folder=static_directory)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.before_request
def before_request_func():
    Base.metadata.create_all(engine)


@app.route("/create_users")
def create_users():
    session.add_all(
        [
            User(name='test user', api_key='test'),
            User(name='qwe user', api_key='qwe'),
            User(name='zxc user', api_key='zxc'),
        ]
    )
    session.commit()
    return {"message": "users created!"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tweets", methods=["POST"])
def post_tweets():
    api_key = request.headers.get("Api-Key")
    tweet_data = request.json.get("tweet_data")
    tweet_media_ids = request.json.get("tweet_media_ids")

    user = session.query(User).filter(User.api_key == api_key).one_or_none()

    new_tweet = Tweet(content=tweet_data, user_id=user.id)
    session.add(new_tweet)

    for media_id in tweet_media_ids:
        media_file = session.query(Media).filter(Media.id == media_id).one_or_none()
        if media_file:
            media_file.tweet_id = new_tweet.id

    session.commit()

    return {
        "result": True,
        "tweet_id": new_tweet.id
    }


@app.route("/api/medias", methods=["POST"])
def post_media():
    api_key = request.headers.get("Api-Key")

    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    new_media = Media(path=f"/static/images/{filename}")
    session.add(new_media)
    session.commit()

    return {
        "result": True,
        "media_id": new_media.id
    }


@app.route("/api/tweets/<int:tweet_id>", methods=["DELETE"])
def delete_tweet(tweet_id: int):
    api_key = request.headers.get("Api-Key")
    user = session.query(User).filter(User.api_key == api_key).one_or_none()
    tweet = session.query(Tweet).where(Tweet.id == tweet_id, Tweet.user_id == user.id).one_or_none()
    session.delete(tweet)
    session.commit()
    return {"result": True}


@app.route("/api/tweets/<int:id>/likes", methods=["POST"])
def set_like(id: int):
    api_key = request.headers.get("Api-Key")
    user = session.query(User).filter(User.api_key == api_key).one_or_none()
    tweet = session.query(Tweet).filter(Tweet.id == id).one_or_none()

    new_like = Like(user_id=user.id, tweet_id=tweet.id)
    session.add(new_like)
    session.commit()
    return {"result": True}


@app.route("/api/tweets/<int:tweet_id>/likes", methods=["DELETE"])
def delete_like(tweet_id: int):
    api_key = request.headers.get("Api-Key")
    user = session.query(User).filter(User.api_key == api_key).one_or_none()
    tweet = session.query(Tweet).filter(Tweet.id == tweet_id).one_or_none()

    like = session.query(Like).filter(Like.user_id == user.id, Like.tweet_id == tweet.id).one_or_none()

    session.delete(like)
    session.commit()
    return {"result": True}


@app.route("/api/users/<int:user_id>/follow", methods=["POST"])
def follow_user(user_id: int):
    api_key = request.headers.get("Api-Key")
    user_me = session.query(User).filter(User.api_key == api_key).one_or_none()
    user_to_follow = session.query(User).filter(User.id == user_id).one_or_none()
    user_me.follow(user_to_follow)
    session.commit()
    return {"result": True}


@app.route("/api/users/<int:user_id>/follow", methods=["DELETE"])
def delete_follow_user(user_id: int):
    api_key = request.headers.get("Api-Key")
    user_me = session.query(User).filter(User.api_key == api_key).one_or_none()
    user_to_unfollow = session.query(User).filter(User.id == user_id).one_or_none()
    user_me.unfollow(user_to_unfollow)
    session.commit()
    return {"result": True}


@app.route("/api/tweets", methods=["GET"])
def get_tweets():
    api_key = request.headers.get("Api-Key")
    user_me = session.query(User).filter(User.api_key == api_key).one_or_none()
    tweets = session.query(Tweet).all()

    data = {
        "result": True,
        "tweets": [tweet.to_json() for tweet in tweets],
    }
    return data


@app.route("/api/users/me", methods=["GET"])
def get_users_me():
    api_key = request.headers.get("Api-Key")
    user_me = session.query(User).filter(User.api_key == api_key).one_or_none()
    data = {
        "result": True,
        "user": {
            "id": user_me.id,
            "name": user_me.name,
            "followers": [usr.id_name_to_json() for usr in user_me.followers.all()],
            "following": [usr.id_name_to_json() for usr in user_me.followed.all()],
        }
    }
    return data


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int):
    user = session.query(User).filter(User.id == user_id).one_or_none()
    data = {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [usr.id_name_to_json() for usr in user.followers.all()],
            "following": [usr.id_name_to_json() for usr in user.followed.all()],
        }
    }
    return data


if __name__ == "__main__":
    app.run(debug=True, port=8000)
