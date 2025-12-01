import flask
from handlers.auth import login_required
from handlers import copy
from db import users as users_db
from db import posts_db
from db import contracts_db # Added to fetch tags

blueprint = flask.Blueprint("core", __name__)

@blueprint.route("/")
@login_required
def index():
    user_profile = flask.g.user
    
    # Optimized fetch: get_posts now returns posts WITH comments and counts already attached.
    # This reduces 20+ database calls to just 2.
    feed_posts = posts_db.get_posts() 
    
    # REMOVED: The slow N+1 loop that was here
    # for post in feed_posts:
    #    post['comments'] = posts_db.get_comments_for_post(post['post_id'])

    friends_list = users_db.get_friends(user_profile['id'])
    pending_requests = users_db.get_pending_friend_requests(user_profile['id'])
    sent_requests = users_db.get_sent_friend_requests(user_profile['id'])

    return flask.render_template(
        "feed.html",
        title=copy.title,
        subtitle=copy.subtitle,
        user=user_profile,
        username=user_profile['username'],
        friends=friends_list,
        pending_requests=pending_requests,
        sent_requests=sent_requests,
        posts=feed_posts
    )

@blueprint.route("/profile")
@login_required
def profile():
    user_profile = flask.g.user
    # Fetch all available tags for the edit modal
    all_tags = contracts_db.get_all_tags()
    
    return flask.render_template(
        "profile.html",
        title=copy.title,
        subtitle=copy.subtitle,
        user=user_profile,
        username=user_profile['username'],
        tags=all_tags
    )

@blueprint.route("/profile/update_tags", methods=["POST"])
@login_required
def update_tags():
    user_id = flask.g.user['id']
    tags = flask.request.form.getlist("tags")
    
    success, message, category = users_db.update_user_tags(user_id, tags)
    
    # CRITICAL FIX: Clear the session cache so the new tags load immediately
    if success and 'user_profile' in flask.session:
        del flask.session['user_profile']
    
    flask.flash(message, category)
    return flask.redirect(flask.url_for('core.profile'))

@blueprint.route("/friend/<username>")
@login_required
def view_friend(username):
    user_profile = flask.g.user
    
    friend_profile = users_db.get_profile_by_username(username)
    if not friend_profile:
        flask.flash("That user does not exist.", "danger")
        return flask.redirect(flask.url_for('core.index'))

    friends_list = users_db.get_friends(user_profile['id'])
    
    # Optimized fetch for specific user as well
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