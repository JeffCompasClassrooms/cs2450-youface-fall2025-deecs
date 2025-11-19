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
    return (
        supabase.table(SUPABASE_TABLE)
        .select("*, profile:profiles(username)")
        .order("created_at", desc=True)
        .execute()
        .data
    )

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

def create_comment(user_id, content, post_id=None, parent_comment_id=None):
    supabase = get_supabase()
    if not post_id and not parent_comment_id:
        raise ValueError("Either post_id or parent_comment_id must be provided")

    comment_data = {
        "user_id": user_id,
        "content": content,
        "post_id": post_id,
        "parent_comment_id": parent_comment_id,
    }
    
    comment_data = {k: v for k, v in comment_data.items() if v is not None}
    
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