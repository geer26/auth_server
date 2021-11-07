import json
import time
import os

from flask import request, redirect, render_template, send_from_directory, send_file
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, logger
from app.workers import add_superuser, add_user, addsu, get_admindata, del_user, change_key
from app.models import Users, Testbatteries, Surveys, Results, Clients, Tokens


'''
upd_log(self, log_text, request = None, type = 0, user = None):
log_type = {0: 'INFO', 1: 'WARNING', 2: 'ERROR', 3: 'FATAL ERROR', 9: 'SYSTEM EVENT'}
'''


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    if current_user.is_authenticated and current_user.is_superuser:
        logger.upd_log('Admin indexpage served', request=request, type=0, user=current_user.username)
        return render_template( 'admin_dashboard.html', data= json.loads(get_admindata()) )

    if current_user.is_authenticated and not current_user.is_superuser:
        logger.upd_log('User indexpage served', request=request, type=0, user=current_user.username)

    logger.upd_log('Unauth indexpage served', request=request, type=0, user='ANONYMUS')
    return render_template('index2.html')


'''
@app.route('/addsu', methods=['POST'])
def add_superuser():
    if not request.json['username'] or not request.json['password']:
        logger.upd_log('Unsuccessful addsuperuser request', request=request, type=2, user='ANONYMUS')
        return 'Username and password must be present!', 500

    username = request.json["username"]
    password = request.json["password"]

    if addsu(str(username), str(password)):
        logger.upd_log('Superuser created', request=request, type=1, user='ANONYMUS')
        return 'Superuser created!', 200
    else:
        logger.upd_log('Unsuccessful addsuperuser request', request=request, type=2, user='ANONYMUS')
        return 'Superuser exists!', 500
'''


@app.route('/admin_dashboard', methods=['GET', 'POST'])
def adm_dashboard():
    if not current_user.is_authenticated or not current_user.is_superuser:
        logger.upd_log('Admin dashboard serve refused', request=request, type=1, user='ANONYMUS')
        return render_template('unauth.html', title='Go away!')
    logger.upd_log('Admin dashboard served', request=request, type=0, user=current_user.username)
    return render_template('admin_page_2.html', title='Admin page', data= json.loads(get_admindata()))


'''
@app.route('/logout', methods=['GET'])
def logout():
    if not current_user.is_authenticated:
        logger.upd_log('Unsuccessful logout request', request=request, type=1, user='ANONYMUS')
        return 'Already logged out!', 400
    logger.upd_log('User logged out', request=request, type=0, user=current_user.username)
    logout_user()
    return redirect('/')
'''

'''
@app.route('/get_current_log', methods=['GET'])
def get_current_log():
    if not current_user.is_authenticated:
        logger.upd_log('Current logfile download refused', request=request, type=1, user='ANONYMUS')
        return '', 401
    if current_user.is_authenticated and not current_user.is_superuser:
        logger.upd_log('Current logfile download refused', request=request, type=1, user=current_user.username)
        return render_template('unauth.html', title='Go away!'), 200
    path = os.path.join(app.config['LOG_FOLDER'], 'log.file')
    logger.upd_log('Current logfile downloaded', request=request, type=0, user=current_user.username)
    return send_file(path, attachment_filename='log.file'), 200


@app.route('/get_archive_log', methods=['GET'])
def get_archive_log():
    if not current_user.is_authenticated:
        logger.upd_log('Archive logfile download refused', request=request, type=1, user='ANONYMUS')
        return '', 401
    if current_user.is_authenticated and not current_user.is_superuser:
        logger.upd_log('Archive logfile download refused', request=request, type=1, user=current_user.username)
        return render_template('unauth.html', title='Go away!'), 200
    path = os.path.join(app.config['LOG_FOLDER'], 'log_archive.zip')
    logger.upd_log('Archive logfile downloaded', request=request, type=0, user=current_user.username)
    return send_file(path, attachment_filename='log_archive.zip'),200
'''