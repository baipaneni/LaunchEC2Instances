from ec2.ec2_login import EC2Login
from log import get_logger

logger = get_logger(__name__)


class EC2Logins:
    """ Class for storing multiple EC2Login objects"""
    def __init__(self):
        self.logins = dict()

    def populate_users_from_config(self, logins_config):
        for user_info in logins_config:
            ec2_login = EC2Login(user_info['login'], user_info['ssh_key'])
            self.logins[user_info['login']] = ec2_login

    def get_logins(self):
        return self.logins
