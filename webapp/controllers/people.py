from flask import Blueprint, url_for, redirect, render_template, flash, session, request, g
from webapp.models import User, Task, Follow, db
from webapp.form import LoginForm, RegisterForm, FollowForm
from flask_login import logout_user, login_user, login_required, current_user


people_blueprint = Blueprint(
    'people',
    __name__
)


@people_blueprint.before_request
def check_user():
    if 'user_id' in session:
        g.current_user = User.query.filter_by(id=int(session['user_id'])).one()
    else:
        g.current_user = None


@people_blueprint.route('/<username>', methods=['POST', 'GET'])
@login_required
def people(username):
    display_user = User.query.filter_by(username=username).first()
    follow = Follow(g.current_user.id)
    is_follow = follow.check_follow(display_user.id)
    form = FollowForm()
    form.follow_id.data = display_user.id
    if form.validate_on_submit():
        if is_follow:
            follow.cancel_follow(display_user.id)
            db.session.commit()
        else:
            follow.set_follow(display_user.id)
            db.session.add(follow)
            db.session.commit()
        return redirect(url_for('people.people', username=username))
    return render_template('people/people.html',
                           display_user=display_user,
                           is_follow=is_follow,
                           form=form
                           )