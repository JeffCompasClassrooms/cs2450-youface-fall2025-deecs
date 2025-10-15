import flask

from db import posts, users, helpers

blueprint = flask.Blueprint("posts", __name__)

def get_user():
    
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
            flask.flash('You need to be logged in to do that.', 'danger')
    return user


@blueprint.route(f'/${user}/posts', methods=['POST'])
def post():
    """Creates a new post."""
    db = helpers.load_db()
    user = get_user()
    if not user:
        return flask.redirect(flask.url_for('login.loginscreen'))

    post = flask.request.form.get('post')
    posts.add_post(db, user, post)

    return flask.redirect(flask.url_for('login.index'))

@blueprint.route(f'/${user}/contracts', methods=['POST'])
def contracts():
    db.helpers.load_db()
    user = get_user()

    if not user:
        return flask.redirect(flask.url_for('login.loginscreen'))


    post = flask.request.form.get('post')
    posts.add_post(db, user, post)

    return flask.redirect(flask.url_for('login.index'))

