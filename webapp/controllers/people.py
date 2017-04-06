from flask import Blueprint, url_for, redirect, render_template, flash, session, request
from webapp.models import User, Task, db
from flask_login import logout_user, login_user, login_required, current_user


people_blueprint = Blueprint(
    'people',
    __name__
)


@people_blueprint.route('/<username>', methods=['POST', 'GET'])
@login_required
def people(username):
    display_user = User.query.filter_by(username=username).first()
    is_follow = current_user.check_following(display_user.id)

    return render_template('people/people.html',
                           display_user=display_user,
                           is_follow=is_follow
                           )


@people_blueprint.route('/follow')
@login_required
def follow():
    follow_id = request.args.get('id')
    if int(follow_id) != current_user.id:
        if current_user.check_following(follow_id):
            current_user.cancel_following(follow_id)
        else:
            current_user.add_following(follow_id)
    return 'hello1'

