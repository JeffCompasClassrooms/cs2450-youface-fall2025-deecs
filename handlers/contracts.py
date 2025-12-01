import flask
from handlers.auth import login_required
from db import contracts_db as contracts_db
from handlers import copy 

blueprint = flask.Blueprint("contracts", __name__)

@blueprint.route("/assignments")
@login_required
def index():
    user_profile = flask.g.user
    
    all_contracts = contracts_db.get_all_contracts()
    claimed_contracts = contracts_db.get_claimed_contracts(user_profile['id'])
    # Removed posted_contracts fetching since we removed that section from UI
    all_tags = contracts_db.get_all_tags()

    return flask.render_template(
        "assignments.html",
        title=copy.title,
        user=user_profile,
        unclaimed_contracts=all_contracts,
        claimed_contracts=claimed_contracts,
        tags=all_tags
    )

@blueprint.route("/assignments/create", methods=["POST"])
@login_required
def create():
    user_id = flask.g.user['id']
    
    title = flask.request.form.get("title")
    description = flask.request.form.get("description")
    pay_amount = flask.request.form.get("pay_amount")
    tags = flask.request.form.getlist("tags") 

    if not title or not description or not pay_amount:
        flask.flash("Title, description, and pay amount are required.", "danger")
        return flask.redirect(flask.url_for("contracts.index"))

    try:
        pay_amount_float = float(pay_amount)
    except ValueError:
        flask.flash("Pay amount must be a valid number.", "danger")
        return flask.redirect(flask.url_for("contracts.index"))

    data, error = contracts_db.create_contract(
        user_id=user_id,
        title=title,
        description=description,
        pay_amount=pay_amount_float,
        tags=tags
    )

    if error:
        flask.flash(f"Error creating directive: {error}", "danger")
    
    # Success flash removed
    
    return flask.redirect(flask.url_for("contracts.index"))

@blueprint.route("/assignments/edit/<contract_id>", methods=["POST"])
@login_required
def edit(contract_id):
    user_id = flask.g.user['id']
    
    title = flask.request.form.get("title")
    description = flask.request.form.get("description")
    pay_amount = flask.request.form.get("pay_amount")
    tags = flask.request.form.getlist("tags")

    if not title or not description or not pay_amount:
        flask.flash("All fields are required.", "danger")
        return flask.redirect(flask.url_for("contracts.index"))

    try:
        pay_amount_float = float(pay_amount)
    except ValueError:
        flask.flash("Pay amount must be a valid number.", "danger")
        return flask.redirect(flask.url_for("contracts.index"))

    data, error = contracts_db.update_contract(
        contract_id=contract_id,
        user_id=user_id,
        title=title,
        description=description,
        pay_amount=pay_amount_float,
        tags=tags
    )

    if error:
        flask.flash(f"Error updating directive: {error}", "danger")
    
    # Success flash removed
    
    return flask.redirect(flask.url_for("contracts.index"))

@blueprint.route("/assignments/claim/<contract_id>", methods=["POST"])
@login_required
def claim(contract_id):
    user_id = flask.g.user['id']
    
    data, error = contracts_db.claim_contract(contract_id, user_id)
    
    if error:
        flask.flash(f"Could not claim directive. {error}", "danger")
    
    # Success flash removed
        
    return flask.redirect(flask.url_for("contracts.index"))

@blueprint.route("/assignments/delete/<contract_id>", methods=["POST"])
@login_required
def delete(contract_id):
    user_id = flask.g.user['id']
    
    data, error = contracts_db.delete_contract(contract_id, user_id)
    
    if error:
        flask.flash(f"Could not delete directive. {error}", "danger")
    else:
        flask.flash("Directive deleted successfully.", "success")
        
    return flask.redirect(flask.url_for("contracts.index"))