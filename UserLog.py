from datetime import datetime
import os

class UserLog:

    def __init__(self, users, username):
        self.username = username
        self.users = users
        self.log_file = '{users}/{username}/log - '.format(users=self.users, username=self.username)

    def _write(self, message):
        current_time = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        
        with open(self.log_file, 'a') as log_file:
            to_write = '{time} - {message}\n'.format(time=current_time, message=message)
            log_file.write(to_write)

    def login_success(self):
        self._write('Accepted credentials')

    def login_failure(self):
        self._write('Failed credentials')

    def register(self):
        self._write('User registered')

    def return_file(self, file):
        self._write('Returning {file}'.format(file=file))

    def read(self):
        lines = []
        
        #Check that user log file exists
        if os.path.exists(self.log_file):
            #Fill lines with lines from log file
            with open(self.log_file, 'r') as log_file:
                lines = log_file.readlines()

            #Fill logs with dictionaries that have a date, time, and message key
            logs = []
            for line in lines:
                log_line = line.split()
                logs.append(dict())
                logs[-1]['date'] = log_line[0]
                logs[-1]['time'] = log_line[1]
                #Index 3 and above contain the message
                logs[-1]['message'] = ' '.join(log_line[3:len(log_line)])

            return logs
        return self.read_error('No such log file exists.')

    #Return an error that fits the template
    def read_error(self, message):
        return [{'date': '0', 'time': '0', 'message': message}]