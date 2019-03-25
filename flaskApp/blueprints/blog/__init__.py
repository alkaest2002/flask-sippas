from flask import Blueprint

bp_blog = Blueprint(
    'blog',
    __name__,
    template_folder = 'templates',
    static_folder = 'static'
)

from . import routes