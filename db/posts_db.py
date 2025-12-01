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
    
    # Get posts for friends + self
    posts = (
        supabase.table(SUPABASE_TABLE)
        .select("*, profile:profiles(username)")
        .in_("user_id", friend_ids)
        .order("created_at", desc=True)
        .execute()
        .data
    )
    
    return _attach_comments_and_counts(posts)

def get_posts_for_user(user_id):
    supabase = get_supabase()
    posts = (
        supabase.table(SUPABASE_TABLE)
        .select("*, profile:profiles(username)")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
        .data
    )
    return _attach_comments_and_counts(posts)

def get_posts():
    """
    Optimized fetch: Gets posts and all associated comments in minimal network requests.
    """
    supabase = get_supabase()
    
    # 1. Fetch all posts
    posts = (
        supabase.table(SUPABASE_TABLE)
        .select("*, profile:profiles(username)")
        .order("created_at", desc=True)
        .execute()
        .data
    )
    
    return _attach_comments_and_counts(posts)

def _attach_comments_and_counts(posts):
    """
    Helper function to batch fetch comments for a list of posts 
    to avoid N+1 query performance issues.
    
    Manually joins profiles since FK relationship might not exist in schema.
    """
    if not posts:
        return []

    supabase = get_supabase()
    post_ids = [p['post_id'] for p in posts]

    # 2. Fetch ALL comments for these posts (Raw fetch, no join)
    all_comments = (
        supabase.table("comments")
        .select("*")
        .in_("post_id", post_ids)
        .order("created_at", desc=False)
        .execute()
        .data
    )
    
    # Map comments to post_ids immediately for counting
    comments_map = {pid: [] for pid in post_ids}
    
    if all_comments:
        # 3. Get unique user IDs from the comments to batch fetch profiles
        user_ids = list(set(c['user_id'] for c in all_comments))
        
        # 4. Fetch profiles in one request
        profiles = (
            supabase.table("profiles")
            .select("id, username, first_name, last_name")
            .in_("id", user_ids)
            .execute()
            .data
        )
        
        # Create lookup dict for profiles
        profiles_map = {p['id']: p for p in (profiles or [])}
        
        # 5. Attach profiles to comments and group by post
        for comment in all_comments:
            uid = comment['user_id']
            # Manual join in memory
            comment['profile'] = profiles_map.get(uid, {
                'username': 'Unknown User',
                'first_name': '',
                'last_name': ''
            })
            
            pid = comment['post_id']
            if pid in comments_map:
                comments_map[pid].append(comment)

    # 6. Attach processed comments to posts
    for post in posts:
        pid = post['post_id']
        comments = comments_map.get(pid, [])
        post['comments'] = comments
        post['comment_count'] = len(comments)
    
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
    """
    Legacy function, kept for compatibility if needed.
    """
    supabase = get_supabase()
    
    # Fetch comments
    comments = (
        supabase.table("comments")
        .select("*")
        .eq("post_id", post_id)
        .order("created_at", desc=False)
        .execute()
        .data
    )
    
    if not comments:
        return []
        
    # Manual Join for single post
    user_ids = list(set(c['user_id'] for c in comments))
    profiles = (
        supabase.table("profiles")
        .select("id, username, first_name, last_name")
        .in_("id", user_ids)
        .execute()
        .data
    )
    profiles_map = {p['id']: p for p in profiles}
    
    for comment in comments:
        comment['profile'] = profiles_map.get(comment['user_id'], {
            'username': 'Unknown User'
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