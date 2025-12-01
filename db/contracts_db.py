from db.client import get_supabase
from datetime import datetime

def get_all_contracts():
    supabase = get_supabase()
    try:
        # Get all contracts with user profile info
        response = supabase.table("contracts").select(
            "*, profile:profiles!contracts_user_id_fkey(username)"
        ).order("created_at", desc=True).execute()
        
        all_contracts = response.data
        
        # Get list of claimed contract IDs
        claimed_response = supabase.table("claimed_contracts").select("contract_id").execute()
        claimed_ids = {item['contract_id'] for item in claimed_response.data}
        
        # Filter out claimed contracts
        unclaimed_contracts = [c for c in all_contracts if c['contract_id'] not in claimed_ids]
        
        return unclaimed_contracts
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

def update_contract(contract_id, user_id, title, description, pay_amount, tags=None):
    """Update an existing contract (only if owned by user)"""
    if tags is None:
        tags = []
    supabase = get_supabase()
    try:
        # First verify the contract belongs to this user
        contract = supabase.table("contracts").select("user_id").eq(
            "contract_id", contract_id
        ).single().execute()
        
        if not contract.data or contract.data['user_id'] != user_id:
            return None, "You don't have permission to edit this directive."
            
        data = {
            "title": title,
            "description": description,
            "pay_amount": pay_amount,
            "tags": tags
        }
        
        response = supabase.table("contracts").update(data).eq(
            "contract_id", contract_id
        ).execute()
        
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

# Removed get_posted_contracts as it is no longer used in the UI

def delete_contract(contract_id, user_id):
    """Delete a contract (only if owned by user)"""
    supabase = get_supabase()
    try:
        # First verify the contract belongs to this user
        contract = supabase.table("contracts").select("user_id").eq(
            "contract_id", contract_id
        ).single().execute()
        
        if not contract.data or contract.data['user_id'] != user_id:
            return None, "You don't have permission to delete this directive."
        
        # Delete associated claims first (due to foreign key constraint)
        supabase.table("claimed_contracts").delete().eq(
            "contract_id", contract_id
        ).execute()
        
        # Delete the contract
        response = supabase.table("contracts").delete().eq(
            "contract_id", contract_id
        ).execute()
        
        return response.data, None
    except Exception as e:
        return None, str(e)