import flask

from db import posts, users, helpers

blueprint = flask.Blueprint("posts", __name__)

def get_user():
    
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)

@blueprint.route(f'/${user}/posts', methods=['POST'])
def post():
    """Creates a new post."""
    db = helpers.load_db()
    user = get_user()
    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    post = flask.request.form.get('post')
    posts.add_post(db, user, post)

    return flask.redirect(flask.url_for('login.index'))

@blueprint.route(f'/${user}.posts', methods=['POST'])
def contracts():
    db.helpers.load_db()
    user = get_user()

    post = flask.request.form.get('post')
    posts.add_post(db, user, post)

    return flask.redirect(flask.url_for('login.index'))

