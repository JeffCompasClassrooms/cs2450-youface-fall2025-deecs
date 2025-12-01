import flask
from functools import wraps
from db.client import get_supabase
from db import users as users_db

blueprint = flask.Blueprint("auth", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = flask.session.get('access_token')
        
        # OPTIMIZATION: Check if we already have the profile cached in the session
        # This saves 2 network round-trips to Supabase on every single page load.
        cached_profile = flask.session.get('user_profile')
        cached_email = flask.session.get('user_email')

        if not access_token:
            return flask.redirect(flask.url_for('auth.login_screen'))

        # If we have cached data, use it directly (FAST PATH)
        if cached_profile and cached_email:
            flask.g.user = cached_profile
            # Mock the auth_user object to keep compatibility with other routes
            class MockAuthUser:
                def __init__(self, email, id):
                    self.email = email
                    self.id = id
                    # Add dummy timestamp if needed for deletion logic
                    self.created_at = "2024-01-01T00:00:00.000000+00:00" 
            
            flask.g.auth_user = MockAuthUser(cached_email, cached_profile['id'])
            return f(*args, **kwargs)

        # If no cache, perform the slow network calls (SLOW PATH - Only happens once)
        supabase = get_supabase()
        try:
            user_response = supabase.auth.get_user(access_token)
            user = user_response.user
            if not user:
                flask.session.clear()
                return flask.redirect(flask.url_for('auth.login_screen'))
            
            # Check if account is marked as deleted
            if user.user_metadata and user.user_metadata.get('account_deleted'):
                flask.session.clear()
                flask.flash("This agent profile has been redacted and can no longer be accessed.", "danger")
                return flask.redirect(flask.url_for('auth.login_screen'))
            
            profile = users_db.get_profile_by_id(user.id)
            if not profile:
                flask.session.clear()
                flask.flash("Your profile could not be found. Please log in again.", "danger")
                return flask.redirect(flask.url_for('auth.login_screen'))
            
            # Check if profile is redacted
            if profile.get('username', '').startswith('[REDACTED]'):
                flask.session.clear()
                flask.flash("This agent profile has been redacted and can no longer be accessed.", "danger")
                return flask.redirect(flask.url_for('auth.login_screen'))

            # CACHE THE DATA
            flask.session['user_profile'] = profile
            flask.session['user_email'] = user.email

            flask.g.user = profile
            flask.g.auth_user = user
        
        except Exception as e:
            # If token is invalid/expired, clear session and redirect
            flask.session.clear()
            # flask.flash(f"Session expired. Please login again.", "danger") # Removed session expired flash
            return flask.redirect(flask.url_for('auth.login_screen'))

        return f(*args, **kwargs)
    return decorated_function


@blueprint.route("/login_screen")
def login_screen():
    if flask.session.get('access_token'):
        return flask.redirect(flask.url_for('core.index'))
    
    return flask.render_template("login.html")

@blueprint.route("/signup_screen")
def signup_screen():
    if flask.session.get('access_token'):
        return flask.redirect(flask.url_for('core.index'))
    
    return flask.render_template("signup.html")

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
        
        user = session_response.user
        
        # Check deleted status
        if user and user.user_metadata:
            if user.user_metadata.get('account_deleted'):
                try: supabase.auth.sign_out(session_response.session.access_token)
                except: pass
                flask.flash("This agent profile has been redacted.", "danger")
                return flask.redirect(flask.url_for('auth.login_screen'))
        
        # Check profile redacted status
        profile = users_db.get_profile_by_id(user.id)
        if profile and profile.get('username', '').startswith('[REDACTED]'):
            try: supabase.auth.sign_out(session_response.session.access_token)
            except: pass
            flask.flash("This agent profile has been redacted.", "danger")
            return flask.redirect(flask.url_for('auth.login_screen'))
        
        # Store in session
        flask.session['access_token'] = session_response.session.access_token
        flask.session['user_profile'] = profile
        flask.session['user_email'] = user.email
        
        # REMOVED SUCCESS FLASH
        # flask.flash("Logged in successfully!", "success")
        return flask.redirect(flask.url_for('core.index'))
    
    except Exception as e:
        flask.flash(f"Login failed: {str(e)}", "danger")
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
        return flask.redirect(flask.url_for('auth.signup_screen'))

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
            # Note: We don't have the full profile object yet (it's created by trigger in DB usually)
            # So we set the token, but clear the profile cache so the first request fetches it
            flask.session['access_token'] = user_response.session.access_token
            if 'user_profile' in flask.session:
                del flask.session['user_profile']
            
            # REMOVED SUCCESS FLASH
            # flask.flash("Account created successfully! You are now logged in.", "success")
            return flask.redirect(flask.url_for('core.index'))
        else:
            flask.flash("Signup failed. Please try again.", "danger")
            return flask.redirect(flask.url_for('auth.signup_screen'))

    except Exception as e:
        flask.flash(f"Signup failed: {e}", "danger")
        return flask.redirect(flask.url_for('auth.signup_screen'))


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

@blueprint.route("/delete_account", methods=['POST'])
@login_required
def delete_account():
    # ... logic remains same ...
    # Just ensure we clear the specific session keys on success
    supabase = get_supabase()
    user_id = flask.g.user['id']
    password = flask.request.form.get("password")
    
    if not password:
        flask.flash("Password is required.", "danger")
        return flask.redirect(flask.url_for('core.profile'))
    
    try:
        # Verify password
        email = flask.g.auth_user.email
        try:
            supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
        except Exception as e:
            flask.flash("Incorrect password.", "danger")
            return flask.redirect(flask.url_for('core.profile'))
        
        success, message, category = users_db.delete_user_account(user_id)
        
        if not success:
            flask.flash(message, category)
            return flask.redirect(flask.url_for('core.profile'))
        
        # Mark auth user deleted
        access_token = flask.session.get('access_token')
        if access_token:
            try:
                supabase.auth.update_user({
                    "data": {
                        "account_deleted": True,
                        "deleted_at": "now()"
                    }
                })
                supabase.auth.sign_out(access_token)
            except:
                pass
        
        flask.session.clear()
        flask.flash("Profile redacted.", "success")
        return flask.redirect(flask.url_for('auth.login_screen'))
        
    except Exception as e:
        print(f"Error: {e}")
        flask.flash(f"Error processing deletion: {e}", "danger")
        return flask.redirect(flask.url_for('core.profile'))