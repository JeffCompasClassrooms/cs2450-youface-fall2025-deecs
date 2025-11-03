from db.client import get_supabase
from datetime import datetime

def get_all_contracts():
    supabase = get_supabase()
    try:
        response = supabase.table("contracts").select(
            "*, profile:profiles(*)"
        ).order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        return []

def create_contract(user_id, title, description, pay_amount, tags=None):
    if tags is None:
        tags = []
    supabase = get_supabase()
    try:
        response = supabase.table("contracts").insert({
            "user_id": user_id,
            "title": title,
            "description": description,
            "pay_amount": pay_amount,
            "tags": tags
        }).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

