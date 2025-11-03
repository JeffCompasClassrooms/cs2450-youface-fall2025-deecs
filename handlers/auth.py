import flask
from functools import wraps
from db.client import get_supabase
from db import users as users_db

blueprint = flask.Blueprint("auth", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        supabase = get_supabase()
        access_token = flask.session.get('access_token')

        if not access_token:
            return flask.redirect(flask.url_for('auth.login_screen'))

        try:
            user_response = supabase.auth.get_user(access_token)
            user = user_response.user
            if not user:
                flask.session.clear()
                return flask.redirect(flask.url_for('auth.login_screen'))
            
            profile = users_db.get_profile_by_id(user.id)
            if not profile:
                flask.session.clear()
                flask.flash("Your profile could not be found. Please log in again.", "danger")
                return flask.redirect(flask.url_for('auth.login_screen'))

            flask.g.user = profile
            flask.g.auth_user = user
        
        except Exception as e:
            flask.session.clear()
            flask.flash(f"Your session has expired or is invalid. Please log in again. {e}", "danger")
            return flask.redirect(flask.url_for('auth.login_screen'))

        return f(*args, **kwargs)
    return decorated_function


@blueprint.route("/login_screen")
def login_screen():
    if flask.session.get('access_token'):
        return flask.redirect(flask.url_for('core.index'))
    
    return flask.render_template("login.html")

@blueprint.route("/login", methods=["POST"])
def login():
    supabase = get_supabase()
    email = flask.request.form.get("email")
    password = flask.request.form.get("password")

    try:
        session_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        flask.session['access_token'] = session_response.session.access_token
        flask.flash("Logged in successfully!", "success")
        return flask.redirect(flask.url_for('core.index'))
    
    except Exception as e:
        flask.flash(f"Login failed: {e}", "danger")
        return flask.redirect(flask.url_for('auth.login_screen'))

@blueprint.route("/signup", methods=["POST"])
def signup():
    supabase = get_supabase()
    email = flask.request.form.get("email")
    password = flask.request.form.get("password")
    username = flask.request.form.get("username")
    first_name = flask.request.form.get("first_name")
    last_name = flask.request.form.get("last_name")

    if not all([email, password, username, first_name, last_name]):
        flask.flash("All fields are required for signup.", "danger")
        return flask.redirect(flask.url_for('auth.login_screen'))

    try:
        user_response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name
                }
            }
        })
        
        if user_response.user:
            flask.session['access_token'] = user_response.session.access_token
            flask.flash("Account created successfully! You are now logged in.", "success")
            return flask.redirect(flask.url_for('core.index'))
        else:
            flask.flash("Signup failed. Please try again.", "danger")
            return flask.redirect(flask.url_for('auth.login_screen'))

    except Exception as e:
        flask.flash(f"Signup failed: {e}", "danger")
        return flask.redirect(flask.url_for('auth.login_screen'))


@blueprint.route("/logout", methods=["POST"])
def logout():
    supabase = get_supabase()
    access_token = flask.session.get('access_token')
    if access_token:
        try:
            supabase.auth.sign_out(access_token)
        except Exception:
            pass 
    
    flask.session.clear()
    flask.flash("You have been logged out.", "success")
    return flask.redirect(flask.url_for('auth.login_screen'))