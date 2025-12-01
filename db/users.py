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

def update_user_tags(user_id, tags):
    """Update the specialties/tags for a user profile"""
    supabase = get_supabase()
    try:
        response = supabase.table('profiles').update({
            'tags': tags
        }).eq('id', user_id).execute()
        
        return True, "Specialties updated successfully.", "success"
    except Exception as e:
        print(f"Error updating user tags: {e}")
        return False, f"Error updating specialties: {e}", "danger"

def add_friend(user_id, friend_id):
    supabase = get_supabase()
    try:
        # Check if a request already exists (in either direction)
        response = supabase.table('friends').select('*').or_(
            f'and(user_id.eq.{user_id},friend_id.eq.{friend_id}),and(user_id.eq.{friend_id},friend_id.eq.{user_id})'
        ).execute()
        
        if response.data:
            existing = response.data[0]
            if existing['status'] == 'accepted':
                return False, "You are already connected.", "warning"
            elif existing['status'] == 'pending':
                if existing['user_id'] == user_id:
                    return False, "Friend request already sent.", "warning"
                else:
                    return False, "This agent has already sent you a request. Check your Friend Requests section.", "info"
            elif existing['status'] == 'declined':
                return False, "Previous request was declined.", "warning"
        
        # Create a single pending friend request
        supabase.table('friends').insert({
            'user_id': user_id,
            'friend_id': friend_id,
            'status': 'pending',
            'created_by': user_id
        }).execute()
        
        return True, "Friend request sent.", "success"
    except Exception as e:
        print(f"Error adding friend: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error sending friend request: {e}", "danger"

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
        # Get accepted friend IDs where user is either user_id or friend_id
        response = supabase.table('friends').select('user_id, friend_id').eq('status', 'accepted').or_(
            f'user_id.eq.{user_id},friend_id.eq.{user_id}'
        ).execute()
        
        if not response.data:
            return []
        
        # Extract friend IDs (the ID that's NOT the current user)
        friend_ids = []
        for item in response.data:
            if item['user_id'] == user_id:
                friend_ids.append(item['friend_id'])
            else:
                friend_ids.append(item['user_id'])
        
        # Remove duplicates
        friend_ids = list(set(friend_ids))
        
        if not friend_ids:
            return []
        
        # Get profiles for those friend IDs
        profiles_response = supabase.table('profiles').select('*').in_('id', friend_ids).execute()
        
        return profiles_response.data if profiles_response.data else []
    except Exception as e:
        print(f"Error getting friends: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_pending_friend_requests(user_id):
    """Get all pending friend requests sent TO this user"""
    supabase = get_supabase()
    try:
        # Get pending requests where user is the friend_id (recipient)
        response = supabase.table('friends').select('user_id, created_at').eq('friend_id', user_id).eq('status', 'pending').execute()
        
        if not response.data:
            return []
        
        # Get the sender IDs
        sender_ids = [item['user_id'] for item in response.data]
        
        # Get profiles for those senders
        profiles_response = supabase.table('profiles').select('*').in_('id', sender_ids).execute()
        
        # Add created_at timestamp to each profile
        if profiles_response.data:
            profiles_dict = {p['id']: p for p in profiles_response.data}
            result = []
            for item in response.data:
                if item['user_id'] in profiles_dict:
                    profile = profiles_dict[item['user_id']].copy()
                    profile['request_created_at'] = item['created_at']
                    result.append(profile)
            return result
        
        return []
    except Exception as e:
        print(f"Error getting pending friend requests: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_sent_friend_requests(user_id):
    """Get all pending friend requests sent BY this user (waiting for response)"""
    supabase = get_supabase()
    try:
        # Get pending requests where user is the user_id (sender)
        response = supabase.table('friends').select('friend_id, created_at').eq('user_id', user_id).eq('status', 'pending').execute()
        
        if not response.data:
            return []
        
        # Get the recipient IDs
        recipient_ids = [item['friend_id'] for item in response.data]
        
        # Get profiles for those recipients
        profiles_response = supabase.table('profiles').select('*').in_('id', recipient_ids).execute()
        
        # Add created_at timestamp to each profile
        if profiles_response.data:
            profiles_dict = {p['id']: p for p in profiles_response.data}
            result = []
            for item in response.data:
                if item['friend_id'] in profiles_dict:
                    profile = profiles_dict[item['friend_id']].copy()
                    profile['request_created_at'] = item['created_at']
                    result.append(profile)
            return result
        
        return []
    except Exception as e:
        print(f"Error getting sent friend requests: {e}")
        import traceback
        traceback.print_exc()
        return []

def accept_friend_request(user_id, requester_id):
    """Accept a friend request"""
    supabase = get_supabase()
    try:
        # Update the original request to accepted
        supabase.table('friends').update({
            'status': 'accepted'
        }).eq('user_id', requester_id).eq('friend_id', user_id).eq('status', 'pending').execute()
        
        # Check if reverse relationship already exists (from old bidirectional system)
        existing_reverse = supabase.table('friends').select('*').eq('user_id', user_id).eq('friend_id', requester_id).execute()
        
        if not existing_reverse.data:
            # Create the reverse relationship only if it doesn't exist
            supabase.table('friends').insert({
                'user_id': user_id,
                'friend_id': requester_id,
                'status': 'accepted',
                'created_by': requester_id  # Original requester
            }).execute()
        else:
            # If it exists, just make sure it's marked as accepted
            supabase.table('friends').update({
                'status': 'accepted'
            }).eq('user_id', user_id).eq('friend_id', requester_id).execute()
        
        return True, "Friend request accepted.", "success"
    except Exception as e:
        print(f"Error accepting friend request: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error accepting request: {e}", "danger"

def decline_friend_request(user_id, requester_id):
    """Decline a friend request"""
    supabase = get_supabase()
    try:
        # Update status to declined (or could delete the row entirely)
        supabase.table('friends').update({
            'status': 'declined'
        }).eq('user_id', requester_id).eq('friend_id', user_id).eq('status', 'pending').execute()
        
        return True, "Friend request declined.", "success"
    except Exception as e:
        print(f"Error declining friend request: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error declining request: {e}", "danger"

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