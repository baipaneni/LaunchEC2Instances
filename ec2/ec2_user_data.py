from jinja2 import Template

from ec2.ec2_volumes import EC2Volumes
from ec2.ec2_logins import EC2Logins
from log import get_logger

logger = get_logger(__name__)

USER_DATA_TEMPLATE = 'templates/userdata_init.sh.j2'


class EC2UserData:

    def __init__(self, ec2_logins: EC2Logins, ec2_volumes: EC2Volumes):
        self.ec2_logins = ec2_logins
        self.ec2_volumes = ec2_volumes

    def _prepare_user_data_device_info(self) -> str:
        """Prepare user_data  device_info for EC2 instance launch """

        devices_info = ''
        for volume_info in self.ec2_volumes.get_volumes():
            if volume_info['mount'] == '/':
                continue
            elif devices_info:
                devices_info += ' \\n  '

            devices_info += volume_info['device'] + ' ' + volume_info['type'] + ' ' + volume_info['mount']

        return devices_info

    def _prepare_user_data_ssh_keys(self) -> str:
        """Prepare user_data SSH keys for EC2 instance launch """

        users_ssh_keys_info = ''

        for login, ec2_login in self.ec2_logins.get_logins().items():
            if users_ssh_keys_info:
                users_ssh_keys_info += ' \\n'

            users_ssh_keys_info += login + ' ' + ec2_login.ssh_public_key

        return users_ssh_keys_info

    def get_user_data(self) -> str:
        """Prepare user_data for EC2 instance launch """
        devices_info = self._prepare_user_data_device_info()
        users_ssh_keys_info = self._prepare_user_data_ssh_keys()

        with open(USER_DATA_TEMPLATE, 'r') as file:
            template = Template(file.read())

        return template.render(DEVICES_INFO=devices_info,
                               USERS_SSH_KEYS_INFO=users_ssh_keys_info)
