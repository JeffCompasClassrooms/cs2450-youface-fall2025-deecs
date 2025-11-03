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