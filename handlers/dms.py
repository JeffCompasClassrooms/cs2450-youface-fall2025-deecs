import flask
from handlers.auth import login_required
from handlers import copy
from db import dms_db
from db import users as users_db

blueprint = flask.Blueprint("dms", __name__)

@blueprint.route("/secure")
@login_required
def secure_channel():
    user_profile = flask.g.user
    user_id = user_profile['id']
    
    # Get optional agent parameter for pre-populating recipient
    agent_username = flask.request.args.get('agent', '').strip()
    
    # Get conversations grouped by partner
    conversations = dms_db.get_conversations(user_id)
    
    # For each conversation, fetch all messages
    for convo in conversations:
        convo['messages'] = dms_db.get_messages_with_user(user_id, convo['partner_id'])

    return flask.render_template(
        "secure.html",
        title=copy.title,
        subtitle=copy.subtitle,
        user=user_profile,
        username=user_profile['username'],
        conversations=conversations,
        agent_username=agent_username  # Pass to template
    )

@blueprint.route("/secure/send", methods=["POST"])
@login_required
def send_secure_message():
    user_id = flask.g.user['id']
    
    recipient_username = flask.request.form.get("username")
    content = flask.request.form.get("content")

    if not all([recipient_username, content]):
        flask.flash("Recipient and message content are required.", "danger")
        return flask.redirect(flask.url_for('dms.secure_channel'))

    # Check for self-messaging BEFORE lookup
    if recipient_username == flask.g.user['username']:
        flask.flash("You cannot send a message to yourself.", "warning")
        return flask.redirect(flask.url_for('dms.secure_channel'))

    recipient = users_db.get_profile_by_username(recipient_username)
    if not recipient:
        flask.flash(f"Agent '{recipient_username}' not found.", "danger")
        return flask.redirect(flask.url_for('dms.secure_channel'))

    new_dm, error = dms_db.send_message(
        sender_id=user_id,
        receiver_username=recipient_username,
        content=content
    )

    if new_dm and not error:
        flask.flash("Message sent successfully.", "success")
    else:
        flask.flash(f"Error sending message: {error or 'Unknown error'}", "danger")

    return flask.redirect(flask.url_for("dms.secure_channel"))