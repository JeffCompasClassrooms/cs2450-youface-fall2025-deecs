import flask
from handlers.auth import login_required
from handlers import copy
from db import dms as dms_db
from db import users as users_db

blueprint = flask.Blueprint("dms", __name__)

@blueprint.route("/secure")
@login_required
def secure_channel():
    user_profile = flask.g.user
    user_id = user_profile['id']
    
    conversations = dms_db.get_messages(user_id)

    return flask.render_template(
        "secure.html",
        title=copy.title,
        subtitle=copy.subtitle,
        user=user_profile,
        username=user_profile['username'],
        conversations=conversations
    )

@blueprint.route("/secure/send", methods=["POST"])
@login_required
def send_message():
    user_id = flask.g.user['id']
    
    recipient_username = flask.request.form.get("recipient_username")
    content = flask.request.form.get("content")

    if not all([recipient_username, content]):
        flask.flash("Recipient and message content are required.", "danger")
        return flask.redirect(flask.url_for('dms.secure_channel'))

    recipient = users_db.get_profile_by_username(recipient_username)
    if not recipient:
        flask.flash(f"Agent '{recipient_username}' not found.", "danger")
        return flask.redirect(flask.url_for('dms.secure_channel'))
    
    if recipient['id'] == user_id:
        flask.flash("You cannot send a message to yourself.", "warning")
        return flask.redirect(flask.url_for('dms.secure_channel'))

    new_dm = dms_db.send_message(
        sender_id=user_id,
        recipient_id=recipient['id'],
        content=content
    )

    if new_dm:
        flask.flash("Message sent successfully.", "success")
    else:
        flask.flash("Error sending message.", "danger")

    return flask.redirect(flask.url_for("dms.secure_channel"))