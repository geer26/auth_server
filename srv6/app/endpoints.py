import json
from flask_restful import Resource, reqparse
from flask_login import current_user, login_user, logout_user, login_required
from flask import request, redirect, render_template, send_from_directory, send_file
from app import api, logger, db
from app.workers import add_superuser, add_user, addsu, get_admindata, del_user, \
    change_key, add_battery, del_battery, add_survey, del_survey, add_client, del_client, \
    clean_database, upd_user, upd_testbattery, get_relevant_data, upd_survey, upd_client
from app.models import Users, Testbatteries, Surveys, Results, Clients, Tokens


class GetAPIDocu(Resource):
    def get(self):
        docu = {}
        if current_user.is_authenticated and not current_user.is_superuser:
            user_docu = {
                {'endpoint': 'login', 'URL': '/API/login', 'usage': '???'}
            }
            #collect docu for user
            docu = user_docu
        elif current_user.is_authenticated and current_user.is_superuser:
            admin_docu = {}
            #collect docu for superuser
            docu = admin_docu
        else:
            guest_docu = {}
            #collect docu for quest
            docu = guest_docu
        return docu, 200


class Healthcheck(Resource):
    def get(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        logger.upd_log('HEALTHCHECK served', request=request, type=0, user=username)
        return {'status': 'healthy'}


class Admindata(Resource):
    def get(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        if not current_user.is_authenticated:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Authentication required!'}, 401
        try:
            data = json.loads(get_relevant_data(current_user))
        except:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'error_code': 1, 'message': 'Error in collecting relevant data!'}, 500

        logger.upd_log(f'Relevant data served to {current_user.username}', request=request, type=0, user=username)
        return data, 200


class ChangeEnable(Resource):
    def post(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)
        #print(json_data)

        if not current_user.is_authenticated or not current_user.is_superuser:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 1, 'message': 'Must be logged in as superuser!'}, 401

        #change enabled here!!!
        try:
            user = Users.query.get( int(json_data['id']) )
        except:
            return {'error_code': 1, 'message': 'Internal server error!'}, 500

        if user.is_enabled: user.is_enabled = False
        else: user.is_enabled = True
        db.session.commit()

        try:
            data = json.loads(get_admindata())
        except:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'error_code': 1, 'message': 'Internal server error!'}, 500

        html = render_template('/admin/admin_container.html', data=data)

        logger.upd_log('API endpoint served', request=request, type=0, user=username)
        return {'status': 0, 'html': html}, 200


class AdmindataHtml(Resource):
    def get(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        if not current_user.is_authenticated or not current_user:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'error_code': 2, 'message': 'Authentication required!'}, 401
        try:
            data = json.loads(get_admindata())
        except:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'error_code': 1, 'message': 'Internal server error!'}, 500

        html = render_template('/admin/admin_container.html', data=data)

        logger.upd_log('API endpoint served', request=request, type=0, user=username)
        return {'status': 0, 'html': html}


class ChangePassword(Resource):
    def post(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)

        if not current_user.is_authenticated or not current_user.is_superuser:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 1, 'message': 'Must be logged in as superuser!'}, 401
        #print(request.json)
        pw = str(json_data['pw'])
        #TODO check pw complexity
        #change password here!!!
        user = current_user

        user.set_password( pw )
        db.session.commit()

        logger.upd_log('API endpoint served', request=request, type=0, user=username)
        return {}, 200


class DelUser(Resource):
    def post(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)

        if not current_user.is_authenticated or not current_user.is_superuser:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 1, 'message': 'Must be logged in as superuser!'}, 401

        if not json_data['uid']:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'status': 2, 'message': 'Data must be presented!'}, 500

        if del_user(int(json_data['uid'])):
            logger.upd_log('API endpoint served', request=request, type=0, user=username)
            return {'status': 0, 'message': 'User deleted succesfully!'}, 200
        else:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'status': 3, 'message': 'Delete user failed!'}, 500


class DelUserHtml(Resource):
    def post(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)

        if not current_user.is_authenticated or not current_user.is_superuser:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 1, 'message': 'Must be logged in as superuser!'}, 401

        if not json_data['uid']:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'status': 2, 'message': 'Data must be presented!'}, 500

        if del_user(int(json_data['uid'])):

            try:
                data = json.loads(get_admindata())
            except:
                logger.upd_log('Internal server error', request=request, type=3, user=username)
                return {'error_code': 1, 'message': 'Internal server error!'}, 500

            html = render_template('/admin/admin_container.html', data=data)
            logger.upd_log('API endpoint served', request=request, type=0, user=username)
            return {'status': 0, 'html': html}, 200

        else:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'status': 3, 'message': 'Internal server error!'}, 500


