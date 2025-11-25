import os
import time
from datetime import datetime, timezone

import flask
import timeago
from dotenv import load_dotenv

from handlers import auth, core, friends, posts, contracts, dms

load_dotenv()

app = flask.Flask(__name__)

@app.template_filter('convert_time')
def convert_time(ts):
    utc_dt = datetime.fromisoformat(ts)
    return timeago.format(utc_dt, datetime.now(timezone.utc))

@app.template_filter('display_username')
def display_username(username):
    """
    Clean username for display - removes timestamp from [REDACTED] usernames.
    [REDACTED]-1234567890 -> [REDACTED]
    """
    if username and username.startswith('[REDACTED]'):
        return '[REDACTED]'
    return username

app.register_blueprint(auth.blueprint)
app.register_blueprint(core.blueprint)
app.register_blueprint(friends.blueprint)
app.register_blueprint(posts.blueprint)
app.register_blueprint(contracts.blueprint)
app.register_blueprint(dms.blueprint)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)