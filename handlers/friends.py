import flask
from handlers.auth import login_required
from db import users as users_db

blueprint = flask.Blueprint("friends", __name__)

@blueprint.route("/addfriend", methods=["POST"])
@login_required
def addfriend():
    user_id = flask.g.user['id']
    friend_username = flask.request.form.get("friend_username")

    if not friend_username:
        flask.flash("Username cannot be empty.", "danger")
        return flask.redirect(flask.url_for('core.index'))

    friend_profile = users_db.get_profile_by_username(friend_username)
    
    if not friend_profile:
        flask.flash(f"Agent '{friend_username}' not found.", "danger")
        return flask.redirect(flask.url_for('core.index'))

    if friend_profile['id'] == user_id:
        flask.flash("You cannot add yourself as a connection.", "warning")
        return flask.redirect(flask.url_for('core.index'))

    success, message, category = users_db.add_friend(user_id, friend_profile['id'])
    
    flask.flash(message, category)
    return flask.redirect(flask.url_for("core.index"))

@blueprint.route("/unfriend", methods=["POST"])
@login_required
def unfriend():
    user_id = flask.g.user['id']
    friend_id = flask.request.form.get("friend_id")

    if not friend_id:
        flask.flash("Invalid request.", "danger")
        return flask.redirect(flask.url_for('core.index'))

    success, message, category = users_db.remove_friend(user_id, friend_id)

    flask.flash(message, category)
    return flask.redirect(flask.url_for("core.index"))

@blueprint.route("/accept_request", methods=["POST"])
@login_required
def accept_request():
    user_id = flask.g.user['id']
    requester_id = flask.request.form.get("requester_id")

    if not requester_id:
        flask.flash("Invalid request.", "danger")
        return flask.redirect(flask.url_for('core.index'))

    success, message, category = users_db.accept_friend_request(user_id, requester_id)

    flask.flash(message, category)
    return flask.redirect(flask.url_for("core.index"))

@blueprint.route("/decline_request", methods=["POST"])
@login_required
def decline_request():
    user_id = flask.g.user['id']
    requester_id = flask.request.form.get("requester_id")

    if not requester_id:
        flask.flash("Invalid request.", "danger")
        return flask.redirect(flask.url_for('core.index'))

    success, message, category = users_db.decline_friend_request(user_id, requester_id)

    flask.flash(message, category)
    return flask.redirect(flask.url_for("core.index"))