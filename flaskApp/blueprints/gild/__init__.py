from flask import Blueprint

bp_gild = Blueprint(
    'gild',
    __name__,
    template_folder = 'templates',
    static_folder = 'static'
)

from . import routes