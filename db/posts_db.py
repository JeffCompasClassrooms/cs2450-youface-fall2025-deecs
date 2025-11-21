from db.client import get_supabase
from db.users import get_profile_by_id

SUPABASE_TABLE = "posts"

def get_feed_for_user(user_id):
    supabase = get_supabase()
    friends = (
        supabase.table("friends")
        .select("friend_id")
        .eq("user_id", user_id)
        .execute()
        .data
    )
    friend_ids = [f["friend_id"] for f in friends] + [user_id]
    
    return (
        supabase.table(SUPABASE_TABLE)
        .select("*, profile:profiles(username)")
        .in_("user_id", friend_ids)
        .order("created_at", desc=True)
        .execute()
        .data
    )

def get_posts_for_user(user_id):
    supabase = get_supabase()
    return (
        supabase.table(SUPABASE_TABLE)
        .select("*, profile:profiles(username)")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
        .data
    )

def get_posts():
    supabase = get_supabase()
    posts = (
        supabase.table(SUPABASE_TABLE)
        .select("*, profile:profiles(username)")
        .order("created_at", desc=True)
        .execute()
        .data
    )
    
    # Add comment count to each post
    for post in posts:
        comment_count = get_comment_count(post['post_id'])
        post['comment_count'] = comment_count
    
    return posts

def create_post(user_id, post_content):
    supabase = get_supabase()
    return (
        supabase.table(SUPABASE_TABLE)
        .insert(
            {
                "user_id": user_id,
                "content": post_content,
            }
        )
        .execute()
        .data
    )

def get_comments_for_post(post_id):
    """Get all comments for a post, flattened (no nested replies)"""
    supabase = get_supabase()
    
    # Get comments
    comments = (
        supabase.table("comments")
        .select("*")
        .eq("post_id", post_id)
        .order("created_at", desc=False)  # Oldest first
        .execute()
        .data
    )
    
    if not comments:
        return []
    
    # Get all unique user IDs
    user_ids = list(set(comment['user_id'] for comment in comments))
    
    # Fetch profiles for all users
    profiles = (
        supabase.table("profiles")
        .select("id, username, first_name, last_name")
        .in_("id", user_ids)
        .execute()
        .data
    )
    
    # Create lookup dictionary
    profiles_dict = {p['id']: p for p in profiles}
    
    # Attach profile to each comment
    for comment in comments:
        comment['profile'] = profiles_dict.get(comment['user_id'], {
            'username': 'Unknown User',
            'first_name': '',
            'last_name': ''
        })
    
    return comments

def get_comment_count(post_id):
    """Get the number of comments for a post"""
    supabase = get_supabase()
    response = (
        supabase.table("comments")
        .select("comment_id", count="exact")
        .eq("post_id", post_id)
        .execute()
    )
    return response.count if response.count else 0

def create_comment(user_id, content, post_id):
    """Create a comment on a post (all comments are top-level)"""
    supabase = get_supabase()
    
    comment_data = {
        "user_id": user_id,
        "content": content,
        "post_id": post_id,
        "parent_comment_id": None  # Always None - flat structure
    }
    
    return (
        supabase.table("comments")
        .insert(comment_data)
        .execute()
        .data
    )

def like_post(post_id, user_id):
    supabase = get_supabase()
    return (
        supabase.table("likes")
        .insert(
            {
                "post_id": post_id,
                "user_id": user_id,
            }
        )
        .execute()
    )

def dislike_post(post_id, user_id):
    supabase = get_supabase()
    return (
        supabase.table("likes")
        .delete()
        .eq("post_id", post_id)
        .eq("user_id", user_id)
        .execute()
    )