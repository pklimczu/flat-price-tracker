import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('views', __name__)


def get_controller_handler():
    """
    Returns controller handler to get access to database
    """
    import sys
    sys.path.append("..")
    import controller

    handler = controller.Controller()
    return handler


def get_all_offers():
    """
    Returns all offers in JSON format
    """
    handler = get_controller_handler()
    return handler.get_all_offers()


def get_details_for_offer(offer_id):
    """
    Returns details for given offer in JSON
    """
    handler = get_controller_handler()
    return (handler.get_offer(offer_id),
            handler.get_details_for_offer(offer_id))


@bp.route('/', methods=['GET'])
def offers():
    offers = get_all_offers()
    
    return render_template("general.html", offers=offers)


@bp.route("/<string:offer_id>", methods=['GET'])
def details(offer_id):
    (offer, details) = get_details_for_offer(offer_id)

    return render_template("details.html", offer=offer, details=details)