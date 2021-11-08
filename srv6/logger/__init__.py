import json
from os.path import basename
from zipfile import ZipFile
from os import listdir, path, stat, rename, remove, mkdir
from datetime import datetime, timedelta


class Logger():

    def __init__(self,
                 app,
                 maxsize = 5120,  #5Mb
                 maxlength = 5000,  #5000 lines
                 maxdue = 7,  #7 days
                 name = 'log.file',
                 archive_name = 'log_archive.zip',
                 ):
        self.folder = app.config['LOG_FOLDER'] or 'logs'
        #self.output = app.config['LOG_OUTPUT'] #terminal, file, both
        self.maxsize = maxsize * 1024  # file size in bytes
        self.maxlength = maxlength  # max number of lines in file
        self.maxdue = maxdue * 24 * 60 * 60  # max time the logfile lives in seconds
        self.name = name  # the name of the logfile
        self.archive_name = archive_name  # the name of the zipped archive

        self.logfile_path = path.join(self.folder, self.name)  # passed_folder/passed_name
        self.archive_path = path.join(self.folder, self.archive_name)  # passed_folder/passed_archive_name.zip

        self.log_type = {0: 'INFO', 1: 'WARNING', 2: 'ERROR', 3: 'FATAL ERROR', 9: 'SYSTEM EVENT'}  # Const types

        self.check()  # init logfile
        return


    def check(self):
        """
            Init logfile. If not exists, creates it
            Checks limit and if reached, archives it, and creates a new one
            :return: 0 if OK
        """
        try:
            files = listdir(self.folder)
        except (FileNotFoundError):
            mkdir(self.folder)
            files = listdir(self.folder)

        logfile_path = path.join(self.folder, self.name)
        archive_path = path.join(self.folder, self.archive_name)

        # check if logfile exists, if not, create it
        if self.name not in files:
            with open(logfile_path, "w", encoding='utf8') as logfile:
                pass

            self.upd_log('Logfile created', type=9, user='SYSTEM')
            return 0

        # check if archive exists, if not, create it
        if self.archive_name not in files:
            with ZipFile(archive_path, 'w') as archive:
                pass
            return 0

        # check if logfile reached sizelimit, linelimit or timedelta limit, if so archive it and recall itself

        size = stat(logfile_path).st_size
        lines = sum(1 for line in open(logfile_path, encoding='utf8'))
        #lines = sum(1 for line in open(logfile_path))

        if size >= self.maxsize or lines >= self.maxlength:
            self.archive()
            self.check()

        # check if logfile reached timelimit, if so archive it and recall check
        # determine first entry's datetime in current logfile
        first_entry = None
        with open(logfile_path, 'r') as logfile:
            first_entry = datetime.fromtimestamp( float( json.loads( logfile.readlines()[0] )['timestamp'] ) )
        # determine due date
        td = first_entry + timedelta(seconds=self.maxdue)
        # compare dates and control the flow
        if datetime.now() > td:
            self.archive()
            self.check()

        return 0


    def upd_log(self, log_text, request = None, type = 0, user = None):

        if user:
            username = user
        else:
            username = 'ANONYMUS'

        if not request:
            message = {
                'type': self.log_type[type],
                'timestamp': f'{datetime.now().timestamp()}',
                'datetime': f'{datetime.now().strftime("%Y.%m.%d-%H:%M:%S")}',
                'executor': f'{username}',
                'event': f'{log_text}'
            }
        else:
            message = {
                'type': self.log_type[type],
                #'timestamp': f'{datetime.now().timestamp()}',
                'datetime': f'{datetime.now().strftime("%Y.%m.%d-%H:%M:%S")}',
                'executor': f'{username}',
                'event': f'{log_text}',
                #'docker source': f'{request.remote_addr}',
                'remote source': f'{request.access_route[-1]}',
                #'remote user': f'{request.remote_user}',
                #'headers': f'{request.headers}',
                'path': f'{request.path}',
                #'method': f'{request.method}',
                #'access route': f'{request.access_route}',
                'request args': f'{request.args}',
                #'endpoint': f'{request.view_args}',
                'request JSON': f'{request.json}',
                'user agent': f'{request.headers.get("User-Agent")}',
                #'FROM': f'{request.headers.get("from")}',
                #'ORIGIN': f'{request.headers.get("origin")}',
            }

        with open(self.logfile_path, 'a+') as logfile:
            logfile.write(json.dumps(message))
            logfile.write('\n')
        self.check()
        return True


    def archive(self):
        """
        Archive a living logfile with an incremented counter in name
        :return: None
        """
        files = listdir(self.folder)
        logfile_path = path.join(self.folder, self.name)
        archive_path = path.join(self.folder, self.archive_name)

        with ZipFile(archive_path, 'r') as archive:
            filecount = len(archive.infolist())

        new_path = path.join(self.folder, f'archive_{filecount + 1}_{datetime.now().strftime("%Y-%m-%d")}')
        rename(logfile_path, new_path)

        with ZipFile(logfile_path, 'a') as archive:
            archive.write(new_path, basename(new_path))
        remove(new_path)

        return


    def return_json(self):
        """
        reads the actual logfile and dumps it into JSON
        :return: JSON string
        """
        log_content = []
        with open(self.logfile_path) as logfile:
            content = logfile.readlines()

        for line in content:
            line = json.loads(line)
            log_content.append(line)

        #print(log_content)

        return (log_content)