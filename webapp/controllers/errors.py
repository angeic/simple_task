from flask import Blueprint, render_template

error_blueprints = Blueprint(
    'errors',
    __name__,

)


@error_blueprints.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@error_blueprints.app_errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


@error_blueprints.app_errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500
