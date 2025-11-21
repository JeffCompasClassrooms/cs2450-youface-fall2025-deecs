from db.client import get_supabase
import flask

def get_conversations(user_id):
    """
    Get conversations grouped by partner.
    Returns a list of conversation objects with the latest message and partner info.
    """
    supabase = get_supabase()
    try:
        # Get all messages for this user
        response = supabase.table("direct_messages").select(
            "*"
        ).or_(
            f"sender_id.eq.{user_id},receiver_id.eq.{user_id}"
        ).order("created_at", desc=True).execute()
        
        messages = response.data if response.data else []
        
        if not messages:
            return []
        
        # Collect all unique user IDs
        user_ids = set()
        for msg in messages:
            user_ids.add(msg['sender_id'])
            user_ids.add(msg['receiver_id'])
        
        # Fetch all profiles
        profiles_response = supabase.table("profiles").select(
            "id, username, first_name, last_name"
        ).in_("id", list(user_ids)).execute()
        
        profiles_dict = {p['id']: p for p in (profiles_response.data or [])}
        
        # Group messages by conversation partner
        conversations = {}
        for msg in messages:
            # Determine the partner (not the current user)
            partner_id = msg['receiver_id'] if msg['sender_id'] == user_id else msg['sender_id']
            
            if partner_id not in conversations:
                conversations[partner_id] = {
                    'partner': profiles_dict.get(partner_id, {'username': 'Unknown User'}),
                    'partner_id': partner_id,
                    'latest_message': msg,
                    'message_count': 0
                }
            
            conversations[partner_id]['message_count'] += 1
        
        # Convert to list and sort by latest message
        conversation_list = list(conversations.values())
        conversation_list.sort(key=lambda x: x['latest_message']['created_at'], reverse=True)
        
        return conversation_list
        
    except Exception as e:
        print(f"Error getting conversations: {e}")
        import traceback
        traceback.print_exc()
        return []


def get_messages_with_user(user_id, partner_id):
    """
    Get all messages in a conversation between two users.
    Returns messages sorted chronologically (oldest first).
    """
    supabase = get_supabase()
    try:
        response = supabase.table("direct_messages").select(
            "*"
        ).or_(
            f"and(sender_id.eq.{user_id},receiver_id.eq.{partner_id}),and(sender_id.eq.{partner_id},receiver_id.eq.{user_id})"
        ).order("created_at", desc=False).execute()
        
        messages = response.data if response.data else []
        
        if not messages:
            return []
        
        # Get profiles for both users
        profiles_response = supabase.table("profiles").select(
            "id, username, first_name, last_name"
        ).in_("id", [user_id, partner_id]).execute()
        
        profiles_dict = {p['id']: p for p in (profiles_response.data or [])}
        
        # Attach profile info
        for msg in messages:
            msg['sender'] = profiles_dict.get(msg['sender_id'], {'username': 'Unknown User'})
            msg['receiver'] = profiles_dict.get(msg['receiver_id'], {'username': 'Unknown User'})
        
        return messages
        
    except Exception as e:
        print(f"Error getting messages: {e}")
        import traceback
        traceback.print_exc()
        return []


def send_message(sender_id, receiver_username, content):
    """
    Send a direct message to a user by username.
    Uses authenticated client which respects RLS policies.
    Returns: (data, error) tuple
    """
    supabase = get_supabase()
    
    try:
        # Look up the receiver's ID by username in profiles table
        receiver_response = supabase.table("profiles").select(
            "id"
        ).eq("username", receiver_username).single().execute()
        
        if not receiver_response.data:
            return None, "User not found"
        
        receiver_id = receiver_response.data["id"]
        
        # Prevent self-messaging
        if sender_id == receiver_id:
            return None, "Cannot send message to yourself"
        
        # Insert the message - RLS will verify auth.uid() == sender_id
        response = supabase.table("direct_messages").insert({
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "content": content
        }).execute()
        
        if response.data:
            return response.data, None
        else:
            return None, "Failed to send message"
            
    except Exception as e:
        error_msg = str(e)
        print(f"Error sending message: {error_msg}")
        import traceback
        traceback.print_exc()
        
        # Provide helpful error messages
        if "42501" in error_msg or "row-level security" in error_msg.lower():
            return None, "Permission denied - authentication issue"
        return None, error_msg