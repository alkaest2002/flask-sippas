
import datetime

from flask import jsonify, current_app, make_response

from . import bp_api

# ################################################################################
# ROUTES 
# ################################################################################

@bp_api.route("/setCookieConsent", methods= ['get','post'])
def set_cookie_consent():

  # prepare response
  resp = make_response(jsonify(message='consent cookie set'), 201)

  # set cookie
  resp.set_cookie("sippas_cookie_consent", value="set",  expires=datetime.datetime.now() + datetime.timedelta(days=365))

  # render view
  return resp