class Login(Resource):

    def post(self):
        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)

        if not json_data:
            logger.upd_log('API endpoint serve refused', request=request, type=2, user=username)
            return {'status': 4, 'message': 'LOGIN request must have params!'}, 400

        if not json_data['username'] or not json_data['password']:
            logger.upd_log('API endpoint serve refused', request=request, type=2, user=username)
            return {'status': 3, 'message': 'Username and password must be presented for login!'}, 400

        username = json_data['username']
        password = json_data['password']
        remember = json_data['remember']

        user = Users.query.filter_by(username=str(username)).one_or_none()
        if not user:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 1, 'message': 'Invalid username!'}, 401
        if not user.check_password(str(password)):
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 1, 'message': 'Invalid password!'}, 401
        if not user.is_enabled:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 1, 'message': 'User is disabled!'}, 401

        login_user(user, remember=remember)

        if user.is_superuser:
            logger.upd_log('API endpoint served', request=request, type=0, user=username)
            return {"status": 0, 'message': 'OK!', "redirect_to": "/admin/", 'role': 'admin', 'username': str(user.username)}, 200
        else:
            logger.upd_log('API endpoint served', request=request, type=0, user=username)
            return {"status": 0, 'message': 'OK!', "redirect_to": "/user/", 'role': 'user', 'username': str(user.username)}, 200


class GetlogAshtml(Resource):
    def get(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        if not current_user.is_superuser:
            if current_user.is_authenticated:
                username = current_user.username
                logger.upd_log('API endpoint serve refused', request=request, type=2, user=username)
            else:
                logger.upd_log('API endpoint serve refused', request=request, type=2, user='ANONYMUS')
            return {'status': 4, 'message': 'Must be superuser!'}, 401

        data = logger.return_json()
        html = render_template('/admin/admin_logentry.html', logs=data)
        logger.upd_log('API endpoint served', request=request, type=0, user=username)
        return {'status': 0, 'html': html}, 200


class AdduserHtm(Resource):
    def post(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)


        if not current_user.is_authenticated or not current_user.is_superuser:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in as superuser!'}, 401

        if add_user(json_data):
            try:
                data = json.loads(get_admindata())
            except:
                logger.upd_log('Internal server error', request=request, type=3, user=username)
                return {'error_code': 1, 'message': 'Internal server error!'}, 500
            html = render_template('/admin/admin_container.html', data=data)
            logger.upd_log('API endpoint served', request=request, type=0, user=username)
            return {'status': 0, 'html': html}, 200
        else:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'status': 1, 'message': 'Internal server error!'}, 500


class Adduser(Resource):
    def post(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)

        if not current_user.is_authenticated or not current_user.is_superuser:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in as superuser!'}, 401

        if add_user(json_data):
            logger.upd_log('API endpoint served', request=request, type=0, user=username)
            return {'status': 0, 'message': f'User <{json_data["username"]}> added!'}, 200
        else:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'status': 1, 'message': 'Internal server error!'}, 500


class Changekey(Resource):
    def get(self):
        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        if not current_user.is_authenticated or not current_user or not current_user.is_superuser:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'error_code': 2, 'message': 'Authentication required!'}, 401

        change_key(username, request)

        logger.upd_log('Secret key changed', request=request, type=1, user=username)
        return {'status': 0}, 200


class AddBattery(Resource):
    def post(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)

        if not current_user.is_authenticated or not current_user.is_superuser:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in as superuser!'}, 401

        if add_battery(json_data):
            try:
                data = json.loads(get_admindata())
            except:
                logger.upd_log('Internal server error', request=request, type=3, user=username)
                return {'error_code': 1, 'message': 'Internal server error!'}, 500
            #html = render_template('/admin/admin_container.html', data=data)
            logger.upd_log('API endpoint served', request=request, type=0, user=username)
            return {'status': 0, 'message': f'Testbattery added!'}, 200
        else:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'status': 1, 'message': 'Internal server error!'}, 500


