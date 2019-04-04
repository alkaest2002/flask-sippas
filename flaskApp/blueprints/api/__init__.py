from flask import Blueprint

bp_api = Blueprint(
    'api',
    __name__,
    template_folder = 'templates',
    static_folder = 'static'
)

from . import routes