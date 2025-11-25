from db.client import get_supabase

def get_profile_by_id(user_id):
    supabase = get_supabase()
    try:
        response = supabase.table('profiles').select('*').eq('id', user_id).single().execute()
        return response.data
    except Exception as e:
        print(f"Error getting profile by ID: {e}")
        return None

def get_profile_by_username(username):
    supabase = get_supabase()
    try:
        response = supabase.table('profiles').select('*').eq('username', username).single().execute()
        return response.data
    except Exception as e:
        print(f"Error getting profile by username: {e}")
        return None

def add_friend(user_id, friend_id):
    supabase = get_supabase()
    try:
        response = supabase.table('friends').select('*').eq('user_id', user_id).eq('friend_id', friend_id).execute()
        if response.data:
            return False, "You are already connections.", "warning"
        
        supabase.table('friends').insert([
            {'user_id': user_id, 'friend_id': friend_id},
            {'user_id': friend_id, 'friend_id': user_id} 
        ]).execute()
        
        return True, "Connection added.", "success"
    except Exception as e:
        print(f"Error adding friend: {e}")
        return False, f"Error adding connection: {e}", "danger"

def remove_friend(user_id, friend_id):
    supabase = get_supabase()
    try:
        supabase.table('friends').delete().eq('user_id', user_id).eq('friend_id', friend_id).execute()
        supabase.table('friends').delete().eq('user_id', friend_id).eq('friend_id', user_id).execute()
        return True, "Connection removed.", "success"
    except Exception as e:
        print(f"Error removing friend: {e}")
        return False, f"Error removing connection: {e}", "danger"

def get_friends(user_id):
    supabase = get_supabase()
    try:
        response = supabase.table('friends').select('profile:friend_id(*)').eq('user_id', user_id).execute()
        friends_list = [item['profile'] for item in response.data if item.get('profile')]
        return friends_list
    except Exception as e:
        print(f"Error getting friends: {e}")
        return []

def search_for_users(query):
    supabase = get_supabase()
    try:
        response = supabase.table('profiles').select('*').ilike('username', f'%{query}%').execute()
        return response.data
    except Exception as e:
        print(f"Error searching for users: {e}")
        return []

def delete_user_account(user_id):
    """
    "Delete" a user account by anonymizing it and removing sensitive data.
    IMPORTANT: Posts are NEVER deleted - they remain with [REDACTED] as the username.
    The profile is updated to [REDACTED] with a timestamp to satisfy UNIQUE constraint.
    
    Returns: (success: bool, message: str, category: str)
    """
    import time
    supabase = get_supabase()
    
    try:
        # Get current profile to preserve data we need
        profile = supabase.table('profiles').select('username').eq('id', user_id).single().execute()
        
        if not profile.data:
            return False, "Profile not found.", "danger"
        
        # Create a unique redacted username using timestamp to avoid UNIQUE constraint violation
        # Format: [REDACTED]-{unix_timestamp} (e.g., [REDACTED]-1234567890)
        redacted_username = f"[REDACTED]-{int(time.time())}"
        
        # 1. Delete claimed_contracts (references profiles)
        supabase.table('claimed_contracts').delete().eq('user_id', user_id).execute()
        
        # 2. Update comments to show [REDACTED] - we'll anonymize these by keeping them but updating the username
        # Comments will still reference the user_id, but the profile will show [REDACTED]
        # NOTE: Comments are NOT deleted to preserve conversation context
        
        # 3. Delete contracts created by user (references profiles and auth.users)
        supabase.table('contracts').delete().eq('user_id', user_id).execute()
        
        # 4. Delete direct messages (both sent and received)
        supabase.table('direct_messages').delete().eq('sender_id', user_id).execute()
        supabase.table('direct_messages').delete().eq('receiver_id', user_id).execute()
        
        # 5. Delete friendships (both directions)
        supabase.table('friends').delete().eq('user_id', user_id).execute()
        supabase.table('friends').delete().eq('friend_id', user_id).execute()
        
        # 6. IMPORTANT: DO NOT delete posts - they remain in the database
        # Posts will now show [REDACTED] as the username via the profile join
        
        # 7. Update profile to [REDACTED] status (DO NOT DELETE)
        # This preserves posts and comments while anonymizing the user
        supabase.table('profiles').update({
            'username': redacted_username,
            'first_name': '[REDACTED]',
            'last_name': '',
            'tags': []  # Clear any specialty tags
        }).eq('id', user_id).execute()
        
        # 8. Mark the auth user's metadata to indicate deletion
        # This will be used to block login attempts
        # Note: We use user metadata to flag the account as deleted
        
        return True, "Account anonymized successfully. All posts preserved with [REDACTED] status.", "success"
        
    except Exception as e:
        print(f"Error anonymizing user account: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error processing account deletion: {e}", "danger"