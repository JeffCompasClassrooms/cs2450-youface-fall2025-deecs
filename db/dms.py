from db.client import get_supabase

def get_messages(user_id):
    supabase = get_supabase()
    try:
        response = supabase.table("direct_messages").select(
            "*, sender:profiles!direct_messages_sender_id_fkey(*), receiver:profiles!direct_messages_receiver_id_fkey(*)"
        ).or_(f"sender_id.eq.{user_id},receiver_id.eq.{user_id}").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        return []

def send_message(sender_id, receiver_username, content):
    supabase = get_supabase()
    try:
        receiver_response = supabase.table("profiles").select("id").eq("username", receiver_username).single().execute()
        if not receiver_response.data:
            return None, "User not found"
        
        receiver_id = receiver_response.data["id"]
        
        response = supabase.table("direct_messages").insert({
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "content": content
        }).execute()
        
        return response.data, None
    except Exception as e:
        return None, str(e)

