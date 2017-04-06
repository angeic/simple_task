from flask import Blueprint, url_for, redirect, render_template, flash, session, request, g
from webapp.models import User, Task, db
from flask_login import logout_user, login_user, login_required, current_user
import requests
import json
from webapp.config import DevConfig
weibo_blueprint = Blueprint(
    'weibo',
    __name__
)


@weibo_blueprint.before_request
def check_user():
    if 'user_id' in session:
        g.current_user = User.query.filter_by(id=int(session['user_id'])).one()
    else:
        g.current_user = None


@weibo_blueprint.route('/callback', methods=['POST', 'GET'])
def callback():
    code = request.args.get('code')
    if code:
        wbsession = requests.Session()
        postdata = {
            'client_id': DevConfig.WBAppKey,
            'client_secret': DevConfig.WBAppSecret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://simple.loadmemory.org/wb/callback'
        }
        # 验证授权信息
        wb_auth = wbsession.post('https://api.weibo.com/oauth2/access_token', postdata)
        if wb_auth.status_code == 200:
            token_data = json.loads(wb_auth.text)
            session['wb_uid'] = token_data['uid']
            session['wb_access_token'] = token_data['access_token']
            user = User.query.filter_by(wb_uid=token_data['uid']).first()

            # 该用户已注册
            if user:
                login_user(user, remember=True)
                return redirect(url_for('task.main'))
            # 该用户未注册
            else:
                get_wbuser = wbsession.get('https://api.weibo.com/2/users/show.json?access_token={}&uid={}'.format(token_data['access_token'], token_data['uid']))
                wbuser_info = json.loads(get_wbuser.text)
                print(get_wbuser.content)
                new_wb_user = User(wbuser_info['screen_name'])
                new_wb_user.wb_reg(token_data['uid'])
                db.session.add(new_wb_user)
                db.session.commit()
                user = User.query.filter_by(wb_uid=token_data['uid']).first()
                login_user(user, remember=True)
                flash('欢迎微博用户{}'.format(wbuser_info['screen_name']), category='info')
                return redirect(url_for('task.main'))
        else:
            return '<验证失败>'


@weibo_blueprint.route('/info', methods=['POST', 'GET'])
def info():
    wbsession = requests.Session()

    return 'a'
