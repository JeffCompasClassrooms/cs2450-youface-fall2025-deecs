import flask
from handlers.auth import login_required
from handlers import copy
from db import users as users_db
from db import posts as posts_db

blueprint = flask.Blueprint("core", __name__)

@blueprint.route("/")
@login_required
def index():
    user_profile = flask.g.user
    
    feed_posts = posts_db.get_posts() 

    friends_list = users_db.get_friends(user_profile['id'])

    return flask.render_template(
        "feed.html",
        title=copy.title,
        subtitle=copy.subtitle,
        user=user_profile,
        username=user_profile['username'],
        friends=friends_list,
        posts=feed_posts
    )

@blueprint.route("/profile")
@login_required
def profile():
    user_profile = flask.g.user
    return flask.render_template(
        "profile.html",
        title=copy.title,
        subtitle=copy.subtitle,
        user=user_profile,
        username=user_profile['username'],
    )

@blueprint.route("/friend/<username>")
@login_required
def view_friend(username):
    user_profile = flask.g.user
    
    friend_profile = users_db.get_profile_by_username(username)
    if not friend_profile:
        flask.flash("That user does not exist.", "danger")
        return flask.redirect(flask.url_for('core.index'))

    friends_list = users_db.get_friends(user_profile['id'])
    friend_posts = posts_db.get_posts_for_user(friend_profile['id'])

    return flask.render_template(
        "friend.html",
        title=copy.title,
        subtitle=copy.subtitle,
        user=user_profile,
        username=user_profile['username'],
        friend=friend_profile,
        friends=friends_list,
        posts=friend_posts
    )

@blueprint.route("/search")
@login_required
def search():
    user_profile = flask.g.user
    q = (flask.request.args.get('q') or '').strip()
    
    search_results = []
    if q:
        search_results = users_db.search_for_users(q)

    return flask.render_template(
        "search.html",
        title=copy.title,
        subtitle=copy.subtitle,
        user=user_profile,
        username=user_profile['username'],
        q=q,
        results=search_results
    )