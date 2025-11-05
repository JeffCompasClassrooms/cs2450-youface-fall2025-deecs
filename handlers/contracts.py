import flask
from handlers.auth import login_required
from handlers import copy
from db import contracts as contracts_db

blueprint = flask.Blueprint("contracts", __name__)

@blueprint.route("/assignments")
@login_required
def assignments():
    user_profile = flask.g.user
    
    all_contracts = contracts_db.get_all_contracts()

    return flask.render_template(
        "assignments.html",
        title=copy.title,
        subtitle=copy.subtitle,
        user=user_profile,
        username=user_profile['username'],
        contracts=all_contracts
    )

@blueprint.route("/contract/create", methods=["POST"])
@login_required
def create_contract():
    user_id = flask.g.user['id']
    title = flask.request.form.get("title")
    description = flask.request.form.get("description")
    pay_amount = flask.request.form.get("pay_amount")
    tags = flask.request.form.getlist("tags")

    if not all([title, description, pay_amount, tags]):
        flask.flash("All fields are required to create a contract.", "danger")
        return flask.redirect(flask.url_for('contracts.assignments'))

    try:
        pay_value = int(pay_amount)
    except ValueError:
        flask.flash("Pay amount must be a valid number.", "danger")
        return flask.redirect(flask.url_for('contracts.assignments'))

    new_contract = contracts_db.create_contract(
        user_id=user_id,
        title=title,
        description=description,
        pay_amount=pay_value,
        tags=tags
    )

    if new_contract:
        flask.flash("Contract posted successfully.", "success")
    else:
        flask.flash("Error posting contract. Please try again.", "danger")

    return flask.redirect(flask.url_for("contracts.assignments"))