class AddBatteryHtm(Resource):
    def post(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)

        if not current_user.is_authenticated or not current_user.is_superuser:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in as superuser!'}, 401

        if add_battery(json_data):
            try:
                data = json.loads(get_admindata())
            except:
                logger.upd_log('Internal server error', request=request, type=3, user=username)
                return {'error_code': 1, 'message': 'Internal server error!'}, 500
            html = render_template('/admin/admin_container.html', data=data)
            logger.upd_log('API endpoint served', request=request, type=0, user=username)
            #return {'status': 0, 'message': f'Testbattery added!'}, 200
            return {'status': 0, 'html': html}, 200
        else:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'status': 1, 'message': 'Internal server error!'}, 500


class DelBattery(Resource):
    def post(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)

        if not current_user.is_authenticated or not current_user.is_superuser:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in as superuser!'}, 401

        if del_battery(json_data):
            try:
                data = json.loads(get_admindata())
            except:
                logger.upd_log('Internal server error', request=request, type=3, user=username)
                return {'error_code': 1, 'message': 'Internal server error!'}, 500
            #html = render_template('/admin/admin_container.html', data=data)
            logger.upd_log('API endpoint served', request=request, type=0, user=username)
            return {'status': 0, 'message': f'Testbattery deleted!'}, 200
        else:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'status': 1, 'message': 'Internal server error!'}, 500


class DelBatteryHtm(Resource):
    def post(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)

        if not current_user.is_authenticated or not current_user.is_superuser:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in as superuser!'}, 401

        if del_battery(json_data):
            try:
                data = json.loads(get_admindata())
            except:
                logger.upd_log('Internal server error', request=request, type=3, user=username)
                return {'error_code': 1, 'message': 'Internal server error!'}, 500
            html = render_template('/admin/admin_container.html', data=data)
            logger.upd_log('API endpoint served', request=request, type=0, user=username)
            #return {'status': 0, 'message': f'Testbattery deleted!'}, 200
            return {'status': 0, 'html': html}, 200
        else:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'status': 1, 'message': 'Internal server error!'}, 500


class AddSurvey(Resource):
    def post(self):
        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)

        if not current_user.is_authenticated:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in as superuser!'}, 401

        if add_survey(json_data):
            try:
                data = json.loads(get_admindata())
            except:
                logger.upd_log('Internal server error', request=request, type=3, user=username)
                return {'error_code': 1, 'message': 'Internal server error!'}, 500
            #html = render_template('/admin/admin_container.html', data=data)
            logger.upd_log('API endpoint served', request=request, type=0, user=username)
            return {'status': 0, 'message': f'Survey added!'}, 200
        else:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'status': 1, 'message': 'Internal server error! FOSSSS!!!'}, 500


class DelSurvey(Resource):
    def post(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)

        if not current_user.is_authenticated:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in!'}, 401

        if del_survey(json_data):
            logger.upd_log('API endpoint served', request=request, type=0, user=username)
            return {'status': 0, 'message': f'Survey deleted!'}, 200
        else:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'status': 1, 'message': 'Survey delete failed!!'}, 500


class AddClient(Resource):
    def post(self):

        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)

        if not current_user.is_authenticated:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in!'}, 401

        if add_client(json_data):
            try:
                data = json.loads(get_admindata())
            except:
                logger.upd_log('Internal server error', request=request, type=3, user=username)
                return {'error_code': 1, 'message': 'Internal server error!'}, 500
            #html = render_template('/admin/admin_container.html', data=data)
            logger.upd_log('API endpoint served', request=request, type=0, user=username)
            return {'status': 0, 'message': f'Client added!'}, 200
        else:
            logger.upd_log('Internal server error', request=request, type=3, user=username)
            return {'status': 1, 'message': 'Internal server error!'}, 500


