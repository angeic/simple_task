from flask import Blueprint, render_template, request
from webapp.models import User
from flask_login import login_required, current_user


people_blueprint = Blueprint(
    'people',
    __name__
)


@people_blueprint.route('/<username>', methods=['POST', 'GET'])
@login_required
def people(username):
    display_user = User.query.filter_by(username=username).first()
    return render_template('people/people.html',
                           display_user=display_user
                           )


@people_blueprint.route('/do')
@login_required
def do():
    follow_id = request.args.get('id')
    if int(follow_id) != current_user.id:
        if current_user.check_following(follow_id):
            current_user.cancel_following(follow_id)
        else:
            current_user.add_following(follow_id)
    return 'hello1'

