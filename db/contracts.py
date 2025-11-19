from db.client import get_supabase
from datetime import datetime

def get_all_contracts():
    supabase = get_supabase()
    try:
        response = supabase.table("contracts").select(
            "*, profile:profiles!contracts_user_id_fkey(username)"
        ).order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        return []

def get_claimed_contracts(user_id):
    supabase = get_supabase()
    try:
        response = supabase.table("claimed_contracts").select(
            "*, contract:contracts(*, profile:profiles!contracts_user_id_fkey(username))"
        ).eq(
            "user_id", user_id
        ).order("claimed_at", desc=True).execute()
        return response.data
    except Exception as e:
        return []

def claim_contract(contract_id, user_id):
    supabase = get_supabase()
    try:
        response = supabase.table("claimed_contracts").insert({
            "contract_id": contract_id,
            "user_id": user_id
        }).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

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

def get_all_tags():
    supabase = get_supabase()
    try:
        response = supabase.rpc('get_all_tags').execute()
        return response.data
    except Exception as e:
        return []