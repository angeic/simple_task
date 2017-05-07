from flask import Blueprint, render_template
from webapp.models import User
from flask_login import login_required, current_user

explore_blueprint = Blueprint(
    'explore',
    __name__
)


@explore_blueprint.route('/')
@login_required
def home():
    return render_template('explore/home.html',
                           page_title='发现',
                           people_list=User.query.order_by(User.reg_date.desc()).all(),
                           display_user=current_user
                           )