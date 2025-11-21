import os
import flask
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")  # This is your anon key

if not url or not key:
    raise EnvironmentError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

# Default client uses anon key
supabase: Client = create_client(url, key)

def get_supabase():
    """
    Get Supabase client with user authentication if available.
    This respects RLS policies.
    """
    access_token = flask.session.get('access_token') if flask.has_request_context() else None
    
    if access_token:
        # Create authenticated client for this request
        client = create_client(url, key)
        # Set the user's session
        client.postgrest.auth(access_token)
        return client
    
    # Return default anon client (no auth)
    return supabase
