import flask
from handlers.auth import login_required
from db import posts as posts_db

blueprint = flask.Blueprint("posts", __name__)

@blueprint.route("/post", methods=["POST"])
@login_required
def post():
    user_id = flask.g.user['id']
    content = flask.request.form.get("post_content")

    if not content:
        flask.flash("Your post cannot be empty.", "danger")
        return flask.redirect(flask.url_for('core.index'))

    new_post = posts_db.create_post(user_id, content)
    
    if new_post:
        flask.flash("Intel transmitted successfully.", "success")
    else:
        flask.flash("Error transmitting intel. Please try again.", "danger")

    return flask.redirect(flask.url_for("core.index"))

@blueprint.route("/post/<post_id>/comment", methods=["POST"])
@login_required
def comment_on_post(post_id):
    user_id = flask.g.user['id']
    content = flask.request.form.get("comment_content")
    
    if not content:
        flask.flash("Your comment cannot be empty.", "danger")
        return flask.redirect(flask.url_for('core.index')) 

    new_comment = posts_db.create_comment(
        user_id=user_id,
        post_id=post_id,
        content=content
    )
    
    if new_comment:
        flask.flash("Comment added.", "success")
    else:
        flask.flash("Error adding comment.", "danger")
        
    return flask.redirect(flask.request.referrer or flask.url_for('core.index'))

@blueprint.route("/comment/<comment_id>/reply", methods=["POST"])
@login_required
def reply_to_comment(comment_id):
    user_id = flask.g.user['id']
    content = flask.request.form.get("reply_content")

    if not content:
        flask.flash("Your reply cannot be empty.", "danger")
        return flask.redirect(flask.request.referrer or flask.url_for('core.index'))

    new_reply = posts_db.create_comment(
        user_id=user_id,
        content=content,
        parent_comment_id=comment_id
    )
    
    if new_reply:
        flask.flash("Reply added.", "success")
    else:
        flask.flash("Error adding reply.", "danger")
        
    return flask.redirect(flask.request.referrer or flask.url_for('core.index'))

@blueprint.route("/post/<post_id>/like", methods=["POST"])
@login_required
def like_post(post_id):
    user_id = flask.g.user['id']
    posts_db.like_post(post_id)
    return flask.redirect(flask.request.referrer or flask.url_for('core.index'))

@blueprint.route("/post/<post_id>/dislike", methods=["POST"])
@login_required
def dislike_post(post_id):
    user_id = flask.g.user['id']
    posts_db.dislike_post(post_id)
    return flask.redirect(flask.request.referrer or flask.url_for('core.index'))