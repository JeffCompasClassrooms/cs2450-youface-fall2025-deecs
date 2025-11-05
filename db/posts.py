from db.client import get_supabase
from datetime import datetime

def get_feed_for_user(user_id):
    supabase = get_supabase()
    try:
        friends_response = supabase.table('friends').select('friend_id').eq('user_id', user_id).execute()
        friend_ids = [item['friend_id'] for item in friends_response.data]
        
        user_ids_for_feed = friend_ids + [user_id]

        response = supabase.table('posts').select(
            '*, profile:profiles(*), comments(*, profile:profiles(*))'
        ).in_('user_id', user_ids_for_feed).order(
            'created_at', desc=True
        ).execute()
        
        for post in response.data:
            if post.get('comments'):
                post['comments'].sort(key=lambda c: c.get('created_at', ''), reverse=True)
        
        return response.data
    except Exception as e:
        print(f"Error getting feed: {e}")
        return []

def get_posts_for_user(user_id):
    supabase = get_supabase()
    try:
        response = supabase.table('posts').select(
            '*, profile:profiles(*), comments(*, profile:profiles(*))'
        ).eq('user_id', user_id).order(
            'created_at', desc=True
        ).execute()

        for post in response.data:
            if post.get('comments'):
                post['comments'].sort(key=lambda c: c.get('created_at', ''), reverse=True)

        return response.data
    except Exception as e:
        print(f"Error getting user posts: {e}")
        return []

def create_post(user_id, content):
    supabase = get_supabase()
    try:
        response = supabase.table('posts').insert({
            'user_id': user_id,
            'content': content
        }).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating post: {e}")
        return None

def create_comment(user_id, content, post_id=None, parent_comment_id=None):
    supabase = get_supabase()
    try:
        comment_data = {
            'user_id': user_id,
            'content': content,
            'post_id': post_id,
            'parent_comment_id': parent_comment_id
        }
        response = supabase.table('comments').insert(comment_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating comment: {e}")
        return None

def like_post(post_id):
    supabase = get_supabase()
    try:
        supabase.rpc('increment_likes', {'post_id_to_update': post_id}).execute()
    except Exception as e:
        print(f"Error liking post: {e}")

def dislike_post(post_id):
    supabase = get_supabase()
    try:
        supabase.rpc('increment_dislikes', {'post_id_to_update': post_id}).execute()
    except Exception as e:
        print(f"Error disliking post: {e}")