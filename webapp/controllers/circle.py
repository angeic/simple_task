from flask import Blueprint, render_template
from flask_login import login_required, current_user

circle_blueprint = Blueprint(
    'circle',
    __name__
)


@circle_blueprint.route('/')
@login_required
def home():
    return render_template('circle/home.html',
                           page_title='圈子动态',
                           tasks=current_user.circle_task(),
                           )