class DelClient(Resource):
    def post(self):
        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)

        if not current_user.is_authenticated:
            logger.upd_log('Client delete refused!', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in!'}, 401

        if del_client(json_data):
            logger.upd_log(f'Client deleted!', request=request, type=0, user=username)
            return {'status': 0, 'message': f'Client deleted!'}, 200
        else:
            logger.upd_log('Client delete failed!', request=request, type=3, user=username)
            return {'status': 1, 'message': 'Internal server error!'}, 500


class ClearData(Resource):
    def get(self):
        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        if not current_user.is_authenticated and not current_user.is_superuser:
            logger.upd_log('API endpoint serve refused', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in as superuser!'}, 401

        if clean_database():
            logger.upd_log('Database wiped', request=request, type=0, user=username)
            return {'status': 0, 'message': f'Database wiped!'}, 200
        else:
            logger.upd_log('Database wipe refused!', request=request, type=3, user=username)
            return {'status': 1, 'message': 'Internal server error!'}, 500


class UpdateUser(Resource):
    def post(self):
        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)
        user = Users.query.get(int(json_data['uid']))
        userid = user.id

        if not current_user.is_authenticated or not current_user.is_superuser:
            logger.upd_log('User update refused!', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in as admin!'}, 401

        if upd_user(json_data, user):
            logger.upd_log(f'User <{userid}> succesfully updated!', request=request, type=0, user=username)
            return {'status': 0, 'message': f'User updated succesfully!'}, 200
        else:
            logger.upd_log(f'User <{userid}> update failed!', request=request, type=0, user=username)
            return {'status': 0, 'message': f'User update failed!'}, 500


class UpdateTestbattery(Resource):
    def post(self):
        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)
        testbattery = Testbatteries.query.get(int(json_data['tbid']))
        tb_user = Users.query.get(int(testbattery.user_id))

        if not current_user.is_authenticated or not current_user.is_superuser or not tb_user.id == testbattery.user_id:
            logger.upd_log('Testbattery update refused!', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in as admin or relevant user!'}, 401

        if upd_testbattery(json_data, testbattery):
            logger.upd_log(f'Testbattery <{testbattery.id}> succesfully updated!', request=request, type=0, user=username)
            return {'status': 0, 'message': f'Testbattery updated succesfully!'}, 200
        else:
            logger.upd_log(f'Testbattery <{testbattery.id}> update failed!', request=request, type=0, user=username)
            return {'status': 0, 'message': f'Testbattery update failed!'}, 500


class UpdateSurvey(Resource):
    def post(self):
        if current_user.is_authenticated:
            username = current_user.username
        else:
            username = 'ANONYMUS'

        json_data = request.get_json(force=True)
        survey = Surveys.query.get(int(json_data['sid']))
        s_tb = Testbatteries.query.get(int(survey.testbattery_id))
        tb_user = Users.query.get(int(s_tb.user_id))

        if not current_user.is_authenticated and not current_user.is_superuser and not tb_user.username == current_user.username:
            logger.upd_log('Survey update refused!', request=request, type=1, user=username)
            return {'status': 2, 'message': 'Must be logged in as admin or relevant user!'}, 401

        if upd_survey(json_data, survey):
            logger.upd_log(f'Survey <{survey.id}> succesfully updated!', request=request, type=0, user=username)
            return {'status': 0, 'message': f'Survey updated succesfully!'}, 200
        else:
            logger.upd_log(f'Survey <{survey.id}> update failed!', request=request, type=0, user=username)
            return {'status': 0, 'message': f'Survey update failed!'}, 500


class UpdateClient(Resource):
    def post(self):
        pass




api.add_resource(Healthcheck, '/healthcheck')
api.add_resource(GetAPIDocu, '/getdocu')
api.add_resource(Admindata, '/API/admindata')
api.add_resource(ChangeEnable, '/API/change_enable')
api.add_resource(AdmindataHtml, '/API/admindata_html')  #returns html content for admin dashboard
api.add_resource(ChangePassword, '/API/change_password')
api.add_resource(DelUser, '/API/deluser')
api.add_resource(DelUserHtml, '/API/deluser_htm')  #returns html content for admin dashboard
api.add_resource(Login, '/API/login')
api.add_resource(GetlogAshtml, '/API/getlog_ashtml')  #returns html content for admin dashboard
api.add_resource(AdduserHtm, '/API/adduser_htm')  #returns html content for admin dashboard
api.add_resource(Adduser, '/API/adduser')
api.add_resource(Changekey, '/API/changekey')
api.add_resource(AddBattery, '/API/addbattery')
api.add_resource(AddBatteryHtm, '/API/addbattery_html')  #returns html content for admin dashboard
api.add_resource(DelBattery, '/API/delbattery')
api.add_resource(DelBatteryHtm, '/API/delbattery_html')  #returns html content for admin dashboard
api.add_resource(AddSurvey, '/API/addsurvey')
api.add_resource(DelSurvey, '/API/delsurvey')
api.add_resource(AddClient, '/API/addclient')
api.add_resource(DelClient, '/API/delclient')
api.add_resource(ClearData, '/API/wipedatabase')
api.add_resource(UpdateUser, '/API/updateuser')
api.add_resource(UpdateTestbattery, '/API/updatebattery')
api.add_resource(UpdateSurvey, '/API/updatesurvey')
api.add_resource(UpdateClient, '/API/updateclient')
