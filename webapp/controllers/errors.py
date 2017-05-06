from flask import Blueprint, render_template, session

error_blueprints = Blueprint(
    'errors',
    __name__,

)


@error_blueprints.app_errorhandler(404)
def page_not_found(error):
    if 'user_id' in session:
        return render_template('404.html'), 404
    else:
        return '你来到了一个荒无人烟的地方'


@error_blueprints.app_errorhandler(403)
def forbidden(error):
    if 'user_id' in session:
        return render_template('403.html'), 403
    else:
        return '看样子你是没权限访问这个页面'


@error_blueprints.app_errorhandler(500)
def error_500(error):
    if 'user_id' in session:
        return render_template('500.html'), 500
    else:
        return '可能我们遇到了一个问题'
